import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)

from loan_with_signals.calculator_dialog import CalculatorDialog


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

        self.calculator_dialog = None

        self.loan_amount_widget = self._create_loan_amount_widget()

        self.interest_rate_input = QLineEdit()
        self.interest_rate_input.setPlaceholderText("Enter annual interest rate (%)")

        self.loan_term_input = QLineEdit()
        self.loan_term_input.setPlaceholderText("Enter loan term (years)")

        calculate_button = QPushButton("Calculate Payment")
        calculate_button.clicked.connect(self._calculate_payment_clicked)

        self.result_label = QLabel("Monthly Payment: $0.00")
        self.result_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; padding: 10px;"
        )
        self.result_label.setAlignment(Qt.AlignCenter)

        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        layout.addRow("Loan Amount ($)", self.loan_amount_widget)
        layout.addRow("Annual Interest Rate (%)", self.interest_rate_input)
        layout.addRow("Loan Term (years)", self.loan_term_input)
        layout.addRow("", calculate_button)
        layout.addRow("", self.result_label)
        self.setLayout(layout)

    def _create_loan_amount_widget(self):
        self.loan_amount_input = QLineEdit()
        self.loan_amount_input.setPlaceholderText("Enter loan amount")
        self.loan_amount_input.setStyleSheet("border: none; margin: 0px; padding: 0px")

        calculator_button = QPushButton()
        calculator_button.setIcon(QIcon("calculator-icon-8176.png"))
        calculator_button.setFlat(True)
        calculator_button.setStyleSheet("border: none; padding: 0px; margin: 0px")
        calculator_button.clicked.connect(self._calculator_button_clicked)

        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.loan_amount_input)
        layout.addWidget(calculator_button)

        return w

    def _calculator_button_clicked(self):
        if self.calculator_dialog is None:
            self.calculator_dialog = CalculatorDialog(self)
            self.calculator_dialog.setModal(False)
            self.calculator_dialog.accepted.connect(self._calculator_dialog_accepted)
            self.calculator_dialog.equals_executed.connect(
                self._calculator_equals_executed
            )

        self.calculator_dialog.show()
        self.calculator_dialog.raise_()
        self.calculator_dialog.activateWindow()

    def _calculator_equals_executed(self, value):
        self.loan_amount_input.setText(value)

    def _calculator_dialog_accepted(self):
        self.loan_amount_input.setText(self.calculator_dialog.get_x_register())

    def _calculate_payment_clicked(self):
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
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
