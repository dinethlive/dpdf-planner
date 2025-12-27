"""
Main Window - Primary application window

Assembles all components into the main application interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
from typing import Optional, Set

from gui.themes.dark_theme import DarkTheme
from gui.components.file_picker import FilePicker # Keep if used elsewhere? No, moved to Sidebar
from gui.components.grid_view import GridView
from gui.components.single_page_window import SinglePageWindow
from gui.components.sidebar import Sidebar
from gui.components.status_bar import StatusBar
from gui.components.toast import show_toast
from services.pdf_service import PDFService
from services.validation_service import ValidationService
from services.config_service import ConfigService
from services.thumbnail_service import ThumbnailService
from utils.file_utils import open_folder_in_explorer, open_file_in_explorer


class MainWindow:
    """
    Main application window that assembles all UI components.
    """
    
    WINDOW_WIDTH = 900  # Increased for Grid View
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = "📄 PDF Page Extractor V2"
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(self.WINDOW_TITLE)
        
        # Initialize services
        self.pdf_service = PDFService()
        self.config_service = ConfigService()
        self.thumbnail_service = ThumbnailService()
        self.thumbnail_service = ThumbnailService()
        
        # Setup window
        self._setup_window()
        self._setup_styles()
        self._setup_styles()
        # Menu removed
        self._create_widgets()
        
        # Bind window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _setup_window(self):
        """Configure the main window."""
        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Widen default size for split layout
        self.WINDOW_WIDTH = 1100
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")
        self.root.minsize(900, 600)
        self.root.resizable(True, True)
        
        # Maximize on startup
        try:
            self.root.state('zoomed')
        except:
            # Fallback for systems that don't support 'zoomed' (e.g. Linux sometimes)
            self.root.attributes('-zoomed', True)
        
        # Configure dark theme for root
        DarkTheme.configure_root(self.root)
        
        # Keyboard Shortcuts
        self.root.bind('<Control-a>', lambda e: self.grid_view.select_all())
        self.root.bind('<Escape>', lambda e: self.grid_view.clear_selection())
    
    def _setup_styles(self):
        """Configure ttk styles."""
        self.style = ttk.Style()
        DarkTheme.configure_ttk_style(self.style)



    def _create_widgets(self):
        """Create all UI widgets in a resizable 2-column layout."""
        # Main container (PanedWindow)
        self.main_pane = ttk.PanedWindow(self.root, orient='horizontal')
        self.main_pane.pack(fill='both', expand=True)
        
        # --- Sidebar ---
        self.main_pane.add(self.sidebar, weight=0)
        
    def _create_widgets(self):
        """Create all UI widgets in a resizable 2-column layout."""
        # Main container (PanedWindow)
        self.main_pane = ttk.PanedWindow(self.root, orient='horizontal')
        self.main_pane.pack(fill='both', expand=True)
        
        # --- Sidebar ---
        self.sidebar = Sidebar(
            self.main_pane,
            initial_input_dir=self.config_service.last_input_dir,
            initial_output_dir=self.config_service.last_output_dir,
            on_file_selected=self._on_file_selected,
            on_output_changed=self._on_output_changed,
            on_extract=self._on_extract,
            on_open_folder=self._on_open_folder,
            on_clear_selection=self._on_clear_selection,
            bg=DarkTheme.COLORS['bg_primary'],
            width=600, # Explicit request
            padx=20,
            pady=20
        )
        self.main_pane.add(self.sidebar, weight=0)
        

        
        
        # --- Content Area (Right) ---
        self.content_area = tk.Frame(
            self.main_pane,
            bg=DarkTheme.COLORS['bg_secondary']
        )
        self.main_pane.add(self.content_area, weight=1)
        
        # Grid View Title inside Content
        title_frame = tk.Frame(self.content_area, bg=DarkTheme.COLORS['bg_secondary'], padx=20, pady=15)
        title_frame.pack(fill='x')
        
        tk.Label(
            title_frame,
            text="Page Selection",
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['text_primary'],
            font=DarkTheme.get_font('header')
        ).pack(side='left')
        
        # Grid View
        self.grid_view = GridView(
            self.content_area,
            thumbnail_service=self.thumbnail_service,
            on_selection_change=self._on_selection_change,
            on_page_click=self._on_page_click,
            bg=DarkTheme.COLORS['bg_secondary'],
            bd=0 
        )
        self.grid_view.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Status Bar (Bottom of Root)
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side='bottom', fill='x')
        
        # Initial state
        self._update_extract_button_state()
    

    
    def _on_file_selected(self, filepath: str):
        """Handle file selection."""
        is_valid, error = ValidationService.validate_pdf_file(filepath)
        if not is_valid:
            self.status_bar.set_status(error, 'error')
            return
        
        success, message = self.pdf_service.load_pdf(filepath)
        
        if success:
            self.grid_view.load_pdf(filepath, self.pdf_service.page_count)
            self.config_service.last_input_dir = filepath
            self.config_service.add_recent_file(filepath)
            
            # Default filename
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            self.sidebar.set_filename(f"{base_name}_extracted")
            
            self.status_bar.set_status(message, 'success')
        else:
            self.status_bar.set_status(message, 'error')
            self.grid_view.clear()
        
        self._update_extract_button_state()
    
    def _on_selection_change(self, selected_pages: Set[int]):
        """Handle selection change from GridView."""
        count = len(selected_pages)
        if count > 0:
            self.status_bar.set_status(f"{count} pages selected.", 'info')
        else:
            self.status_bar.set_status("No pages selected.", 'info')
        self._update_extract_button_state()

    def _on_page_click(self, page_num: int):
        """Handle click on a page thumbnail."""
        if not self.pdf_service.is_loaded:
            return
            
        # Get high-res image (request large width for zooming)
        img = self.thumbnail_service.get_thumbnail(self.pdf_service.filepath, page_num, width=1600)
        
        # Determine current rotation to pass to viewer
        current_rot = self.grid_view.get_rotations().get(page_num, 0)
        
        if img:
            SinglePageWindow(
                self.root, 
                page_num, 
                img, 
                initial_rotation=current_rot,
                on_rotate=self._on_page_rotate
            )
            
    def _on_page_rotate(self, page_num: int, angle: int):
        """Handle rotation from single page viewer."""
        self.grid_view.set_page_rotation(page_num, angle)

    def _on_clear_selection(self):
        """Clear all selected pages."""
        self.grid_view.clear_selection()
    
    def _on_output_changed(self):
        """Handle output config changes."""
        filename = self.sidebar.get_filename()
        if filename:
            is_valid, error = ValidationService.validate_filename(filename)
            if not is_valid:
                self.sidebar.set_filename_validation(error)
        self._update_extract_button_state()
    
    def _update_extract_button_state(self):
        """Update extract button enabled state."""
        can_extract = self._validate_form_complete()
        self.sidebar.set_extract_enabled(can_extract)
    
    def _validate_form_complete(self) -> bool:
        """Check if form is ready for extraction."""
        if not self.pdf_service.is_loaded:
            return False
        if not self.grid_view.selected_pages:
            return False
        
        filename = self.sidebar.get_filename()
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
            
        pages = sorted(list(self.grid_view.selected_pages))
        output_path = self.sidebar.get_full_output_path()
        
        if os.path.exists(output_path):
            if not messagebox.askyesno("File Exists", f"Overwrite {os.path.basename(output_path)}?"):
                return
        
        self.sidebar.set_processing(True)
        self.status_bar.set_status("Extracting...", 'processing')
        self.status_bar.show_progress(True)
        
        # Ensure output dir
        output_dir = self.sidebar.get_output_directory()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        self.config_service.last_output_dir = output_dir
        
        def progress_callback(current, total):
            self.status_bar.set_progress(current, total)
        
        rotations = self.grid_view.get_rotations()
        success, message = self.pdf_service.extract_pages(
            pages, output_path, rotations, progress_callback
        )
        
        self.sidebar.set_processing(False)
        self.status_bar.show_progress(False)
        
        if success:
            self.status_bar.set_status(message, 'success')
            if messagebox.askyesno("Success", f"{message}\nOpen folder?"):
                open_file_in_explorer(output_path)
        else:
            self.status_bar.set_status(message, 'error')
            messagebox.showerror("Error", message)

    def _on_open_folder(self):
        output_dir = self.sidebar.get_output_directory()
        if os.path.exists(output_dir):
            open_folder_in_explorer(output_dir)
        else:
            messagebox.showwarning("Not Found", "Output folder does not exist.")



    def _on_close(self):
        self.pdf_service.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
