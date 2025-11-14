import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QWidget,
)


class SimpleMessageBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        button = QPushButton("Explode")
        button.clicked.connect(self.button_clicked)
        layout.addWidget(button)

    def button_clicked(self):
        selected_button = QMessageBox.critical(
            self,
            "Boom",
            "Boom!!!!!",
            buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            defaultButton=QMessageBox.StandardButton.Cancel,
        )
        if selected_button == QMessageBox.StandardButton.Ok:
            print("OK clicked")
        else:
            print("Cancel clicked")


def main():
    app = QApplication(sys.argv)
    window = SimpleMessageBox()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
