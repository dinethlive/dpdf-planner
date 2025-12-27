"""
Grid View Component - Displays PDF page thumbnails in a scrollable grid
"""
import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional, Set
from PIL import ImageTk, Image

from services.thumbnail_service import ThumbnailService

class GridView(tk.Frame):
    """
    A scrollable grid of page thumbnails with selection capabilities.
    """
    
    def __init__(self, parent, thumbnail_service: ThumbnailService, 
                 on_selection_change: Callable[[Set[int]], None], 
                 on_page_click: Optional[Callable[[int], None]] = None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        
        self.thumbnail_service = thumbnail_service
        self.on_selection_change = on_selection_change
        self.on_page_click = on_page_click
        
        # State
        self.pdf_path: Optional[str] = None
        self.total_pages: int = 0
        self.selected_pages: Set[int] = set()
        self.rotation_overrides: dict = {} # Map page_num -> angle (degrees CW)
        self.thumbnails: dict = {}  # Map page_num -> dict
        
        self._setup_ui()
    # ... (existing methods until _create_thumbnail_item or _load_image) ...
    
    # Just replacing the end of file for brevity in tool usage?
    # I need to be careful with replace_file_content.
    # The file is 206 lines. I have read it.
    
    # I'll replace from `load_pdf` downwards to update `load_pdf`, `_load_image` and add methods.
    
    # Wait, I need to insert `rotation_overrides` in init.
    # I'll do two replaces. One for init. One for methods.

        
    def _setup_ui(self):
        """Setup the scrollable grid UI."""
        # Canvas with scrollbar
        self.canvas = tk.Canvas(self, bg=self['bg'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.content_frame = tk.Frame(self.canvas, bg=self.canvas['bg'])
        
        # Configure scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        self.content_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Layout
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Grid state
        self.thumb_width = 280 # 240 + padding
        self.current_cols = 1
        
    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_canvas_configure(self, event):
        """Resize the inner frame to match the canvas width and re-grid if needed."""
        width = event.width
        self.canvas.itemconfig(self.canvas_window, width=width)
        
        # Calculate columns
        cols = max(1, width // self.thumb_width)
        if cols != self.current_cols and self.total_pages > 0:
            self.current_cols = cols
            self._regrid()
        
    def _regrid(self):
        """Re-layout thumbnails based on current columns."""
        for page_num in sorted(self.thumbnails.keys()):
            idx = page_num - 1
            row = idx // self.current_cols
            col = idx % self.current_cols
            frame = self.thumbnails[page_num]['frame']
            frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def load_pdf(self, pdf_path: str, total_pages: int):
        """Load a new PDF into the grid."""
        self.clear()
        self.pdf_path = pdf_path
        self.total_pages = total_pages
        
        # Force update to get accurate width logic
        self.update_idletasks()
        width = self.canvas.winfo_width()
        if width > 1:
            self.current_cols = max(1, width // self.thumb_width)
            
        # Initial create widgets
        for i in range(total_pages):
            page_num = i + 1
            self._create_thumbnail_item(page_num)
            
        # Trigger explicit regrid just in case
        self.after(100, self._regrid)
    def _create_thumbnail_item(self, page_num: int):
        """Create a single thumbnail item."""
        # Calculate logical grid position
        idx = page_num - 1
        row = idx // self.current_cols
        col = idx % self.current_cols
        
        # Card Container (Acts as Border)
        # Default border color (unselected)
        border_color = "#333333" if page_num not in self.selected_pages else "#00aaff" # Cyan highlight
        card = tk.Frame(self.content_frame, bg=border_color, padx=3, pady=3)
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        
        # Inner Content Frame
        # Use a slightly lighter dark bg for the content background
        content_bg = "#252526"
        content_frame = tk.Frame(card, bg=content_bg)
        content_frame.pack(fill="both", expand=True)
        
        # Image Label
        lbl_img = tk.Label(content_frame, text=f"Page {page_num}", bg="white", fg="black")
        lbl_img.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Page Number Label (Overlay or below?)
        # Let's put it below cleanly
        lbl_num = tk.Label(content_frame, text=f"Page {page_num}", bg=content_bg, fg="#cccccc", font=("Segoe UI", 9))
        lbl_num.pack(fill="x", pady=(5, 2))
        
        # Bind interactions
        for widget in (card, content_frame, lbl_img, lbl_num):
            widget.bind("<Button-1>", lambda e, p=page_num: self._handle_click(p))
            widget.bind("<Double-Button-1>", lambda e, p=page_num: self._handle_double_click(p))
        
        # Store refs
        self.thumbnails[page_num] = {
            'frame': card,      # This controls border color
            'label': lbl_img,
        }
        
        # Asynchronously load
        self.after(20 * page_num, lambda: self._load_image(page_num))
        
    def _load_image(self, page_num):
        """Load the actual image for a thumbnail."""
        if not self.pdf_path:
            return
            
        # Request larger width for better quality grid
        img = self.thumbnail_service.get_thumbnail(self.pdf_path, page_num, width=240)
        if img:
            # Apply rotation if override exists
            if page_num in self.rotation_overrides:
                # PIL rotate is CCW, we track CW
                angle = self.rotation_overrides[page_num]
                img = img.rotate(-angle, expand=True)

            photo = ImageTk.PhotoImage(img)
            lbl = self.thumbnails[page_num]['label']
            lbl.configure(image=photo, text="", width=240) 
            lbl.image = photo 
            
    def _handle_click(self, page_num: int):
        """Handle click on page card - Toggle selection."""
        if page_num in self.selected_pages:
            self.selected_pages.discard(page_num)
        else:
            self.selected_pages.add(page_num)
            
        self._update_card_style(page_num)
        self.on_selection_change(self.selected_pages)

    def _handle_double_click(self, page_num: int):
        """Handle double click to view page details."""
        if self.on_page_click:
            self.on_page_click(page_num)
        
    def _update_card_style(self, page_num):
        """Update visual style of card based on selection."""
        if page_num not in self.thumbnails:
            return
            
        card = self.thumbnails[page_num]['frame']
        if page_num in self.selected_pages:
            card.configure(bg="#00aaff") # Highlight Color
        else:
            card.configure(bg="#333333") # Default Border

    def clear_selection(self):
        """Clear all selections."""
        # Create a list copy to iterate safely if needed, or just iterate visible
        old_selection = list(self.selected_pages)
        self.selected_pages.clear()
        
        for p in old_selection:
            self._update_card_style(p)
            
        self.on_selection_change(self.selected_pages)

    def refresh_view(self):
        """Refresh the view to match internal state (e.g. selection)."""
        for page_num in self.thumbnails:
            self._update_card_style(page_num)
        
    def clear(self):
        """Clear the grid."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()
        self.selected_pages.clear()
        self.rotation_overrides.clear()
        self.pdf_path = None
        self.total_pages = 0
        
    def set_page_rotation(self, page_num: int, angle: int):
        """Update rotation for a specific page and refresh thumbnail."""
        self.rotation_overrides[page_num] = angle
        # Reload image to reflect rotation
        self._load_image(page_num)
        
    def get_rotations(self) -> dict:
        """Get current rotation overrides."""
        return self.rotation_overrides.copy()
