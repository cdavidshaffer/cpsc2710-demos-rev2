from dataclasses import dataclass
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


@dataclass()
class Issue:
    title: str
    status: Status
    priority: Priority
    assigned_to: str
    notes: str


if __name__ == "__main__":
    issue = Issue("broken", Status.NEW, Priority.MEDIUM, "Bob", "")
    print(issue)
    for s in Status:
        print(s.value)
