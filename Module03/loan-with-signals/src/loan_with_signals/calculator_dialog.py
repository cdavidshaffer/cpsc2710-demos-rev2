from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from loan_with_signals.calculator import Pycalc


class CalculatorDialog(QDialog):
    equals_executed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculator = Pycalc()
        self.calculator.equals_executed.connect(self.equals_executed)

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
