from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from issue_tracker.issue import Issue, Priority, Status


class IssueEditor(QWidget):
    save_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "issue-editor")
        self._build_ui()
        self._populate_combo_boxes()
        self._connect_widgets()

    def _build_ui(self):
        self.title_edit = QLineEdit(self)
        self.status_combo = QComboBox(self)
        self.priority_combo = QComboBox(self)
        self.assigned_to_edit = QLineEdit(self)
        self.notes_plain_text = QPlainTextEdit(self)
        self.save_button = QPushButton(self.tr("Save"), self)
        self.cancel_button = QPushButton(self.tr("Cancel"), self)

        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )
        form_layout.addRow(self.tr("&Title"), self.title_edit)
        form_layout.addRow(self.tr("&Status"), self.status_combo)
        form_layout.addRow(self.tr("&Priority"), self.priority_combo)
        form_layout.addRow(self.tr("&Assigned to"), self.assigned_to_edit)
        form_layout.addRow(self.tr("&Notes"), self.notes_plain_text)

        button_layout = QHBoxLayout()
        button_layout.addItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def _populate_combo_boxes(self):
        for status in Status:
            self.status_combo.addItem(status.name, status)
        for priority in Priority:
            self.priority_combo.addItem(priority.name, priority)

    def _connect_widgets(self):
        self.save_button.clicked.connect(self.save_clicked)
        self.cancel_button.clicked.connect(self.cancel_clicked)

    def show_issue(self, issue: Issue):
        self.title_edit.setText(issue.title)
        self.status_combo.setCurrentIndex(self.status_combo.findData(issue.status))
        self.priority_combo.setCurrentIndex(
            self.priority_combo.findData(issue.priority)
        )
        self.assigned_to_edit.setText(issue.assigned_to)
        self.notes_plain_text.setPlainText(issue.notes)

    def clear(self):
        self.title_edit.clear()
        self.status_combo.setCurrentIndex(-1)
        self.priority_combo.setCurrentIndex(-1)
        self.assigned_to_edit.clear()
        self.notes_plain_text.clear()

    def update_issue(self, issue: Issue):
        issue.title = self.title_edit.text()
        issue.status = self.status_combo.currentData()
        issue.priority = self.priority_combo.currentData()
        issue.assigned_to = self.assigned_to_edit.text()
        issue.notes = self.notes_plain_text.toPlainText()
