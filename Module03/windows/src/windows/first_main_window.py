"""
QMainWindow Demo - Introduction to Main Windows and Menus

This demo introduces QMainWindow, which provides a standard application window
with support for menu bars, toolbars, status bars, and dock widgets.
"""

import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """
    A basic QMainWindow demonstrating menus and a simple form.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow Demo")

        self._create_central_widget()
        self._create_menu_bar()

        self.statusBar().showMessage("Ready")

    def _create_central_widget(self):
        """
        Create and set up the central widget with a form.

        The central widget is the main content area of a QMainWindow.
        Unlike QWidget, QMainWindow requires you to explicitly set a central widget.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        form_layout.addRow("Name:", self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        form_layout.addRow("Email:", self.email_input)

        self.comments_input = QTextEdit()
        self.comments_input.setPlaceholderText("Enter any comments")
        self.comments_input.setMaximumHeight(100)
        form_layout.addRow("Comments:", self.comments_input)

        main_layout.addLayout(form_layout)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self._on_submit)
        main_layout.addWidget(submit_button)

        # Add stretch to push everything to the top
        main_layout.addStretch()

    def _create_menu_bar(self):
        """
        Create the menu bar with File and Help menus.

        QMainWindow provides menuBar() which returns a QMenuBar.
        Menus are added to the menu bar, and actions are added to menus.
        """
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")  # & creates Alt+F shortcut

        clear_action = QAction("&Clear Form", self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.setStatusTip("Clear all form fields")
        clear_action.triggered.connect(self._clear_form)
        file_menu.addAction(clear_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Note on MacOS the menu items in this menu get folded into the "Apple" menu (to follow UI guidelines).
        help_menu = menu_bar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.setStatusTip("Show information about this application")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _on_submit(self):
        """Handle the submit button click."""
        name = self.name_input.text()
        email = self.email_input.text()
        comments = self.comments_input.toPlainText()

        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return

        message = f"Name: {name}\nEmail: {email}\nComments: {comments}"
        QMessageBox.information(self, "Form Submitted", message)

        self.statusBar().showMessage(f"Form submitted by {name}", 3000)

    def _clear_form(self):
        """Clear all form fields."""
        self.name_input.clear()
        self.email_input.clear()
        self.comments_input.clear()
        self.statusBar().showMessage("Form cleared", 2000)

    def _show_about(self):
        """Show the About dialog."""
        QMessageBox.about(
            self,
            "About QMainWindow Demo",
            "This is a basic demonstration of QMainWindow.\n\n"
            "Features shown:\n"
            "• Menu bar with File and Help menus\n"
            "• Status bar with messages\n"
            "• Central widget with a form layout\n"
            "• Keyboard shortcuts (Ctrl+Q, Ctrl+L)",
        )


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
