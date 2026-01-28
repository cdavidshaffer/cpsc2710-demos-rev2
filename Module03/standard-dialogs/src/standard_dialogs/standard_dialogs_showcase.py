"""
Qt Standard Dialogs Showcase

This demo showcases all the standard dialog types available in Qt.
Each button opens the corresponding dialog modally.
"""

import sys

from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QErrorMessage,
    QFileDialog,
    QFontDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StandardDialogsShowcase(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Standard Dialogs Showcase")
        self.setMinimumSize(500, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Instructions
        instructions = QLabel(
            "Click any button below to see a Qt standard dialog.\n"
            "All dialogs open modally."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        layout.addSpacing(20)

        # Native dialog control
        self.use_native_checkbox = QCheckBox("Use Native Dialogs")
        self.use_native_checkbox.setChecked(True)
        self.use_native_checkbox.setToolTip(
            "When unchecked, uses Qt's cross-platform dialog instead of OS native dialogs"
        )
        layout.addWidget(self.use_native_checkbox)

        layout.addSpacing(20)

        # QFileDialog buttons
        file_group_label = QLabel("File Dialogs:")
        file_group_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(file_group_label)

        file_button_layout = QHBoxLayout()

        open_file_btn = QPushButton("Open File")
        open_file_btn.clicked.connect(self.open_file_btn_clicked)
        file_button_layout.addWidget(open_file_btn)

        save_file_btn = QPushButton("Save File")
        save_file_btn.clicked.connect(self.save_file_btn_clicked)
        file_button_layout.addWidget(save_file_btn)

        open_dir_btn = QPushButton("Open Directory")
        open_dir_btn.clicked.connect(self.open_dir_btn_clicked)
        file_button_layout.addWidget(open_dir_btn)

        layout.addLayout(file_button_layout)

        layout.addSpacing(10)

        # Color and Font dialogs
        appearance_group_label = QLabel("Appearance Dialogs:")
        appearance_group_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(appearance_group_label)

        appearance_button_layout = QHBoxLayout()

        color_btn = QPushButton("Color Dialog")
        color_btn.clicked.connect(self.color_btn_clicked)
        appearance_button_layout.addWidget(color_btn)

        font_btn = QPushButton("Font Dialog")
        font_btn.clicked.connect(self.font_btn_clicked)
        appearance_button_layout.addWidget(font_btn)

        layout.addLayout(appearance_button_layout)

        layout.addSpacing(10)

        # Input dialogs
        input_group_label = QLabel("Input Dialogs:")
        input_group_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(input_group_label)

        input_button_layout1 = QHBoxLayout()

        text_input_btn = QPushButton("Text Input")
        text_input_btn.clicked.connect(self.text_input_btn_clicked)
        input_button_layout1.addWidget(text_input_btn)

        int_input_btn = QPushButton("Integer Input")
        int_input_btn.clicked.connect(self.int_input_btn_clicked)
        input_button_layout1.addWidget(int_input_btn)

        double_input_btn = QPushButton("Double Input")
        double_input_btn.clicked.connect(self.double_input_btn_clicked)
        input_button_layout1.addWidget(double_input_btn)

        layout.addLayout(input_button_layout1)

        input_button_layout2 = QHBoxLayout()

        item_input_btn = QPushButton("Item Selection")
        item_input_btn.clicked.connect(self.item_input_btn_clicked)
        input_button_layout2.addWidget(item_input_btn)

        multiline_input_btn = QPushButton("Multiline Text")
        multiline_input_btn.clicked.connect(self.multiline_input_btn_clicked)
        input_button_layout2.addWidget(multiline_input_btn)

        layout.addLayout(input_button_layout2)

        layout.addSpacing(10)

        # Message dialogs
        message_group_label = QLabel("Message Dialogs:")
        message_group_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(message_group_label)

        message_button_layout = QHBoxLayout()

        info_msg_btn = QPushButton("Information")
        info_msg_btn.clicked.connect(self.info_msg_btn_clicked)
        message_button_layout.addWidget(info_msg_btn)

        warning_msg_btn = QPushButton("Warning")
        warning_msg_btn.clicked.connect(self.warning_msg_btn_clicked)
        message_button_layout.addWidget(warning_msg_btn)

        error_msg_btn = QPushButton("Error Message")
        error_msg_btn.clicked.connect(self.error_msg_btn_clicked)
        message_button_layout.addWidget(error_msg_btn)

        layout.addLayout(message_button_layout)

        layout.addSpacing(20)

        # Status label
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        layout.addStretch()

        # Keep reference to error message dialog
        self.error_message_dialog = None

    def get_dialog_options(self):
        """Get dialog options based on native checkbox state."""
        use_native = self.use_native_checkbox.isChecked()
        if use_native:
            return QFileDialog.Option(0)  # Default options (native)
        else:
            return QFileDialog.DontUseNativeDialog

    def open_file_btn_clicked(self):
        """Show open file dialog."""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
            options=self.get_dialog_options(),
        )
        if file_name:
            self.status_label.setText(f"Status: Selected file: {file_name}")
        else:
            self.status_label.setText("Status: Open file dialog cancelled")

    def save_file_btn_clicked(self):
        """Show save file dialog."""
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "untitled.txt",
            "Text Files (*.txt);;All Files (*)",
            options=self.get_dialog_options(),
        )
        if file_name:
            self.status_label.setText(f"Status: Save to: {file_name}")
        else:
            self.status_label.setText("Status: Save file dialog cancelled")

    def open_dir_btn_clicked(self):
        """Show open directory dialog."""
        dir_name = QFileDialog.getExistingDirectory(
            self, "Select Directory", "", options=self.get_dialog_options()
        )
        if dir_name:
            self.status_label.setText(f"Status: Selected directory: {dir_name}")
        else:
            self.status_label.setText("Status: Directory selection cancelled")

    def color_btn_clicked(self):
        """Show color picker dialog."""
        use_native = self.use_native_checkbox.isChecked()
        options = (
            QColorDialog.ColorDialogOption(0)
            if use_native
            else QColorDialog.DontUseNativeDialog
        )

        color = QColorDialog.getColor(QColor(255, 0, 0), self, "Select Color", options)
        if color.isValid():
            self.status_label.setText(f"Status: Selected color: {color.name()}")
        else:
            self.status_label.setText("Status: Color selection cancelled")

    def font_btn_clicked(self):
        """Show font picker dialog."""
        use_native = self.use_native_checkbox.isChecked()
        options = (
            QFontDialog.FontDialogOption(0)
            if use_native
            else QFontDialog.DontUseNativeDialog
        )

        font, ok = QFontDialog.getFont(QFont("Arial", 12), self, "Select Font", options)
        if ok:
            font_info = f"{font.family()}, {font.pointSize()}pt"
            self.status_label.setText(f"Status: Selected font: {font_info}")
        else:
            self.status_label.setText("Status: Font selection cancelled")

    def text_input_btn_clicked(self):
        """Show text input dialog."""
        text, ok = QInputDialog.getText(self, "Text Input", "Enter your name:")
        if ok and text:
            self.status_label.setText(f"Status: You entered: {text}")
        else:
            self.status_label.setText("Status: Text input cancelled")

    def int_input_btn_clicked(self):
        """Show integer input dialog."""
        value, ok = QInputDialog.getInt(
            self,
            "Integer Input",
            "Enter a number:",
            value=42,
            minValue=0,
            maxValue=100,
            step=1,
        )
        if ok:
            self.status_label.setText(f"Status: You entered: {value}")
        else:
            self.status_label.setText("Status: Integer input cancelled")

    def double_input_btn_clicked(self):
        """Show double input dialog."""
        value, ok = QInputDialog.getDouble(
            self,
            "Double Input",
            "Enter a decimal number:",
            value=3.14,
            minValue=0.0,
            maxValue=100.0,
            decimals=2,
        )
        if ok:
            self.status_label.setText(f"Status: You entered: {value}")
        else:
            self.status_label.setText("Status: Double input cancelled")

    def item_input_btn_clicked(self):
        """Show item selection dialog."""
        items = ["Red", "Green", "Blue", "Yellow", "Purple"]
        item, ok = QInputDialog.getItem(
            self,
            "Item Selection",
            "Select your favorite color:",
            items,
            current=0,
            editable=False,
        )
        if ok and item:
            self.status_label.setText(f"Status: You selected: {item}")
        else:
            self.status_label.setText("Status: Item selection cancelled")

    def multiline_input_btn_clicked(self):
        """Show multiline text input dialog."""
        text, ok = QInputDialog.getMultiLineText(
            self,
            "Multiline Text Input",
            "Enter multiple lines of text:",
            "Line 1\nLine 2\nLine 3",
        )
        if ok and text:
            lines = text.count("\n") + 1
            self.status_label.setText(f"Status: You entered {lines} lines of text")
        else:
            self.status_label.setText("Status: Multiline input cancelled")

    def info_msg_btn_clicked(self):
        """Show information message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Information")
        msg_box.setText("This is an information message from QMessageBox.")
        msg_box.setStandardButtons(QMessageBox.Ok)

        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        msg_box.exec()
        self.status_label.setText("Status: Information message shown")

    def warning_msg_btn_clicked(self):
        """Show warning message box."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText("This is a warning message from QMessageBox.")
        msg_box.setStandardButtons(QMessageBox.Ok)

        use_native = self.use_native_checkbox.isChecked()
        msg_box.setOption(QMessageBox.DontUseNativeDialog, not use_native)

        msg_box.exec()
        self.status_label.setText("Status: Warning message shown")

    def error_msg_btn_clicked(self):
        """Show error message dialog using QErrorMessage."""
        if self.error_message_dialog is None:
            self.error_message_dialog = QErrorMessage(self)

        self.error_message_dialog.showMessage(
            "This is an error message from QErrorMessage.\n\n"
            "Note: QErrorMessage doesn't support the native/non-native option."
        )
        self.status_label.setText("Status: Error message shown")


def main():
    app = QApplication(sys.argv)
    window = StandardDialogsShowcase()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
