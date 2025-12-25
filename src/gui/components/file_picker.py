"""
File Picker Component - PDF file selection widget

Provides a file picker with browse button and drag-drop zone.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from typing import Callable, Optional

from gui.themes.dark_theme import DarkTheme


class FilePicker(ttk.Frame):
    """
    File picker widget with browse button and optional drag-drop.
    """
    
    def __init__(
        self, 
        parent,
        on_file_selected: Callable[[str], None],
        initial_dir: str = "",
        **kwargs
    ):
        super().__init__(parent, style='Card.TFrame', **kwargs)
        
        self.on_file_selected = on_file_selected
        self.initial_dir = initial_dir
        self._current_file: Optional[str] = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the file picker UI elements."""
        # Configure grid
        self.columnconfigure(0, weight=1)
        
        # Title label
        title_label = ttk.Label(
            self,
            text="📄 PDF File",
            style='Card.TLabel',
            font=DarkTheme.get_font('large', bold=True)
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 8))
        
        # File display area (acts as drop zone)
        self.file_frame = tk.Frame(
            self,
            bg=DarkTheme.COLORS['bg_input'],
            highlightbackground=DarkTheme.COLORS['border'],
            highlightthickness=1,
            height=60
        )
        self.file_frame.grid(row=1, column=0, sticky='ew', padx=(0, 8))
        self.file_frame.grid_propagate(False)
        
        # File name label
        self.file_label = tk.Label(
            self.file_frame,
            text="No file selected",
            bg=DarkTheme.COLORS['bg_input'],
            fg=DarkTheme.COLORS['text_secondary'],
            font=DarkTheme.get_font('normal'),
            anchor='w',
            padx=12
        )
        self.file_label.place(relx=0, rely=0.3, relwidth=1, anchor='w')
        
        # Hint label
        self.hint_label = tk.Label(
            self.file_frame,
            text="Click Browse or drag & drop a PDF file",
            bg=DarkTheme.COLORS['bg_input'],
            fg=DarkTheme.COLORS['text_muted'],
            font=DarkTheme.get_font('small'),
            anchor='w',
            padx=12
        )
        self.hint_label.place(relx=0, rely=0.65, relwidth=1, anchor='w')
        
        # Browse button
        self.browse_btn = ttk.Button(
            self,
            text="Browse...",
            command=self._browse_file,
            width=12
        )
        self.browse_btn.grid(row=1, column=1, sticky='ns')
        
        # Bind click on file frame to browse
        self.file_frame.bind('<Button-1>', lambda e: self._browse_file())
        self.file_label.bind('<Button-1>', lambda e: self._browse_file())
        self.hint_label.bind('<Button-1>', lambda e: self._browse_file())
        
        # Hover effects
        self.file_frame.bind('<Enter>', self._on_enter)
        self.file_frame.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        """Mouse enter hover effect."""
        self.file_frame.configure(highlightbackground=DarkTheme.COLORS['border_hover'])
    
    def _on_leave(self, event):
        """Mouse leave hover effect."""
        color = DarkTheme.COLORS['border_focus'] if self._current_file else DarkTheme.COLORS['border']
        self.file_frame.configure(highlightbackground=color)
    
    def _browse_file(self):
        """Open file browser dialog."""
        filetypes = [
            ('PDF files', '*.pdf'),
            ('All files', '*.*')
        ]
        
        filepath = filedialog.askopenfilename(
            title="Select PDF File",
            initialdir=self.initial_dir,
            filetypes=filetypes
        )
        
        if filepath:
            self.set_file(filepath)
    
    def set_file(self, filepath: str):
        """
        Set the currently selected file.
        
        Args:
            filepath: Path to the PDF file
        """
        import os
        
        self._current_file = filepath
        filename = os.path.basename(filepath)
        
        # Update display
        self.file_label.configure(
            text=filename,
            fg=DarkTheme.COLORS['text_primary']
        )
        self.hint_label.configure(text="Click Browse to change file")
        self.file_frame.configure(highlightbackground=DarkTheme.COLORS['border_focus'])
        
        # Notify callback
        if self.on_file_selected:
            self.on_file_selected(filepath)
    
    def clear(self):
        """Clear the current selection."""
        self._current_file = None
        self.file_label.configure(
            text="No file selected",
            fg=DarkTheme.COLORS['text_secondary']
        )
        self.hint_label.configure(text="Click Browse or drag & drop a PDF file")
        self.file_frame.configure(highlightbackground=DarkTheme.COLORS['border'])
    
    @property
    def current_file(self) -> Optional[str]:
        """Get the currently selected file path."""
        return self._current_file
    
    def set_initial_dir(self, directory: str):
        """Set the initial directory for the file browser."""
        self.initial_dir = directory
