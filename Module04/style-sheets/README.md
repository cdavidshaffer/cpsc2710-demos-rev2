# QSS Demo Application - Cat Gallery Manager

A demonstration application for teaching Qt Style Sheets (QSS) in CPSC 2710.

## Overview

This cat-themed application demonstrates all major QSS features:
- Type selectors (styling all QPushButton widgets)
- ID selectors (using `objectName`)
- Class selectors (using custom properties)
- Descendant selectors (styling widgets within specific parents)
- The box model (margin, border, padding, content)
- Sub-controls (styling parts of complex widgets like QComboBox::drop-down)
- Dynamic pseudo-states (:hover, :pressed, :checked, :disabled, :focus, :selected)

## Running the Application

```bash
uv run style-sheets
```

## Teaching with This Application

### Incremental Styling Approach

You can demonstrate QSS features incrementally by:

1. **Start with no styles** - Comment out the stylesheet loading in `main.py` to show default Qt styling
2. **Add basic type selectors** - Uncomment sections of `styles.qss` one at a time
3. **Show ID selectors** - Demonstrate how `#header` targets the specific label
4. **Demonstrate class selectors** - Show how `QPushButton[class="danger"]` works
5. **Explain the box model** - Point to the QListWidget styling with margin/border/padding comments
6. **Show sub-controls** - Demonstrate QComboBox styling with its parts
7. **Interactive dynamic states** - Have students hover, click, and interact to see state changes

### Key Demo Points

**Type Selectors** (`styles.qss:7-68`):
- Show how `QPushButton` styles ALL buttons in the application
- Point out property groups: colors, borders, padding, fonts

**ID Selectors** (`styles.qss:74-108`):
- `#header` - The main title label
- `#addButton` - Override the default button color
- `#statusLabel` - Status bar with custom border
- Show that IDs provide more specific targeting

**Class Selectors** (`styles.qss:114-123`):
- `QPushButton[class="danger"]` - The red "Remove Cat" button
- Explain custom properties set via `setProperty()`

**Descendant Selectors** (`styles.qss:129-144`):
- `QDialog QPushButton` - All buttons in dialogs get purple styling
- Open the "Add Cat" dialog to demonstrate
- Show how this creates visual separation between main window and dialog

**Box Model** (`styles.qss:150-170`):
- QListWidget demonstrates margin, border, padding
- Use browser dev tools analogy
- Explain inside-out: content → padding → border → margin

**Sub-controls** (`styles.qss:176-220`):
- QComboBox with custom dropdown arrow
- QCheckBox with custom indicator
- Explain sub-control positioning

**Dynamic States** (`styles.qss:226-285`):
- `:hover` - Mouse over effects
- `:pressed` - Click effects
- `:checked` - Toggle states (Favorite button)
- `:disabled` - Grayed out appearance
- `:focus` - Input field highlighting
- `:selected` - List item selection

## File Structure

```
src/style_sheets/
├── __init__.py          # Package entry point
├── main.py              # Application entry and stylesheet loading
├── cat_window.py        # Main window (QMainWindow)
├── add_cat_dialog.py    # Custom dialog (QDialog)
└── styles.qss           # Complete stylesheet with comments
```

## Features to Explore

1. **Main Window**:
   - Add/Remove/Favorite buttons with different styles
   - Filter checkboxes
   - Breed combo box with custom dropdown
   - Cat list with hover and selection states
   - Status label with custom styling

2. **Add Cat Dialog**:
   - Demonstrates descendant selectors (purple theme)
   - Form inputs with focus states
   - Dialog buttons styled differently from main window buttons

## Customization Ideas for Students

- Change the color scheme
- Add animations (limited in QSS, but some properties work)
- Create different themes (dark mode, etc.)
- Style additional widgets
- Experiment with different box model values
- Create more complex sub-control styles
