import time

from PySide6.QtCore import QObject, Signal, Slot


class Counter(QObject):
    finished = Signal(name="finished")
    progress = Signal(int, name="progress")

    def go(self):
        for i in range(0, 11):
            self.progress.emit(i)
            time.sleep(1)
        self.finished.emit()


@Slot()
def task_finished():
    print("Finished!")


@Slot()
def task_progress(value):
    print(f"Progress: {value}")


def main():
    task = Counter()
    task.finished.connect(task_finished)
    task.progress.connect(task_progress)

    task.go()


if __name__ == "__main__":
    main()
