from contacts.contact import Contact


def get_samples():
    """Return a list of sample Contact objects based on Flintstones characters."""
    return [
        Contact(
            name="Fred Flintstone",
            address="301 Cobblestone Way, Bedrock",
            email="fred.flintstone@bedrock.com",
            phone="555-0101"
        ),
        Contact(
            name="Wilma Flintstone",
            address="301 Cobblestone Way, Bedrock",
            email="wilma.flintstone@bedrock.com",
            phone="555-0102"
        ),
        Contact(
            name="Barney Rubble",
            address="303 Cobblestone Way, Bedrock",
            email="barney.rubble@bedrock.com",
            phone="555-0201"
        ),
        Contact(
            name="Betty Rubble",
            address="303 Cobblestone Way, Bedrock",
            email="betty.rubble@bedrock.com",
            phone="555-0202"
        ),
        Contact(
            name="Pebbles Flintstone",
            address="301 Cobblestone Way, Bedrock",
            email="pebbles.flintstone@bedrock.com",
            phone="555-0103"
        ),
        Contact(
            name="Bamm-Bamm Rubble",
            address="303 Cobblestone Way, Bedrock",
            email="bammbamm.rubble@bedrock.com",
            phone="555-0203"
        ),
    ]
