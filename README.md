# dpdf-planner

<div align="center">

**A Modern Windows Desktop Application for PDF Page Extraction**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

*Extract specific page ranges from PDF files with an intuitive, modern interface*

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Building from Source](#building-from-source)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**dpdf-planner** is a desktop application designed to simplify PDF page extraction. Whether you need to extract a single page, a range, or use quick presets, this tool provides an efficient, user-friendly solution with a modern dark-themed interface.

### Why dpdf-planner?

- **No Complex Tools**: Simple, focused functionality without overwhelming features
- **Offline Processing**: All operations happen locally—no cloud uploads
- **Smart Defaults**: Auto-suggested filenames and remembered preferences
- **Professional UI**: Modern dark theme with vibrant accents

---

## ✨ Features

### Core Functionality
| Feature | Description |
|---------|-------------|
| 📄 **PDF Loading** | Load and validate PDF files with comprehensive error checking |
| 📊 **Page Range Selection** | Extract specific pages using 1-indexed, human-readable numbering |
| 💾 **Custom Output** | Name your extracted files with automatic `.pdf` extension |
| ⚡ **Progress Tracking** | Real-time progress bar during extraction |
| ✅ **Validation** | Live input validation with inline error messages |

### User Experience Enhancements
| Feature | Description |
|---------|-------------|
| 🎨 **Dark Theme** | Modern dark UI with vibrant coral accent (#e94560) |
| ⚡ **Quick Actions** | Preset buttons: First 10, Last 10, First Half, All Pages |
| 💾 **Persistent Preferences** | Remembers last-used folders and settings |
| 📂 **Quick Access** | Open output folder directly from the app |
| 🔄 **Auto-Suggestions** | Intelligent filename suggestions based on source PDF |
| 🛡️ **Overwrite Protection** | Confirmation dialogs prevent accidental file replacement |

---

## 🚀 Quick Start

### For End Users (Standalone Executable)

1. **Download** the latest `dpdf-planner.exe` from the releases
2. **Double-click** to run (no installation needed)
3. **Browse** for a PDF file
4. **Select** your page range
5. **Extract** and done!

### For Developers (From Source)

```bash
# Clone the repository
git clone <repository-url>
cd dpdf-planner

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

---

## 📦 Installation

### Option 1: Standalone Executable (Recommended)

**No Python installation required!**

1. Download `dpdf-planner.exe` from the [releases page](#)
2. Place it anywhere on your computer
3. Run the executable

**System Requirements:**
- Windows 10 or Windows 11
- ~20 MB disk space

### Option 2: From Source

**Requirements:**
- Python 3.13 or higher
- pip (Python package manager)

**Installation Steps:**

```bash
# 1. Clone the repository
git clone <repository-url>
cd dpdf-planner

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python src/main.py
```

---

## 📖 Usage

### Basic Workflow

```
1. Load PDF → 2. Select Range → 3. Name Output → 4. Extract
```

### Step-by-Step Guide

#### 1. **Load a PDF File**
   - Click the **Browse** button
   - Navigate to your PDF file
   - Select and open

   *The app will display the total page count*

#### 2. **Select Page Range**
   - **Manual Entry**: Type start and end page numbers
   - **Quick Actions**: Use preset buttons
     - `First 10` - Pages 1-10
     - `Last 10` - Last 10 pages
     - `First Half` - First 50% of pages
     - `All Pages` - Entire document

#### 3. **Configure Output**
   - **Filename**: Auto-suggested or enter custom name
   - **Location**: Default is `Documents/Extracted PDFs`
   - **Change Folder**: Click `Change` to select different location

#### 4. **Extract Pages**
   - Click **Extract Pages** button
   - Monitor progress bar
   - Choose to open output folder when complete

### Example Scenarios

**Scenario 1: Extract Chapter from eBook**
```
Input: ebook.pdf (500 pages)
Range: Pages 45-78
Output: ebook_chapter_3.pdf
```

**Scenario 2: Extract Last Page (Receipt)**
```
Input: invoice_2024.pdf (3 pages)
Range: Pages 3-3
Output: invoice_2024_receipt.pdf
```

**Scenario 3: Split Large PDF in Half**
```
Input: manual.pdf (200 pages)
Quick Action: "First Half"
Output: manual_pages_1-100.pdf
```

---

## 📚 Documentation

Comprehensive documentation is available in the `[app]docs/` directory:

| Document | Description |
|----------|-------------|
| **[USER_GUIDE.md]([app]docs/USER_GUIDE.md)** | Complete user manual with screenshots and examples |
| **[CHANGELOG.md]([app]docs/CHANGELOG.md)** | Development journey and version history |
| **[ARCHITECTURE.md]([app]docs/ARCHITECTURE.md)** | Technical architecture and design decisions |

### Quick Links

- **First-time users**: Start with [USER_GUIDE.md]([app]docs/USER_GUIDE.md)
- **Developers**: See [ARCHITECTURE.md]([app]docs/ARCHITECTURE.md)
- **Version history**: Check [CHANGELOG.md]([app]docs/CHANGELOG.md)

---

## 🔧 Building from Source

### Prerequisites

```bash
pip install pyinstaller
```

### Build Steps

```bash
# 1. Navigate to project directory
cd dpdf-planner

# 2. Run PyInstaller with spec file
pyinstaller build.spec

# 3. Find executable in dist/ folder
# Output: dist/dpdf-planner.exe
```

### Build Configuration

The `build.spec` file includes:
- Application icon embedding
- Asset bundling
- Hidden imports for PyPDF2 and PIL
- No console window (GUI only)

### Troubleshooting Build Issues

**Issue**: `ModuleNotFoundError` in executable
```bash
# Solution: Clean rebuild
pyinstaller build.spec --clean
```

**Issue**: Icon not embedded
```bash
# Ensure icon exists at: assets/icon.ico
# Supported formats: 16x16, 32x32, 48x48, 256x256
```

---

## 📁 Project Structure

```
dpdf-planner/
│
├── src/                          # Source code
│   ├── main.py                   # Application entry point
│   │
│   ├── gui/                      # User interface
│   │   ├── main_window.py        # Main application window
│   │   ├── components/           # Reusable UI components
│   │   │   ├── file_picker.py    # PDF file selector
│   │   │   ├── page_range.py     # Page range input
│   │   │   ├── output_config.py  # Output configuration
│   │   │   └── status_bar.py     # Status and progress
│   │   └── themes/
│   │       └── dark_theme.py     # Color palette & styling
│   │
│   ├── services/                 # Business logic
│   │   ├── pdf_service.py        # PDF operations
│   │   ├── validation_service.py # Input validation
│   │   └── config_service.py     # User preferences
│   │
│   └── utils/                    # Utilities
│       └── file_utils.py         # File system helpers
│
├── [app]docs/                    # Documentation
│   ├── USER_GUIDE.md             # User manual
│   ├── CHANGELOG.md              # Development history
│   └── ARCHITECTURE.md           # Technical docs
│
├── [initial]docs/                # Requirements
│   └── SRS.md                    # Software Requirements Spec
│
├── assets/                       # Resources
│   └── icon.ico                  # Application icon
│
├── build.spec                    # PyInstaller configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

### Architecture Layers

```
┌─────────────────────────────────┐
│      GUI Layer (Tkinter)        │  ← User Interface
├─────────────────────────────────┤
│     Service Layer (Logic)       │  ← Business Logic
├─────────────────────────────────┤
│    Utils Layer (Helpers)        │  ← Utilities
└─────────────────────────────────┘
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check existing issues
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information

### Suggesting Features

1. Open an issue with `[Feature Request]` prefix
2. Describe the feature and use case
3. Explain why it would be valuable

### Code Contributions

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 dpdf-planner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- **PyPDF2**: PDF processing library
- **Pillow**: Image processing for thumbnails
- **PyInstaller**: Executable packaging
- **Tkinter**: GUI framework

---

## 📞 Support

- **Documentation**: See `[app]docs/` folder
- **Issues**: GitHub Issues (if repository is public)
- **Email**: [Your contact email]

---

<div align="center">

**Made with ❤️ for efficient PDF management**

[⬆ Back to Top](#dpdf-planner)

</div>
