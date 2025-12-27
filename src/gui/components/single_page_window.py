"""
Single Page Window - View a specific page in detail with Zoom and Pan
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class SinglePageWindow(tk.Toplevel):
    """
    Popup window to view a single page with zoom and pan capabilities.
    """
    
    def __init__(self, parent, page_num: int, image: Image.Image, 
                 initial_rotation: int = 0, on_rotate=None, on_close=None):
        super().__init__(parent)
        self.page_num = page_num
        self.title(f"Page {page_num} - Viewer")
        self.geometry("800x900")
        
        # State
        self.original_image = image
        self.current_scale = 1.0
        self.min_scale = 0.1
        self.max_scale = 5.0
        self.rotation_angle = initial_rotation % 360 # Clockwise degrees
        
        self.on_close_callback = on_close
        self.on_rotate_callback = on_rotate
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._setup_ui()
        self._show_image()
        
    def _setup_ui(self):
        """Setup UI components."""
        # Toolbar
        toolbar = tk.Frame(self, bg="#2b2b2b", padx=5, pady=5)
        toolbar.pack(side="top", fill="x")
        
        ttk.Button(toolbar, text="Zoom In (+)", command=self._zoom_in).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Zoom Out (-)", command=self._zoom_out).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Fit Width", command=self._fit_width).pack(side="left", padx=5)
        
        # Zoom Dropdown
        self.zoom_values = ["25%", "50%", "75%", "100%", "125%", "150%", "200%", "300%", "400%"]
        self.zoom_combo = ttk.Combobox(toolbar, values=self.zoom_values, width=6)
        self.zoom_combo.set("100%")
        self.zoom_combo.pack(side="left", padx=5)
        self.zoom_combo.bind("<<ComboboxSelected>>", self._on_zoom_select)
        self.zoom_combo.bind("<Return>", self._on_zoom_select)
        
        # Rotation Button
        ttk.Button(toolbar, text="Rotate ⟳", command=self._rotate_cw).pack(side="left", padx=5)
        
        ttk.Button(toolbar, text="Close", command=self._on_close).pack(side="right", padx=5)
        
        # Canvas Frame
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        self.v_scroll = ttk.Scrollbar(self.canvas_frame, orient="vertical")
        self.h_scroll = ttk.Scrollbar(self.canvas_frame, orient="horizontal")
        
        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            highlightthickness=0,
            bg="#1e1e1e",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set
        )
        
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)
        
        # Layout
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Bindings
        self.canvas.bind("<ButtonPress-1>", self._start_pan)
        self.canvas.bind("<B1-Motion>", self._pan)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind("<Control-MouseWheel>", self._on_zoom_wheel)  # Windows Zoom
        
    def _show_image(self):
        """Display the image with current scale and rotation."""
        if not self.original_image:
            return
            
        # 1. Rotate (PIL rotates Counter-Clockwise, so use negative for CW)
        # expand=True to ensure corners aren't cropped
        rotated_img = self.original_image.rotate(-self.rotation_angle, expand=True)
            
        # 2. Calculate new size based on ROTATED dimensions
        width, height = rotated_img.size
        new_width = int(width * self.current_scale)
        new_height = int(height * self.current_scale)
        
        # 3. Resize
        resized = rotated_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        
        # Update Canvas
        self.canvas.delete("all")
        # Center image
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        
    def _rotate_cw(self):
        """Rotate clockwise 90 degrees."""
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self._show_image()
        if self.on_rotate_callback:
            self.on_rotate_callback(self.page_num, self.rotation_angle)

    def _zoom_in(self):
        self._set_scale(self.current_scale * 1.2)
        
    def _zoom_out(self):
        self._set_scale(self.current_scale * 0.8)
    
    def _on_zoom_select(self, event=None):
        """Handle zoom selection from dropdown."""
        val = self.zoom_combo.get().strip('%')
        try:
            scale = float(val) / 100.0
            self._set_scale(scale)
            # Refocus canvas to allow scrolling
            self.canvas.focus_set()
        except ValueError:
            pass
        
    def _fit_width(self):
        if not self.original_image: return
        
        # Account for rotation in dimensions
        if self.rotation_angle % 180 != 0:
            # Swapped
            img_width = self.original_image.size[1]
        else:
            img_width = self.original_image.size[0]
            
        canvas_width = self.canvas.winfo_width()
        if canvas_width > 1:
            self._set_scale(canvas_width / img_width)
            
    def _set_scale(self, scale):
        self.current_scale = max(self.min_scale, min(self.max_scale, scale))
        # Update combo text
        if hasattr(self, 'zoom_combo'):
            self.zoom_combo.set(f"{int(self.current_scale * 100)}%")
        self._show_image()

    def _on_mousewheel(self, event):
        """Scroll vertically."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _on_zoom_wheel(self, event):
        """Zoom with Ctrl+Wheel."""
        if event.delta > 0:
            self._zoom_in()
        else:
            self._zoom_out()
            
    def _start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)
        
    def _pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def _on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
