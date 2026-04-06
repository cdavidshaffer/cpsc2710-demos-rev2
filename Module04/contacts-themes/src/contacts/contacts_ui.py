import sys

from PySide6.QtCore import QFile, QLocale, QTranslator
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSplitter,
    QStyleFactory,
)

import contacts.resources_rc  # noqa: F401
from contacts.contact_db import ContactDB
from contacts.contact_editor import ContactEditor
from contacts.contact_list import ContactList
from themes.theme import DarkTheme, LightTheme, theme_manager


class ContactsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._database = ContactDB()
        self._contacts = self._database.get_all()
        self._is_dark = False

        self._create_toolbar()
        self._create_menus()

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

    def _create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)

        self._new_action = QAction(theme_manager.icon("add.svg"), "New Contact", self)
        self._new_action.setStatusTip("Create a new contact")
        self._new_action.triggered.connect(self._toolbar_new_contact)
        toolbar.addAction(self._new_action)

        self._delete_action = QAction(
            theme_manager.icon("delete.svg"), "Delete Contact", self
        )
        self._delete_action.setStatusTip("Delete selected contact")
        self._delete_action.triggered.connect(self._toolbar_delete_contact)
        toolbar.addAction(self._delete_action)

        toolbar.addSeparator()

        self._save_action = QAction(theme_manager.icon("save.svg"), "Save", self)
        self._save_action.setStatusTip("Save current contact")
        self._save_action.triggered.connect(self._toolbar_save)
        toolbar.addAction(self._save_action)

    def _create_menus(self):
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("&View")

        self._toggle_theme_action = QAction(
            theme_manager.icon("theme.svg"),
            "Switch to Dark Theme",
            self,
        )
        self._toggle_theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(self._toggle_theme_action)

        self._themed_icons = [
            (self._new_action, "add.svg"),
            (self._delete_action, "delete.svg"),
            (self._save_action, "save.svg"),
            (self._toggle_theme_action, "theme.svg"),
        ]
        theme_manager.theme_changed.connect(self._update_icons)

    def _update_icons(self):
        for widget, icon_name in self._themed_icons:
            widget.setIcon(theme_manager.icon(icon_name))

    def _toggle_theme(self):
        app = QApplication.instance()
        if self._is_dark:
            theme_manager.set_theme(LightTheme())
            theme_manager.install(app)
            self._toggle_theme_action.setText("Switch to Dark Theme")
        else:
            theme_manager.set_theme(DarkTheme())
            theme_manager.install(app)
            self._toggle_theme_action.setText("Switch to Light Theme")
        self._is_dark = not self._is_dark
        app.setStyleSheet(app.styleSheet())

    def _toolbar_new_contact(self):
        self._contact_list._new_contact_button_clicked()

    def _toolbar_delete_contact(self):
        self._contact_list._remove_contact_button_clicked()

    def _toolbar_save(self):
        self._contact_editor._save_button_clicked()

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


def load_translations(app):
    locale = QLocale.system()
    translator = QTranslator(app)
    if translator.load(locale, "translation", "_", ":/translations"):
        app.installTranslator(translator)
    else:
        print(f"translations for {locale} not found")


def load_style_sheet(app):
    file = QFile(":/styles/default.qss")
    if not file.open(QFile.ReadOnly):
        print(f"Unable to open style file {file}")
    else:
        app.setStyleSheet(file.readAll().toStdString())
        file.close()


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    theme_manager.set_theme(LightTheme())
    theme_manager.install(app)

    load_translations(app)
    load_style_sheet(app)

    window = ContactsWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
