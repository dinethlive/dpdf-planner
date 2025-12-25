"""
dpdf-planner - PDF Page Extractor

Main entry point for the application.
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from gui.main_window import MainWindow


def main():
    """Application entry point."""
    # Create root window
    root = tk.Tk()
    
    # Set app icon if available
    icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception:
            pass  # Icon loading failed, continue without it
    
    # Create and run main window
    app = MainWindow(root)
    app.run()


if __name__ == "__main__":
    main()
