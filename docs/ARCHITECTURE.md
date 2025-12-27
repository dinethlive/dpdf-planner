# PDF Page Extractor - Architecture

## Technology Stack

### Core Technologies
- **Python 3.8+**: Primary language
- **Tkinter/ttk**: GUI framework
- **PyPDF2**: PDF manipulation (extraction, rotation)
- **PyMuPDF (fitz)**: High-quality PDF rendering
- **Pillow (PIL)**: Image processing

### Key Libraries
- `PyPDF2`: Page extraction and rotation
- `fitz` (PyMuPDF): Thumbnail generation
- `PIL`: Image manipulation and display

## Project Structure

```
dpdf-planner/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gui/
│   │   ├── main_window.py      # Main application window
│   │   ├── components/
│   │   │   ├── sidebar.py      # Sidebar component (NEW in V2)
│   │   │   ├── grid_view.py    # Page grid display
│   │   │   ├── single_page_window.py  # Page viewer
│   │   │   ├── file_picker.py
│   │   │   ├── output_config.py
│   │   │   ├── status_bar.py
│   │   │   └── toast.py        # Toast notifications (NEW in V2)
│   │   └── themes/
│   │       └── dark_theme.py   # Theme configuration
│   └── services/
│       ├── pdf_service.py      # PDF operations
│       ├── thumbnail_service.py # Thumbnail caching
│       ├── validation_service.py
│       └── config_service.py
├── docs/                       # Documentation
├── requirements.txt
└── README.md
```

## Component Architecture

### Main Window (`MainWindow`)
- **Responsibility**: Application orchestration
- **Layout**: `ttk.PanedWindow` for resizable split-view
- **Components**:
  - `Sidebar`: Left panel with controls
  - `GridView`: Right panel with page thumbnails
  - `StatusBar`: Bottom status display

### Sidebar (`Sidebar`)
**New in V2** - Modularized component
- Encapsulates `FilePicker`, `OutputConfig`, `ActionBar`
- Exposes clean API: `set_filename()`, `get_output_directory()`, etc.
- Reduces `MainWindow` complexity

### Grid View (`GridView`)
- **Rendering**: Canvas-based scrollable grid
- **Layout**: Dynamic columns based on window width
- **Features**:
  - Page selection tracking
  - Rotation state management
  - Hover effects
  - Thumbnail caching

### Single Page Window (`SinglePageWindow`)
- **Rendering**: High-resolution page display (1600px base)
- **Features**:
  - Zoom (buttons, dropdown, Ctrl+Scroll)
  - Pan (click-drag)
  - Rotation (90° increments)
- **Callbacks**: Notifies parent of rotation changes

### Services Layer

#### PDF Service (`PDFService`)
- **Load**: Opens PDF with PyPDF2
- **Extract**: Creates new PDF with selected pages
- **Rotation**: Applies rotation overrides during extraction
- **Key Method**: `extract_pages(pages, output_path, rotations, callback)`

#### Thumbnail Service (`ThumbnailService`)
- **Rendering**: Uses PyMuPDF for high-quality thumbnails
- **Caching**: In-memory cache with composite keys (path, page, width)
- **Performance**: Lazy loading for large PDFs

## Data Flow

### Page Selection Flow
```
User Click → GridView._handle_click() 
          → Update selected_pages set
          → _update_card_style() (visual feedback)
          → on_selection_change callback
          → MainWindow._on_selection_change()
          → StatusBar update
```

### Page Rotation Flow
```
User Rotate → SinglePageWindow._rotate_cw()
           → Update rotation_angle
           → on_rotate callback
           → MainWindow._on_page_rotate()
           → GridView.set_page_rotation()
           → Refresh thumbnail with rotation
```

### Extraction Flow
```
User Extract → MainWindow._on_extract()
            → Get selected pages + rotations
            → PDFService.extract_pages()
            → For each page:
                - Clone page
                - Apply rotation if override exists
                - Add to output PDF
            → Save to disk
```

## Design Patterns

### Observer Pattern
- Components use callbacks for loose coupling
- Example: `GridView` notifies `MainWindow` of selection changes

### Service Layer
- Business logic separated from UI
- Services are stateless (except caching)

### Component Composition
- `Sidebar` composes `FilePicker`, `OutputConfig`, `ActionBar`
- Promotes reusability and testability

## Key Design Decisions

### Why PanedWindow?
- Native Tkinter resizable split-view
- No external dependencies
- Smooth user experience

### Why Separate Sidebar Component?
- Reduces `MainWindow` from 400+ to ~300 lines
- Clearer separation of concerns
- Easier to test and maintain

### Why In-Memory Thumbnail Cache?
- Fast access for grid scrolling
- Acceptable memory footprint (thumbnails are small)
- Composite key allows multiple resolutions

### Rotation Implementation
- **Non-destructive**: Original PDF never modified
- **Applied at extraction**: Rotation happens during `extract_pages()`
- **Visual feedback**: Thumbnails rotated via PIL for preview

## Performance Considerations

### Lazy Loading
- Thumbnails loaded asynchronously with `after()` delays
- Prevents UI freeze on large PDFs

### Progressive Rendering
- Grid items created immediately (placeholders)
- Images loaded in background

### Caching Strategy
- Thumbnails cached by (path, page, width)
- High-res images cached separately
- No disk caching (simplicity over persistence)

## Future Enhancements

### Potential Improvements
- Drag-and-drop file loading
- Batch processing multiple PDFs
- Custom zoom levels (manual entry)
- Page reordering (drag-drop in grid)
- PDF metadata editing
