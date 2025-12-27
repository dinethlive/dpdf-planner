# PDF Page Extractor - User Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Interface Overview](#interface-overview)
- [Features](#features)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Tips & Tricks](#tips--tricks)

## Getting Started

### Installation
1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Launching the Application
```bash
python src/main.py
```

The application will launch in maximized mode with a modern dark theme.

## Interface Overview

### Split-View Layout
The application features a **resizable split-view** layout:

- **Sidebar (Left)**: Controls for loading PDFs, configuring output, and extraction
  - Default width: 600px
  - **Resizable**: Drag the divider to adjust width
  
- **Workspace (Right)**: Grid view of PDF pages
  - Responsive columns (auto-adjusts to window width)
  - Large thumbnails (240px) with A4 aspect ratio

### Components

#### 1. Source Section
- **Select PDF**: Browse and load a PDF file
- Displays filename and page count

#### 2. Output Section
- **Output Directory**: Choose where to save extracted PDFs
- **Filename**: Set the output filename (auto-populated from source)

#### 3. Actions
- **Extract Selected Pages**: Process and save selected pages
- **Clear Selection**: Deselect all pages
- **Open Folder**: Open output directory in file explorer

## Features

### Page Selection
- **Click** any page to select/deselect (blue border indicates selection)
- **Ctrl+A**: Select all pages
- **Esc**: Clear selection
- **Hover Effect**: Pages light up when you hover over them

### Page Viewer (Double-Click)
Double-click any page to open the detailed viewer with:

#### Zoom Controls
- **Zoom In/Out Buttons**: Adjust zoom level
- **Zoom Dropdown**: Quick selection (25%, 50%, 100%, 200%, 400%)
- **Fit Width**: Auto-fit page to window width
- **Ctrl + Mouse Wheel**: Zoom in/out

#### Pan
- **Click and Drag**: Move around the zoomed page

#### Rotation
- **Rotate ⟳ Button**: Rotate page 90° clockwise
- Rotation is applied to the extracted PDF
- Original PDF remains unchanged
- Rotation state is reflected in grid thumbnails

### Interactive Grid
- **Hover Effects**: Visual feedback when hovering over pages
- **Selection Indicator**: Cyan/blue border for selected pages
- **Dynamic Layout**: Columns adjust automatically to window size

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + A` | Select all pages |
| `Esc` | Clear selection |
| `Ctrl + Mouse Wheel` | Zoom in/out (in page viewer) |

## Tips & Tricks

### Efficient Workflow
1. Load your PDF
2. Use `Ctrl+A` to select all, then click to deselect unwanted pages
3. Double-click pages to verify content and rotate if needed
4. Extract to your chosen location

### Rotation Best Practices
- Rotate pages in the viewer before extraction
- The grid thumbnail updates immediately to show the new orientation
- All rotations are applied during extraction (original file is safe)

### Performance
- Thumbnails are cached for faster loading
- High-resolution images are generated on-demand for the viewer
- Large PDFs (100+ pages) load progressively

### Customization
- Resize the sidebar by dragging the divider
- The layout remembers your last output directory
