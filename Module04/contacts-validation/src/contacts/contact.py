class Contact:
    """A Contact.

    Eventually this will be a dataclass!"""

    def __init__(self, name, address, email, phone, id=None):
        self.id = id
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone

    def __str__(self):
        return (
            f"contact name={self.name}, address={self.address}, "
            + f"email={self.email}, phone={self.phone}, "
            + f"id={self.id}"
        )


if __name__ == "__main__":
    c = Contact("Fred", "Bedrock", "fred@whatever.net", "555-1212")
    print(c)
