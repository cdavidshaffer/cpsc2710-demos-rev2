from .bank_account import BankAccount


def main() -> None:
    account = BankAccount(123456, "Fred")
    print(account)
    print(account.owner)
    account.owner = "Betty"
    print(account)
    # account.owner = "f"
    # account.owner = None
    print(account)
    print(account.balance)

    barneys_account = BankAccount(1231212, "Barney")
    barneys_account.deposit(100)
    barneys_account.withdraw(71)


if __name__ == "__main__":
    main()
