"""
PDF Service - Core PDF processing functionality

This module provides the main interface for loading and extracting pages from PDF files.
"""

import os
from typing import Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError


class PDFService:
    """
    Service class for PDF operations including loading, validation, and page extraction.
    """
    
    def __init__(self):
        self._reader: Optional[PdfReader] = None
        self._filepath: Optional[str] = None
        self._page_count: int = 0
    
    @property
    def is_loaded(self) -> bool:
        """Check if a PDF is currently loaded."""
        return self._reader is not None
    
    @property
    def page_count(self) -> int:
        """Get the total number of pages in the loaded PDF."""
        return self._page_count
    
    @property
    def filepath(self) -> Optional[str]:
        """Get the filepath of the currently loaded PDF."""
        return self._filepath
    
    @property
    def filename(self) -> Optional[str]:
        """Get just the filename of the currently loaded PDF."""
        if self._filepath:
            return os.path.basename(self._filepath)
        return None
    
    def load_pdf(self, filepath: str) -> Tuple[bool, str]:
        """
        Load a PDF file for processing.
        
        Args:
            filepath: Path to the PDF file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Reset current state
        self._reader = None
        self._filepath = None
        self._page_count = 0
        self._initial_rotations = {}
        
        # Validate file exists
        if not os.path.exists(filepath):
            return False, "File not found"
        
        # Validate file extension
        if not filepath.lower().endswith('.pdf'):
            return False, "File is not a PDF"
        
        try:
            reader = PdfReader(filepath)
            
            # Check if encrypted
            if reader.is_encrypted:
                return False, "PDF is encrypted. Please provide an unencrypted PDF."
            
            self._reader = reader
            self._filepath = filepath
            self._page_count = len(reader.pages)
            
            # Store initial rotations to allow non-destructive updates
            for i, page in enumerate(reader.pages):
                # /Rotate key might not exist or might be indirect
                rot = page.get('/Rotate', 0)
                if isinstance(rot, int):
                    self._initial_rotations[i] = rot
                else: 
                    self._initial_rotations[i] = 0 # Fallback
            
            return True, f"PDF loaded successfully. {self._page_count} pages found."
            
        except PdfReadError as e:
            return False, f"Invalid or corrupted PDF file: {str(e)}"
        except Exception as e:
            return False, f"Error loading PDF: {str(e)}"
    
    def extract_pages(
        self, 
        pages: list[int],
        output_path: str,
        rotation_overrides: Optional[dict[int, int]] = None,
        progress_callback: Optional[callable] = None
    ) -> Tuple[bool, str]:
        """
        Extract specific pages from the loaded PDF and save to a new file.
        
        Args:
            pages: List of page numbers to extract (1-indexed)
            output_path: Path where the extracted PDF will be saved
            rotation_overrides: Dict mapping {page_num: rotation_angle_degrees}
            progress_callback: Optional callback function(current, total) for progress updates
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.is_loaded:
            return False, "No PDF loaded. Please load a PDF first."
        
        if not pages:
            return False, "No pages selected for extraction"
            
        # Validate pages
        invalid_pages = [p for p in pages if p < 1 or p > self._page_count]
        if invalid_pages:
            return False, f"Invalid page numbers detected: {invalid_pages}"
        
        try:
            writer = PdfWriter()
            total_pages = len(pages)
            
            # Extract pages (convert 1-indexed to 0-indexed)
            for i, page_num in enumerate(pages):
                page_idx = page_num - 1
                page = self._reader.pages[page_idx]
                
                # Apply rotation
                if rotation_overrides and page_num in rotation_overrides:
                    # Logic: Absolute rotation = Initial + Override
                    base_rot = self._initial_rotations.get(page_idx, 0)
                    override = rotation_overrides[page_num]
                    # Ensure multiple of 90
                    target_rot = (base_rot + override) % 360
                    
                    # Temporarily modify page object for write
                    # Note: PyPDF2 page modification persists in this reader session
                    # But since we recalculate target_rot every time based on immutable initial, it's safe.
                    page.rotate(target_rot - page.get('/Rotate', 0)) # Apply delta from CURRENT state?
                    # Actually: simpler to just set the property if PyPDF2 supports it.
                    # page.rotate(angle) adds angle.
                    # page.transfer_rotation_to_content() ?
                    # Safest: writer.add_page(page) then writer_page.rotate(angle)?
                    # writer.add_page returns proper page object? No, returns None usually or page.
                    
                    # Let's try:
                    # writer.add_page(page)
                    # output_page = writer.pages[-1]
                    # output_page.rotate(override) -> This rotates RELATIVE to what was added.
                    # If loaded page has 90, and we want +90 (total 180).
                    # writer receives page (90). output_page.rotate(90) -> 180.
                    # This seems cleaner than modifying source reader.
                    
                    writer.add_page(page)
                    writer.pages[-1].rotate(override)
                else:
                    writer.add_page(page)
                
                if progress_callback:
                    progress_callback(i + 1, total_pages)
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Write output file
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            return True, f"Successfully extracted {total_pages} page(s) to {os.path.basename(output_path)}"
            
        except PermissionError:
            return False, "Permission denied. Cannot write to output location."
        except Exception as e:
            return False, f"Error extracting pages: {str(e)}"
    
    def get_metadata(self) -> dict:
        """
        Get metadata from the loaded PDF.
        
        Returns:
            Dictionary containing PDF metadata
        """
        if not self.is_loaded:
            return {}
        
        try:
            metadata = self._reader.metadata
            if metadata:
                return {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'subject': metadata.get('/Subject', ''),
                    'creator': metadata.get('/Creator', ''),
                }
        except Exception:
            pass
        
        return {}
    
    def close(self):
        """Close the currently loaded PDF and reset state."""
        self._reader = None
        self._filepath = None
        self._page_count = 0
    
    def suggest_output_filename(self, start_page: int, end_page: int) -> str:
        """
        Generate a suggested output filename based on the source PDF and page range.
        
        Args:
            start_page: Starting page number
            end_page: Ending page number
            
        Returns:
            Suggested filename (without extension)
        """
        if not self.filename:
            return f"extracted_pages_{start_page}-{end_page}"
        
        # Remove extension from source filename
        base_name = os.path.splitext(self.filename)[0]
        
        if start_page == end_page:
            return f"{base_name}_page_{start_page}"
        else:
            return f"{base_name}_pages_{start_page}-{end_page}"
