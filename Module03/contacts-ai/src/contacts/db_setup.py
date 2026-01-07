"""Database setup and initialization utilities."""

from contacts.repository import ContactRepository
from contacts import sample_data


def initialize_database(db_path: str = "contacts.db", seed_data: bool = True) -> ContactRepository:
    """Initialize the contacts database.

    Args:
        db_path: Path to SQLite database file
        seed_data: Whether to seed with sample data if database is empty

    Returns:
        Initialized ContactRepository instance
    """
    repo = ContactRepository(db_path)
    repo.init_db()

    if seed_data:
        repo.seed_sample_data(sample_data.get_samples())

    return repo


if __name__ == "__main__":
    print("Initializing contacts database...")
    repo = initialize_database()
    contacts = repo.get_all()
    print(f"Database initialized with {len(contacts)} contacts")
    for contact in contacts:
        print(f"  - {contact.name}")
