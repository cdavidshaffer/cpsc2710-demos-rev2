def format_interest_statement(amount: float, interest_rate: float) -> str:
    balance = (1 + interest_rate) * amount
    return f"Total balance after interest earned on {amount} at {interest_rate} is {balance}"


def main() -> None:
    from datetime import date

    print(format_interest_statement(1000, 0.05))
    print(format_interest_statement(2500.75, 0.035))
    print(format_interest_statement("42", date.today()))  # note IDE errors


if __name__ == "__main__":
    main()
