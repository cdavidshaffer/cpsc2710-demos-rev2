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
  3 + 17   -- (x = 17, y = 3, op = +)
  3 + 17 = -- (x = 20, y = None, op = None)
"""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

display = None
x_register = ""
y_register = ""
operator_register = None


def main():
    global display
    app = QApplication(sys.argv)
    window_layout = QVBoxLayout()
    display = QLineEdit()
    display.setEnabled(False)
    window_layout.addWidget(display)
    button_layout = QHBoxLayout()
    create_digit_buttons(button_layout)
    create_operator_buttons(button_layout)
    window_layout.addLayout(button_layout)

    window = QWidget()
    window.setWindowTitle("PyCalc")
    window.setLayout(window_layout)
    window.show()
    sys.exit(app.exec())


def create_digit_buttons(button_layout):
    button_0 = QPushButton("0")
    button_0.clicked.connect(zero_clicked)
    button_layout.addWidget(button_0)
    button_1 = QPushButton("1")
    button_1.clicked.connect(one_clicked)
    button_layout.addWidget(button_1)
    button_2 = QPushButton("2")
    button_2.clicked.connect(two_clicked)
    button_layout.addWidget(button_2)


def create_operator_buttons(button_layout):
    button_plus = QPushButton("+")
    button_plus.clicked.connect(plus_clicked)
    button_layout.addWidget(button_plus)
    button_minus = QPushButton("-")
    button_minus.clicked.connect(minus_clicked)
    button_layout.addWidget(button_minus)
    button_equals = QPushButton("=")
    button_equals.clicked.connect(equals_clicked)
    button_layout.addWidget(button_equals)


def equals_clicked():
    global x_register, y_register, operator_register, display
    match operator_register:
        case "+":
            new_value = float(y_register) + float(x_register)
        case "-":
            new_value = float(y_register) - float(x_register)
        case _:
            new_value = x_register
    x_register = str(new_value)
    y_register = ""
    operator_register = None
    display.setText(x_register)


def minus_clicked():
    operator_clicked("-")


def plus_clicked():
    operator_clicked("+")


def operator_clicked(operator):
    global x_register, y_register, operator_register, display
    y_register = x_register
    x_register = ""
    operator_register = operator
    display.setText(x_register)


def zero_clicked():
    digit_clicked(0)


def one_clicked():
    digit_clicked(1)


def two_clicked():
    digit_clicked(2)


def digit_clicked(digit):
    global display, x_register
    new_text = display.text() + str(digit)
    x_register = new_text
    display.setText(x_register)
