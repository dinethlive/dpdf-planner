# Software Requirements Specification (SRS)
## dpdf-planner – Desktop Application (Windows)

---

## 1. Purpose & Scope

### 1.1 Purpose
The purpose of this document is to define the complete functional and non-functional requirements for a desktop software application that allows users to extract a specified range of pages from a single PDF file and save the extracted pages as a new PDF file using a graphical user interface.

This document is intended to be used as a **source of truth for automated and AI-assisted code generation**.

### 1.2 Scope
The application will:
- Run as a **Windows desktop application**
- Accept **one PDF file at a time**
- Allow the user to define a **page range**
- Generate a **new PDF file** with a user-defined name
- Save the output to a designated folder
- Be packaged as a **standalone executable (.exe)**

Out of scope:
- Cloud processing
- Multi-user collaboration
- Web-based access

---

## 2. User Personas

### 2.1 Primary User
- Non-technical or semi-technical Windows user
- Works with large PDF documents
- Requires quick page extraction without complex tools

---

## 3. Functional Requirements (MECE)

### 3.1 Application Startup & Lifecycle

#### Must-Have
- Application shall launch via a Windows executable
- Application shall open with a graphical user interface
- Application shall terminate cleanly without leaving background processes

#### Nice-to-Have
- Application shall remember last-used folders
- Application shall auto-create required directories on startup

---

### 3.2 PDF Input Management

#### Must-Have
- Application shall allow loading exactly **one PDF file at a time**
- Application shall accept PDF input via file browser dialog
- Application shall validate that the selected file is a valid PDF
- Application shall display the loaded PDF filename in the UI

#### Nice-to-Have
- Drag-and-drop PDF support
- Display total page count of the loaded PDF
- Warn user if encrypted or corrupted PDF is loaded

---

### 3.3 Page Range Selection

#### Must-Have
- Application shall allow user to input:
  - Start page number (integer)
  - End page number (integer)
- Page numbering shall be **1-based (human readable)**
- Application shall validate:
  - Start page ≥ 1
  - End page ≤ total number of pages
  - Start page ≤ End page
- Application shall prevent PDF generation if validation fails

#### Nice-to-Have
- Auto-fill end page with total page count
- Slider-based page range selection
- Live validation feedback (inline error messages)

---

### 3.4 Output PDF Configuration

#### Must-Have
- Application shall allow user to input a custom output PDF name
- Output filename shall be validated (no illegal filesystem characters)
- Output file shall be saved as `.pdf`
- Application shall save output files to a predefined output directory

#### Nice-to-Have
- Allow user to choose custom output directory
- Auto-generate output filename based on input PDF and page range
- Option to overwrite or auto-increment filenames

---

### 3.5 PDF Processing Logic

#### Must-Have
- Application shall extract only the specified page range
- Application shall preserve original page order
- Application shall not modify page content
- Application shall generate a valid PDF file

#### Nice-to-Have
- Preserve original PDF metadata
- Option to compress output PDF
- Support password-protected PDFs (with user input)

---

### 3.6 User Interface & Interaction

#### Must-Have
- UI shall include:
  - Load PDF button
  - Start page input
  - End page input
  - Output filename input
  - Generate / Create PDF button
- UI shall provide clear success and error messages
- UI shall prevent actions in invalid states

#### Nice-to-Have
- Modern themed UI (e.g., dark mode)
- Progress indicator during PDF generation
- Keyboard shortcuts for common actions

---

### 3.7 Error Handling & Validation

#### Must-Have
- Application shall display user-friendly error messages
- Application shall handle:
  - Invalid page ranges
  - Missing input fields
  - File access errors
  - PDF read/write failures
- Application shall not crash due to user input

#### Nice-to-Have
- Error codes for internal debugging
- Optional error log file for diagnostics

---

## 4. Non-Functional Requirements (MECE)

### 4.1 Performance

#### Must-Have
- Application shall handle PDFs up to at least 1,000 pages
- PDF extraction shall complete within reasonable time on consumer hardware

#### Nice-to-Have
- Background processing with UI responsiveness
- Progress percentage display

---

### 4.2 Usability

#### Must-Have
- UI shall be intuitive and require no training
- Labels and controls shall use clear, human-readable language

#### Nice-to-Have
- Tooltips for all user inputs
- Inline usage guidance

---

### 4.3 Reliability

#### Must-Have
- Application shall not corrupt input PDF files
- Application shall ensure output PDF integrity

#### Nice-to-Have
- Auto-retry on transient file errors
- Graceful recovery after unexpected failure

---

### 4.4 Security

#### Must-Have
- Application shall process PDFs locally only
- Application shall not transmit data externally

#### Nice-to-Have
- Optional password protection for output PDF
- Secure deletion of temporary files

---

### 4.5 Compatibility & Deployment

#### Must-Have
- Application shall run on Windows 10 and Windows 11
- Application shall be distributed as a single `.exe` file
- Application shall not require Python installation on end-user machines

#### Nice-to-Have
- Installer package with Start Menu shortcut
- Code-signing support for enterprise deployment

---

## 5. Technical Constraints

#### Must-Have
- Programming language: Python
- GUI framework: Tkinter or equivalent
- PDF processing library: PyPDF2 or equivalent
- Packaging tool: PyInstaller

#### Nice-to-Have
- Modular architecture with service separation
- Logging and diagnostics support

---

## 6. Quality Attributes

- Maintainability
- Scalability (future feature additions)
- Testability
- Clear separation of concerns

---

## 7. Future Enhancements (Explicitly Out of Scope)

- Batch PDF processing
- OCR integration
- PDF editing beyond page extraction
- Cloud synchronization
- Cross-platform support (macOS, Linux)

---

## 8. Acceptance Criteria

- User can load a PDF
- User can select valid page range
- User can name output PDF
- Output PDF contains only selected pages
- Output file is saved successfully
- Application runs as a standalone Windows executable

---

## End of Document
