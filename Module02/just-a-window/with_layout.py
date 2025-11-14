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
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
)


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("My Application")
    window.setLayout(create_window_layout())
    window.show()
    sys.exit(app.exec())


def create_window_layout():
    label = QLabel("Hello, World!")
    button_box = create_button_layout()
    checkbox = QCheckBox("Awesome app?")
    checkbox.setChecked(True)

    grid = create_hair_and_location_layout()

    form = create_name_and_disposition_layout()

    window_layout = QVBoxLayout()
    window_layout.addWidget(label)
    window_layout.addLayout(button_box)
    window_layout.addWidget(checkbox)
    window_layout.addLayout(grid)
    window_layout.addLayout(form)
    return window_layout


def create_name_and_disposition_layout():
    name = QLineEdit()
    name.setPlaceholderText("Enter your cat's name")

    disposition = QComboBox()
    disposition.addItems(["Friendly", "Shy", "Aggressive"])

    form = QFormLayout()
    form.addRow("Name", name)
    form.addRow("Disposition", disposition)
    return form


def create_hair_and_location_layout():
    location_label = QLabel("Location:")
    indoor = QRadioButton("Indoor")
    outdoor = QRadioButton("Outdoor")
    location_group = QButtonGroup()
    location_group.addButton(indoor)
    location_group.addButton(outdoor)

    hair_label = QLabel("Hair Length:")
    short_hair = QRadioButton("Short Hair")
    long_hair = QRadioButton("Long Hair")
    hair_group = QButtonGroup()
    hair_group.addButton(short_hair)
    hair_group.addButton(long_hair)

    grid = QGridLayout()
    grid.addWidget(location_label, 0, 0)
    grid.addWidget(indoor, 0, 1)
    grid.addWidget(outdoor, 0, 2)
    grid.addWidget(hair_label, 1, 0)
    grid.addWidget(short_hair, 1, 1)
    grid.addWidget(long_hair, 1, 2)
    return grid


def create_button_layout():
    button1 = QPushButton("Button 1")
    button2 = QPushButton("Button 2")
    button3 = QPushButton("Button 3")
    button4 = QPushButton("Button 4")

    button_box = QHBoxLayout()
    button_box.addWidget(button1, 2)
    button_box.addStretch(1)
    button_box.addWidget(button2, 1)
    button_box.addWidget(button3, 1)
    button_box.addWidget(button4, 1)
    return button_box


if __name__ == "__main__":
    main()
