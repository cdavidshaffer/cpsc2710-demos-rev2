import os
import tempfile

import pytest

from bank.bank_account import BankAccount


class NewCode:
    @pytest.fixture
    def account_file_1(self):
        handle = tempfile.NamedTemporaryFile(suffix=".acct", delete=False)
        path = handle.name
        handle.close()

        account = BankAccount(100, "Pebbles")
        account.deposit(75)
        account.save(path)

        yield path

        if os.path.exists(path):
            os.remove(path)

    @pytest.fixture
    def account_file(self, tmp_path):
        """Same as account_file_1 but uses built-in tmp_path fixture"""
        path = tmp_path / "account.acct"

        account = BankAccount(100, "Pebbles")
        account.deposit(75)
        account.save(path)

        return path

    def test_load_account_from_file(self, account_file):
        account = BankAccount.load(account_file)

        assert account.owner == "Pebbles"
        assert account.get_balance() == 75

    def test_save_updated_account(self, account_file):
        account = BankAccount.load(account_file)
        account.withdraw(25)
        account.save(account_file)

        reloaded = BankAccount.load(account_file)
        assert reloaded.get_balance() == 50

    @pytest.fixture
    def account(self):
        return BankAccount(1001, "Fred")

    def test_overdraw(self, account):
        with pytest.raises(ValueError) as exc:
            account.withdraw(50)
        assert "Insufficient funds" in str(exc.value)
