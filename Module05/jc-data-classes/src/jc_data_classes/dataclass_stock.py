"""
Stock class examples demonstrating dataclass decorator.
"""

from dataclasses import dataclass, field
from datetime import date
from pprint import pprint
from typing import Optional


@dataclass(frozen=True, order=True)
class Stock:
    """
    A class representing a publicly traded stock.

    The @dataclass decorator automatically generates:
    - __init__
    - __repr__
    - __eq__

    Note: frozen=False means instances are mutable (attributes can be changed).
    Set frozen=True to make instances immutable.

    When frozen=True:
    - Instances cannot be modified after creation
    - __hash__ is automatically generated
    - Attempting to modify attributes raises FrozenInstanceError
    """

    symbol: str = field(init=True, doc="The ticker for this stock")
    company_name: str
    exchange: str
    sector: str
    ipo_date: date
    industry: Optional[str] = field(default=None)
    alternative_names: list[str] = field(
        default_factory=list, compare=False, hash=False
    )


def main():
    apple = Stock(
        symbol="AAPL",
        company_name="Apple Inc.",
        exchange="NASDAQ",
        sector="Technology",
        ipo_date=date(1980, 12, 12),
        industry="Consumer Electronics",
        alternative_names=["Peaches", "Apricots"],
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

    print("\n" + ("*" * 80) + "\n")

    print(apple < microsoft)
    print(apple < apple2)
    print(apple <= apple2)

    lst = [apple, microsoft, apple2, apple, microsoft, microsoft]
    lst.sort()
    print(lst)


if __name__ == "__main__":
    main()
