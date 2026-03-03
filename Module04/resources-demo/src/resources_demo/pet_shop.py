import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import resources_demo.resources_rc  # noqa: F401

ICONS_DIR = ":/icons/"


class PetStoreWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paws & Claws Pet Store")

        # Menu bar with an icon
        menu_bar = self.menuBar()
        pets_menu = menu_bar.addMenu("Pets")
        turtle_action = QAction(QIcon(ICONS_DIR + "turtle.png"), "Turtle", self)
        pets_menu.addAction(turtle_action)

        # Buttons
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        button_row = QHBoxLayout()
        for name in ("dog", "cat", "fish", "bird"):
            btn = QPushButton(QIcon(ICONS_DIR + f"{name}.png"), name.title())
            btn.setIconSize(btn.iconSize() * 2)
            button_row.addWidget(btn)

        layout.addLayout(button_row)


def main() -> None:
    app = QApplication(sys.argv)
    window = PetStoreWindow()
    window.show()
    sys.exit(app.exec())
