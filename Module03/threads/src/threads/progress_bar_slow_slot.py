import sys
import time

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class BasicProgressBarDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        button = QPushButton("Run Task...")
        button.clicked.connect(self._button_clicked)
        input = QLineEdit()
        checkbox = QCheckBox("Click me")
        self.bar = QProgressBar(minimum=0, maximum=100)

        layout = QVBoxLayout(self)
        layout.addWidget(button)
        layout.addWidget(input)
        layout.addWidget(checkbox)
        layout.addWidget(self.bar)

    def _button_clicked(self):
        for i in range(0, 101):
            self.bar.setValue(i)
            time.sleep(0.1)  # work


def main():
    app = QApplication(sys.argv)
    w = BasicProgressBarDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
