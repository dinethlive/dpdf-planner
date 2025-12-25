"""
Main Window - Primary application window

Assembles all components into the main application interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from typing import Optional

from gui.themes.dark_theme import DarkTheme
from gui.components.file_picker import FilePicker
from gui.components.page_range import PageRangeSelector
from gui.components.output_config import OutputConfig
from gui.components.status_bar import StatusBar, ActionBar
from services.pdf_service import PDFService
from services.validation_service import ValidationService
from services.config_service import ConfigService
from utils.file_utils import open_folder_in_explorer, open_file_in_explorer


class MainWindow:
    """
    Main application window that assembles all UI components.
    """
    
    WINDOW_WIDTH = 550
    WINDOW_HEIGHT = 580
    WINDOW_TITLE = "📄 PDF Page Extractor"
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(self.WINDOW_TITLE)
        
        # Initialize services
        self.pdf_service = PDFService()
        self.config_service = ConfigService()
        
        # Setup window
        self._setup_window()
        self._setup_styles()
        self._create_widgets()
        
        # Bind window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _setup_window(self):
        """Configure the main window."""
        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
        self.root.minsize(500, 520)
        self.root.resizable(True, True)
        
        # Configure dark theme for root
        DarkTheme.configure_root(self.root)
    
    def _setup_styles(self):
        """Configure ttk styles."""
        self.style = ttk.Style()
        DarkTheme.configure_ttk_style(self.style)
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Main container with padding
        self.main_frame = tk.Frame(
            self.root,
            bg=DarkTheme.COLORS['bg_primary'],
            padx=24,
            pady=20
        )
        self.main_frame.pack(fill='both', expand=True)
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)
        
        # Header
        header = tk.Label(
            self.main_frame,
            text="PDF Page Extractor",
            bg=DarkTheme.COLORS['bg_primary'],
            fg=DarkTheme.COLORS['text_primary'],
            font=DarkTheme.get_font('header', bold=True)
        )
        header.grid(row=0, column=0, sticky='w', pady=(0, 4))
        
        subtitle = tk.Label(
            self.main_frame,
            text="Extract specific pages from your PDF documents",
            bg=DarkTheme.COLORS['bg_primary'],
            fg=DarkTheme.COLORS['text_secondary'],
            font=DarkTheme.get_font('small')
        )
        subtitle.grid(row=1, column=0, sticky='w', pady=(0, 20))
        
        # File picker section
        self.file_picker = FilePicker(
            self.main_frame,
            on_file_selected=self._on_file_selected,
            initial_dir=self.config_service.last_input_dir
        )
        self.file_picker.grid(row=2, column=0, sticky='ew', pady=(0, 16))
        self._add_card_padding(self.file_picker)
        
        # Page range section
        self.page_range = PageRangeSelector(
            self.main_frame,
            on_range_changed=self._on_range_changed
        )
        self.page_range.grid(row=3, column=0, sticky='ew', pady=(0, 16))
        self._add_card_padding(self.page_range)
        
        # Output config section
        self.output_config = OutputConfig(
            self.main_frame,
            default_directory=self.config_service.last_output_dir,
            on_config_changed=self._on_output_changed
        )
        self.output_config.grid(row=4, column=0, sticky='ew', pady=(0, 20))
        self._add_card_padding(self.output_config)
        
        # Action bar
        self.action_bar = ActionBar(
            self.main_frame,
            on_extract=self._on_extract,
            on_open_folder=self._on_open_folder
        )
        self.action_bar.grid(row=5, column=0, sticky='ew', pady=(0, 16))
        
        # Separator
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.grid(row=6, column=0, sticky='ew', pady=(0, 12))
        
        # Status bar
        self.status_bar = StatusBar(self.main_frame)
        self.status_bar.grid(row=7, column=0, sticky='ew')
        
        # Initial state
        self._update_extract_button_state()
    
    def _add_card_padding(self, widget):
        """Add padding to a card-style widget."""
        widget.configure(padding=(16, 12))
    
    def _on_file_selected(self, filepath: str):
        """Handle file selection."""
        # Validate file first
        is_valid, error = ValidationService.validate_pdf_file(filepath)
        if not is_valid:
            self.status_bar.set_status(error, 'error')
            return
        
        # Load PDF
        success, message = self.pdf_service.load_pdf(filepath)
        
        if success:
            # Update page range
            self.page_range.set_total_pages(self.pdf_service.page_count)
            
            # Auto-suggest filename
            start, end = self.page_range.get_range()
            suggested_name = self.pdf_service.suggest_output_filename(
                start or 1,
                end or self.pdf_service.page_count
            )
            self.output_config.set_filename(suggested_name)
            
            # Update config with input directory
            self.config_service.last_input_dir = filepath
            self.config_service.add_recent_file(filepath)
            
            # Update status
            self.status_bar.set_status(message, 'success')
        else:
            self.status_bar.set_status(message, 'error')
            self.page_range.reset()
        
        self._update_extract_button_state()
    
    def _on_range_changed(self, start: int, end: int):
        """Handle page range changes."""
        if self.pdf_service.is_loaded:
            # Validate range
            is_valid, error = ValidationService.validate_page_range(
                start, end, self.pdf_service.page_count
            )
            
            if not is_valid:
                self.page_range.set_validation_message(error)
            else:
                self.page_range.set_validation_message("")
                
                # Update suggested filename
                suggested_name = self.pdf_service.suggest_output_filename(start, end)
                self.output_config.set_filename(suggested_name)
        
        self._update_extract_button_state()
    
    def _on_output_changed(self):
        """Handle output config changes."""
        filename = self.output_config.get_filename()
        if filename:
            is_valid, error = ValidationService.validate_filename(filename)
            if not is_valid:
                self.output_config.set_filename_validation(error)
        
        self._update_extract_button_state()
    
    def _update_extract_button_state(self):
        """Update the extract button enabled state based on form validity."""
        can_extract = self._validate_form_complete()
        self.action_bar.set_extract_enabled(can_extract)
    
    def _validate_form_complete(self) -> bool:
        """Check if the form is complete and valid."""
        # Check PDF is loaded
        if not self.pdf_service.is_loaded:
            return False
        
        # Check page range
        start, end = self.page_range.get_range()
        if start is None or end is None:
            return False
        
        is_valid, _ = ValidationService.validate_page_range(
            start, end, self.pdf_service.page_count
        )
        if not is_valid:
            return False
        
        # Check filename
        filename = self.output_config.get_filename()
        if not filename:
            return False
        
        is_valid, _ = ValidationService.validate_filename(filename)
        if not is_valid:
            return False
        
        return True
    
    def _on_extract(self):
        """Handle extract button click."""
        if not self._validate_form_complete():
            return
        
        # Get values
        start, end = self.page_range.get_range()
        output_path = self.output_config.get_full_output_path()
        
        # Check if file exists
        if os.path.exists(output_path):
            result = messagebox.askyesno(
                "File Exists",
                f"A file named '{os.path.basename(output_path)}' already exists.\n\nDo you want to replace it?",
                icon='warning'
            )
            if not result:
                return
        
        # Set processing state
        self.action_bar.set_processing(True)
        self.status_bar.set_status("Extracting pages...", 'processing')
        self.status_bar.show_progress(True)
        
        # Ensure output directory exists
        output_dir = self.output_config.get_output_directory()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                self.status_bar.set_status(f"Cannot create output directory: {e}", 'error')
                self.action_bar.set_processing(False)
                self.status_bar.show_progress(False)
                return
        
        # Update last output directory
        self.config_service.last_output_dir = output_dir
        
        # Extract pages with progress callback
        def progress_callback(current, total):
            self.status_bar.set_progress(current, total)
        
        success, message = self.pdf_service.extract_pages(
            start, end, output_path, progress_callback
        )
        
        # Reset processing state
        self.action_bar.set_processing(False)
        self.status_bar.show_progress(False)
        
        if success:
            self.status_bar.set_status(message, 'success')
            
            # Ask to open file location
            result = messagebox.askyesno(
                "Success",
                f"{message}\n\nWould you like to open the output folder?",
                icon='info'
            )
            if result:
                open_file_in_explorer(output_path)
        else:
            self.status_bar.set_status(message, 'error')
            messagebox.showerror("Extraction Failed", message)
    
    def _on_open_folder(self):
        """Handle open folder button click."""
        output_dir = self.output_config.get_output_directory()
        if os.path.exists(output_dir):
            open_folder_in_explorer(output_dir)
        else:
            messagebox.showwarning(
                "Folder Not Found",
                f"The output folder does not exist yet:\n{output_dir}"
            )
    
    def _on_close(self):
        """Handle window close."""
        self.pdf_service.close()
        self.root.destroy()
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
