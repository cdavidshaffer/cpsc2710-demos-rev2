import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from contacts.contact import Contact
from contacts.db_setup import initialize_database


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.repo = initialize_database()
        self._contacts = self.repo.get_all()
        splitter = QSplitter()
        self._list = self._create_list()
        left_widget = self._create_left_widget()
        splitter.addWidget(left_widget)
        splitter.addWidget(self._create_form())
        self.setCentralWidget(splitter)

    def _create_left_widget(self):
        button_layout = QHBoxLayout()
        new_contact_button = QPushButton("+")
        new_contact_button.clicked.connect(self._new_contact_button_clicked)
        delete_contact_button = QPushButton("-")
        delete_contact_button.clicked.connect(self._delete_contact_button_clicked)
        button_layout.addWidget(new_contact_button)
        button_layout.addWidget(delete_contact_button)

        layout = QVBoxLayout()
        layout.addWidget(self._list)
        layout.addLayout(button_layout)

        left = QWidget()
        left.setLayout(layout)
        return left

    def _new_contact_button_clicked(self):
        contact = Contact("New Contact", "", "", "")
        new_contact = self.repo.save(contact)
        item = self._add_contact_to_list(self._list, new_contact)
        self._list.setCurrentItem(item)

    def _delete_contact_button_clicked(self):
        # Get current selection
        selection = self._list.selectedItems()
        if len(selection) == 0:
            return

        # Get the contact from the selected item
        item = selection[0]
        contact = item.data(Qt.ItemDataRole.UserRole)

        self.repo.delete(contact.id)
        self._list.takeItem(self._list.row(item))

    def _create_list(self):
        list = QListWidget()
        list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        for c in self._contacts:
            self._add_contact_to_list(list, c)
        list.itemSelectionChanged.connect(self._list_item_selection_changed)
        return list

    def _add_contact_to_list(self, list, c):
        item = QListWidgetItem()
        item.setText(c.name)
        item.setData(Qt.ItemDataRole.UserRole, c)
        list.addItem(item)
        return item

    def _create_form(self):
        form_layout = QFormLayout()
        self._name_edit = QLineEdit()
        form_layout.addRow("Name", self._name_edit)
        self._address_edit = QPlainTextEdit()
        form_layout.addRow("Address", self._address_edit)
        self._phone_edit = QLineEdit()
        form_layout.addRow("Phone", self._phone_edit)
        self._email_edit = QLineEdit()
        form_layout.addRow("Email", self._email_edit)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self._save_button_clicked)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self._cancel_button_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(save_button)
        hbox.addWidget(cancel_button)

        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        vbox.addLayout(hbox)

        form_widget = QWidget()
        form_widget.setLayout(vbox)
        return form_widget

    def _save_button_clicked(self):
        # Get current selection
        selection = self._list.selectedItems()
        if len(selection) == 0:
            return

        # Get the contact from the selected item
        item = selection[0]
        contact = item.data(Qt.ItemDataRole.UserRole)

        # Update contact with form values
        contact.name = self._name_edit.text()
        contact.address = self._address_edit.toPlainText()
        contact.phone = self._phone_edit.text()
        contact.email = self._email_edit.text()

        # Save to database (automatically creates or updates)
        saved = self.repo.save(contact)

        # Update the contact reference and list item display
        item.setData(Qt.ItemDataRole.UserRole, saved)
        item.setText(saved.name)

    def _cancel_button_clicked(self):
        self._list_item_selection_changed()

    def _list_item_selection_changed(self):
        selection = self._list.selectedItems()
        print(f"selection: {selection}")
        if len(selection) == 0:
            self._clear_form()
            return
        if len(selection) != 1:
            raise ValueError("Bug: selection size should always be zero or 1!")
        item = selection[0].data(Qt.ItemDataRole.UserRole)
        self._name_edit.setText(item.name)
        self._address_edit.setPlainText(item.address)
        self._phone_edit.setText(item.phone)
        self._email_edit.setText(item.email)

    def _clear_form(self):
        self._name_edit.clear()
        self._address_edit.clear()
        self._phone_edit.clear()
        self._email_edit.clear()


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
