"""
File Utilities - File system helper functions
"""

import os
import subprocess
import sys
from pathlib import Path


def open_folder_in_explorer(folder_path: str) -> bool:
    """
    Open a folder in Windows Explorer.
    
    Args:
        folder_path: Path to the folder to open
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(folder_path):
            return False
        
        # Use os.startfile on Windows for best results
        if sys.platform == 'win32':
            os.startfile(folder_path)
        else:
            # Fallback for other platforms
            subprocess.Popen(['explorer', folder_path])
        
        return True
    except Exception:
        return False


def open_file_in_explorer(file_path: str) -> bool:
    """
    Open Windows Explorer with the specified file selected.
    
    Args:
        file_path: Path to the file to highlight
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            return False
        
        if sys.platform == 'win32':
            subprocess.Popen(['explorer', '/select,', file_path])
            return True
        
        return False
    except Exception:
        return False


def get_file_size_formatted(file_path: str) -> str:
    """
    Get the file size in a human-readable format.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Formatted size string (e.g., "1.5 MB")
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return format_bytes(size_bytes)
    except Exception:
        return "Unknown"


def format_bytes(size_bytes: int) -> str:
    """
    Format bytes into a human-readable string.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            if unit == 'B':
                return f"{size_bytes} {unit}"
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def ensure_unique_filename(file_path: str) -> str:
    """
    Ensure a filename is unique by appending a number if needed.
    
    Args:
        file_path: Original file path
        
    Returns:
        Unique file path (with number suffix if original exists)
    """
    if not os.path.exists(file_path):
        return file_path
    
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    while True:
        new_filename = f"{name} ({counter}){ext}"
        new_path = os.path.join(directory, new_filename)
        if not os.path.exists(new_path):
            return new_path
        counter += 1


def truncate_path(path: str, max_length: int = 50) -> str:
    """
    Truncate a file path for display, keeping the filename visible.
    
    Args:
        path: Full file path
        max_length: Maximum length of the returned string
        
    Returns:
        Truncated path with ellipsis if needed
    """
    if len(path) <= max_length:
        return path
    
    filename = os.path.basename(path)
    
    # If filename itself is too long, just truncate it
    if len(filename) >= max_length - 3:
        return '...' + filename[-(max_length - 3):]
    
    # Otherwise, truncate the directory part
    remaining = max_length - len(filename) - 4  # 4 for "...\"
    if remaining > 0:
        directory = os.path.dirname(path)
        return '...' + directory[-remaining:] + os.sep + filename
    
    return '...' + filename
