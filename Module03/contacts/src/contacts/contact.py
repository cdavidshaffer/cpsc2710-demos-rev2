from dataclasses import dataclass


@dataclass
class Contact:
    name: str
    address: str
    email: str
    phone: str
