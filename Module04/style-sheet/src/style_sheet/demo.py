import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import style_sheet.resources_rc  # noqa: F401


class DemoWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Style Sheet Demo")

        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("First button"))
        layout.addWidget(QPushButton("Second button"))
        layout.addWidget(QCheckBox("Having a good time?"))
        b = QPushButton("Delete my files?")
        b.setObjectName("delete-button")
        layout.addWidget(b)

        h = QHBoxLayout()
        b2 = QPushButton("Special button 1")
        b2.setProperty("class", "special")
        b3 = QPushButton("Special button 2")
        b3.setProperty("class", "special")
        h.addWidget(b2)
        h.addWidget(b3)

        layout.addLayout(h)


def load_style_sheet(app):
    file = QFile(":/stylesheets/style.qss")
    if file.open(QIODevice.OpenModeFlag.ReadOnly):
        app.setStyleSheet(file.readAll().toStdString())
    else:
        print("Style sheet not found")


def main():
    app = QApplication(sys.argv)

    load_style_sheet(app)

    window = DemoWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
