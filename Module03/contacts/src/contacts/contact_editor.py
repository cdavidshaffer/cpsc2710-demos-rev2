import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QFormLayout, QHBoxLayout, QLineEdit, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from contacts.contact import Contact


class ContactEditor(QWidget):
    cancelled = Signal()
    saved = Signal(Contact)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._contact = None
        form = self._create_contact_form()
        
        layout = QVBoxLayout(self)
        layout.addWidget(form)


    def _create_contact_form(self):
        self._name_input = QLineEdit()
        self._address_input = QPlainTextEdit()
        self._phone_input = QLineEdit()
        self._email_input = QLineEdit()

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self._cancel_button_clicked)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self._save_button_clicked)

        form_layout = QFormLayout()
        form_layout.addRow("Name", self._name_input)
        form_layout.addRow("Address", self._address_input)
        form_layout.addRow("Phone", self._phone_input)
        form_layout.addRow("Email", self._email_input)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(cancel_button, 0)
        button_layout.addWidget(save_button, 0)

        form_widget = QWidget()
        widget_layout = QVBoxLayout(form_widget)
        widget_layout.addLayout(form_layout)
        widget_layout.addLayout(button_layout)
        return form_widget
    
    def _save_button_clicked(self):
        if self._contact is None:
            return
        self._contact.name = self._name_input.text()
        self._contact.address = self._address_input.toPlainText()
        self._contact.phone = self._phone_input.text()
        self._contact.email = self._email_input.text()
        self.saved.emit(self._contact)

    def _cancel_button_clicked(self):
        self.cancelled.emit()

    def edit_contact(self, contact):
        self._contact = contact
        if contact is None:
            self._clear_contact_form()
        else:
            self._edit_actual_contact(contact)

    def _edit_actual_contact(self, contact):
        self._name_input.setText(contact.name)
        self._address_input.setPlainText(contact.address)
        self._phone_input.setText(contact.phone)
        self._email_input.setText(contact.email)

    def _clear_contact_form(self):
        for w in [self._name_input, self._address_input, 
                  self._phone_input, self._email_input]:
            w.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ContactEditor()
    contact = Contact("Bob", "Here", "bob@here.net", "555-1212")
    w.edit_contact(contact)
    w.saved.connect(lambda: print(f"saved: {contact}"))
    w.cancelled.connect(lambda: print("cancelled"))
    w.show()
    sys.exit(app.exec())