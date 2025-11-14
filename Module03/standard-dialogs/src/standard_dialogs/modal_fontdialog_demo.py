"""
Modal QFontDialog Demo

This demo shows QFontDialog using open() and signals (modal dialog).
Try interacting with the checkbox or combobox while the dialog is open - you can't!
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QCheckBox, QComboBox, QLabel, QTextEdit, QFontDialog
)
from PySide6.QtGui import QFont


class ModalFontDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modal QFontDialog Demo")
        self.setMinimumSize(500, 400)

        # Keep a reference to the dialog
        self.font_dialog = None

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instructions
        instructions = QLabel(
            "Click 'Choose Font' to open a MODAL font dialog.\n"
            "Try clicking the checkbox or combobox while the dialog is open!"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Extra widgets to demonstrate modality
        self.checkbox = QCheckBox("Try to toggle me when dialog is open")
        self.checkbox.stateChanged.connect(self.checkbox_stateChanged)
        layout.addWidget(self.checkbox)

        self.combobox = QComboBox()
        self.combobox.addItems(["Sip coffee", "Relax and watch TV", "Save the planet"])
        self.combobox.currentTextChanged.connect(self.combobox_currentTextChanged)
        layout.addWidget(self.combobox)

        layout.addSpacing(20)

        # Native dialog control
        self.use_native_checkbox = QCheckBox("Use Native Dialogs")
        self.use_native_checkbox.setChecked(True)
        self.use_native_checkbox.setToolTip(
            "When unchecked, uses Qt's cross-platform dialog instead of OS native dialogs"
        )
        layout.addWidget(self.use_native_checkbox)

        layout.addSpacing(10)

        # Text edit that will have its font changed
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(
            "This is sample text.\n\n"
            "Change the font to see it update!\n\n"
            "Notice how the dialog is MODAL - you can't interact with this window "
            "while the font dialog is open."
        )
        layout.addWidget(self.text_edit)

        # Button to open font dialog
        font_btn = QPushButton("Choose Font")
        font_btn.clicked.connect(self.font_btn_clicked)
        layout.addWidget(font_btn)

        # Status label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

    def font_btn_clicked(self):
        """Show a modal font dialog using open() and signals."""
        # Create the dialog
        self.font_dialog = QFontDialog(self)
        self.font_dialog.setCurrentFont(self.text_edit.font())

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        self.font_dialog.setOption(QFontDialog.DontUseNativeDialog, not use_native)

        # Connect the fontSelected signal
        self.font_dialog.fontSelected.connect(self.font_dialog_fontSelected)

        # Connect finished signal to know when dialog closes
        self.font_dialog.finished.connect(self.font_dialog_finished)

        # open() makes it modal (blocks the main window)
        # It returns immediately but blocks user interaction with parent
        self.font_dialog.open()
        self.status_label.setText("Status: Font dialog is open (MODAL)")

    def font_dialog_fontSelected(self, font: QFont):
        """Handle font selection from dialog."""
        self.text_edit.setFont(font)
        font_info = f"{font.family()}, {font.pointSize()}pt"
        if font.bold():
            font_info += ", Bold"
        if font.italic():
            font_info += ", Italic"
        self.status_label.setText(f"Status: Font changed to {font_info}")

    def font_dialog_finished(self, result):
        """Handle dialog closing."""
        if result == QFontDialog.Rejected:
            self.status_label.setText("Status: Font dialog was cancelled")

    def checkbox_stateChanged(self, state):
        """Handle checkbox state changes."""
        self.status_label.setText(f"Status: Checkbox is {'checked' if state else 'unchecked'}")

    def combobox_currentTextChanged(self, text):
        """Handle combobox selection changes."""
        self.status_label.setText(f"Status: Selected {text}")


def main():
    app = QApplication(sys.argv)
    window = ModalFontDialogDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
