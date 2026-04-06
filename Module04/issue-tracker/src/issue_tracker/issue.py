from enum import Enum


class Status(Enum):
    NEW = 1
    IN_PROGRESS = 2
    CLOSED = 3


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Issue:
    def __init__(self, title, status, priority, assigned_to, notes):
        self.title = title
        self.status = status
        self.priority = priority
        self.assigned_to = assigned_to
        self.notes = notes


if __name__ == "__main__":
    issue = Issue("broken", Status.NEW, Priority.MEDIUM, "Bob", "")
    print(issue)
    for s in Status:
        print(s.value)
