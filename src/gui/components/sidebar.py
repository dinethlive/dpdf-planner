"""
Sidebar Component
Encapsulates the FilePicker, OutputConfig, and ActionBar.
"""
import tkinter as tk
from tkinter import ttk
from gui.themes.dark_theme import DarkTheme
from gui.components.file_picker import FilePicker
from gui.components.output_config import OutputConfig
from gui.components.status_bar import ActionBar

class Sidebar(tk.Frame):
    def __init__(self, parent, 
                 initial_input_dir: str,
                 initial_output_dir: str,
                 on_file_selected,
                 on_output_changed,
                 on_extract,
                 on_open_folder,
                 on_clear_selection,
                 **kwargs):
        super().__init__(parent, **kwargs)
        
        self.initial_input_dir = initial_input_dir
        self.initial_output_dir = initial_output_dir
        self.on_file_selected = on_file_selected
        self.on_output_changed = on_output_changed
        self.on_extract = on_extract
        self.on_open_folder = on_open_folder
        self.on_clear_selection = on_clear_selection
        
        self._setup_ui()
        
    def _setup_ui(self):
        # Header
        tk.Label(
            self,
            text="PDF Extractor",
            bg=self['bg'],
            fg=DarkTheme.COLORS['text_primary'],
            font=DarkTheme.get_font('header', bold=True)
        ).pack(anchor='w', pady=(0, 20))
        
        # 1. Source File
        tk.Label(self, text="SOURCE", font=DarkTheme.get_font('small', bold=True), 
                 bg=self['bg'], fg=DarkTheme.COLORS['text_secondary']).pack(anchor='w')
        
        self.file_picker = FilePicker(
            self,
            on_file_selected=self.on_file_selected,
            initial_dir=self.initial_input_dir
        )
        self.file_picker.pack(fill='x', pady=(5, 20))
        self._add_card_padding(self.file_picker)
        
        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=(0, 20))
        
        # 2. Output Settings
        tk.Label(self, text="OUTPUT", font=DarkTheme.get_font('small', bold=True), 
                 bg=self['bg'], fg=DarkTheme.COLORS['text_secondary']).pack(anchor='w')
        
        self.output_config = OutputConfig(
            self,
            default_directory=self.initial_output_dir,
            on_config_changed=self.on_output_changed
        )
        self.output_config.pack(fill='x', pady=(5, 20))
        self._add_card_padding(self.output_config)
        
        # Separator
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=(0, 20))
        
        # 3. Actions
        self.action_bar = ActionBar(
            self,
            on_extract=self.on_extract,
            on_open_folder=self.on_open_folder,
            on_clear_selection=self.on_clear_selection
        )
        self.action_bar.pack(fill='x', pady=(0, 20))
        
    def _add_card_padding(self, widget):
        widget.configure(padding=(16, 12))

    # Public Interface
    def set_filename(self, name):
        self.output_config.set_filename(name)
        
    def get_filename(self):
        return self.output_config.get_filename()
        
    def set_filename_validation(self, error):
        self.output_config.set_filename_validation(error)
        
    def get_output_directory(self):
        return self.output_config.get_output_directory()
        
    def get_full_output_path(self):
        return self.output_config.get_full_output_path()
        
    def set_extract_enabled(self, enabled: bool):
        self.action_bar.set_extract_enabled(enabled)
        
    def set_processing(self, processing: bool):
        self.action_bar.set_processing(processing)
