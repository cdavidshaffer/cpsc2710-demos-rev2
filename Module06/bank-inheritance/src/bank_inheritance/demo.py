from bank_inheritance.accounts import BankAccount, CheckingAccount, SavingsAccount


def show(account: BankAccount) -> None:
    print(account)


def main() -> None:
    ordinary = BankAccount(1001, "Alice", 100)
    savings = SavingsAccount(2001, "Bob", 1000, annual_interest_rate=0.06)
    checking = CheckingAccount(
        3001, "Charlie", 50, overdraft_limit=100, overdraft_fee=10
    )

    ordinary.withdraw(40)
    savings.withdraw(40)
    savings.monthly_update()
    checking.withdraw(75)

    accounts: list[BankAccount] = [ordinary, savings, checking]

    for account in accounts:
        show(account)


if __name__ == "__main__":
    main()
