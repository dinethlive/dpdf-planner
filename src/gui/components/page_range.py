"""
Page Range Component - Page range selection widget

Provides start/end page inputs with validation and quick action buttons.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Tuple

from gui.themes.dark_theme import DarkTheme


class PageRangeSelector(ttk.Frame):
    """
    Page range selector with start/end inputs and quick action buttons.
    """
    
    def __init__(
        self, 
        parent,
        on_range_changed: Optional[Callable[[int, int], None]] = None,
        **kwargs
    ):
        super().__init__(parent, style='Card.TFrame', **kwargs)
        
        self.on_range_changed = on_range_changed
        self._total_pages = 0
        self._validation_callback: Optional[Callable] = None
        
        self._create_widgets()
        self.set_enabled(False)  # Disabled until PDF is loaded
    
    def _create_widgets(self):
        """Create the page range UI elements."""
        # Title with page count
        title_frame = ttk.Frame(self, style='Card.TFrame')
        title_frame.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(0, 8))
        
        title_label = ttk.Label(
            title_frame,
            text="📊 Page Range",
            style='Card.TLabel',
            font=DarkTheme.get_font('large', bold=True)
        )
        title_label.pack(side='left')
        
        self.page_count_label = ttk.Label(
            title_frame,
            text="",
            style='Card.TLabel',
            font=DarkTheme.get_font('small')
        )
        self.page_count_label.pack(side='left', padx=(8, 0))
        
        # Start page
        start_label = ttk.Label(
            self,
            text="Start Page:",
            style='Card.TLabel'
        )
        start_label.grid(row=1, column=0, sticky='w', pady=4)
        
        self.start_var = tk.StringVar(value="1")
        self.start_entry = ttk.Spinbox(
            self,
            from_=1,
            to=1,
            width=10,
            textvariable=self.start_var,
            validate='key',
            validatecommand=(self.register(self._validate_number), '%P')
        )
        self.start_entry.grid(row=1, column=1, sticky='w', padx=(8, 16), pady=4)
        self.start_var.trace_add('write', self._on_range_change)
        
        # End page
        end_label = ttk.Label(
            self,
            text="End Page:",
            style='Card.TLabel'
        )
        end_label.grid(row=1, column=2, sticky='w', pady=4)
        
        self.end_var = tk.StringVar(value="1")
        self.end_entry = ttk.Spinbox(
            self,
            from_=1,
            to=1,
            width=10,
            textvariable=self.end_var,
            validate='key',
            validatecommand=(self.register(self._validate_number), '%P')
        )
        self.end_entry.grid(row=1, column=3, sticky='w', padx=(8, 0), pady=4)
        self.end_var.trace_add('write', self._on_range_change)
        
        # Quick actions frame
        quick_frame = ttk.Frame(self, style='Card.TFrame')
        quick_frame.grid(row=2, column=0, columnspan=4, sticky='w', pady=(12, 0))
        
        quick_label = ttk.Label(
            quick_frame,
            text="⚡ Quick:",
            style='Card.TLabel'
        )
        quick_label.pack(side='left', padx=(0, 8))
        
        # Quick action buttons
        self.quick_buttons = []
        
        btn_first_10 = ttk.Button(
            quick_frame,
            text="First 10",
            command=lambda: self._quick_select('first', 10),
            style='Secondary.TButton',
            width=10
        )
        btn_first_10.pack(side='left', padx=2)
        self.quick_buttons.append(btn_first_10)
        
        btn_last_10 = ttk.Button(
            quick_frame,
            text="Last 10",
            command=lambda: self._quick_select('last', 10),
            style='Secondary.TButton',
            width=10
        )
        btn_last_10.pack(side='left', padx=2)
        self.quick_buttons.append(btn_last_10)
        
        btn_first_half = ttk.Button(
            quick_frame,
            text="First Half",
            command=lambda: self._quick_select('first_half'),
            style='Secondary.TButton',
            width=10
        )
        btn_first_half.pack(side='left', padx=2)
        self.quick_buttons.append(btn_first_half)
        
        btn_all = ttk.Button(
            quick_frame,
            text="All Pages",
            command=lambda: self._quick_select('all'),
            style='Secondary.TButton',
            width=10
        )
        btn_all.pack(side='left', padx=2)
        self.quick_buttons.append(btn_all)
        
        # Validation message
        self.validation_label = tk.Label(
            self,
            text="",
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['error'],
            font=DarkTheme.get_font('small'),
            anchor='w'
        )
        self.validation_label.grid(row=3, column=0, columnspan=4, sticky='w', pady=(8, 0))
    
    def _validate_number(self, value: str) -> bool:
        """Validate that input is a valid number."""
        if value == "":
            return True
        try:
            num = int(value)
            return num >= 0
        except ValueError:
            return False
    
    def _on_range_change(self, *args):
        """Handle range value changes."""
        start, end = self.get_range()
        
        # Clear validation message on change
        self.set_validation_message("")
        
        # Notify callback
        if self.on_range_changed and start is not None and end is not None:
            self.on_range_changed(start, end)
    
    def _quick_select(self, mode: str, count: int = 0):
        """Apply quick selection preset."""
        if self._total_pages == 0:
            return
        
        if mode == 'first':
            start = 1
            end = min(count, self._total_pages)
        elif mode == 'last':
            start = max(1, self._total_pages - count + 1)
            end = self._total_pages
        elif mode == 'first_half':
            start = 1
            end = max(1, self._total_pages // 2)
        elif mode == 'all':
            start = 1
            end = self._total_pages
        else:
            return
        
        self.start_var.set(str(start))
        self.end_var.set(str(end))
    
    def set_total_pages(self, total: int):
        """
        Set the total page count and update UI accordingly.
        
        Args:
            total: Total number of pages in the PDF
        """
        self._total_pages = total
        
        # Update spinbox ranges
        self.start_entry.configure(to=total)
        self.end_entry.configure(to=total)
        
        # Update page count display
        self.page_count_label.configure(text=f"(Total: {total} pages)")
        
        # Set default values
        self.start_var.set("1")
        self.end_var.set(str(total))
        
        # Enable controls
        self.set_enabled(True)
    
    def get_range(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Get the current page range.
        
        Returns:
            Tuple of (start_page, end_page), or (None, None) if invalid
        """
        try:
            start = int(self.start_var.get()) if self.start_var.get() else None
            end = int(self.end_var.get()) if self.end_var.get() else None
            return start, end
        except ValueError:
            return None, None
    
    def set_enabled(self, enabled: bool):
        """Enable or disable the page range controls."""
        state = 'normal' if enabled else 'disabled'
        self.start_entry.configure(state=state)
        self.end_entry.configure(state=state)
        
        for btn in self.quick_buttons:
            btn.configure(state=state)
    
    def set_validation_message(self, message: str, is_error: bool = True):
        """
        Set or clear the validation message.
        
        Args:
            message: Validation message to display (empty to clear)
            is_error: Whether this is an error (red) or info (blue)
        """
        if message:
            color = DarkTheme.COLORS['error'] if is_error else DarkTheme.COLORS['info']
            self.validation_label.configure(text=f"⚠ {message}", fg=color)
        else:
            self.validation_label.configure(text="")
    
    def reset(self):
        """Reset the page range controls."""
        self._total_pages = 0
        self.start_var.set("1")
        self.end_var.set("1")
        self.page_count_label.configure(text="")
        self.set_validation_message("")
        self.set_enabled(False)
