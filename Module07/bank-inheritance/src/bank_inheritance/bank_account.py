class WouldOverdraw(Exception):
    """Raised when a withdrawal would overdraw the account."""

    pass


class BankAccount:
    """A simple bank account with deposit and withdrawal."""

    def __init__(self, account_number: int, owner: str):
        """Initialize with account number and owner name."""
        self._account_number = account_number
        self._owner = owner
        self._balance: float = 0

    @property
    def account_number(self) -> int:
        return self._account_number

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, owner: str) -> None:
        """Set the owner name; must be a string of length >= 3."""
        if not isinstance(owner, str) or len(owner) < 3:
            raise ValueError("Owner must be a string with a minimum length of 3")
        self._owner = owner

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: float) -> None:
        """Deposit amount into the account."""
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Withdraw amount; raises WouldOverdraw if insufficient funds."""
        if amount > self._balance:
            raise WouldOverdraw("Insufficient funds")
        self._balance -= amount

    def __str__(self) -> str:
        """Return a string representation of the account."""
        return (
            f"Account number {self._account_number} "
            f"owned by {self._owner} "
            f"with balance {self._balance}"
        )


class SavingsAccount(BankAccount):
    def __init__(
        self, account_number: int, owner: str, interest_rate: float = 0.001
    ) -> None:
        super().__init__(account_number, owner)
        self._interest_rate = interest_rate

    def accrue_monthly_interest(self) -> None:
        self._balance += self._interest_rate * self._balance


class CheckingAccount(BankAccount):
    def __init__(
        self,
        account_number: int,
        owner: str,
        overdraft_limit: float = 100,
        overdraft_fee: float = 10,
    ) -> None:
        super().__init__(account_number, owner)
        self.overdraft_limit = overdraft_limit
        self.overdraft_fee = overdraft_fee

    def withdraw(self, amount: float) -> None:
        if amount > self._balance + self.overdraft_limit:
            raise WouldOverdraw("Insufficient funds")
        self._balance -= amount
        if self._balance < 0:
            self._balance -= self.overdraft_fee


class PremierCheckingAccount(CheckingAccount):
    pass


def transfer(amount: float, from_account: BankAccount, to_account: BankAccount):
    from_account.withdraw(amount)
    to_account.deposit(amount)


def main():
    ca = CheckingAccount(100, "Fred")
    ca.deposit(150)

    sa = SavingsAccount(101, "Fred")

    transfer(200, ca, sa)

    print(f"{ca.balance=}, {sa.balance=}")


if __name__ == "__main__":
    main()
