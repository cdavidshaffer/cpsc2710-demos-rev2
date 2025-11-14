import sys
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

# Note this all uppercase variable name follows PEP8 conventions: https://peps.python.org/pep-0008/#constants
ASSETS_PATH = Path(__file__).parent / "assets"

DEFAULT_SELECTION_MODEL = QAbstractItemView.SingleSelection


class ListDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.list = QListWidget()
        self.list.setIconSize(QSize(64, 64))
        self.list.setSelectionMode(DEFAULT_SELECTION_MODEL)
        self._add_initial_items()
        self.list.itemDoubleClicked.connect(self._list_item_double_clicked)
        self.list.itemSelectionChanged.connect(self._list_item_selection_changed)
        layout.addWidget(self.list)

        button = QPushButton("Print items")
        button.clicked.connect(self._print_items_button_clicked)
        layout.addWidget(button)

        selection_group = self._create_selection_mode_group()
        layout.addWidget(selection_group)

        self.setLayout(layout)

    def _create_selection_mode_group(self):
        group = QGroupBox("Selection Mode")
        layout = QHBoxLayout()

        button_group = QButtonGroup(self)
        button_group.buttonClicked.connect(self._selection_mode_changed)

        modes = [
            ("No Selection", QAbstractItemView.NoSelection),
            ("Single Selection", QAbstractItemView.SingleSelection),
            ("Multi Selection", QAbstractItemView.MultiSelection),
            ("Extended Selection", QAbstractItemView.ExtendedSelection),
            ("Contiguous Selection", QAbstractItemView.ContiguousSelection),
        ]

        for label, mode in modes:
            radio = QRadioButton(label)
            button_group.addButton(radio, mode.value)
            layout.addWidget(radio)
            if mode == DEFAULT_SELECTION_MODEL:
                radio.setChecked(True)

        group.setLayout(layout)
        return group

    def _add_initial_items(self):
        # add a string to the list (creates QListItem in addItem())
        self.list.addItem("Wilma Flintstone")

        # add a QListWidgetItem with just a title
        self.list.addItem(QListWidgetItem("Barney Rubble"))

        # add a QListWidgetItem with a title and icon where the title can be edited
        icon = QIcon(str(ASSETS_PATH / "fred.png"))
        item = QListWidgetItem(icon, "Fred Flintstone")
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.list.addItem(item)

        # a couple additional features of QListWidgetItem (see docs for many more!)
        item = QListWidgetItem("Betty Rubble")
        item.setCheckState(Qt.CheckState.Checked)
        item.setBackground(
            QBrush(QColor(200, 0, 100, 100))
        )  # r g b alpha   each value between 0 and 255.
        item.setFont(QFont("Times New Roman", 12, QFont.Bold))
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.list.addItem(item)

        self.list.addItem("Dino")
        self.list.addItem("Pebbles Flintstone")
        self.list.addItem("Bamm-Bamm Rubble")
        self.list.addItem("Mr. Slate")

    def _selection_mode_changed(self, button):
        mode_id = self.sender().id(button)
        self.list.setSelectionMode(QAbstractItemView.SelectionMode(mode_id))

    def _list_item_selection_changed(self):
        print(f"selection changed: {[i.text() for i in self.list.selectedItems()]}")

    def _print_items_button_clicked(self):
        print("-" * 80)
        for index in range(self.list.count()):
            item = self.list.item(index)
            print(f"{item.text()}(checked={item.checkState()}")
        print("-" * 80 + "\n")

    def _list_item_double_clicked(self, item):
        if item.flags() & Qt.ItemIsEditable:
            self.list.editItem(item)
        else:
            QMessageBox.warning(
                self,
                "Item is not editable!",
                "The item you double-clicked on cannot be edited",
            )


def main():
    app = QApplication(sys.argv)
    demo = ListDemo()
    demo.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
