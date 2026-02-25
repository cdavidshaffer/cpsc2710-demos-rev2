import time

from PySide6.QtCore import QObject, QThread, Signal, Slot


class Counter(QObject):
    finished = Signal(name="finished")
    progress = Signal(int, name="progress")

    @Slot()
    def go(self):
        for i in range(0, 101):
            if QThread.currentThread().isInterruptionRequested():
                return
            self.progress.emit(i)
            time.sleep(0.05)
        self.finished.emit()
