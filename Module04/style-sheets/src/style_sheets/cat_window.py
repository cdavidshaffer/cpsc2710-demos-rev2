import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from style_sheets.add_cat_dialog import AddCatDialog


class CatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cat Gallery Manager")
        self.setMinimumSize(600, 500)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Header with title
        header_label = QLabel("Cat Gallery Manager")
        header_label.setObjectName("header")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        # Control panel with buttons
        controls_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Cat")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_button_clicked)
        controls_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Cat")
        self.remove_button.setProperty("class", "danger")
        self.remove_button.clicked.connect(self.remove_button_clicked)
        controls_layout.addWidget(self.remove_button)

        self.favorite_button = QPushButton("Favorite")
        self.favorite_button.setCheckable(True)
        self.favorite_button.clicked.connect(self.favorite_button_clicked)
        controls_layout.addWidget(self.favorite_button)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        # Filter section
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()

        self.show_favorites = QCheckBox("Show Only Favorites")
        filter_layout.addWidget(self.show_favorites)

        self.show_adopted = QCheckBox("Show Adopted")
        self.show_adopted.setChecked(True)
        filter_layout.addWidget(self.show_adopted)

        filter_layout.addWidget(QLabel("Breed:"))
        self.breed_combo = QComboBox()
        self.breed_combo.addItems(
            ["All Breeds", "Persian", "Siamese", "Maine Coon", "Bengal", "Ragdoll"]
        )
        filter_layout.addWidget(self.breed_combo)

        filter_layout.addStretch()
        filter_group.setLayout(filter_layout)
        main_layout.addWidget(filter_group)

        # Cat list
        list_label = QLabel("Cat Collection:")
        list_label.setProperty("class", "section-label")
        main_layout.addWidget(list_label)

        self.cat_list = QListWidget()
        self.cat_list.addItems(
            [
                "Whiskers - Persian (Favorite)",
                "Shadow - Siamese",
                "Mittens - Maine Coon (Adopted)",
                "Tiger - Bengal",
                "Fluffy - Ragdoll (Favorite)",
            ]
        )
        main_layout.addWidget(self.cat_list)

        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)

        # Bottom action buttons
        bottom_layout = QHBoxLayout()

        self.info_button = QPushButton("Info")
        self.info_button.clicked.connect(self.info_button_clicked)
        bottom_layout.addWidget(self.info_button)

        bottom_layout.addStretch()

        self.quit_button = QPushButton("Quit")
        self.quit_button.setEnabled(True)
        self.quit_button.clicked.connect(self.close)
        bottom_layout.addWidget(self.quit_button)

        main_layout.addLayout(bottom_layout)

    def add_button_clicked(self):
        dialog = AddCatDialog(self)
        result = dialog.exec()

        if result:
            cat_name = dialog.get_cat_name()
            cat_breed = dialog.get_cat_breed()
            self.cat_list.addItem(f"{cat_name} - {cat_breed}")
            self.status_label.setText(f"Added {cat_name} to the gallery!")

    def remove_button_clicked(self):
        current_item = self.cat_list.currentItem()
        if current_item:
            self.cat_list.takeItem(self.cat_list.row(current_item))
            self.status_label.setText("Cat removed from gallery")
        else:
            self.status_label.setText("Please select a cat to remove")

    def favorite_button_clicked(self, checked):
        if checked:
            self.status_label.setText("Showing favorite cats")
        else:
            self.status_label.setText("Showing all cats")

    def info_button_clicked(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About Cat Gallery")
        msg.setText("Cat Gallery Manager v1.0")
        msg.setInformativeText("Manage your collection of cats!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()


def main():
    app = QApplication(sys.argv)

    # Load stylesheet
    qss_path = Path(__file__).parent.parent.parent / "styles.qss"
    if qss_path.exists():
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())

    window = CatWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
