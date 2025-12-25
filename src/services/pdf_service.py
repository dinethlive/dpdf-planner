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
            
            return True, f"PDF loaded successfully. {self._page_count} pages found."
            
        except PdfReadError as e:
            return False, f"Invalid or corrupted PDF file: {str(e)}"
        except Exception as e:
            return False, f"Error loading PDF: {str(e)}"
    
    def extract_pages(
        self, 
        start_page: int, 
        end_page: int, 
        output_path: str,
        progress_callback: Optional[callable] = None
    ) -> Tuple[bool, str]:
        """
        Extract a range of pages from the loaded PDF and save to a new file.
        
        Args:
            start_page: Starting page number (1-indexed, inclusive)
            end_page: Ending page number (1-indexed, inclusive)
            output_path: Path where the extracted PDF will be saved
            progress_callback: Optional callback function(current, total) for progress updates
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.is_loaded:
            return False, "No PDF loaded. Please load a PDF first."
        
        # Validate page range
        if start_page < 1:
            return False, "Start page must be at least 1"
        
        if end_page > self._page_count:
            return False, f"End page cannot exceed {self._page_count}"
        
        if start_page > end_page:
            return False, "Start page cannot be greater than end page"
        
        try:
            writer = PdfWriter()
            total_pages = end_page - start_page + 1
            
            # Extract pages (convert 1-indexed to 0-indexed)
            for i, page_num in enumerate(range(start_page - 1, end_page)):
                writer.add_page(self._reader.pages[page_num])
                
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
