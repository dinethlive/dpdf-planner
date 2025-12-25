"""
Validation Service - Input validation for the application

Provides validation functions for page ranges, filenames, and file paths.
"""

import os
import re
from typing import Tuple, Optional


class ValidationService:
    """
    Service class for validating user inputs.
    """
    
    # Characters not allowed in Windows filenames
    INVALID_FILENAME_CHARS = r'[<>:"/\\|?*]'
    INVALID_FILENAME_PATTERN = re.compile(INVALID_FILENAME_CHARS)
    
    # Reserved Windows filenames
    RESERVED_NAMES = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    @classmethod
    def validate_page_range(
        cls, 
        start_page: Optional[int], 
        end_page: Optional[int], 
        total_pages: int
    ) -> Tuple[bool, str]:
        """
        Validate a page range against the total page count.
        
        Args:
            start_page: Starting page number (1-indexed)
            end_page: Ending page number (1-indexed)
            total_pages: Total number of pages in the PDF
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if start_page is None:
            return False, "Start page is required"
        
        if end_page is None:
            return False, "End page is required"
        
        if not isinstance(start_page, int) or not isinstance(end_page, int):
            return False, "Page numbers must be integers"
        
        if start_page < 1:
            return False, "Start page must be at least 1"
        
        if end_page < 1:
            return False, "End page must be at least 1"
        
        if start_page > total_pages:
            return False, f"Start page ({start_page}) exceeds total pages ({total_pages})"
        
        if end_page > total_pages:
            return False, f"End page ({end_page}) exceeds total pages ({total_pages})"
        
        if start_page > end_page:
            return False, f"Start page ({start_page}) cannot be greater than end page ({end_page})"
        
        return True, ""
    
    @classmethod
    def validate_filename(cls, filename: str) -> Tuple[bool, str]:
        """
        Validate a filename for Windows filesystem compatibility.
        
        Args:
            filename: The filename to validate (without path, without extension)
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not filename:
            return False, "Filename cannot be empty"
        
        if not filename.strip():
            return False, "Filename cannot be only whitespace"
        
        # Check for invalid characters
        if cls.INVALID_FILENAME_PATTERN.search(filename):
            return False, 'Filename contains invalid characters: < > : " / \\ | ? *'
        
        # Check for reserved names
        name_upper = filename.upper().split('.')[0]
        if name_upper in cls.RESERVED_NAMES:
            return False, f"'{filename}' is a reserved Windows filename"
        
        # Check length (Windows max is 255 chars for filename)
        if len(filename) > 200:  # Leave room for extension and path
            return False, "Filename is too long (max 200 characters)"
        
        # Check for leading/trailing spaces or periods
        if filename.startswith(' ') or filename.endswith(' '):
            return False, "Filename cannot start or end with spaces"
        
        if filename.endswith('.'):
            return False, "Filename cannot end with a period"
        
        return True, ""
    
    @classmethod
    def validate_output_path(cls, output_path: str) -> Tuple[bool, str]:
        """
        Validate an output file path.
        
        Args:
            output_path: Full path where the file will be saved
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not output_path:
            return False, "Output path is required"
        
        # Get directory
        directory = os.path.dirname(output_path)
        
        if directory:
            # Check if directory exists or can be created
            if not os.path.exists(directory):
                try:
                    # Try to check if we can create it
                    parent = os.path.dirname(directory)
                    if parent and not os.path.exists(parent):
                        return False, f"Parent directory does not exist: {parent}"
                except Exception as e:
                    return False, f"Invalid directory path: {str(e)}"
            elif not os.path.isdir(directory):
                return False, f"Path is not a directory: {directory}"
            elif not os.access(directory, os.W_OK):
                return False, f"No write permission for directory: {directory}"
        
        # Validate filename
        filename = os.path.basename(output_path)
        if filename.lower().endswith('.pdf'):
            filename = filename[:-4]
        
        return cls.validate_filename(filename)
    
    @classmethod
    def validate_pdf_file(cls, filepath: str) -> Tuple[bool, str]:
        """
        Validate that a file path points to a valid PDF file.
        
        Args:
            filepath: Path to the PDF file
            
        Returns:
            Tuple of (is_valid: bool, error_message: str)
        """
        if not filepath:
            return False, "No file selected"
        
        if not os.path.exists(filepath):
            return False, "File does not exist"
        
        if not os.path.isfile(filepath):
            return False, "Path is not a file"
        
        if not filepath.lower().endswith('.pdf'):
            return False, "File is not a PDF (must have .pdf extension)"
        
        if not os.access(filepath, os.R_OK):
            return False, "No read permission for file"
        
        return True, ""
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """
        Sanitize a filename by removing or replacing invalid characters.
        
        Args:
            filename: The filename to sanitize
            
        Returns:
            Sanitized filename
        """
        # Remove invalid characters
        sanitized = cls.INVALID_FILENAME_PATTERN.sub('_', filename)
        
        # Remove leading/trailing spaces and periods
        sanitized = sanitized.strip(' .')
        
        # If empty after sanitization, provide default
        if not sanitized:
            sanitized = "extracted_pages"
        
        # Truncate if too long
        if len(sanitized) > 200:
            sanitized = sanitized[:200]
        
        return sanitized
