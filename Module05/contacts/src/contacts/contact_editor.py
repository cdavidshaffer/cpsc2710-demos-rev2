import sys
from functools import partial

from PySide6.QtCore import QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from contacts.contact import Contact
from themes.theme import theme_manager


class ContactEditor(QWidget):
    cancelled = Signal()
    saved = Signal(Contact)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._validated_inputs = []
        self._contact = None
        form = self._create_contact_form()

        layout = QVBoxLayout(self)
        layout.addWidget(form)

        self._configure_validated_inputs()

    def _create_contact_form(self):
        self._name_input = QLineEdit()
        self._validated_inputs.append(self._name_input)
        self._address_input = QPlainTextEdit()
        self._phone_input = QLineEdit()
        self._validated_inputs.append(self._phone_input)
        self._phone_input.setInputMask("(000) 999-9999")
        self._email_input = QLineEdit()
        self._validated_inputs.append(self._email_input)
        regex = QRegularExpression("^[\\w.-]+@[\\w.-]+\\.[A-Za-z]{2,4}$")
        validator = QRegularExpressionValidator(regex)
        self._email_input.setValidator(validator)

        self._cancel_button = QPushButton(
            theme_manager.icon("cancel.svg"), self.tr("Cancel")
        )
        self._cancel_button.clicked.connect(self._cancel_button_clicked)
        self._save_button = QPushButton(
            theme_manager.icon("save.svg"), self.tr("Save")
        )
        self._save_button.clicked.connect(self._save_button_clicked)

        self._themed_icons = [
            (self._cancel_button, "cancel.svg"),
            (self._save_button, "save.svg"),
        ]
        theme_manager.theme_changed.connect(self._update_icons)

        form_layout = QFormLayout()
        form_layout.addRow(self.tr("Name"), self._name_input)
        form_layout.addRow(self.tr("Address"), self._address_input)
        form_layout.addRow(self.tr("Phone"), self._phone_input)
        form_layout.addRow(self.tr("Email"), self._email_input)
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self._cancel_button, 0)
        button_layout.addWidget(self._save_button, 0)

        form_widget = QWidget()
        widget_layout = QVBoxLayout(form_widget)
        widget_layout.addLayout(form_layout)
        widget_layout.addLayout(button_layout)
        return form_widget

    def _update_icons(self):
        for widget, icon_name in self._themed_icons:
            widget.setIcon(theme_manager.icon(icon_name))

    def _configure_validated_inputs(self):
        for input in self._validated_inputs:
            input.setProperty("invalid", "false")
            input.textChanged.connect(partial(self._validate_input, input))
            # note: lecture showed textEdited signal as well but this is not needed
            # as textChanged is emitted both by setText() and when the user
            # edits the text.

    def _save_button_clicked(self):
        if self._contact is None:
            return
        if not self._phone_input.hasAcceptableInput():
            QMessageBox.warning(
                self,
                "Invalid phone number",
                "The phone number you entered was not valid.",
            )
            return
        if not self._email_input.hasAcceptableInput():
            QMessageBox.warning(
                self,
                "Invalid email address",
                "The email address you entered is not valid",
            )
            return
        self._contact.name = self._name_input.text()
        self._contact.address = self._address_input.toPlainText()
        self._contact.phone = self._phone_input.text()
        self._contact.email = self._email_input.text()
        self.saved.emit(self._contact)

    def _validate_input(self, input, *args):
        if not input.hasAcceptableInput():
            input.setProperty("invalid", "true")
        else:
            input.setProperty("invalid", "false")
        input.style().unpolish(input)
        input.style().polish(input)

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
        for w in [
            self._name_input,
            self._address_input,
            self._phone_input,
            self._email_input,
        ]:
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
