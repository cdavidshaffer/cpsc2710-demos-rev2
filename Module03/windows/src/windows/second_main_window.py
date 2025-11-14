"""
QMainWindow Demo - Adding a Toolbar

This demo builds on the first demo by adding a toolbar.
Toolbars provide quick access to common actions through buttons.
"""

import sys
from pathlib import Path

from PySide6.QtGui import QAction, QIcon
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
    A QMainWindow demonstrating menus, toolbars, and a simple form.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow Demo - Toolbar")

        # Create actions first (so they can be shared between menu and toolbar)
        self._create_actions()

        self._create_central_widget()
        self._create_menu_bar()
        self._create_tool_bar()

        self.statusBar().showMessage("Ready")

    def _create_actions(self):
        """
        Create actions that can be shared between menus and toolbars.

        This is a common pattern: create QAction objects once, then add them
        to both menus and toolbars. This ensures consistent behavior.

        Icons are loaded from the icons/ directory using QIcon.
        The icons are from Heroicons (heroicons.com) - MIT licensed.
        """

        icons_dir = Path(__file__).parent / "icons"

        self.submit_action = QAction(
            QIcon(str(icons_dir / "check-circle.svg")), "Submit", self
        )
        self.submit_action.setShortcut("Ctrl+S")
        self.submit_action.setStatusTip("Submit the form")
        self.submit_action.triggered.connect(self._on_submit)

        self.clear_action = QAction(
            QIcon(str(icons_dir / "trash.svg")), "&Clear Form", self
        )
        self.clear_action.setShortcut("Ctrl+L")
        self.clear_action.setStatusTip("Clear all form fields")
        self.clear_action.triggered.connect(self._clear_form)

        self.exit_action = QAction(QIcon(str(icons_dir / "x-mark.svg")), "E&xit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Exit the application")
        self.exit_action.triggered.connect(self.close)

        self.about_action = QAction("&About", self)
        self.about_action.setStatusTip("Show information about this application")
        self.about_action.triggered.connect(self._show_about)

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

        main_layout.addStretch()

    def _create_menu_bar(self):
        """
        Create the menu bar with File and Help menus.

        Notice how we use the same action objects created in _create_actions().
        """
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.clear_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _create_tool_bar(self):
        """
        Create a toolbar with quick-access buttons.

        Toolbars are created with addToolBar() and actions are added to them.
        You can create multiple toolbars and position them on different sides.
        """
        toolbar = self.addToolBar("Main Toolbar")

        # Configure toolbar properties -- experiment with these!
        toolbar.setMovable(False)
        toolbar.setFloatable(False)

        toolbar.addAction(self.submit_action)
        toolbar.addAction(self.clear_action)

        toolbar.addSeparator()

        toolbar.addAction(self.exit_action)

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

        self.statusBar().showMessage(f"Form submitted by {name}", 3000)  # 3 seconds

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
            "This demonstration shows QMainWindow with a toolbar.\n\n"
            "Features shown:\n"
            "• Menu bar with File and Help menus\n"
            "• Toolbar with icon buttons\n"
            "• Status bar with messages\n"
            "• Central widget with a form layout\n"
            "• Shared actions between menu and toolbar\n"
            "• SVG icons loaded with QIcon\n"
            "• Keyboard shortcuts (Ctrl+Q, Ctrl+L, Ctrl+S)\n\n"
            "Icons: Heroicons (MIT licensed)",
        )


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
