import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .calculator import Pycalc


class CalculatorWindow(QDialog):
    """A standalone calculator window.

    This is a QDialog that wraps the Pycalc calculator and can be shown
    as a standalone window.

    :ivar calculator: The Pycalc calculator widget
    :vartype calculator: Pycalc
    """

    def __init__(self, parent=None):
        """Initialize the calculator window.

        :param parent: The parent widget
        :type parent: QWidget or None
        """
        super().__init__(parent)

        self.calculator = Pycalc()
        button_layout = self._create_button_box_layout()

        layout = QVBoxLayout()
        layout.addWidget(self.calculator, 1)
        layout.addLayout(button_layout, 0)
        self.setLayout(layout)
        self.setWindowTitle("Calculator")

    def _create_button_box_layout(self):
        ok_button = QPushButton("Ok")
        ok_button.setDefault(True)
        ok_button.clicked.connect(self._ok_button_clicked)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self._cancel_button_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(cancel_button, 0)
        button_layout.addWidget(ok_button, 0)
        return button_layout

    def _ok_button_clicked(self):
        # ... what to do here? ...
        pass

    def _cancel_button_clicked(self):
        # ... what to do here? ...
        pass


class LoanCalculator(QWidget):
    """A loan payment calculator application.

    Calculates monthly loan payments based on loan amount, annual interest rate,
    and loan term in years. Includes an integrated calculator button for the
    loan amount field.

    Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    Where:
        M = Monthly payment
        P = Principal (loan amount)
        r = Monthly interest rate (annual rate / 12)
        n = Number of payments (years * 12)
    """

    def __init__(self, parent=None):
        """Initialize the loan calculator widget.

        :param parent: The parent widget
        :type parent: QWidget or None
        """
        super().__init__(parent)
        self.calculator_window = None

        self.loan_amount_input = QLineEdit()
        self.loan_amount_input.setPlaceholderText("Enter loan amount")

        self.interest_rate_input = QLineEdit()
        self.interest_rate_input.setPlaceholderText("Enter annual interest rate (%)")

        self.loan_term_input = QLineEdit()
        self.loan_term_input.setPlaceholderText("Enter loan term (years)")

        calculate_button = QPushButton("Calculate Payment")
        calculate_button.clicked.connect(self._calculate_payment)

        self.result_label = QLabel("Monthly Payment: $0.00")
        self.result_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; padding: 10px;"
        )
        self.result_label.setAlignment(Qt.AlignCenter)

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        layout.addRow("Loan Amount ($)", self._create_amount_input())
        layout.addRow("Annual Interest Rate (%)", self.interest_rate_input)
        layout.addRow("Loan Term (years)", self.loan_term_input)
        layout.addRow("", calculate_button)
        layout.addRow("", self.result_label)
        self.setLayout(layout)

    def _create_amount_input(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.loan_amount_input = QLineEdit()
        self.loan_amount_input.setPlaceholderText("Enter loan amount")
        layout.addWidget(self.loan_amount_input)

        calc_button = QPushButton()
        calc_button.setIcon(QIcon("calculator-icon-8176.png"))
        calc_button.setMaximumWidth(50)
        calc_button.clicked.connect(self._open_calculator)
        calc_button.setToolTip("Open Calculator")

        layout.addWidget(calc_button)

        w = QWidget()
        w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        w.setLayout(layout)
        return w

    def _open_calculator(self):
        """Open the calculator as a standalone window."""
        if self.calculator_window is None:
            self.calculator_window = CalculatorWindow()
            self.calculator_window.setModal(True)
        self.calculator_window.show()
        self.calculator_window.exec()
        print("...after exec()...")

    def _calculate_payment(self):
        """Calculate and display the monthly loan payment."""
        try:
            # Get input values
            principal = float(self.loan_amount_input.text())
            annual_rate = float(self.interest_rate_input.text())
            years = float(self.loan_term_input.text())

            # Calculate monthly payment
            # Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
            monthly_rate = (annual_rate / 100) / 12
            num_payments = years * 12

            if monthly_rate == 0:
                # If interest rate is 0, payment is simply principal / number of payments
                monthly_payment = principal / num_payments
            else:
                monthly_payment = (
                    principal
                    * (monthly_rate * (1 + monthly_rate) ** num_payments)
                    / ((1 + monthly_rate) ** num_payments - 1)
                )

            # Display result
            self.result_label.setText(f"Monthly Payment: ${monthly_payment:.2f}")
            self.result_label.setStyleSheet(
                "font-size: 18px; font-weight: bold; padding: 10px; color: #00ff00;"
            )

        except ValueError:
            self.result_label.setText("Error: Please enter valid numbers")
            self.result_label.setStyleSheet(
                "font-size: 18px; font-weight: bold; padding: 10px; color: #ff0000;"
            )
        except ZeroDivisionError:
            self.result_label.setText("Error: Invalid loan term")
            self.result_label.setStyleSheet(
                "font-size: 18px; font-weight: bold; padding: 10px; color: #ff0000;"
            )


class LoanCalculatorWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setCentralWidget(LoanCalculator())

        menuBar = self.menuBar()
        menu = menuBar.addMenu("&Help")
        action = QAction("About", self)
        action.triggered.connect(self._about_action_triggered)
        menu.addAction(action)

    def _about_action_triggered(self):
        QMessageBox.about(
            self,
            "About",
            'Icon from <a href="https://www.freeiconspng.com/img/8176">Calculator Simple Png</a>',
        )


def main():
    """Run the loan calculator application."""
    app = QApplication(sys.argv)

    window = LoanCalculatorWindow()
    window.setWindowTitle("Loan Payment Calculator")
    window.resize(500, 300)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
