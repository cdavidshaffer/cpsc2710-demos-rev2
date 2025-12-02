"""
Stock class examples demonstrating manual implementation (ie without dataclass)
"""

from datetime import date
from pprint import pprint
from typing import Optional


class Stock:
    """
    A class representing a publicly traded stock.
    """

    def __init__(
        self,
        symbol: str,
        company_name: str,
        exchange: str,
        sector: str,
        ipo_date: date,
        industry: Optional[str] = None,
    ):
        self.symbol = symbol
        self.company_name = company_name
        self.exchange = exchange
        self.sector = sector
        self.ipo_date = ipo_date
        self.industry = industry

    def __repr__(self) -> str:
        return (
            f"Stock("
            f"symbol={self.symbol!r}, "
            f"company_name={self.company_name!r}, "
            f"exchange={self.exchange!r}, "
            f"sector={self.sector!r}, "
            f"ipo_date={self.ipo_date!r}, "
            f"industry={self.industry!r})"
        )

    def __str__(self):
        return f"a stock with ticker {self.symbol}"

    def __eq__(self, other) -> bool:
        """
        Compare two Stock instances for equality.

        Two stocks are considered equal if all their attributes match.
        """
        if not isinstance(other, Stock):
            return NotImplemented

        return (
            self.symbol == other.symbol
            and self.company_name == other.company_name
            and self.exchange == other.exchange
            and self.sector == other.sector
            and self.ipo_date == other.ipo_date
            and self.industry == other.industry
        )

    def __hash__(self) -> int:
        """
        Return a hash of the Stock instance.

        This allows Stock instances to be used in sets and as dict keys.
        Note: In practice, you'd only implement __hash__ if the object
        is truly immutable, which we're simulating here.
        """
        return hash(
            (
                self.symbol,
                self.company_name,
                self.exchange,
                self.sector,
                self.ipo_date,
                self.industry,
            )
        )


def main():
    apple = Stock(
        symbol="AAPL",
        company_name="Apple Inc.",
        exchange="NASDAQ",
        sector="Technology",
        ipo_date=date(1980, 12, 12),
        industry="Consumer Electronics",
    )

    microsoft = Stock(
        symbol="MSFT",
        company_name="Microsoft Corporation",
        exchange="NASDAQ",
        sector="Technology",
        ipo_date=date(1986, 3, 13),
        industry="Software",
    )

    # Another Apple instance with same values
    apple2 = Stock(
        symbol="AAPL",
        company_name="Apple Inc.",
        exchange="NASDAQ",
        sector="Technology",
        ipo_date=date(1980, 12, 12),
        industry="Consumer Electronics",
    )

    print(repr(apple))
    print(str(apple))
    print(apple)

    print("\n" + ("*" * 80) + "\n")

    print(apple == microsoft)
    print(apple == apple)
    print(apple == apple2)

    print("\n" + ("*" * 80) + "\n")

    s = {apple, microsoft}
    pprint(s)
    apple.industry = None  # Bad!  May change hash code!
    pprint(s)


if __name__ == "__main__":
    main()
