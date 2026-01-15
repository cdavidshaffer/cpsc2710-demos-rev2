from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contacts.contact import Contact
from contacts.db_models import Base, ContactModel


class ContactRepository:
    """Repository interface for managing contacts in SQLite database."""

    def __init__(self, db_path: str = "contacts.db"):
        """Initialize repository with database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.SessionLocal = sessionmaker(bind=self.engine)

    def init_db(self):
        """Initialize database schema."""
        Base.metadata.create_all(self.engine)

    def _to_model(self, contact: Contact) -> ContactModel:
        """Convert Contact dataclass to ContactModel."""
        model = ContactModel(
            name=contact.name,
            address=contact.address,
            email=contact.email,
            phone=contact.phone
        )
        if contact.id is not None:
            model.id = contact.id  # type: ignore
        return model

    def _from_model(self, model: ContactModel) -> Contact:
        """Convert ContactModel to Contact dataclass."""
        return Contact(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            address=model.address,  # type: ignore
            email=model.email,  # type: ignore
            phone=model.phone  # type: ignore
        )

    def create(self, contact: Contact) -> Contact:
        """Create a new contact in the database.

        Args:
            contact: Contact to create (id will be ignored if provided)

        Returns:
            Created contact with assigned id
        """
        with self.SessionLocal() as session:
            model = self._to_model(contact)
            model.id = None  # type: ignore  # Ensure auto-increment handles id
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._from_model(model)

    def get_all(self) -> list[Contact]:
        """Get all contacts from the database.

        Returns:
            List of all contacts
        """
        with self.SessionLocal() as session:
            models = session.query(ContactModel).all()
            return [self._from_model(model) for model in models]

    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        """Get a contact by id.

        Args:
            contact_id: ID of contact to retrieve

        Returns:
            Contact if found, None otherwise
        """
        with self.SessionLocal() as session:
            model = session.query(ContactModel).filter(ContactModel.id == contact_id).first()
            return self._from_model(model) if model else None

    def update(self, contact: Contact) -> Optional[Contact]:
        """Update an existing contact.

        Args:
            contact: Contact with updated data (must have valid id)

        Returns:
            Updated contact if found, None otherwise
        """
        if contact.id is None:
            raise ValueError("Contact must have an id to update")

        with self.SessionLocal() as session:
            model = session.query(ContactModel).filter(ContactModel.id == contact.id).first()
            if model is None:
                return None

            model.name = contact.name  # type: ignore
            model.address = contact.address  # type: ignore
            model.email = contact.email  # type: ignore
            model.phone = contact.phone  # type: ignore
            session.commit()
            session.refresh(model)
            return self._from_model(model)

    def save(self, contact: Contact) -> Contact:
        """Save a contact (create if new, update if existing).

        Args:
            contact: Contact to save

        Returns:
            Saved contact with id
        """
        if contact.id is None:
            return self.create(contact)
        else:
            result = self.update(contact)
            if result is None:
                raise ValueError(f"Contact with id {contact.id} not found")
            return result

    def delete(self, contact_id: int) -> bool:
        """Delete a contact by id.

        Args:
            contact_id: ID of contact to delete

        Returns:
            True if contact was deleted, False if not found
        """
        with self.SessionLocal() as session:
            model = session.query(ContactModel).filter(ContactModel.id == contact_id).first()
            if model is None:
                return False
            session.delete(model)
            session.commit()
            return True

    def seed_sample_data(self, contacts: list[Contact]):
        """Seed the database with sample data (only if database is empty).

        Args:
            contacts: List of contacts to seed
        """
        with self.SessionLocal() as session:
            count = session.query(ContactModel).count()
            if count == 0:
                for contact in contacts:
                    model = self._to_model(contact)
                    model.id = None  # type: ignore
                    session.add(model)
                session.commit()
