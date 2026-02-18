import sys
import time

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SlowSlotWidget(QWidget):
    """Demonstrate the problem with a long-running task in Qt."""

    def __init__(self, parent=None):
        super().__init__(parent)
        button = QPushButton("Run task...")
        button.clicked.connect(self._button_clicked)
        input = QLineEdit()
        checkbox = QCheckBox("Click me")

        layout = QVBoxLayout(self)
        layout.addWidget(button)
        layout.addWidget(input)
        layout.addWidget(checkbox)

    def _button_clicked(self):
        print("Task is running...")
        time.sleep(10)  # simulate a long-running task
        print("Task is done")


def main():
    app = QApplication(sys.argv)
    window = SlowSlotWidget()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
