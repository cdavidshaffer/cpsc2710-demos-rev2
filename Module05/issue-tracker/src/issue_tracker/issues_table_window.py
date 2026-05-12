import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from issue_tracker.issue import Issue, Priority, Status
from issue_tracker.sample_issues import get_samples
from ui.main_window import Ui_MainWindow


class IssuesTableWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._issues = get_samples()

        self.setupUi(self)
        self._setup_combo_boxes()
        self._setup_issues_table()
        self._connect_widgets()

    def _setup_combo_boxes(self):
        for p in Priority:
            self.priority_combo.addItem(p.name, p)
        for s in Status:
            self.status_combo.addItem(s.name, s)

    def _setup_issues_table(self):
        self._update_issues_table()

    def _connect_widgets(self):
        self.save_button.clicked.connect(self._save_button_clicked)
        self.cancel_button.clicked.connect(self._cancel_button_clicked)
        self.issues_table.itemSelectionChanged.connect(
            self._issues_table_item_selection_changed
        )
        self.new_issue_button.clicked.connect(self._new_issue_button_clicked)
        self.delete_issue_button.clicked.connect(self._delete_issue_button_clicked)

    def _update_ui(self):
        """Make all objects changes visible in the UI.

        Currently only the issues table needs to be updated..."""
        self._update_issues_table()

    def _update_issues_table(self):
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

    def _save_button_clicked(self):
        selected = self._get_selected_issue()
        if selected is None:
            return
        self._update_issue_from_form(selected)

    def _cancel_button_clicked(self):
        self._issues_table_item_selection_changed()

    def _new_issue_button_clicked(self):
        self._issues.append(Issue("New Issue", Status.NEW, Priority.MEDIUM, None, ""))
        self._update_ui()
        self.issues_table.selectRow(len(self._issues) - 1)

    def _delete_issue_button_clicked(self):
        selected = self._get_selected_issue()
        if selected is None:
            return
        self._issues.remove(selected)
        self._update_ui()
        self.issues_table.clearSelection()

    def _issues_table_item_selection_changed(self):
        selected = self._get_selected_issue()
        if selected is None:
            self._clear_form()
        else:
            self._show_issue(selected)

    def _clear_form(self):
        self.title_edit.clear()
        self.status_combo.setCurrentIndex(-1)
        self.priority_combo.setCurrentIndex(-1)
        self.notes_plain_text.clear()
        self.assigned_to_edit.clear()

    def _show_issue(self, issue):
        self.title_edit.setText(issue.title)
        self.status_combo.setCurrentIndex(self.status_combo.findData(issue.status))
        self.priority_combo.setCurrentIndex(
            self.priority_combo.findData(issue.priority)
        )
        self.notes_plain_text.setPlainText(issue.notes)
        self.assigned_to_edit.setText(issue.assigned_to)

    def _update_issue_from_form(self, issue):
        issue.title = self.title_edit.text()
        issue.status = self.status_combo.currentData()
        issue.priority = self.priority_combo.currentData()
        issue.notes = self.notes_plain_text.toPlainText()
        issue.assigned_to = self.assigned_to_edit.text()
        self._update_ui()

    def _get_selected_issue(self):
        """The user may or may not have selected a row in the table.  If not, return None, otherwise return the Issue
        object corresponding to the selected row.  This issue is stored in UserRole data in column 0 of the selected row."""
        selected_indices = self.issues_table.selectionModel().selectedRows()
        assert len(selected_indices) < 2

        return (
            self.issues_table.item(selected_indices[0].row(), 0).data(
                Qt.ItemDataRole.UserRole
            )
            if len(selected_indices) > 0
            else None
        )


def main():
    app = QApplication(sys.argv)
    window = IssuesTableWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
