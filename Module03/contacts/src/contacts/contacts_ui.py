import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
)

from contacts.contact_db import ContactDB
from contacts.contact_editor import ContactEditor
from contacts.contact_list import ContactList


class ContactsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._database = ContactDB()
        self._contacts = self._database.get_all()
        splitter = QSplitter()
        self._contact_list = ContactList()
        self._contact_list.show_contacts(self._contacts)
        self._contact_list.contact_selected.connect(self._contact_selected)
        self._contact_list.contact_removed.connect(self._contact_list_contact_removed)
        self._contact_editor = ContactEditor()
        self._contact_editor.saved.connect(self._contact_editor_saved)
        self._contact_editor.cancelled.connect(self._contact_editor_cancelled)
        splitter.addWidget(self._contact_list)
        splitter.addWidget(self._contact_editor)
        self.setCentralWidget(splitter)

    def _contact_selected(self, selected_contact):
        self._contact_editor.edit_contact(selected_contact)

    def _contact_editor_saved(self, contact):
        if contact.id is None:
            self._database.save(contact)
        else:
            self._database.update(contact)

        self._contact_list.update_contact(contact)

    def _contact_editor_cancelled(self):
        self._list_item_selection_changed()

    def _contact_list_contact_removed(self, contact):
        if contact.id is not None:
            self._database.delete(contact)


def main():
    app = QApplication(sys.argv)
    window = ContactsWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
