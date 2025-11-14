"""
Non-Modal QFontDialog Demo

This demo shows QFontDialog in non-modal mode using show() instead of open().
You can interact with the main window while the dialog is open!
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QComboBox, QLabel, QTextEdit, QFontDialog
)
from PySide6.QtGui import QFont


class NonModalFontDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Non-Modal QFontDialog Demo")
        self.setMinimumSize(500, 400)

        # Keep a reference to the dialog
        self.font_dialog = None

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instructions
        instructions = QLabel(
            "Click 'Choose Font' to open a NON-MODAL font dialog.\n"
            "You CAN interact with the checkbox and combobox while the dialog is open!\n"
            "The font updates in real-time as you select options in the dialog."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Extra widgets to demonstrate non-modality
        self.checkbox = QCheckBox("You can toggle me even when the dialog is open!")
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
            "Change the font to see it update in REAL-TIME!\n\n"
            "Notice how the dialog is NON-MODAL - you can interact with this window "
            "while the font dialog is open. Try typing here, toggling the checkbox, "
            "or changing the combobox while the dialog is open!"
        )
        layout.addWidget(self.text_edit)

        # Buttons
        button_layout = QHBoxLayout()

        font_btn = QPushButton("Choose Font")
        font_btn.clicked.connect(self.font_btn_clicked)
        button_layout.addWidget(font_btn)

        close_dialog_btn = QPushButton("Close Font Dialog")
        close_dialog_btn.clicked.connect(self.close_dialog_btn_clicked)
        button_layout.addWidget(close_dialog_btn)

        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

    def font_btn_clicked(self):
        """Show a non-modal font dialog using show() instead of open()."""
        # Close existing dialog if open
        if self.font_dialog is not None:
            self.font_dialog.close()

        # Create the dialog
        self.font_dialog = QFontDialog(self)
        self.font_dialog.setCurrentFont(self.text_edit.font())

        # Set it to be non-modal
        self.font_dialog.setModal(False)

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        self.font_dialog.setOption(QFontDialog.DontUseNativeDialog, not use_native)

        # Connect the currentFontChanged signal for real-time updates
        self.font_dialog.currentFontChanged.connect(self.font_dialog_currentFontChanged)

        # Connect the fontSelected signal (when user clicks OK)
        self.font_dialog.fontSelected.connect(self.font_dialog_fontSelected)

        # Connect finished signal to know when dialog closes
        self.font_dialog.finished.connect(self.font_dialog_finished)

        # Use show() instead of open() or exec() for non-modal
        self.font_dialog.show()
        self.status_label.setText("Status: Font dialog is open (NON-MODAL)")

    def close_dialog_btn_clicked(self):
        """Close the font dialog if it's open."""
        if self.font_dialog is not None:
            self.font_dialog.close()
            self.font_dialog = None
            self.status_label.setText("Status: Font dialog closed programmatically")

    def font_dialog_currentFontChanged(self, font: QFont):
        """Handle real-time font changes as user selects in the dialog."""
        self.text_edit.setFont(font)
        font_info = f"{font.family()}, {font.pointSize()}pt"
        if font.bold():
            font_info += ", Bold"
        if font.italic():
            font_info += ", Italic"
        self.status_label.setText(f"Status: Preview - {font_info}")

    def font_dialog_fontSelected(self, font: QFont):
        """Handle font selection when user clicks OK."""
        self.text_edit.setFont(font)
        font_info = f"{font.family()}, {font.pointSize()}pt"
        if font.bold():
            font_info += ", Bold"
        if font.italic():
            font_info += ", Italic"
        self.status_label.setText(f"Status: Font confirmed - {font_info}")

    def font_dialog_finished(self, result):
        """Handle dialog closing."""
        if result == QFontDialog.Rejected:
            self.status_label.setText("Status: Font dialog was cancelled")
        self.font_dialog = None

    def checkbox_stateChanged(self, state):
        """Handle checkbox state changes."""
        self.status_label.setText(f"Status: Checkbox is {'checked' if state else 'unchecked'}")

    def combobox_currentTextChanged(self, text):
        """Handle combobox selection changes."""
        self.status_label.setText(f"Status: Selected {text}")


def main():
    app = QApplication(sys.argv)
    window = NonModalFontDialogDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
