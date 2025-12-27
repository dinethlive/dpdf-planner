# Changelog

All notable changes to PDF Page Extractor will be documented in this file.

## [2.0.0] - 2025-12-27

### Major Features
- **Page Rotation**: Rotate individual pages 90° clockwise before extraction
- **Quick Zoom Dropdown**: Select zoom levels (25%-400%) in page viewer
- **Resizable Sidebar**: Drag divider to adjust sidebar width (default 600px)
- **Keyboard Shortcuts**: `Ctrl+A` (Select All), `Esc` (Clear Selection)

### UI/UX Enhancements
- **Modular Sidebar Component**: Cleaner code architecture
- **Hover Effects**: Interactive grid with visual feedback
- **Toast Notifications**: Non-blocking success messages
- **Maximized Startup**: Application launches in full-screen mode
- **Wider Sidebar**: Increased from 300px to 600px default

### Technical Improvements
- **Component Refactoring**: Extracted `Sidebar` into dedicated component
- **PanedWindow Layout**: Replaced grid layout with resizable split-view
- **Removed Project Feature**: Simplified workflow (no save/load projects)
- **Code Cleanup**: Reduced `MainWindow` complexity by ~100 lines

### Bug Fixes
- Fixed grid layout calculation on initial PDF load
- Fixed duplicate imports and initialization
- Corrected TclError with PanedWindow width parameter

## [1.0.0] - 2024

### Initial Release
- Visual page selection with grid view
- PDF page extraction
- Dark theme UI
- Output configuration
- Status bar with progress tracking
- File picker with recent files
- Validation services
- Configuration persistence

---

## Version Comparison

### V1 → V2 Key Changes

| Feature | V1 | V2 |
|---------|----|----|
| Page Rotation | ❌ | ✅ 90° increments |
| Zoom Levels | Manual only | Dropdown + Manual |
| Sidebar | Fixed 300px | Resizable, 600px default |
| Shortcuts | None | Ctrl+A, Esc |
| Grid Interaction | Basic | Hover effects |
| Code Structure | Monolithic | Modular (Sidebar) |
| Notifications | Blocking dialogs | Toast messages |
| Project Save/Load | ✅ | ❌ (Removed for simplicity) |

### Migration Notes (V1 → V2)
- **Project files are no longer supported**: V2 focuses on direct PDF-to-PDF workflow
- **No breaking changes** for basic extraction workflow
- **New shortcuts** available for power users
