# Quick Start Guide

## Installation

```bash
# From the project directory
uv sync
```

## Running the Demos

### Option 1: Using the script commands (after installation)

```bash
uv run modal-messagebox       # Modal QMessageBox demo
uv run modal-fontdialog        # Modal QFontDialog demo
uv run nonmodal-messagebox     # Non-Modal QMessageBox demo
uv run nonmodal-fontdialog     # Non-Modal QFontDialog demo
uv run dialogs-showcase        # All standard dialogs showcase
```

### Option 2: Using Python module syntax

```bash
python -m standard_dialogs.modal_messagebox_demo
python -m standard_dialogs.modal_fontdialog_demo
python -m standard_dialogs.nonmodal_messagebox_demo
python -m standard_dialogs.nonmodal_fontdialog_demo
python -m standard_dialogs.standard_dialogs_showcase
```

### Option 3: Direct execution

```bash
python src/standard_dialogs/modal_messagebox_demo.py
python src/standard_dialogs/modal_fontdialog_demo.py
python src/standard_dialogs/nonmodal_messagebox_demo.py
python src/standard_dialogs/nonmodal_fontdialog_demo.py
python src/standard_dialogs/standard_dialogs_showcase.py
```

## What to Look For

### Modal Demos (1 & 2)
- Try clicking the checkbox or combobox when a dialog is open
- Notice you CANNOT interact with the main window
- The dialog MUST be closed before continuing
- **Demo 1 only**: Toggle "Use Native Dialogs" to see OS native vs Qt cross-platform dialogs

### Non-Modal Demos (3 & 4)
- Try clicking the checkbox or combobox when a dialog is open
- Notice you CAN interact with the main window
- You can even open multiple dialogs simultaneously (demo 3)
- In demo 4, font changes happen in REAL-TIME as you preview fonts

## Key Code Patterns

### Modal QMessageBox (Instance with exec())
```python
# Create instance for more control (e.g., setting options)
msg_box = QMessageBox(self)
msg_box.setIcon(QMessageBox.Information)
msg_box.setWindowTitle("Title")
msg_box.setText("Message")
msg_box.setStandardButtons(QMessageBox.Ok)

# Control native dialog appearance
msg_box.setOption(QMessageBox.DontUseNativeDialog, True)  # Use Qt dialogs
msg_box.setOption(QMessageBox.DontUseNativeDialog, False) # Use OS native

# Show modally - blocks until user responds
result = msg_box.exec()

# Note: Static methods also work but don't allow setting options
# QMessageBox.information(self, "Title", "Message")
```

### Modal QFontDialog (open() with signals)
```python
dialog = QFontDialog(self)
dialog.fontSelected.connect(self.on_font_selected)
dialog.open()  # Modal - blocks parent
```

### Non-Modal QMessageBox (show() method)
```python
msg_box = QMessageBox(self)
msg_box.setText("Message")
msg_box.show()  # Non-modal - doesn't block
# Keep reference or it will be garbage collected!
```

### Non-Modal QFontDialog (show() method)
```python
dialog = QFontDialog(self)
dialog.setModal(False)  # Explicitly set non-modal
dialog.currentFontChanged.connect(self.on_preview)  # Real-time
dialog.fontSelected.connect(self.on_confirmed)
dialog.show()  # Non-modal
```

## Teaching Notes

For students learning about dialogs:

1. Start with **Modal QMessageBox** demo - simplest to understand
2. Move to **Modal QFontDialog** demo - introduces signals pattern
3. Compare with **Non-Modal QMessageBox** - see the behavior difference
4. Finish with **Non-Modal QFontDialog** - most complex, shows real-time updates

Key concepts:
- **Modality**: Does the dialog block the parent window?
- **Static methods vs instances**: Static = always modal, instances = you choose
- **Signals**: Different signals for different stages (preview vs confirm)
- **Object lifetime**: Non-modal dialogs need references or they disappear!
