class BankAccount:
    def __init__(self, account_number: int, owner: str) -> None:
        self.account_number = account_number
        self.owner = owner
        self._balance: float = 0

    def deposit(self, amount: float) -> None:
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        self._balance -= amount

    def get_balance(self) -> float:
        return self._balance

    def __str__(self) -> str:
        return (
            f"Account number {self.account_number} "
            f"owned by {self.owner} "
            f"with balance {self._balance}"
        )


def main() -> None:
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


if __name__ == "__main__":
    main()
