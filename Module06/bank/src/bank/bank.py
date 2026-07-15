class WouldOverdraw(Exception):
    pass


class BankAccount:
    """
    A simple representation of a bank account.

    This class models a basic bank account with an account number,
    an owner, and a running balance. It provides methods to deposit
    and withdraw funds, as well as a string representation of the
    account state.

    Attributes:
        account_number (int): A unique identifier for the account.
        owner (str): The name of the account holder.
        _balance (float): The current balance of the account, initialized to 0.
    """

    # ...

    def __init__(self, account_number: int, owner: str):
        """
        Initialize a new BankAccount.

        Args:
            account_number (int): The account's unique identifier.
            owner (str): The name of the account holder.
        """
        self.account_number = account_number
        self.owner = owner
        self._balance: float = 0

    def deposit(self, amount: float) -> None:
        """
        Add money to this account.

        Args:
            amount (float): The amount to deposit.
        """
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Remove money from this account.

        Args:
            amount (float): The amount to withdraw.
        """
        if amount > self._balance:
            raise WouldOverdraw("Insufficient funds")
        self._balance -= amount

    def get_balance(self) -> float:
        """
        Return the balance in this account.

        Returns:
            float: the balance of this account
        """
        return self._balance

    def __str__(self) -> str:
        """
        Return a human-readable representation of the account.

        Returns:
            str: A string describing the account.
        """
        return (
            f"Account number {self.account_number} "
            f"owned by {self.owner} "
            f"with balance {self._balance}"
        )


def main() -> None:
    """Demo of BankAccount"""
    account: BankAccount = BankAccount(123456, "Alice")
    print(account)  # Account number 123456 owned by Alice with balance 0
    account.deposit(1000)
    print(account.get_balance())  # 1000
    account.withdraw(250)
    print(account.get_balance())  # 750
    print(account)  # Account number 123456 owned by Alice with balance 750

    accounts: list[BankAccount] = [
        BankAccount(1001, "Bob"),
        BankAccount(1002, "Charlie"),
    ]
    for a in accounts:
        print(a)

    print(type(accounts))


if __name__ == "__main__":
    main()
