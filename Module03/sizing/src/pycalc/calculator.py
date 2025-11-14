import sys
from functools import partial

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

_debug = True


class Pycalc(QWidget):
    """A GUI 4-function calculator.

    ```
    window = QWidget()
    window_layout = VBoxLayout()
    calculator = Pycalc()
    window_layout.addWidget(calculator)
    window.set_layout(window_layout)
    window.show()
    ```

    State machine example::

        3        -- (x = 3, y = None, op = None)
        3 +      -- (x = None, y = 3, op = +)
        3 + 12   -- (x = 12, y = 3, op = +)
        3 + 12 = -- (x = 15, y = None, op = None)

    :ivar x_register: The X register which is shown on the display
    :vartype x_register: str
    :ivar y_register: The Y register
    :vartype y_register: str
    :ivar operator_register: The operator register
    :vartype operator_register: str or None
    """

    def __init__(self, parent=None):
        """Initialize the calculator widget.

        :param parent: The parent widget
        :type parent: QWidget or None
        """
        super().__init__(parent)
        self.display = None
        self.x_register = ""
        self.y_register = ""
        self.operator_register = None
        self.y_debug = None
        self.operator_debug = None

        calculator_layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setEnabled(False)
        self.y_debug = QLineEdit()
        self.y_debug.setEnabled(False)
        self.y_debug.setVisible(_debug)
        self.operator_debug = QLineEdit()
        self.operator_debug.setEnabled(False)
        self.operator_debug.setVisible(_debug)
        calculator_layout.addWidget(self.display)
        calculator_layout.addWidget(self.y_debug)
        calculator_layout.addWidget(self.operator_debug)
        button_layout = QGridLayout()
        self._create_digit_buttons(button_layout)
        self._create_operator_buttons(button_layout)
        calculator_layout.addLayout(button_layout)
        self.setLayout(calculator_layout)

    def _create_digit_buttons(self, button_layout):
        """Create digit buttons (0...9) and add them to button_layout.

        :param button_layout: the grid layout which will contain the 10 digit buttons as well as other buttons
        :type button_layout: QGridLayout
        """
        for i in range(9):
            digit = i + 1
            button = CalculatorButton(str(digit))
            button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            )
            button.clicked.connect(partial(self._digit_clicked, digit))
            button_layout.addWidget(button, 2 - i // 3, i % 3)
        button_0 = CalculatorButton("0")
        button_0.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        button_0.clicked.connect(partial(self._digit_clicked, 0))
        button_layout.addWidget(button_0, 3, 1)

    def _create_operator_buttons(self, button_layout):
        """Create operator buttons (+, -, *, /, =) and add them to button_layout.

        :param button_layout: The grid layout which will contain the operator buttons
        :type button_layout: QGridLayout
        """
        for index, operator in enumerate(["/", "*", "-", "+"]):
            button = CalculatorButton(operator)
            button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            )
            button.clicked.connect(partial(self._operator_clicked, operator))
            button_layout.addWidget(button, index, 3)

        button_equals = CalculatorButton("=")
        button_equals.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        button_equals.clicked.connect(self._equals_clicked)
        button_layout.addWidget(button_equals, 3, 2)

    def _equals_clicked(self):
        """Handle the equals button click event.

        Performs the calculation based on the operator register and updates
        the x_register with the result. Clears the y_register and operator_register.
        """
        match self.operator_register:
            case "+":
                new_value = float(self.y_register) + float(self.x_register)
            case "-":
                new_value = float(self.y_register) - float(self.x_register)
            case "*":
                new_value = float(self.y_register) * float(self.x_register)
            case "/":
                new_value = float(self.y_register) / float(self.x_register)
            case _:
                new_value = self.x_register
        self.x_register = str(new_value)
        self.y_register = ""
        self.operator_register = None
        self._update_ui()

    def _operator_clicked(self, operator):
        """Handle an operator button click event.

        Moves the x_register value to y_register, clears x_register, and sets
        the operator_register to the clicked operator.

        :param operator: The operator that was clicked (+, -, *, or /)
        :type operator: str
        """
        self.y_register = self.x_register
        self.x_register = ""
        self.operator_register = operator
        self._update_ui()

    def _digit_clicked(self, digit):
        """Handle a digit button click event.

        Appends the clicked digit to the current display value and updates
        the x_register.

        :param digit: The digit that was clicked (0-9)
        :type digit: int
        """
        new_text = self.display.text() + str(digit)
        self.x_register = new_text
        self._update_ui()

    def _update_ui(self):
        """Update on-screen widgets to reflect the state of the calculator registers."""
        self.display.setText(self.x_register)
        self.y_debug.setText(self.y_register)
        self.operator_debug.setText(self.operator_register)


class CalculatorButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def sizeHint(self):
        default = super().sizeHint()
        return QSize(default.width() + 20, default.height() + 20)


def main():
    """Run the calculator application.

    Creates and displays a single calculator widget in a window.
    """
    app = QApplication(sys.argv)
    window_layout = QVBoxLayout()
    c = Pycalc()
    window_layout.addWidget(c)

    window = QWidget()
    window.setWindowTitle("PyCalc")
    window.setLayout(window_layout)
    window.show()
    sys.exit(app.exec())
