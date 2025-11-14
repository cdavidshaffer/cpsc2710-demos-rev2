type number = int | float


class BankAccount:
    def __init__(self, account_number: int, owner: str):
        self.account_number: int = account_number
        self.owner: str = owner
        self._balance: number = 0

    def deposit(self, amount: number) -> None:
        self._balance += amount

    def withdraw(self, amount: number) -> None:
        self._balance -= amount

    def get_balance(self) -> number:
        return self._balance

    def _set_balance(self, bal: number) -> None:
        self._balance = bal

    def __str__(self) -> str:
        return (
            f"Account number {self.account_number} "
            f"owned by {self.owner} "
            f"with balance {self._balance}"
        )
