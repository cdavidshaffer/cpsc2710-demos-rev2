from issue_tracker.issue import Issue, Priority, Status
from issue_tracker.issue_editor import IssueEditor


def test_show_issue(qtbot):
    widget = IssueEditor()
    qtbot.addWidget(widget)
    issue = Issue(
        title="Broken login",
        status=Status.IN_PROGRESS,
        priority=Priority.HIGH,
        assigned_to="Bob",
        notes="Users can't log in on Safari.",
    )

    widget.show_issue(issue)

    assert widget.title_edit.text() == issue.title
    assert widget.status_combo.currentData() == issue.status
    assert widget.priority_combo.currentData() == issue.priority
    assert widget.assigned_to_edit.text() == issue.assigned_to
    assert widget.notes_plain_text.toPlainText() == issue.notes


def test_clear(qtbot):
    widget = IssueEditor()
    qtbot.addWidget(widget)
    issue = Issue(
        title="Broken login",
        status=Status.IN_PROGRESS,
        priority=Priority.HIGH,
        assigned_to="Bob",
        notes="Users can't log in on Safari.",
    )
    widget.show_issue(issue)

    widget.clear()

    assert widget.title_edit.text() == ""
    assert widget.status_combo.currentIndex() == -1
    assert widget.priority_combo.currentIndex() == -1
    assert widget.assigned_to_edit.text() == ""
    assert widget.notes_plain_text.toPlainText() == ""


def test_update_issue(qtbot):
    widget = IssueEditor()
    qtbot.addWidget(widget)
    issue = Issue(
        title="Old title",
        status=Status.NEW,
        priority=Priority.LOW,
        assigned_to="Alice",
        notes="Old notes",
    )
    widget.title_edit.setText("New title")
    widget.status_combo.setCurrentIndex(widget.status_combo.findData(Status.CLOSED))
    widget.priority_combo.setCurrentIndex(
        widget.priority_combo.findData(Priority.URGENT)
    )
    widget.assigned_to_edit.setText("Carol")
    widget.notes_plain_text.setPlainText("New notes")

    widget.update_issue(issue)

    assert issue.title == "New title"
    assert issue.status == Status.CLOSED
    assert issue.priority == Priority.URGENT
    assert issue.assigned_to == "Carol"
    assert issue.notes == "New notes"
