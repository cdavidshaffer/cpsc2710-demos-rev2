import pytest

from bank_inheritance.accounts import (
    BankAccount,
    CheckingAccount,
    SavingsAccount,
    WouldOverdraw,
)


def test_bank_account_deposit_and_withdraw() -> None:
    account = BankAccount(1001, "Alice")

    account.deposit(100)
    account.withdraw(25)

    assert account.balance == 75


def test_bank_account_rejects_overdraw() -> None:
    account = BankAccount(1001, "Alice", 50)

    with pytest.raises(WouldOverdraw):
        account.withdraw(75)


def test_savings_account_inherits_withdrawal_and_adds_interest() -> None:
    account = SavingsAccount(2001, "Bob", 1200, annual_interest_rate=0.12)

    account.withdraw(200)
    account.monthly_update()

    assert account.balance == pytest.approx(1010)


def test_checking_account_overrides_withdrawal_for_overdraft() -> None:
    account = CheckingAccount(
        3001, "Charlie", opening_balance=50, overdraft_limit=100, overdraft_fee=10
    )

    account.withdraw(75)

    assert account.balance == -35


def test_checking_account_still_rejects_too_much_overdraft() -> None:
    account = CheckingAccount(
        3001, "Charlie", opening_balance=50, overdraft_limit=100, overdraft_fee=10
    )

    with pytest.raises(WouldOverdraw):
        account.withdraw(150)
