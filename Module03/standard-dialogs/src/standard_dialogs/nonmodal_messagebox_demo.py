"""
Non-Modal QMessageBox Demo

This demo shows QMessageBox in non-modal mode using show() instead of exec().
Try interacting with the checkbox or combobox while a dialog is open - you CAN!
That's the difference between modal and non-modal.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QComboBox, QLabel, QMessageBox
)


class NonModalMessageBoxDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Non-Modal QMessageBox Demo")
        self.setMinimumSize(400, 300)

        # Keep references to dialogs so they don't get garbage collected
        self.message_boxes = []

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instructions
        instructions = QLabel(
            "Click any button below to open a NON-MODAL dialog.\n"
            "You CAN interact with the checkbox and combobox while dialogs are open!\n"
            "You can even open multiple dialogs at once!"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Extra widgets to demonstrate non-modality
        self.checkbox = QCheckBox("You can toggle me even when dialogs are open!")
        self.checkbox.stateChanged.connect(self.checkbox_stateChanged)
        layout.addWidget(self.checkbox)

        self.combobox = QComboBox()
        self.combobox.addItems(["Sip coffee", "Relax and watch TV", "Save the planet"])
        self.combobox.currentTextChanged.connect(self.combobox_currentTextChanged)
        layout.addWidget(self.combobox)

        layout.addSpacing(20)

        # Native dialog control
        self.use_native_checkbox = QCheckBox("Use Native Dialogs (might be ignored!)")
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

    def create_message_box(self, icon, title, text):
        """Create a non-modal message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Set to non-modal - CRITICAL for non-blocking behavior
        msg_box.setModal(False)

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        # Connect finished signal to handle cleanup
        msg_box.finished.connect(lambda result: self.message_box_finished(msg_box, result))

        # Keep reference to prevent garbage collection
        self.message_boxes.append(msg_box)

        # Use show() instead of exec() for non-modal
        msg_box.show()

        return msg_box

    def info_btn_clicked(self):
        """Show a non-modal information message box."""
        self.create_message_box(
            QMessageBox.Information,
            "Information",
            "This is a NON-MODAL information message.\n\n"
            "Try interacting with the main window!\n"
            "You can even open multiple dialogs!"
        )
        self.status_label.setText("Status: Information dialog opened (non-modal)")

    def warning_btn_clicked(self):
        """Show a non-modal warning message box."""
        self.create_message_box(
            QMessageBox.Warning,
            "Warning",
            "This is a NON-MODAL warning message.\n\n"
            "The main window is still active!"
        )
        self.status_label.setText("Status: Warning dialog opened (non-modal)")

    def critical_btn_clicked(self):
        """Show a non-modal critical message box."""
        self.create_message_box(
            QMessageBox.Critical,
            "Critical Error",
            "This is a NON-MODAL critical error!\n\n"
            "You can still use the main window!"
        )
        self.status_label.setText("Status: Critical dialog opened (non-modal)")

    def question_btn_clicked(self):
        """Show a non-modal question message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Question")
        msg_box.setText(
            "Do you understand non-modal dialogs?\n\n"
            "While this dialog is open, you can still interact with the main window!"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.Yes)

        # Set to non-modal - CRITICAL for non-blocking behavior
        msg_box.setModal(False)

        # Set the DontUseNativeDialog option based on checkbox
        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        # Connect buttonClicked signal to handle the response
        msg_box.buttonClicked.connect(self.question_dialog_buttonClicked)

        # Connect finished signal for cleanup
        msg_box.finished.connect(lambda result: self.message_box_finished(msg_box, result))

        self.message_boxes.append(msg_box)
        msg_box.show()

        self.status_label.setText("Status: Question dialog opened (non-modal)")

    def question_dialog_buttonClicked(self, button):
        """Handle question dialog button clicks."""
        sender = self.sender()
        if sender.standardButton(button) == QMessageBox.Yes:
            self.status_label.setText("Status: You clicked Yes!")
        else:
            self.status_label.setText("Status: You clicked No!")

    def message_box_finished(self, msg_box, _result):
        """Handle message box closing and cleanup."""
        if msg_box in self.message_boxes:
            self.message_boxes.remove(msg_box)

    def checkbox_stateChanged(self, state):
        """Handle checkbox state changes."""
        self.status_label.setText(f"Status: Checkbox is {'checked' if state else 'unchecked'}")

    def combobox_currentTextChanged(self, text):
        """Handle combobox selection changes."""
        self.status_label.setText(f"Status: Selected {text}")


def main():
    app = QApplication(sys.argv)
    window = NonModalMessageBoxDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
