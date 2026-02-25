import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from contacts.contact import Contact
from contacts.sample_data import get_samples


class ContactList(QWidget):
    contact_selected = Signal(Contact)
    contact_removed = Signal(Contact)
    contacted_added = Signal(Contact)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._contacts = []

        self._create_contact_list()

        remove_contact_button = QPushButton("-")
        remove_contact_button.clicked.connect(self._remove_contact_button_clicked)
        new_contact_button = QPushButton("+")
        new_contact_button.clicked.connect(self._new_contact_button_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(remove_contact_button)
        button_layout.addWidget(new_contact_button)

        layout = QVBoxLayout()
        layout.addWidget(self._list)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def show_contacts(self, contacts):
        self._contacts = contacts
        self._populate_contact_list()

    def update_contact(self, contact):
        "The contact may have changed, update the corresponding list widget item"
        item = self._item_for_contact(contact)
        if item is None:
            return
        item.setText(contact.name)

    def _item_for_contact(self, contact):
        for i in range(0, self._list.count()):
            item = self._list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == contact:
                return item
        return None

    def _create_contact_list(self):
        self._list = QListWidget()
        self._list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self._list.itemSelectionChanged.connect(self._list_item_selection_changed)
        self._populate_contact_list()
        return self._list

    def _list_item_selection_changed(self):
        selected = self._get_selected_contact()
        self.contact_selected.emit(selected)

    def _new_contact_button_clicked(self):
        c = Contact("New Contact", "Address", "Email", "Phone")
        self._contacts.append(c)
        self._populate_contact_list()
        item = self._list.item(len(self._contacts) - 1)
        self._list.setCurrentItem(item)
        self.contacted_added.emit(c)

    def _remove_contact_button_clicked(self):
        selected_contact = self._get_selected_contact()
        if selected_contact is None:
            return
        self._contacts.remove(selected_contact)
        self._populate_contact_list()
        self.contact_removed.emit(selected_contact)

    def _populate_contact_list(self):
        self._list.clear()
        for contact in self._contacts:
            item = QListWidgetItem()
            item.setText(contact.name)
            item.setData(Qt.ItemDataRole.UserRole, contact)
            self._list.addItem(item)

    def _get_selected_contact(self):
        """Get the contact selected in the contact list.

        :return: corresponding contact
        :rtype: Contact
        """
        selection = self._list.selectedItems()
        if len(selection) == 0:
            return None
        assert len(selection) == 1
        selected_item = selection[0]
        return selected_item.data(Qt.ItemDataRole.UserRole)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ContactList()
    w.show_contacts(get_samples())
    w.contact_selected.connect(lambda c: print(f"selected: {c}"))
    w.show()
    sys.exit(app.exec())
