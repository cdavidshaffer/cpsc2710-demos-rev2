class Contact:
    def __init__(self, name, address, email, phone):
        self.name = name
        self.address = address
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"contact name={self.name}, address={self.address}, "+\
                f"email={self.email}, phone={self.phone}"

if __name__ == "__main__":
    c = Contact("Fred", "Bedrock", "fred@whatever.net", "555-1212")
    print(c)