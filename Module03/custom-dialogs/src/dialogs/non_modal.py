import sys
from functools import partial

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DemoDialog(QDialog):
    """Just used for demonstration purposes.  Do not create buttons this way in a dialog!  They
    may follow your platform's look and feel guidelines at the very least and there are better
    tools for this job.
    """

    def __init__(self, message, parent=None):
        super().__init__(parent)
        message_label = QLabel(message)
        ok_button = QPushButton("Ok (triggers accept)")
        cancel_button = QPushButton("Cancel (triggers reject)")
        extra_button = QPushButton("Extra (triggers done(99))")
        close_button = QPushButton("Close (calls close())")
        set_visible_false_button = QPushButton("set visible False")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        extra_button.clicked.connect(partial(self.done, 99))
        close_button.clicked.connect(self.close)
        set_visible_false_button.clicked.connect(partial(self.setVisible, False))
        layout = QVBoxLayout()
        layout.addWidget(message_label)
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(extra_button)
        button_layout.addWidget(close_button)
        button_layout.addWidget(set_visible_false_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)


class DemoWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QPushButton("Press to open dialog")
        self.button.clicked.connect(self.open_clicked)
        self.label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def open_clicked(self):
        dialog = DemoDialog("Message box text", self)
        dialog.setModal(False)
        dialog.rejected.connect(self.message_box_rejected)
        dialog.accepted.connect(self.message_box_accepted)
        dialog.finished.connect(self.message_box_finished)
        dialog.show()

    def message_box_rejected(self):
        print("Rejected")

    def message_box_accepted(self):
        print("Accepted")

    def message_box_finished(self, val):
        print(f"Finished({val})")


def main():
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())
