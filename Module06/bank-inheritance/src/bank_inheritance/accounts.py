class WouldOverdraw(Exception):
    """Raised when a withdrawal would take an account past its allowed balance."""


class BankAccount:
    """A simple bank account with shared deposit and withdrawal behavior."""

    def __init__(self, account_number: int, owner: str, opening_balance: float = 0):
        self.account_number = account_number
        self.owner = owner
        self._balance = 0.0
        if opening_balance:
            self.deposit(opening_balance)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._validate_positive(amount)
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        self._validate_positive(amount)
        if amount > self._balance:
            raise WouldOverdraw("Insufficient funds")
        self._balance -= amount

    def get_balance(self) -> float:
        return self._balance

    def monthly_update(self) -> None:
        """Hook for account types that do month-end processing."""

    @staticmethod
    def _validate_positive(amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")

    def __str__(self) -> str:
        return (
            f"{type(self).__name__} {self.account_number} "
            f"owned by {self.owner} "
            f"with balance ${self._balance:,.2f}"
        )


class SavingsAccount(BankAccount):
    """A bank account that earns monthly interest."""

    def __init__(
        self,
        account_number: int,
        owner: str,
        opening_balance: float = 0,
        annual_interest_rate: float = 0.03,
    ):
        super().__init__(account_number, owner, opening_balance)
        self.annual_interest_rate = annual_interest_rate

    def monthly_update(self) -> None:
        monthly_rate = self.annual_interest_rate / 12
        interest = self.balance * monthly_rate
        if interest > 0:
            self.deposit(interest)


class CheckingAccount(BankAccount):
    """A bank account that allows limited overdraft with a fee."""

    def __init__(
        self,
        account_number: int,
        owner: str,
        opening_balance: float = 0,
        overdraft_limit: float = 100,
        overdraft_fee: float = 25,
    ):
        super().__init__(account_number, owner, opening_balance)
        self.overdraft_limit = overdraft_limit
        self.overdraft_fee = overdraft_fee

    def withdraw(self, amount: float) -> None:
        self._validate_positive(amount)
        will_overdraw = amount > self.balance
        total_charge = amount + self.overdraft_fee if will_overdraw else amount

        if self.balance - total_charge < -self.overdraft_limit:
            raise WouldOverdraw("Overdraft limit exceeded")

        if amount <= self.balance:
            super().withdraw(amount)
        else:
            self._balance -= amount
            self._balance -= self.overdraft_fee
