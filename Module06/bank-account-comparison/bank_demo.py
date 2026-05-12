from bank_account import BankAccount


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
    account.account_number = 99


if __name__ == "__main__":
    main()
