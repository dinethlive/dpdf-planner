"""
Single Page Window - View a specific page in detail with Zoom and Pan
"""
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

class SinglePageWindow(tk.Toplevel):
    """
    Popup window to view a single page with zoom, pan and crop capabilities.
    """

    def __init__(self, parent, page_num: int, image: Image.Image,
                 initial_rotation: int = 0, initial_crop=None,
                 on_rotate=None, on_crop=None, on_close=None):
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

        # Crop state. crop_norm is (l, t, r, b) normalized to ORIGINAL (un-rotated)
        # image space, top-left origin. None = no crop.
        self.crop_norm = initial_crop
        self.crop_mode = False
        self._crop_drag_start = None  # (x, y) in canvas coords
        self._crop_canvas_id = None   # Tkinter canvas item for the rect overlay

        self.on_close_callback = on_close
        self.on_rotate_callback = on_rotate
        self.on_crop_callback = on_crop

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

        # Crop controls
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=8)
        self.crop_btn = ttk.Button(toolbar, text="Crop", command=self._toggle_crop_mode)
        self.crop_btn.pack(side="left", padx=5)
        ttk.Button(toolbar, text="Clear Crop", command=self._clear_crop).pack(side="left", padx=5)

        # Crop status label
        self.crop_status = tk.Label(toolbar, text="", bg="#2b2b2b", fg="#9ad0ff", font=("Segoe UI", 9))
        self.crop_status.pack(side="left", padx=10)

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
            yscrollcommand=self.v_scroll.set,
            cursor="arrow"
        )

        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        # Layout
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bindings
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind("<Control-MouseWheel>", self._on_zoom_wheel)  # Windows Zoom

        self._update_crop_status()

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
        self._crop_canvas_id = None
        # Center image
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        self.canvas.config(scrollregion=(0, 0, new_width, new_height))

        # Redraw existing crop rectangle if any
        if self.crop_norm:
            self._draw_crop_overlay()

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

    # ---------------- Crop logic ----------------

    def _toggle_crop_mode(self):
        """Enter/exit crop selection mode."""
        self.crop_mode = not self.crop_mode
        if self.crop_mode:
            self.crop_btn.configure(text="Crop: ON")
            self.canvas.configure(cursor="crosshair")
        else:
            self.crop_btn.configure(text="Crop")
            self.canvas.configure(cursor="arrow")
        self._update_crop_status()

    def _clear_crop(self):
        """Remove the current crop selection."""
        if self.crop_norm is None and self._crop_canvas_id is None:
            return
        self.crop_norm = None
        if self._crop_canvas_id is not None:
            self.canvas.delete(self._crop_canvas_id)
            self._crop_canvas_id = None
        self._update_crop_status()
        if self.on_crop_callback:
            self.on_crop_callback(self.page_num, None)

    def _update_crop_status(self):
        """Update the small status label next to crop buttons."""
        if self.crop_mode:
            self.crop_status.configure(
                text="Drag on the page to select a crop area.",
                fg="#ffc080"
            )
        elif self.crop_norm is not None:
            l, t, r, b = self.crop_norm
            self.crop_status.configure(
                text=f"Crop set: {int((r-l)*100)}% × {int((b-t)*100)}% of page",
                fg="#9ad0ff"
            )
        else:
            self.crop_status.configure(text="", fg="#9ad0ff")

    def _on_mouse_down(self, event):
        """Either start panning or start drawing crop rect."""
        if self.crop_mode:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            self._crop_drag_start = (x, y)
            # Remove previous overlay
            if self._crop_canvas_id is not None:
                self.canvas.delete(self._crop_canvas_id)
            self._crop_canvas_id = self.canvas.create_rectangle(
                x, y, x, y, outline="#00ff88", width=2, dash=(6, 4)
            )
        else:
            self.canvas.scan_mark(event.x, event.y)

    def _on_mouse_drag(self, event):
        """Either pan or update crop rect."""
        if self.crop_mode and self._crop_drag_start is not None:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            x0, y0 = self._crop_drag_start
            self.canvas.coords(self._crop_canvas_id, x0, y0, x, y)
        else:
            self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mouse_up(self, event):
        """Finish crop selection."""
        if not self.crop_mode or self._crop_drag_start is None:
            return
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        x0, y0 = self._crop_drag_start
        self._crop_drag_start = None

        # Normalize coords (top-left, bottom-right)
        cl, cr = sorted((x0, x))
        ct, cb = sorted((y0, y))

        # Clamp to displayed image area
        disp_w, disp_h = self._displayed_image_size()
        cl = max(0, min(cl, disp_w))
        cr = max(0, min(cr, disp_w))
        ct = max(0, min(ct, disp_h))
        cb = max(0, min(cb, disp_h))

        # Ignore tiny selections (< 1% of page)
        if (cr - cl) < disp_w * 0.01 or (cb - ct) < disp_h * 0.01:
            if self._crop_canvas_id is not None:
                self.canvas.delete(self._crop_canvas_id)
                self._crop_canvas_id = None
            return

        # Convert displayed-canvas rect to normalized ORIGINAL-image coords
        self.crop_norm = self._displayed_rect_to_original_norm((cl, ct, cr, cb))

        # Snap the on-screen rect to the clamped values
        self.canvas.coords(self._crop_canvas_id, cl, ct, cr, cb)

        # Exit crop mode automatically once a selection is made
        self.crop_mode = False
        self.crop_btn.configure(text="Crop")
        self.canvas.configure(cursor="arrow")
        self._update_crop_status()

        if self.on_crop_callback:
            self.on_crop_callback(self.page_num, self.crop_norm)

    def _displayed_image_size(self):
        """Size in canvas pixels of the rotated+scaled image currently displayed."""
        ow, oh = self.original_image.size
        if self.rotation_angle % 180 != 0:
            ow, oh = oh, ow
        return ow * self.current_scale, oh * self.current_scale

    def _displayed_rect_to_original_norm(self, rect):
        """
        Convert a rect in canvas coords (post-rotation, post-scale) to a
        normalized (l, t, r, b) in the ORIGINAL un-rotated image.
        """
        cl, ct, cr, cb = rect
        s = self.current_scale
        # Un-scale → coords in the rotated (but unscaled) image
        dl, dt, dr, db = cl / s, ct / s, cr / s, cb / s

        ow, oh = self.original_image.size  # original (un-rotated) size
        angle = self.rotation_angle % 360

        if angle == 0:
            ol, ot, or_, ob = dl, dt, dr, db
        elif angle == 90:
            # Display image is rotated 90 CW from original (size oh × ow)
            ol, ot = dt, oh - dr
            or_, ob = db, oh - dl
        elif angle == 180:
            ol, ot = ow - dr, oh - db
            or_, ob = ow - dl, oh - dt
        elif angle == 270:
            ol, ot = ow - db, dl
            or_, ob = ow - dt, dr
        else:
            # Non-multiple of 90 not supported; treat as identity
            ol, ot, or_, ob = dl, dt, dr, db

        return (ol / ow, ot / oh, or_ / ow, ob / oh)

    def _original_norm_to_displayed_rect(self, crop_norm):
        """
        Convert normalized (l, t, r, b) in ORIGINAL image space to canvas
        coords for drawing the overlay on the currently displayed image.
        """
        l, t, r, b = crop_norm
        ow, oh = self.original_image.size
        ol, ot, or_, ob = l * ow, t * oh, r * ow, b * oh

        angle = self.rotation_angle % 360
        if angle == 0:
            dl, dt, dr, db = ol, ot, or_, ob
        elif angle == 90:
            dl, dt = oh - ob, ol
            dr, db = oh - ot, or_
        elif angle == 180:
            dl, dt = ow - or_, oh - ob
            dr, db = ow - ol, oh - ot
        elif angle == 270:
            dl, dt = ot, ow - or_
            dr, db = ob, ow - ol
        else:
            dl, dt, dr, db = ol, ot, or_, ob

        s = self.current_scale
        return (dl * s, dt * s, dr * s, db * s)

    def _draw_crop_overlay(self):
        """Draw the current crop rectangle on the canvas."""
        if self.crop_norm is None:
            return
        rect = self._original_norm_to_displayed_rect(self.crop_norm)
        self._crop_canvas_id = self.canvas.create_rectangle(
            *rect, outline="#00ff88", width=2, dash=(6, 4)
        )

    def _start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_close(self):
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
