import sys

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from threads.counter import Counter


class BasicProgressBarDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.button = QPushButton("Run Task...")
        self.button.clicked.connect(self._button_clicked)
        input = QLineEdit()
        checkbox = QCheckBox("Click me")
        self.bar = QProgressBar(minimum=0, maximum=100)
        self.status = QLabel("")

        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(input)
        layout.addWidget(checkbox)
        layout.addWidget(self.bar)
        layout.addWidget(self.status)

    def _button_clicked(self):
        self.thread = QThread()
        self.worker = Counter()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.go)
        self.worker.finished.connect(self._worker_finished)
        self.worker.progress.connect(self.bar.setValue)

        self.thread.start()
        self.button.setEnabled(False)
        self.status.setText("Started")

    def _worker_finished(self):
        self.thread.quit()
        self.thread.wait()

        self.thread.deleteLater()
        self.worker.deleteLater()

        self.thread = None
        self.worker = None

        self.status.setText("Finished")
        self.button.setEnabled(True)

    def about_to_quit(self):
        if self.thread is not None:
            self.thread.requestInterruption()
            self.thread.quit()
            self.thread.wait()


def main():
    app = QApplication(sys.argv)
    w = BasicProgressBarDemo()
    app.aboutToQuit.connect(w.about_to_quit)
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
