"""
Modal QMessageBox Demo

This demo shows QMessageBox in modal mode using exec().
Try interacting with the checkbox or combobox while a dialog is open - you can't!
That's what modal means.

This demo also shows how to control the DontUseNativeDialog option.
Toggle "Use Native Dialogs" to see the difference between OS native dialogs
and Qt's cross-platform dialogs.
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ModalMessageBoxDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modal QMessageBox Demo")
        self.setMinimumSize(400, 300)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instructions
        instructions = QLabel(
            "Click any button below to open a MODAL dialog.\n"
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

        # Dialog buttons
        button_layout = QHBoxLayout()

        info_btn = QPushButton("Information")
        info_btn.clicked.connect(self.info_btn_clicked)
        button_layout.addWidget(info_btn)

        warning_btn = QPushButton("Warning")
        warning_btn.clicked.connect(self.warning_btn_clicked)
        button_layout.addWidget(warning_btn)

        layout.addLayout(button_layout)

        button_layout2 = QHBoxLayout()

        critical_btn = QPushButton("Critical")
        critical_btn.clicked.connect(self.critical_btn_clicked)
        button_layout2.addWidget(critical_btn)

        question_btn = QPushButton("Question")
        question_btn.clicked.connect(self.question_btn_clicked)
        button_layout2.addWidget(question_btn)

        layout.addLayout(button_layout2)

        # Status label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        layout.addStretch()

    def info_btn_clicked(self):
        """Show an information message box."""
        msg_box = QMessageBox(
            QMessageBox.Information,
            "Information",
            "This is an information message.\n\n"
            "Notice you can't interact with the main window while this dialog is open!",
            standardButtons=QMessageBox.Ok,
            parent=self,
        )

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        msg_box.exec()  # Modal - blocks until closed
        self.status_label.setText("Status: Information dialog was closed")

    def warning_btn_clicked(self):
        """Show a warning message box."""
        msg_box = QMessageBox(
            QMessageBox.Warning,
            "Warning",
            "This is a warning message.\n\n"
            "The main window is blocked until you close this dialog.",
            standardButtons=QMessageBox.Ok,
            parent=self,
        )

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        msg_box.exec()  # Modal - blocks until closed
        self.status_label.setText("Status: Warning dialog was closed")

    def critical_btn_clicked(self):
        """Show a critical message box."""
        msg_box = QMessageBox(
            QMessageBox.Critical,
            "Critical Error",
            "This is a critical error message!\n\nStill can't touch the main window!",
            standardButtons=QMessageBox.Ok,
            parent=self,
        )

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        msg_box.exec()  # Modal - blocks until closed
        self.status_label.setText("Status: Critical dialog was closed")

    def question_btn_clicked(self):
        """Show a question message box."""
        msg_box = QMessageBox(
            QMessageBox.Question,
            "Question",
            "Do you understand modal dialogs?\n\n"
            "While this dialog is open, the main window is blocked.",
            standardButtons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.Yes,
            parent=self,
        )

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        result = msg_box.exec()  # Modal - blocks until closed

        if result == QMessageBox.Yes:
            self.status_label.setText("Status: You clicked Yes!")
        else:
            self.status_label.setText("Status: You clicked No!")

    def checkbox_stateChanged(self, state):
        """Handle checkbox state changes."""
        self.status_label.setText(
            f"Status: Checkbox is {'checked' if state else 'unchecked'}"
        )

    def combobox_currentTextChanged(self, text):
        """Handle combobox selection changes."""
        self.status_label.setText(f"Status: Selected {text}")


def main():
    app = QApplication(sys.argv)
    window = ModalMessageBoxDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
