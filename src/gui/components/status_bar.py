"""
Status Bar Component - Status display and progress indicator

Provides status messages, progress bar, and action buttons.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional

from gui.themes.dark_theme import DarkTheme


class StatusBar(ttk.Frame):
    """
    Status bar with message display and progress indicator.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='TFrame', **kwargs)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the status bar UI elements."""
        self.columnconfigure(0, weight=1)
        
        # Status icon and message
        self.status_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_primary'])
        self.status_frame.grid(row=0, column=0, sticky='ew')
        
        self.status_icon = tk.Label(
            self.status_frame,
            text="✅",
            bg=DarkTheme.COLORS['bg_primary'],
            fg=DarkTheme.COLORS['success'],
            font=DarkTheme.get_font('normal')
        )
        self.status_icon.pack(side='left')
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            bg=DarkTheme.COLORS['bg_primary'],
            fg=DarkTheme.COLORS['text_secondary'],
            font=DarkTheme.get_font('normal'),
            anchor='w'
        )
        self.status_label.pack(side='left', padx=(4, 0))
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(
            self,
            mode='determinate',
            style='TProgressbar'
        )
        self.progress.grid(row=1, column=0, sticky='ew', pady=(8, 0))
        self.progress.grid_remove()  # Hide initially
        
        # Progress label
        self.progress_label = tk.Label(
            self,
            text="",
            bg=DarkTheme.COLORS['bg_primary'],
            fg=DarkTheme.COLORS['text_muted'],
            font=DarkTheme.get_font('small')
        )
        self.progress_label.grid(row=2, column=0, sticky='w', pady=(4, 0))
        self.progress_label.grid_remove()  # Hide initially
    
    def set_status(self, message: str, status_type: str = 'info'):
        """
        Set the status message.
        
        Args:
            message: Status message to display
            status_type: One of 'info', 'success', 'warning', 'error', 'processing'
        """
        icons = {
            'info': ('ℹ️', DarkTheme.COLORS['text_secondary']),
            'success': ('✅', DarkTheme.COLORS['success']),
            'warning': ('⚠️', DarkTheme.COLORS['warning']),
            'error': ('❌', DarkTheme.COLORS['error']),
            'processing': ('⏳', DarkTheme.COLORS['info']),
            'ready': ('✅', DarkTheme.COLORS['success'])
        }
        
        icon, color = icons.get(status_type, icons['info'])
        
        self.status_icon.configure(text=icon, fg=color)
        self.status_label.configure(text=message, fg=color)
    
    def show_progress(self, show: bool = True):
        """Show or hide the progress bar."""
        if show:
            self.progress['value'] = 0
            self.progress.grid()
            self.progress_label.grid()
        else:
            self.progress.grid_remove()
            self.progress_label.grid_remove()
    
    def set_progress(self, current: int, total: int):
        """
        Update the progress bar.
        
        Args:
            current: Current progress value
            total: Total value
        """
        percentage = (current / total * 100) if total > 0 else 0
        self.progress['value'] = percentage
        self.progress_label.configure(text=f"Extracting page {current} of {total}...")
        
        # Force update to show progress
        self.update_idletasks()
    
    def reset(self):
        """Reset status bar to initial state."""
        self.set_status("Ready", 'ready')
        self.show_progress(False)


class ActionBar(ttk.Frame):
    """
    Action bar with main action button and secondary actions.
    """
    
    def __init__(
        self, 
        parent, 
        on_extract: Optional[callable] = None,
        on_open_folder: Optional[callable] = None,
        **kwargs
    ):
        super().__init__(parent, style='TFrame', **kwargs)
        
        self.on_extract = on_extract
        self.on_open_folder = on_open_folder
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the action bar UI elements."""
        self.columnconfigure(0, weight=1)
        
        # Main extract button
        self.extract_btn = ttk.Button(
            self,
            text="🔧 Extract Pages",
            command=self._handle_extract,
            style='Accent.TButton'
        )
        self.extract_btn.grid(row=0, column=0, sticky='ew', pady=(0, 12))
        
        # Secondary actions frame
        secondary_frame = ttk.Frame(self, style='TFrame')
        secondary_frame.grid(row=1, column=0, sticky='ew')
        secondary_frame.columnconfigure(1, weight=1)
        
        # Open folder button
        self.open_folder_btn = ttk.Button(
            secondary_frame,
            text="📂 Open Output Folder",
            command=self._handle_open_folder,
            style='Secondary.TButton'
        )
        self.open_folder_btn.grid(row=0, column=0, sticky='w')
        
        # Version label
        version_label = ttk.Label(
            secondary_frame,
            text="v1.0.0",
            style='Secondary.TLabel'
        )
        version_label.grid(row=0, column=2, sticky='e')
    
    def _handle_extract(self):
        """Handle extract button click."""
        if self.on_extract:
            self.on_extract()
    
    def _handle_open_folder(self):
        """Handle open folder button click."""
        if self.on_open_folder:
            self.on_open_folder()
    
    def set_extract_enabled(self, enabled: bool):
        """Enable or disable the extract button."""
        state = 'normal' if enabled else 'disabled'
        self.extract_btn.configure(state=state)
    
    def set_extract_text(self, text: str):
        """Set the extract button text."""
        self.extract_btn.configure(text=text)
    
    def set_processing(self, processing: bool):
        """Set processing state (disable button, change text)."""
        if processing:
            self.set_extract_enabled(False)
            self.set_extract_text("⏳ Processing...")
        else:
            self.set_extract_enabled(True)
            self.set_extract_text("🔧 Extract Pages")
