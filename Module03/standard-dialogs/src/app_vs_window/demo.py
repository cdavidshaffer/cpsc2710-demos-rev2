import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def make_dialog(title, modality, parent):
    """Helper to create and configure a modal dialog."""
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setWindowModality(modality)
    dlg.setModal(True)

    layout = QVBoxLayout(dlg)
    label = QLabel(f"This dialog is {title.lower()}.")
    ok = QPushButton("Close")
    layout.addWidget(label)
    layout.addWidget(ok)

    ok.clicked.connect(dlg.accept)
    return dlg


def make_main_window(title, modality, x_offset):
    """Create a main window with some interactive widgets."""
    win = QWidget()
    win.setWindowTitle(title)

    layout = QVBoxLayout(win)

    # Add a large gap so the user can see the controls below the dialog on MacOS
    layout.addSpacing(300)

    # Add some interactive components
    entry = QLineEdit()
    entry.setPlaceholderText("Try typing here...")
    check = QCheckBox("Try toggling this box")

    btn = QPushButton(f"Show {title.split()[-2]} Dialog")  # dynamic label

    layout.addWidget(QLabel("Interactive area:"))
    layout.addWidget(entry)
    layout.addWidget(check)
    layout.addWidget(btn)

    # Attach dialog
    dialog = make_dialog(title.split()[1] + " Modal", modality, win)
    btn.clicked.connect(dialog.exec)

    win.move(x_offset, 100)
    win.show()
    return win


def main():
    app = QApplication(sys.argv)

    # Window-modal demo
    win1 = make_main_window("Window Modal Demo", Qt.WindowModal, 100)

    # Application-modal demo
    win2 = make_main_window("Application Modal Demo", Qt.ApplicationModal, 500)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
