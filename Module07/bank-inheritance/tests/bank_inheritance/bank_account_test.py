import pytest

from bank_inheritance.bank_account import BankAccount, CheckingAccount, WouldOverdraw


@pytest.fixture
def bank_account():
    return BankAccount(1001, "Fred")


@pytest.fixture
def checking_account():
    return CheckingAccount(1002, "Barney")


class TestBankAccount:
    def test_given_new_account_then_balance_is_zero(self, bank_account):
        assert bank_account.balance == 0

    def test_given_new_account_when_deposit_then_balance_increases(self, bank_account):
        bank_account.deposit(100)
        assert bank_account.balance == 100

    def test_given_account_with_balance_when_deposit_then_balance_increases(
        self, bank_account
    ):
        bank_account.deposit(100)

        bank_account.deposit(50)
        bank_account.deposit(25)

        assert bank_account.balance == 175

    def test_given_account_with_balance_when_withdraw_less_than_balance_then_balance_reduced(
        self, bank_account
    ):
        bank_account.deposit(100)

        bank_account.withdraw(25)

        assert bank_account.balance == 75

    def test_given_account_when_withdraw_greater_than_balance_then_exception(
        self, bank_account
    ):
        bank_account.deposit(100)

        with pytest.raises(WouldOverdraw) as exc:
            bank_account.withdraw(150)
        assert "Insufficient funds" in str(exc.value)

    def test_given_checking_when_overdraw_less_than_limit_then_balance_becomes_negative_and_fee_imposed(
        self, checking_account
    ):
        checking_account.deposit(100)

        checking_account.withdraw(105)

        assert checking_account.balance == -15

    def test_given_checking_when_overdraw_more_than_limit_then_overdraw_exception(
        self, checking_account
    ):
        checking_account.deposit(100)

        with pytest.raises(WouldOverdraw):
            checking_account.withdraw(201)
