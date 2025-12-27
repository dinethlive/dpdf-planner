# 📄 PDF Page Extractor V2

A modern, user-friendly desktop application for extracting, rotating, and managing PDF pages with an intuitive visual interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### Core Functionality
- **Visual Page Selection**: Grid view with large, clear thumbnails
- **Page Rotation**: Rotate individual pages 90° before extraction
- **Smart Extraction**: Extract selected pages to a new PDF
- **Non-Destructive**: Original PDFs remain unchanged

### User Experience
- **Resizable Interface**: Adjustable sidebar (600px default)
- **Quick Zoom**: Dropdown selection (25%-400%) + manual controls
- **Keyboard Shortcuts**: `Ctrl+A` (Select All), `Esc` (Clear)
- **Interactive Grid**: Hover effects and visual feedback
- **Modern Dark Theme**: Professional, eye-friendly interface

### Advanced Features
- **High-Quality Rendering**: Crystal-clear thumbnails and viewer
- **Zoom & Pan**: Detailed page inspection with smooth controls
- **Progress Tracking**: Real-time extraction progress
- **Smart Defaults**: Auto-populated filenames and directories

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dpdf-planner.git
   cd dpdf-planner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/main.py
   ```

## 📖 Usage

### Basic Workflow
1. **Load PDF**: Click "Select PDF" in the sidebar
2. **Select Pages**: Click pages to select (blue border indicates selection)
3. **Rotate (Optional)**: Double-click pages to rotate if needed
4. **Extract**: Click "Extract Selected Pages"

### Keyboard Shortcuts
- `Ctrl + A`: Select all pages
- `Esc`: Clear selection
- `Ctrl + Mouse Wheel`: Zoom in/out (in page viewer)

### Tips
- **Resize Sidebar**: Drag the divider between sidebar and grid
- **Quick Selection**: Use `Ctrl+A` then click to deselect unwanted pages
- **Verify Pages**: Double-click to view high-resolution preview

## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md) - Detailed usage instructions
- [Architecture](docs/ARCHITECTURE.md) - Technical documentation
- [Changelog](docs/CHANGELOG.md) - Version history

## 🛠️ Technology Stack

- **GUI**: Tkinter/ttk (Python standard library)
- **PDF Processing**: PyPDF2, PyMuPDF (fitz)
- **Image Handling**: Pillow (PIL)
- **Theme**: Custom dark theme

## 🎯 What's New in V2

- ✅ **Page Rotation** with visual feedback
- ✅ **Quick Zoom Dropdown** (25%-400%)
- ✅ **Resizable Sidebar** (drag to adjust)
- ✅ **Keyboard Shortcuts** for power users
- ✅ **Hover Effects** on grid items
- ✅ **Modular Architecture** (cleaner code)
- ✅ **Toast Notifications** (non-blocking)

See [CHANGELOG.md](docs/CHANGELOG.md) for full details.

## 📋 Requirements

```
PyPDF2>=3.0.0
Pillow>=10.0.0
PyMuPDF>=1.23.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- PDF processing powered by PyPDF2 and PyMuPDF
- Icons and UI inspired by modern design principles

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for PDF enthusiasts**
