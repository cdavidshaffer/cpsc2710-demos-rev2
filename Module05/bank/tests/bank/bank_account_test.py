import pytest

from bank.bank_account import BankAccount, WouldOverdraw


@pytest.fixture
def bank_account():
    return BankAccount(1001, "Fred")


class TestBankAccount:
    def test_given_new_account_then_balance_is_zero(self, bank_account):
        # Arrange
        # Done in fixture

        # Act
        # Nothing

        # Assert
        assert bank_account.get_balance() == 0

    def test_given_new_account_when_deposit_then_balance_increases(self, bank_account):
        # Arrange
        # Done in fixture

        # Act
        bank_account.deposit(100)

        # Assert
        assert bank_account.get_balance() == 100

    def test_given_account_with_balance_when_deposit_then_balance_increases(
        self, bank_account
    ):
        # Arrange
        bank_account.deposit(100)

        # Act
        bank_account.deposit(50)
        bank_account.deposit(25)

        # Assert
        assert bank_account.get_balance() == 175

    def test_given_account_with_balance_when_withdraw_less_than_balance_then_balance_reduced(
        self, bank_account
    ):
        bank_account.deposit(100)

        bank_account.withdraw(25)

        assert bank_account.get_balance() == 75

    def test_given_account_when_withdraw_greater_than_balance_then_exception(
        self, bank_account
    ):
        bank_account.deposit(100)

        with pytest.raises(WouldOverdraw) as exc:
            bank_account.withdraw(150)
        assert "Insufficient funds" in str(exc.value)
