import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QCheckBox,
    QRadioButton,
    QButtonGroup,
    QLineEdit,
    QComboBox,
)


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("My Application")
    window.resize(400, 300)

    QLabel("Hello, World!", parent=window).move(10, 10)

    QPushButton("Click Me", parent=window).move(10, 30)
    checkbox = QCheckBox("Awesome app?", parent=window)
    checkbox.move(10, 60)
    checkbox.setChecked(True)

    indoor = QRadioButton("Indoor", parent=window)
    outdoor = QRadioButton("Outdoor", parent=window)
    indoor.move(10, 90)
    outdoor.move(10, 120)
    location_group = QButtonGroup()
    location_group.addButton(indoor)
    location_group.addButton(outdoor)

    short_hair = QRadioButton("Short Hair", parent=window)
    long_hair = QRadioButton("Long Hair", parent=window)
    short_hair.move(10, 150)
    long_hair.move(10, 180)
    hair_group = QButtonGroup()
    hair_group.addButton(short_hair)
    hair_group.addButton(long_hair)

    name = QLineEdit(parent=window)
    name.move(10, 210)
    name.setPlaceholderText("Enter your name")

    disposition = QComboBox(parent=window)
    disposition.addItems(["Friendly", "Shy", "Aggressive"])
    disposition.move(10, 240)

    print(window.children())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
