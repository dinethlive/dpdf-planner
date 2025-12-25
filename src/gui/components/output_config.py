"""
Output Config Component - Output filename and directory selection

Provides input for output filename and directory chooser.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional

from gui.themes.dark_theme import DarkTheme


class OutputConfig(ttk.Frame):
    """
    Output configuration widget with filename input and directory picker.
    """
    
    def __init__(
        self, 
        parent,
        default_directory: str = "",
        on_config_changed: Optional[Callable] = None,
        **kwargs
    ):
        super().__init__(parent, style='Card.TFrame', **kwargs)
        
        self.on_config_changed = on_config_changed
        self._output_dir = default_directory
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the output config UI elements."""
        # Configure grid
        self.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            self,
            text="💾 Output Settings",
            style='Card.TLabel',
            font=DarkTheme.get_font('large', bold=True)
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 12))
        
        # Filename input
        filename_label = ttk.Label(
            self,
            text="Filename:",
            style='Card.TLabel'
        )
        filename_label.grid(row=1, column=0, sticky='w', pady=4)
        
        filename_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_secondary'])
        filename_frame.grid(row=1, column=1, columnspan=2, sticky='ew', padx=(8, 0), pady=4)
        filename_frame.columnconfigure(0, weight=1)
        
        self.filename_var = tk.StringVar()
        self.filename_entry = ttk.Entry(
            filename_frame,
            textvariable=self.filename_var,
            font=DarkTheme.get_font('normal')
        )
        self.filename_entry.grid(row=0, column=0, sticky='ew')
        self.filename_var.trace_add('write', self._on_config_change)
        
        pdf_label = tk.Label(
            filename_frame,
            text=".pdf",
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['text_muted'],
            font=DarkTheme.get_font('normal')
        )
        pdf_label.grid(row=0, column=1, padx=(4, 0))
        
        # Validation message
        self.name_validation_label = tk.Label(
            self,
            text="",
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['error'],
            font=DarkTheme.get_font('small'),
            anchor='w'
        )
        self.name_validation_label.grid(row=2, column=1, columnspan=2, sticky='w', padx=(8, 0))
        
        # Output directory
        dir_label = ttk.Label(
            self,
            text="Save to:",
            style='Card.TLabel'
        )
        dir_label.grid(row=3, column=0, sticky='w', pady=(8, 4))
        
        # Directory display
        self.dir_display = tk.Label(
            self,
            text=self._truncate_path(self._output_dir),
            bg=DarkTheme.COLORS['bg_input'],
            fg=DarkTheme.COLORS['text_secondary'],
            font=DarkTheme.get_font('small'),
            anchor='w',
            padx=8,
            pady=4
        )
        self.dir_display.grid(row=3, column=1, sticky='ew', padx=(8, 8), pady=(8, 4))
        
        # Change directory button
        self.change_dir_btn = ttk.Button(
            self,
            text="Change",
            command=self._browse_directory,
            style='Secondary.TButton',
            width=10
        )
        self.change_dir_btn.grid(row=3, column=2, sticky='e', pady=(8, 4))
    
    def _on_config_change(self, *args):
        """Handle configuration changes."""
        # Clear validation on change
        self.set_filename_validation("")
        
        if self.on_config_changed:
            self.on_config_changed()
    
    def _browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self._output_dir
        )
        
        if directory:
            self.set_output_directory(directory)
    
    def _truncate_path(self, path: str, max_length: int = 50) -> str:
        """Truncate a path for display."""
        if len(path) <= max_length:
            return path
        return "..." + path[-(max_length - 3):]
    
    def set_output_directory(self, directory: str):
        """
        Set the output directory.
        
        Args:
            directory: Path to the output directory
        """
        self._output_dir = directory
        self.dir_display.configure(text=self._truncate_path(directory))
        self._on_config_change()
    
    def get_output_directory(self) -> str:
        """Get the current output directory."""
        return self._output_dir
    
    def get_filename(self) -> str:
        """Get the current output filename (without .pdf extension)."""
        return self.filename_var.get().strip()
    
    def set_filename(self, filename: str):
        """
        Set the output filename.
        
        Args:
            filename: Filename without .pdf extension
        """
        # Remove .pdf extension if present
        if filename.lower().endswith('.pdf'):
            filename = filename[:-4]
        self.filename_var.set(filename)
    
    def get_full_output_path(self) -> str:
        """
        Get the full output file path.
        
        Returns:
            Full path to the output file (with .pdf extension)
        """
        import os
        filename = self.get_filename()
        if not filename.lower().endswith('.pdf'):
            filename = f"{filename}.pdf"
        return os.path.join(self._output_dir, filename)
    
    def set_filename_validation(self, message: str):
        """Set or clear filename validation message."""
        if message:
            self.name_validation_label.configure(text=f"⚠ {message}")
        else:
            self.name_validation_label.configure(text="")
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the output config controls."""
        state = 'normal' if enabled else 'disabled'
        self.filename_entry.configure(state=state)
        self.change_dir_btn.configure(state=state)
    
    def reset(self):
        """Reset the output config to defaults."""
        self.filename_var.set("")
        self.set_filename_validation("")
