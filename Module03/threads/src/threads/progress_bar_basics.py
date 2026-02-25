import sys

from PySide6.QtWidgets import (
    QApplication,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class BasicProgressBarDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        button = QPushButton("Increase")
        button.clicked.connect(self._button_clicked)
        self.bar = QProgressBar(minimum=0, maximum=100)

        layout = QVBoxLayout(self)
        layout.addWidget(button)
        layout.addWidget(self.bar)

    def _button_clicked(self):
        self.bar.setValue(self.bar.value() + 10)


def main():
    app = QApplication(sys.argv)
    w = BasicProgressBarDemo()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
