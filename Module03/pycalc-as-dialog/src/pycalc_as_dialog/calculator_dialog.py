from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from pycalc_as_dialog.calculator import Pycalc


class CalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = Pycalc()

        button_box = QDialogButtonBox(
            standardButtons=QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
        )

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.calculator)
        layout.addWidget(button_box)

    def get_x_register(self):
        return self.calculator.x_register
