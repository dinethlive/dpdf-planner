"""
Toast Notification Component
Displays a temporary, non-blocking message overlay.
"""
import tkinter as tk
from gui.themes.dark_theme import DarkTheme

class Toast:
    def __init__(self, root, message: str, duration: int = 2500, kind: str = "info"):
        self.root = root
        self.duration = duration
        
        # Colors based on kind
        if kind == "success":
            bg_color = DarkTheme.COLORS['success']
            fg_color = "#ffffff"
        elif kind == "error":
            bg_color = DarkTheme.COLORS['error']
            fg_color = "#ffffff"
        else:
            bg_color = DarkTheme.COLORS['accent']
            fg_color = "#ffffff"
            
        # Create Toplevel for overlay
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True) # Remove window decorations
        
        # Label
        lbl = tk.Label(
            self.window, 
            text=message, 
            bg=bg_color, 
            fg=fg_color,
            font=DarkTheme.get_font('medium', bold=True),
            padx=20,
            pady=10,
            relief='flat'
        )
        lbl.pack()
        
        # Position logic (Bottom Center of Root)
        self.window.update_idletasks()
        
        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()
        root_w = root.winfo_width()
        root_h = root.winfo_height()
        
        win_w = self.window.winfo_width()
        win_h = self.window.winfo_height()
        
        pos_x = root_x + (root_w // 2) - (win_w // 2)
        pos_y = root_y + root_h - win_h - 60 # 60px padding from bottom
        
        self.window.geometry(f"+{pos_x}+{pos_y}")
        
        # Fade animation handling
        self.alpha = 0.0
        self.window.attributes("-alpha", self.alpha)
        self._fade_in()
        
    def _fade_in(self):
        self.alpha += 0.1
        if self.alpha < 1.0:
            self.window.attributes("-alpha", self.alpha)
            self.window.after(15, self._fade_in)
        else:
            self.window.attributes("-alpha", 1.0)
            self.window.after(self.duration, self._fade_out)
            
    def _fade_out(self):
        self.alpha -= 0.1
        if self.alpha > 0:
            self.window.attributes("-alpha", self.alpha)
            self.window.after(20, self._fade_out)
        else:
            self.window.destroy()

def show_toast(root, message, duration=2500, kind="info"):
    """Helper to show a toast."""
    Toast(root, message, duration, kind)
