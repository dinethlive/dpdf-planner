"""
Thumbnail Service - Generates images for PDF pages
"""
import fitz  # PyMuPDF
from PIL import Image
import io
from typing import Optional, Dict

class ThumbnailService:
    """
    Service for rendering PDF pages as images efficiently.
    """
    
    def __init__(self):
        self._cache: Dict[str, Dict[int, Image.Image]] = {}
        
    def get_thumbnail(self, pdf_path: str, page_num: int, width: int = 200) -> Optional[Image.Image]:
        """
        Get a thumbnail for a specific page.
        
        Args:
            pdf_path: Path to the PDF file
            page_num: Page number (1-indexed)
            width: Desired thumbnail width
            
        Returns:
            PIL Image object or None if failed
        """
        # Check cache
        cache_key = (page_num, width)
        if pdf_path in self._cache and cache_key in self._cache[pdf_path]:
            return self._cache[pdf_path][cache_key]
            
        try:
            doc = fitz.open(pdf_path)
            
            if page_num < 1 or page_num > len(doc):
                return None
                
            page = doc.load_page(page_num - 1)
            
            # Calculate zoom factor to match desired width
            pix_width = page.rect.width
            zoom = width / pix_width
            mat = fitz.Matrix(zoom, zoom)
            
            # Render page to pixmap
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Cache the result
            if pdf_path not in self._cache:
                self._cache[pdf_path] = {}
            self._cache[pdf_path][cache_key] = img
            
            doc.close()
            return img
            
        except Exception as e:
            print(f"Error generating thumbnail for {pdf_path} page {page_num}: {e}")
            return None

    def clear_cache(self, pdf_path: Optional[str] = None):
        """
        Clear thumbnail cache.
        
        Args:
            pdf_path: Optional specific PDF path to clear. If None, clears all.
        """
        if pdf_path:
            if pdf_path in self._cache:
                del self._cache[pdf_path]
        else:
            self._cache.clear()
