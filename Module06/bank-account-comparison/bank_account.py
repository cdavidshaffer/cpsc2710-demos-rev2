class BankAccount:
    def __init__(self, account_number: int, owner: str):
        self.__account_number = account_number
        self._owner = owner
        self._balance: float = 0

    @property
    def account_number(self) -> int:
        return self.__account_number

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, owner: str) -> None:
        if not isinstance(owner, str) or len(owner) < 3:
            raise ValueError("Owner must be a string with a minimum length of 3")
        self._owner = owner

    @property
    def balance(self):
        return self._balance

    def get_balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        self._balance -= amount

    def __str__(self) -> str:
        return (
            f"Account number {self.__account_number} "
            f"owned by {self._owner} "
            f"with balance {self._balance}"
        )
