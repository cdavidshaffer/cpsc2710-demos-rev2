import pytest


@pytest.fixture
def account():
    return BankAccount(1, "Fred")


def test_withdraw(account):
    account.deposit(100)
    account.withdraw(40)
    assert account.balance == 60
