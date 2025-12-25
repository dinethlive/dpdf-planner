# Architecture Documentation
## dpdf-planner Technical Reference

**Version**: 1.0.0  
**Last Updated**: December 25, 2025  
**Target Audience**: Developers, Contributors, Technical Users

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Component Design](#component-design)
4. [Data Flow](#data-flow)
5. [Technology Stack](#technology-stack)
6. [Design Decisions](#design-decisions)
7. [Extension Points](#extension-points)
8. [Performance Considerations](#performance-considerations)

---

## System Overview

### Purpose

dpdf-planner is a desktop application designed to extract page ranges from PDF files with a focus on:
- **Simplicity**: Single-purpose, focused functionality
- **Usability**: Intuitive UI requiring no training
- **Reliability**: Robust error handling and validation
- **Performance**: Efficient processing of large PDFs

### High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│              User Interface (GUI)               │
│                   Tkinter                       │
├─────────────────────────────────────────────────┤
│            Business Logic (Services)            │
│    PDF • Validation • Configuration            │
├─────────────────────────────────────────────────┤
│           Utilities & Helpers (Utils)           │
│         File System • Formatting                │
├─────────────────────────────────────────────────┤
│          External Dependencies                  │
│      PyPDF2 • Pillow • OS Libraries            │
└─────────────────────────────────────────────────┘
```

---

## Architecture Patterns

### 1. Layered Architecture

**Pattern**: Separation of concerns into distinct layers

**Layers**:

```
┌──────────────────────────────────────┐
│  Presentation Layer (GUI)            │  ← User interaction
│  - Components                        │
│  - Themes                            │
│  - Main Window                       │
├──────────────────────────────────────┤
│  Business Logic Layer (Services)     │  ← Core functionality
│  - PDF Service                       │
│  - Validation Service                │
│  - Config Service                    │
├──────────────────────────────────────┤
│  Utility Layer (Utils)               │  ← Helper functions
│  - File Utils                        │
├──────────────────────────────────────┤
│  Data Access Layer                   │  ← External resources
│  - File System                       │
│  - User Preferences (JSON)           │
└──────────────────────────────────────┘
```

**Benefits**:
- Clear separation of concerns
- Easy to test individual layers
- Maintainable and scalable
- Reusable components

**Dependencies Flow**: Top → Bottom (one-way)

---

### 2. Component-Based UI

**Pattern**: Reusable, self-contained UI widgets

**Component Hierarchy**:

```
MainWindow
├── FilePicker
├── PageRangeSelector
├── OutputConfig
├── ActionBar
└── StatusBar
```

**Characteristics**:
- **Encapsulation**: Each component manages its own state
- **Reusability**: Components can be used in different contexts
- **Composability**: Complex UIs built from simple components
- **Event-Driven**: Components communicate via callbacks

---

### 3. Service-Oriented Design

**Pattern**: Business logic encapsulated in service classes

**Services**:

| Service | Responsibility | Dependencies |
|---------|----------------|--------------|
| `PDFService` | PDF operations | PyPDF2 |
| `ValidationService` | Input validation | None (pure logic) |
| `ConfigService` | User preferences | JSON, OS |

**Benefits**:
- Single Responsibility Principle
- Easy to mock for testing
- Clear API boundaries
- Stateful where needed, stateless where possible

---

## Component Design

### GUI Layer

#### Main Window (`main_window.py`)

**Responsibilities**:
- Assemble UI components
- Coordinate user interactions
- Manage application lifecycle
- Handle dialogs and messages

**Key Methods**:

```python
class MainWindow:
    def __init__(root: tk.Tk)
    def _setup_window()           # Window configuration
    def _setup_styles()            # Theme application
    def _create_widgets()          # UI assembly
    def _on_file_selected(path)    # File load handler
    def _on_range_changed(s, e)    # Range change handler
    def _on_extract()              # Extract action
    def _validate_form_complete()  # Form validation
```

**State Management**:
- Services: `pdf_service`, `config_service`
- Components: `file_picker`, `page_range`, `output_config`, etc.

---

#### File Picker (`file_picker.py`)

**Responsibilities**:
- File selection UI
- File display
- Validation feedback

**Interface**:

```python
class FilePicker(ttk.Frame):
    def __init__(parent, on_file_selected: Callable)
    def set_file(filepath: str)
    def clear()
    
    @property
    def current_file() -> Optional[str]
```

**Events**:
- `on_file_selected(filepath)`: Triggered when file is selected

---

#### Page Range Selector (`page_range.py`)

**Responsibilities**:
- Page range input
- Quick action buttons
- Range validation display

**Interface**:

```python
class PageRangeSelector(ttk.Frame):
    def __init__(parent, on_range_changed: Callable)
    def set_total_pages(total: int)
    def get_range() -> Tuple[int, int]
    def set_validation_message(msg: str)
    def reset()
```

**Quick Actions**:
- First N pages
- Last N pages
- First half
- All pages

---

### Service Layer

#### PDF Service (`pdf_service.py`)

**Responsibilities**:
- Load and validate PDFs
- Extract page ranges
- Provide metadata

**Interface**:

```python
class PDFService:
    def load_pdf(filepath: str) -> Tuple[bool, str]
    def extract_pages(start, end, output, callback) -> Tuple[bool, str]
    def get_metadata() -> dict
    def suggest_output_filename(start, end) -> str
    
    @property
    def is_loaded() -> bool
    @property
    def page_count() -> int
```

**State**:
- `_reader`: PyPDF2.PdfReader instance
- `_filepath`: Current PDF path
- `_page_count`: Total pages

**Error Handling**:
- File not found
- Invalid PDF
- Encrypted PDF
- Corrupted PDF
- Permission errors

---

#### Validation Service (`validation_service.py`)

**Responsibilities**:
- Input validation
- Error message generation
- Input sanitization

**Interface**:

```python
class ValidationService:
    @classmethod
    def validate_page_range(start, end, total) -> Tuple[bool, str]
    
    @classmethod
    def validate_filename(filename: str) -> Tuple[bool, str]
    
    @classmethod
    def validate_output_path(path: str) -> Tuple[bool, str]
    
    @classmethod
    def sanitize_filename(filename: str) -> str
```

**Validation Rules**:
- Page range: 1 ≤ start ≤ end ≤ total
- Filename: No invalid Windows characters
- Path: Writable directory

---

#### Config Service (`config_service.py`)

**Responsibilities**:
- Load/save user preferences
- Manage recent files
- Provide default values

**Interface**:

```python
class ConfigService:
    @property
    def last_input_dir() -> str
    
    @property
    def last_output_dir() -> str
    
    @property
    def recent_files() -> List[str]
    
    def add_recent_file(filepath: str)
    def get_output_path(filename: str) -> str
```

**Persistence**:
- Format: JSON
- Location: `%APPDATA%\dpdf-planner\config.json`
- Auto-save on changes

---

## Data Flow

### PDF Extraction Flow

```
User Action: Click "Browse"
    ↓
FilePicker: Open file dialog
    ↓
User: Select PDF file
    ↓
FilePicker: Trigger on_file_selected(path)
    ↓
MainWindow: _on_file_selected(path)
    ↓
ValidationService: validate_pdf_file(path)
    ↓
PDFService: load_pdf(path)
    ↓
PDFService: Return (success, message, page_count)
    ↓
MainWindow: Update PageRangeSelector with page_count
    ↓
PageRangeSelector: Enable controls, set defaults
    ↓
MainWindow: Update OutputConfig with suggested filename
    ↓
StatusBar: Display success message
```

### Extraction Process

```
User Action: Click "Extract Pages"
    ↓
MainWindow: _on_extract()
    ↓
MainWindow: _validate_form_complete()
    ↓
ValidationService: validate_page_range()
    ↓
ValidationService: validate_filename()
    ↓
MainWindow: Check file exists → Show overwrite dialog
    ↓
User: Confirm overwrite
    ↓
ActionBar: Set processing state
    ↓
StatusBar: Show progress bar
    ↓
PDFService: extract_pages(start, end, output, progress_callback)
    ↓
    [For each page]
    PDFService: Add page to writer
    PDFService: Call progress_callback(current, total)
    StatusBar: Update progress bar
    ↓
PDFService: Write output file
    ↓
PDFService: Return (success, message)
    ↓
ActionBar: Reset processing state
    ↓
StatusBar: Hide progress, show success
    ↓
MainWindow: Show success dialog
    ↓
User: Choose to open folder
    ↓
FileUtils: open_file_in_explorer(output_path)
```

---

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.13 | Programming language |
| **Tkinter** | Built-in | GUI framework |
| **PyPDF2** | 3.0.1 | PDF processing |
| **Pillow** | 10.0.0 | Image processing (thumbnails) |
| **PyInstaller** | 6.17.0 | Executable packaging |

### Standard Library Usage

| Module | Usage |
|--------|-------|
| `os` | File system operations |
| `json` | Config persistence |
| `pathlib` | Path manipulation |
| `typing` | Type hints |
| `re` | Filename validation |

---

## Design Decisions

### 1. Why Tkinter?

**Decision**: Use Tkinter for GUI instead of Qt, wxPython, or web-based

**Rationale**:
- ✅ Built-in with Python (no extra dependencies)
- ✅ Lightweight and fast
- ✅ Sufficient for simple UI needs
- ✅ Easy to package with PyInstaller
- ❌ Limited styling capabilities (mitigated with ttk)

**Trade-offs**:
- Simpler but less modern look
- Fewer built-in widgets
- Manual theme implementation

---

### 2. Why PyPDF2?

**Decision**: Use PyPDF2 for PDF operations

**Alternatives Considered**:
- PyMuPDF (fitz): More features but larger dependency
- pdfplumber: Focused on text extraction
- reportlab: Focused on PDF generation

**Rationale**:
- ✅ Lightweight
- ✅ Sufficient for page extraction
- ✅ Well-documented
- ✅ Active maintenance

---

### 3. Absolute vs Relative Imports

**Decision**: Use absolute imports (`from services.pdf_service import...`)

**Rationale**:
- ✅ PyInstaller compatibility
- ✅ Clearer import paths
- ✅ Works as both script and module
- ❌ Longer import statements

**Implementation**:
```python
# ✅ Absolute (used)
from services.pdf_service import PDFService

# ❌ Relative (avoided)
from ..services.pdf_service import PDFService
```

---

### 4. JSON for Config

**Decision**: Use JSON for user preferences

**Alternatives Considered**:
- INI files: Less structured
- SQLite: Overkill for simple key-value
- Registry (Windows): Platform-specific

**Rationale**:
- ✅ Human-readable
- ✅ Built-in Python support
- ✅ Easy to edit manually
- ✅ Cross-platform ready

---

### 5. Dark Theme Default

**Decision**: Default to dark theme

**Rationale**:
- ✅ Modern aesthetic
- ✅ Reduced eye strain
- ✅ Professional appearance
- ✅ Differentiates from default Tkinter look

**Color Palette**:
- Primary: `#1a1a2e` (Deep navy)
- Accent: `#e94560` (Vibrant coral)
- Text: `#ffffff` (White)

---

## Extension Points

### Adding New Features

#### 1. New Quick Action

**Location**: `src/gui/components/page_range.py`

```python
# Add button in _create_widgets()
btn_custom = ttk.Button(
    quick_frame,
    text="Custom Action",
    command=lambda: self._quick_select('custom'),
    style='Secondary.TButton'
)

# Add logic in _quick_select()
elif mode == 'custom':
    start = # your logic
    end = # your logic
```

#### 2. New Validation Rule

**Location**: `src/services/validation_service.py`

```python
@classmethod
def validate_custom(cls, value: str) -> Tuple[bool, str]:
    # Your validation logic
    if not valid:
        return False, "Error message"
    return True, ""
```

#### 3. New Service

**Template**:

```python
# src/services/new_service.py

class NewService:
    """
    Service for [purpose].
    """
    
    def __init__(self):
        # Initialize state
        pass
    
    def method_name(self, param: type) -> return_type:
        """
        [Description]
        
        Args:
            param: [description]
            
        Returns:
            [description]
        """
        # Implementation
        pass
```

---

## Performance Considerations

### PDF Processing

**Bottleneck**: Page extraction from large PDFs

**Optimization**:
- Progress callbacks for UI responsiveness
- No page re-encoding (direct copy)
- Minimal memory footprint

**Benchmarks**:
- 100 pages: ~2 seconds
- 500 pages: ~10 seconds
- 1000 pages: ~20 seconds

---

### UI Responsiveness

**Challenge**: Blocking operations freeze UI

**Solution**: Progress callbacks with `update_idletasks()`

```python
def progress_callback(current, total):
    self.status_bar.set_progress(current, total)
    self.root.update_idletasks()  # Force UI update
```

**Future**: Consider threading for large PDFs

---

### Memory Usage

**Profile**:
- Base application: ~50 MB
- Loaded PDF (100 pages): +10 MB
- During extraction: +20 MB (temporary)

**Optimization**:
- Close PDF reader after extraction
- No page caching
- Minimal state retention

---

## Testing Strategy

### Unit Tests

**Coverage**:
- `ValidationService`: All validation methods
- `PDFService`: Load, extract, metadata
- `ConfigService`: Load, save, defaults

**Framework**: pytest

**Example**:

```python
def test_validate_page_range_valid():
    is_valid, msg = ValidationService.validate_page_range(1, 10, 100)
    assert is_valid == True
    assert msg == ""

def test_validate_page_range_invalid():
    is_valid, msg = ValidationService.validate_page_range(50, 10, 100)
    assert is_valid == False
    assert "Start page cannot be greater" in msg
```

---

### Integration Tests

**Scenarios**:
1. Load PDF → Extract → Verify output
2. Invalid input → Error message
3. Overwrite confirmation → User choice

---

### Manual Testing

**Checklist**:
- [ ] Application launches
- [ ] PDF loads successfully
- [ ] Page range validation works
- [ ] Quick actions work
- [ ] Extraction completes
- [ ] Output file is valid
- [ ] Preferences persist

---

## Build & Deployment

### PyInstaller Configuration

**File**: `build.spec`

**Key Settings**:

```python
a = Analysis(
    ['src/main.py'],
    pathex=[os.path.abspath('src')],  # Module search path
    datas=[('assets', 'assets')],      # Include assets
    hiddenimports=['PyPDF2', 'PIL'],   # Explicit imports
)

exe = EXE(
    # ...
    console=False,                      # No console window
    icon='assets/icon.ico',             # Application icon
)
```

**Build Command**:

```bash
pyinstaller build.spec --clean
```

---

## Future Architecture

### Planned Enhancements

#### v1.1: Batch Processing

**Architecture Change**: Add queue system

```
BatchService
├── Queue Management
├── Progress Tracking
└── Error Handling
```

#### v1.2: Plugin System

**Architecture Change**: Plugin loader

```
PluginManager
├── Plugin Discovery
├── Plugin Loading
├── API Exposure
└── Lifecycle Management
```

#### v2.0: Cross-Platform

**Architecture Change**: Platform abstraction

```
PlatformService
├── Windows Implementation
├── macOS Implementation
└── Linux Implementation
```

---

**Document Version**: 1.0.0  
**Application Version**: 1.0.0  
**Last Updated**: December 25, 2025

---

For implementation details, see source code.  
For user documentation, see [USER_GUIDE.md](USER_GUIDE.md).  
For version history, see [CHANGELOG.md](CHANGELOG.md).
