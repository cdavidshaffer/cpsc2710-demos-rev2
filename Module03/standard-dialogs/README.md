# Standard Dialogs Demo Applications

This project contains demo applications that demonstrate Qt standard dialogs in PySide6, designed for CPSC 2710 Software Construction at Auburn University.

## Overview

The demos include:
- Four applications showing the difference between **modal** and **non-modal** dialogs
- One comprehensive showcase of all Qt standard dialog types

**Modal Dialogs**: Block interaction with the parent window until closed
**Non-Modal Dialogs**: Allow interaction with the parent window while open

## Demo Applications

### 1. Modal QMessageBox Demo (`modal_messagebox_demo.py`)

Demonstrates QMessageBox in **modal mode** using **exec()** method.
- Shows Information, Warning, Critical, and Question dialogs
- All dialogs are modal - you cannot interact with the main window while they're open
- Creates QMessageBox instances and uses `exec()` for modal behavior
- **Includes "Use Native Dialogs" checkbox** to toggle the `DontUseNativeDialog` option
  - When checked: Uses OS native dialogs (macOS, Windows, Linux native look)
  - When unchecked: Uses Qt's cross-platform dialog appearance

**Run with:**
```bash
python -m standard_dialogs.modal_messagebox_demo
```

### 2. Modal QFontDialog Demo (`modal_fontdialog_demo.py`)

Demonstrates QFontDialog using **open()** method and **signals**.
- Opens a font selection dialog
- Updates text font when a font is selected
- Dialog is modal - main window is blocked during font selection
- Uses `open()` method and connects to `fontSelected` signal

**Run with:**
```bash
python -m standard_dialogs.modal_fontdialog_demo
```

### 3. Non-Modal QMessageBox Demo (`nonmodal_messagebox_demo.py`)

Demonstrates QMessageBox in **non-modal** mode using **show()** method.
- Shows the same dialog types as demo #1
- Dialogs are non-modal - you CAN interact with the main window while they're open
- You can even open multiple dialogs simultaneously
- Uses custom QMessageBox instances with `show()` method

**Run with:**
```bash
python -m standard_dialogs.nonmodal_messagebox_demo
```

### 4. Non-Modal QFontDialog Demo (`nonmodal_fontdialog_demo.py`)

Demonstrates QFontDialog in **non-modal** mode using **show()** method.
- Opens a font selection dialog that doesn't block the main window
- Shows **real-time** font updates using `currentFontChanged` signal
- You can continue typing and interacting with the main window while the dialog is open
- Uses `show()` method and `setModal(False)`

**Run with:**
```bash
python -m standard_dialogs.nonmodal_fontdialog_demo
```

### 5. Standard Dialogs Showcase (`standard_dialogs_showcase.py`)

Comprehensive showcase of **all Qt standard dialog types**.
- QFileDialog: Open File, Save File, Select Directory
- QColorDialog: Color picker
- QFontDialog: Font picker
- QInputDialog: Text, Integer, Double, Item selection, Multiline text
- QMessageBox: Information, Warning
- QErrorMessage: Error messages
- All dialogs open modally
- Includes "Use Native Dialogs" checkbox to see native vs Qt appearance

**Run with:**
```bash
python -m standard_dialogs.standard_dialogs_showcase
# or
uv run dialogs-showcase
```

## Key Learning Points

### Modal vs Non-Modal

**Modal dialogs:**
- Created with static methods (QMessageBox) or `open()` method (QFontDialog)
- Block parent window interaction
- User must close dialog before continuing
- Good for critical decisions or required information

**Non-modal dialogs:**
- Created with `show()` method
- Allow parent window interaction
- User can work with both dialog and main window
- Good for settings, preferences, or continuous updates

### Signal Usage

The demos illustrate different signals:
- `fontSelected`: Emitted when user confirms font selection
- `currentFontChanged`: Emitted when user previews a font (real-time updates)
- `finished`: Emitted when dialog is closed
- `buttonClicked`: Emitted when a button is clicked in a message box

### Important Implementation Details

1. **QMessageBox static methods are always modal** - for non-modal, you must create an instance
2. **Keep references to non-modal dialogs** - they'll be garbage collected otherwise
3. **Use `open()` for modal, `show()` for non-modal** (or `setModal(False)` + `show()`)
4. **Real-time updates** - `currentFontChanged` vs `fontSelected` signals

## Testing Modality

Each demo includes:
- A **QCheckBox** you can toggle
- A **QComboBox** you can change
- A **status label** that updates

Try interacting with these widgets while dialogs are open to see the difference between modal and non-modal behavior!

## Project Setup

This project uses Python 3.14+ and PySide6. To install dependencies:

```bash
uv sync
```

To run the main entry point (shows available demos):

```bash
uv run standard-dialogs
```

## Course Context

These demos are part of CPSC 2710 - Software Construction at Auburn University. Students should have already learned about:
- QWidget basics
- Layouts (QVBoxLayout, QHBoxLayout)
- Signals and slots
- Basic widgets (QPushButton, QCheckBox, QComboBox)
- QMainWindow

This module introduces standard dialogs and the concept of modality in GUI applications.
