"""
Module description
------------------
A GUI 4-function calculator.

Module variables
----------------
x_register: the X register which is shown on the display
y_register: the Y register
operator_register: the operator register

Example
-------
  3        -- (x = 3, y = None, op = None)
  3 +      -- (x = None, y = 3, op = +)
  3 + 12   -- (x = 12, y = 3, op = +)
  3 + 12 = -- (x = 15, y = None, op = None)
"""

import sys
from functools import partial

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

display = None
x_register = ""
y_register = ""
operator_register = None
y_debug = None
operator_debug = None


def main():
    global display, y_debug, operator_debug
    app = QApplication(sys.argv)
    window_layout = QVBoxLayout()
    display = QLineEdit()
    display.setEnabled(False)
    y_debug = QLineEdit()
    y_debug.setEnabled(False)
    operator_debug = QLineEdit()
    operator_debug.setEnabled(False)
    window_layout.addWidget(display)
    window_layout.addWidget(y_debug)
    window_layout.addWidget(operator_debug)
    button_layout = QGridLayout()
    _create_digit_buttons(button_layout)
    _create_operator_buttons(button_layout)
    window_layout.addLayout(button_layout)

    window = QWidget()
    window.setWindowTitle("PyCalc")
    window.setLayout(window_layout)
    window.show()
    sys.exit(app.exec())


def _create_digit_buttons(button_layout):
    """Create digit buttons (0...9) and add them to button_layout.

    :param button_layout: the grid layout which will contain the 10 digit buttons as well as other buttons
    :type button_layout: QGridLayout
    """
    for i in range(9):
        digit = i + 1
        button_1 = QPushButton(str(digit))
        button_1.clicked.connect(partial(_digit_clicked, digit))
        button_layout.addWidget(button_1, 2 - i // 3, i % 3)
    button_0 = QPushButton("0")
    button_0.clicked.connect(partial(_digit_clicked, 0))
    button_layout.addWidget(button_0, 3, 1)


def _create_operator_buttons(button_layout):
    for index, operator in enumerate(["/", "*", "-", "+"]):
        button = QPushButton(operator)
        button.clicked.connect(partial(_operator_clicked, operator))
        button_layout.addWidget(button, index, 3)

    button_equals = QPushButton("=")
    button_equals.clicked.connect(_equals_clicked)
    button_layout.addWidget(button_equals, 3, 2)


def _equals_clicked():
    global x_register, y_register, operator_register, display
    match operator_register:
        case "+":
            new_value = float(y_register) + float(x_register)
        case "-":
            new_value = float(y_register) - float(x_register)
        case "*":
            new_value = float(y_register) * float(x_register)
        case "/":
            new_value = float(y_register) / float(x_register)
        case _:
            new_value = x_register
    x_register = str(new_value)
    y_register = ""
    operator_register = None
    _update_ui()


def _operator_clicked(operator):
    global x_register, y_register, operator_register, display
    y_register = x_register
    x_register = ""
    operator_register = operator
    _update_ui()


def _digit_clicked(digit):
    global display, x_register
    new_text = display.text() + str(digit)
    x_register = new_text
    _update_ui()


def _update_ui():
    """Update on-screen widgets to reflect the state of the calculator registers."""
    global display
    display.setText(x_register)
    y_debug.setText(y_register)
    operator_debug.setText(operator_register)
