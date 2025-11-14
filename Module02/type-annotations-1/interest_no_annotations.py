def format_interest_statement(amount, interest_rate):
    balance = (1 + interest_rate) * amount
    return f"Total balance after interest earned on {amount} at {interest_rate} is {balance}"


class Monkey:
    def __radd__(self, other):
        return 5


def main():
    from datetime import date

    print(format_interest_statement(1000, 0.05))
    print(format_interest_statement(2500.75, 0.035))
    # print(format_interest_statement("42", date.today()))  # notice IDE gives no errors but fails at runtime
    print(
        format_interest_statement("42", Monkey())
    )  # no IDE errors, works at runtime if Monkey has __radd__


if __name__ == "__main__":
    main()
