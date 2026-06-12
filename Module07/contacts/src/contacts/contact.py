from dataclasses import dataclass
from typing import Optional


@dataclass()
class Contact:
    """A Contact"""

    name: str
    address: str
    email: str
    phone: str
    id: Optional[int] = None

    def __str__(self) -> str:
        return (
            f"contact name={self.name}, address={self.address}, "
            + f"email={self.email}, phone={self.phone}, "
            + f"id={self.id}"
        )


if __name__ == "__main__":
    c = Contact("Fred", "Bedrock", "fred@whatever.net", "555-1212")
    print(c)
