import sys
import time

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Worker(QObject):
    progress = Signal(int)
    finished = Signal()

    def run(self):
        # Simulate a task with 101 steps (step number 0, 1, 2, ..., 100)
        # since the progress bar has a range of 0 to 100, this ensures that
        # the progress value will start at 0 and end at 100 (progress bar full)
        #
        # In practice it can be difficult to break a real task up into even
        # run-time segments.  You've probably noticed this problem in real
        # application progress bars (such as OS updates or software installs).
        for i in range(101):
            time.sleep(0.05)  # Simulate portion of long-running work
            self.progress.emit(i)
        self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threaded vs Non-Threaded Demo")

        # --- Status widgets ---
        self.status_label = QLabel("Idle")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)

        # --- Misc input widgets to prove UI liveness ---
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Type here while task runs")

        self.choice_box = QComboBox()
        self.choice_box.addItems(["Option A", "Option B", "Option C"])

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_edit)
        form_layout.addRow("Choice:", self.choice_box)

        # --- Buttons ---
        self.threaded_button = QPushButton("Start (Threaded)")
        self.threaded_button.clicked.connect(self.start_task_threaded)

        self.nothread_button = QPushButton("Start (NO Thread)")
        self.nothread_button.clicked.connect(self.start_task_nothread)

        # --- Layout ---
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addLayout(form_layout)
        layout.addWidget(self.threaded_button)
        layout.addWidget(self.nothread_button)
        self.setLayout(layout)

        self.thread = None
        self.worker = None

    # ------------------------------------------------------------
    # Threaded version (GOOD)
    # ------------------------------------------------------------
    def start_task_threaded(self):
        self._prepare_ui("Working (threaded)...")

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._task_finished)
        self.worker.finished.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    # ------------------------------------------------------------
    # Non-threaded version (BAD)
    # ------------------------------------------------------------
    def start_task_nothread(self):
        self._prepare_ui("Working (NO thread)...")

        self.worker = Worker()
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self._task_finished)

        # Perform the worker's task in GUI thread
        self.worker.run()
        self.worker.deleteLater()
        self.worker = None

        self._task_finished()

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------
    def _prepare_ui(self, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(0)
        self.threaded_button.setEnabled(False)
        self.nothread_button.setEnabled(False)

    def _task_finished(self):
        self.status_label.setText("Done")

        self.worker = None
        self.thread = None

        self.threaded_button.setEnabled(True)
        self.nothread_button.setEnabled(True)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
