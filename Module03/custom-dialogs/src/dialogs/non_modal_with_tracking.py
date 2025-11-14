import sys
from weakref import WeakSet

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QWidget


class MyDialog(QDialog):
    # Shared weak set for tracking all open instances of this dialog type
    _instances = WeakSet()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Example Dialog")

        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("Close", self, clicked=self.close))

        # Add self to the set of open dialogs
        self._instances.add(self)

        # When dialog is destroyed, it’ll automatically vanish from _instances
        # because we use WeakSet (no need for explicit cleanup).

    @classmethod
    def open_dialog(cls, parent=None):
        """Factory method for creating and showing a new non-modal dialog."""
        dlg = cls(parent)
        dlg.setAttribute(Qt.WA_DeleteOnClose, True)
        dlg.show()
        return dlg

    @classmethod
    def open_dialogs(cls):
        """Optional helper for introspection."""
        return list(cls._instances)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("Open Dialog", self, clicked=self.open_dialog))

    def open_dialog(self):
        MyDialog.open_dialog(self)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
