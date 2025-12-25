# User Guide
## dpdf-planner - PDF Page Extractor

**Version 1.0.0** | Last Updated: December 25, 2025

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Interface Overview](#interface-overview)
4. [Step-by-Step Tutorials](#step-by-step-tutorials)
5. [Features Reference](#features-reference)
6. [Tips & Best Practices](#tips--best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Introduction

### What is dpdf-planner?

dpdf-planner is a Windows desktop application that allows you to extract specific pages from PDF documents quickly and easily. Whether you need a single page, a range, or a preset selection, dpdf-planner provides an intuitive interface to get the job done.

### Who is this for?

- **Students**: Extract chapters or specific pages from textbooks
- **Professionals**: Pull out specific sections from reports or manuals
- **Researchers**: Organize PDF documents by extracting relevant pages
- **Anyone**: Who works with PDF files regularly

### Key Benefits

✅ **Simple**: No complex menus or confusing options  
✅ **Fast**: Extract pages in seconds  
✅ **Offline**: All processing happens on your computer  
✅ **Free**: No subscriptions or hidden costs  
✅ **Portable**: Standalone executable, no installation needed

---

## Getting Started

### System Requirements

| Requirement | Specification |
|-------------|---------------|
| **Operating System** | Windows 10 or Windows 11 |
| **Disk Space** | ~20 MB for application |
| **RAM** | 100 MB minimum |
| **Python** | Not required (for .exe version) |

### First Launch

1. **Locate** the `dpdf-planner.exe` file
2. **Double-click** to launch
3. **Wait** for the window to appear (2-3 seconds)

> **Note**: Windows may show a security warning on first launch. Click "More info" → "Run anyway"

### Initial Setup

The application will automatically:
- Create a config folder in `%APPDATA%\dpdf-planner`
- Set default output location to `Documents\Extracted PDFs`
- Initialize user preferences

No manual configuration needed!

---

## Interface Overview

### Main Window Layout

```
┌─────────────────────────────────────────────────────────┐
│  📄 PDF Page Extractor                            [─][□][×] │
├─────────────────────────────────────────────────────────┤
│  PDF Page Extractor                                     │
│  Extract specific pages from your PDF documents         │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📄 PDF File                                     │   │
│  │ ┌─────────────────────────────┐  [Browse...]    │   │
│  │ │ No file selected            │                 │   │
│  │ │ Click Browse or drag & drop │                 │   │
│  │ └─────────────────────────────┘                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 📊 Page Range (Total: -- pages)                │   │
│  │ Start Page: [____]    End Page: [____]         │   │
│  │                                                 │   │
│  │ ⚡ Quick: [First 10] [Last 10] [First Half]    │   │
│  │          [All Pages]                            │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 💾 Output Settings                              │   │
│  │ Filename: [_________________________.pdf]       │   │
│  │ Save to:  [Documents/Extracted PDFs] [Change]   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │           🔧 Extract Pages                        │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  [📂 Open Output Folder]                        v1.0.0  │
│  ✅ Status: Ready                                       │
└─────────────────────────────────────────────────────────┘
```

### UI Components Explained

#### 1. PDF File Section
- **Browse Button**: Opens file picker dialog
- **File Display**: Shows selected PDF filename
- **Drag Zone**: Visual area for file selection

#### 2. Page Range Section
- **Start Page**: First page to extract (inclusive)
- **End Page**: Last page to extract (inclusive)
- **Quick Actions**: Preset buttons for common ranges
- **Page Count**: Total pages in loaded PDF

#### 3. Output Settings
- **Filename Input**: Name for extracted PDF
- **Save Location**: Directory where file will be saved
- **Change Button**: Select different output folder

#### 4. Action Buttons
- **Extract Pages**: Primary action button
- **Open Output Folder**: Quick access to saved files

#### 5. Status Bar
- **Status Message**: Current application state
- **Progress Bar**: Extraction progress (when active)

---

## Step-by-Step Tutorials

### Tutorial 1: Basic Page Extraction

**Goal**: Extract pages 10-20 from a PDF

**Steps**:

1. **Load PDF**
   - Click `Browse` button
   - Navigate to your PDF file
   - Select file and click `Open`
   - ✅ Verify: Filename appears, page count shows

2. **Set Page Range**
   - Click in `Start Page` field
   - Type `10`
   - Click in `End Page` field
   - Type `20`
   - ✅ Verify: No error messages appear

3. **Name Output**
   - Review auto-suggested filename
   - Edit if desired (e.g., `chapter_2`)
   - ✅ Verify: Filename is valid (no special characters)

4. **Extract**
   - Click `Extract Pages` button
   - Watch progress bar
   - Click `Yes` when asked to open folder
   - ✅ Verify: New PDF opens in Explorer

**Expected Result**: New PDF with exactly 11 pages (10-20 inclusive)

---

### Tutorial 2: Using Quick Actions

**Goal**: Extract first 10 pages using quick action

**Steps**:

1. **Load PDF** (same as Tutorial 1)

2. **Use Quick Action**
   - Click `First 10` button
   - ✅ Verify: Start Page = 1, End Page = 10

3. **Extract** (same as Tutorial 1, step 4)

**Time Saved**: ~30 seconds vs manual entry

---

### Tutorial 3: Extracting Single Page

**Goal**: Extract only page 5

**Steps**:

1. **Load PDF**

2. **Set Range**
   - Start Page: `5`
   - End Page: `5`

3. **Extract**

**Expected Result**: 1-page PDF containing only page 5

---

### Tutorial 4: Changing Output Location

**Goal**: Save to Desktop instead of default folder

**Steps**:

1. **Load PDF and Set Range**

2. **Change Location**
   - Click `Change` button
   - Navigate to `Desktop`
   - Click `Select Folder`
   - ✅ Verify: Path updates to Desktop

3. **Extract**

**Expected Result**: PDF saved to Desktop

---

## Features Reference

### PDF File Loading

#### Supported Formats
- ✅ Standard PDF files (.pdf)
- ❌ Encrypted/password-protected PDFs
- ❌ Corrupted or invalid PDFs

#### Validation Checks
- File exists and is readable
- File has `.pdf` extension
- PDF is not encrypted
- PDF is not corrupted

#### Error Messages
| Error | Meaning | Solution |
|-------|---------|----------|
| "File not found" | Path is invalid | Check file location |
| "File is not a PDF" | Wrong extension | Select .pdf file |
| "PDF is encrypted" | Password-protected | Remove password first |
| "Invalid or corrupted PDF" | File is damaged | Try different file |

---

### Page Range Selection

#### Rules
- **1-indexed**: First page is page 1 (not 0)
- **Inclusive**: Range 1-5 includes both page 1 and page 5
- **Valid Range**: Start ≤ End ≤ Total Pages

#### Quick Actions Reference

| Button | Behavior | Example (100-page PDF) |
|--------|----------|------------------------|
| **First 10** | Pages 1 to 10 | 1-10 |
| **Last 10** | Last 10 pages | 91-100 |
| **First Half** | First 50% of pages | 1-50 |
| **All Pages** | Entire document | 1-100 |

#### Validation Messages

| Message | Meaning | Fix |
|---------|---------|-----|
| "Start page must be at least 1" | Invalid start | Enter ≥ 1 |
| "End page exceeds total pages" | End too large | Enter ≤ total |
| "Start > End" | Range backwards | Swap values |

---

### Output Configuration

#### Filename Rules

**Allowed Characters**:
- Letters (A-Z, a-z)
- Numbers (0-9)
- Spaces
- Underscore (_)
- Hyphen (-)
- Period (.)

**Forbidden Characters**:
```
< > : " / \ | ? *
```

**Reserved Names** (Windows):
```
CON, PRN, AUX, NUL, COM1-9, LPT1-9
```

#### Auto-Suggested Filenames

| Source PDF | Range | Suggested Name |
|------------|-------|----------------|
| `report.pdf` | 1-10 | `report_pages_1-10` |
| `book.pdf` | 5-5 | `book_page_5` |
| `manual.pdf` | 1-100 | `manual_pages_1-100` |

#### Output Directory

**Default Location**:
```
C:\Users\[YourName]\Documents\Extracted PDFs\
```

**Persistence**: Last-used folder is remembered

**Creation**: Folder is auto-created if it doesn't exist

---

### Progress Tracking

#### Progress Bar States

| State | Appearance | Meaning |
|-------|------------|---------|
| **Hidden** | Not visible | No extraction in progress |
| **0%** | Empty bar | Starting extraction |
| **1-99%** | Filling bar | Processing pages |
| **100%** | Full bar | Extraction complete |

#### Status Messages

| Icon | Message | Meaning |
|------|---------|---------|
| ✅ | "Ready" | Idle, waiting for action |
| ⏳ | "Extracting pages..." | Processing in progress |
| ✅ | "Successfully extracted..." | Completed successfully |
| ❌ | "Error: ..." | Operation failed |

---

## Tips & Best Practices

### Efficiency Tips

1. **Use Quick Actions** for common patterns
   - Saves time vs manual entry
   - Reduces typo errors

2. **Keep Default Output Folder**
   - All extractions in one place
   - Easy to find later

3. **Let Auto-Suggest Work**
   - Descriptive filenames automatically
   - Includes page range for reference

4. **Check Page Count First**
   - Verify PDF loaded correctly
   - Plan your range selection

### Workflow Optimization

**For Repetitive Tasks**:
```
1. Load PDF
2. Quick Action (e.g., "First 10")
3. Accept suggested filename
4. Extract
```
⏱️ **Time**: ~10 seconds per extraction

**For Precise Extraction**:
```
1. Load PDF
2. Manual page entry
3. Custom filename
4. Verify range
5. Extract
```
⏱️ **Time**: ~30 seconds per extraction

### File Organization

**Recommended Structure**:
```
Documents/
└── Extracted PDFs/
    ├── Work/
    │   ├── report_section1.pdf
    │   └── report_section2.pdf
    ├── Personal/
    │   └── book_chapter3.pdf
    └── Archive/
        └── old_extractions.pdf
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Application Won't Start

**Symptoms**: Double-click does nothing or shows error

**Solutions**:
1. **Check Windows Version**
   - Requires Windows 10 or 11
   - Right-click Start → System → Check version

2. **Run as Administrator**
   - Right-click `dpdf-planner.exe`
   - Select "Run as administrator"

3. **Antivirus Blocking**
   - Add exception for dpdf-planner.exe
   - Temporarily disable antivirus and test

4. **Corrupted Download**
   - Re-download the .exe file
   - Verify file size (~15-20 MB)

---

#### Issue 2: PDF Won't Load

**Symptoms**: Error message when selecting PDF

**Solutions**:

| Error | Solution |
|-------|----------|
| "File not found" | Verify file still exists at that location |
| "Not a PDF" | Ensure file extension is `.pdf` |
| "Encrypted" | Remove password protection using Adobe Acrobat |
| "Corrupted" | Try opening in PDF reader first to verify |

---

#### Issue 3: Extraction Fails

**Symptoms**: Error during extraction process

**Solutions**:

1. **Check Disk Space**
   - Ensure enough space for output file
   - Rule of thumb: 2x input file size

2. **Verify Permissions**
   - Output folder must be writable
   - Try changing to Desktop

3. **Close Source PDF**
   - Don't have PDF open in another program
   - Close Adobe Reader/other PDF viewers

4. **Simplify Filename**
   - Remove special characters
   - Use only letters and numbers

---

#### Issue 4: Slow Performance

**Symptoms**: Extraction takes very long

**Expected Times**:
- Small PDF (1-50 pages): 1-5 seconds
- Medium PDF (51-500 pages): 5-30 seconds
- Large PDF (501-1000 pages): 30-60 seconds

**If Slower**:
1. Close other applications
2. Check CPU usage (Task Manager)
3. Verify PDF isn't corrupted
4. Try smaller page ranges

---

### Error Code Reference

| Code | Message | Solution |
|------|---------|----------|
| E001 | Permission denied | Run as administrator |
| E002 | Invalid page range | Check start ≤ end ≤ total |
| E003 | File access error | Close PDF in other programs |
| E004 | Invalid filename | Remove special characters |

---

## FAQ

### General Questions

**Q: Is my data sent to the cloud?**  
A: No. All processing happens locally on your computer. No internet connection required.

**Q: Can I process multiple PDFs at once?**  
A: Not in v1.0. Batch processing is planned for v1.1.

**Q: Does it work on Mac or Linux?**  
A: Currently Windows only. Cross-platform support is planned for v2.0.

**Q: Is it free?**  
A: Yes, completely free and open-source (MIT License).

---

### Technical Questions

**Q: What PDF version is supported?**  
A: All standard PDF versions (1.0 through 2.0).

**Q: Can it handle password-protected PDFs?**  
A: Not currently. Remove password protection first.

**Q: Maximum PDF size?**  
A: Tested up to 1,000 pages. Larger files may work but performance varies.

**Q: Does it preserve PDF quality?**  
A: Yes. Pages are extracted without re-encoding or quality loss.

---

### Usage Questions

**Q: Can I extract non-consecutive pages (e.g., 1, 5, 10)?**  
A: Not in v1.0. Only consecutive ranges supported currently.

**Q: Can I merge multiple PDFs?**  
A: Not in v1.0. Planned for v1.2.

**Q: Can I reorder pages?**  
A: Not in v1.0. Planned for v1.2.

**Q: Does it preserve bookmarks/links?**  
A: No. Only page content is extracted.

---

### Troubleshooting Questions

**Q: Why does Windows show a security warning?**  
A: The .exe is not code-signed. This is normal for open-source software. Click "More info" → "Run anyway".

**Q: Where are my preferences stored?**  
A: `%APPDATA%\dpdf-planner\config.json`

**Q: How do I reset to defaults?**  
A: Delete `%APPDATA%\dpdf-planner\config.json` and restart the app.

**Q: Can I change the theme to light mode?**  
A: Not in v1.0. Theme customization planned for future release.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file browser (planned) |
| `Ctrl+E` | Extract pages (planned) |
| `Ctrl+Q` | Quit application (planned) |

*Note: Keyboard shortcuts are planned for v1.1*

---

## Getting Help

### Resources

1. **This Guide**: Comprehensive user manual
2. **README.md**: Quick start and overview
3. **CHANGELOG.md**: Version history and updates
4. **ARCHITECTURE.md**: Technical documentation (for developers)

### Support Channels

- **Issues**: Report bugs or request features
- **Email**: [Your support email]
- **Documentation**: Check `[app]docs/` folder

---

## Appendix

### Glossary

| Term | Definition |
|------|------------|
| **Page Range** | Consecutive sequence of pages (e.g., 1-10) |
| **1-indexed** | Numbering starts at 1 (not 0) |
| **Extraction** | Process of copying pages to new PDF |
| **Validation** | Checking inputs for correctness |
| **Persistence** | Saving preferences between sessions |

### File Locations

| Item | Path |
|------|------|
| **Executable** | `dist/dpdf-planner.exe` |
| **Config** | `%APPDATA%\dpdf-planner\config.json` |
| **Default Output** | `%USERPROFILE%\Documents\Extracted PDFs\` |

---

**Document Version**: 1.0.0  
**Last Updated**: December 25, 2025  
**Application Version**: 1.0.0

---

<div align="center">

**Need more help?** Check [CHANGELOG.md](CHANGELOG.md) for updates or [README.md](../README.md) for developer info.

</div>
