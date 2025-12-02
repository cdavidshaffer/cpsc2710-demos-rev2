import sys

from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget

from .calculator import Pycalc


def main():
    """Run the dual calculator application.

    Creates and displays two calculator widgets side by side in a window.
    """
    app = QApplication(sys.argv)
    window_layout = QHBoxLayout()
    c1 = Pycalc()
    window_layout.addWidget(c1)
    c2 = Pycalc()
    window_layout.addWidget(c2)

    window = QWidget()
    window.setWindowTitle("PyCalc")
    window.setLayout(window_layout)
    window.show()
    sys.exit(app.exec())
