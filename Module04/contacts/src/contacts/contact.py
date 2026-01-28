from dataclasses import dataclass
from typing import Optional


@dataclass
class Contact:
    name: str
    address: str
    email: str
    phone: str
    id: Optional[int] = None
