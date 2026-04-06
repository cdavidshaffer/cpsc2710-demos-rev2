import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from issue_tracker.issue import Priority, Status
from issue_tracker.sample_issues import get_samples
from ui.main_window import Ui_MainWindow


class IssuesTableWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._issues = get_samples()

        self.setupUi(self)
        self.retranslateUi(self)
        self.setup_combo_boxes()
        self.setup_issues_table()
        self._connect_widgets()

    def setup_combo_boxes(self):
        for p in Priority:
            self.priority_combo.addItem(p.name, p)
        for s in Status:
            self.status_combo.addItem(s.name, s)

    def setup_issues_table(self):
        columns = ["Title", "Status", "Priority", "Assigned to"]
        self.issues_table.setColumnCount(len(columns))
        self.issues_table.setHorizontalHeaderLabels(columns)
        self.update_issues_table()

    def update_issues_table(self):
        self.issues_table.setRowCount(len(self._issues))
        for row, issue in enumerate(self._issues):
            for column, widget_item in enumerate(
                self._issue_to_table_widget_items(issue)
            ):
                self.issues_table.setItem(row, column, widget_item)
        self.issues_table.resizeColumnsToContents()

    def _issue_to_table_widget_items(self, issue):
        title_item = QTableWidgetItem(issue.title)
        title_item.setData(Qt.ItemDataRole.UserRole, issue)
        return [
            title_item,
            QTableWidgetItem(issue.status.name),
            QTableWidgetItem(issue.priority.name),
            QTableWidgetItem(issue.assigned_to),
        ]

    def _connect_widgets(self):
        self.issues_table.itemSelectionChanged.connect(
            self._issues_table_selection_changed
        )
        self.cancel_button.clicked.connect(self._cancel_button_clicked)
        self.save_button.clicked.connect(self._save_button_clicked)

    def _issues_table_selection_changed(self):
        self._enable_disable_form()
        selected = self._get_selected_rows()
        if len(selected) == 0:
            self._clear_form()
        else:
            assert len(selected) == 1
            self._populate_form_from_row(selected[0])

    def _populate_form_from_row(self, row):
        issue = self.issues_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        self.title_edit.setText(issue.title)
        index = self.priority_combo.findData(issue.priority)
        self.priority_combo.setCurrentIndex(index)
        index = self.status_combo.findData(issue.status)
        self.status_combo.setCurrentIndex(index)
        self.notes_plain_text.setPlainText(issue.notes)
        self.assigned_to_edit.setText(issue.assigned_to)

    def _get_selected_rows(self):
        selected = self.issues_table.selectedIndexes()
        return list(set([s.row() for s in selected]))

    def _form_widgets(self):
        return [
            self.title_edit,
            self.status_combo,
            self.priority_combo,
            self.notes_plain_text,
            self.assigned_to_edit,
        ]

    def _clear_form(self):
        for w in self._form_widgets():
            w.clear()

    def _enable_disable_form(self):
        enabled = len(self._get_selected_rows()) == 1
        for w in self._form_widgets():
            w.setEnabled(enabled)
        if enabled:
            self.setup_combo_boxes()

    def _cancel_button_clicked(self):
        self._issues_table_selection_changed()

    def _save_button_clicked(self):
        # ... save to database ...
        pass


def main():
    app = QApplication(sys.argv)
    window = IssuesTableWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
