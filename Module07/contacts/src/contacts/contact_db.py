"""SQLite persistence layer for the Contacts application (Peewee ORM)."""

from peewee import CharField, Model, SqliteDatabase

from contacts.contact import Contact

_db = SqliteDatabase(None)  # initialized later via ContactDB


class ContactRecord(Model):
    """Peewee model — defines the contacts table schema."""
    name = CharField()
    address = CharField(default="")
    email = CharField(default="")
    phone = CharField(default="")

    class Meta:
        database = _db
        table_name = "contacts"


class ContactDB:
    """Public persistence API. Translates between Contact and ContactRecord."""

    def __init__(self, db_path: str = "contacts.db"):
        _db.init(db_path)
        _db.connect()
        _db.create_tables([ContactRecord], safe=True)  # CREATE TABLE IF NOT EXISTS

    def close(self) -> None:
        if not _db.is_closed():
            _db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def save(self, contact: Contact) -> None:
        """INSERT a new contact; assigns generated id back to contact.id."""
        if contact.id is not None:
            raise ValueError("Contact already has an id; use update() instead.")
        record = ContactRecord.create(
            name=contact.name,
            address=contact.address,
            email=contact.email,
            phone=contact.phone,
        )
        contact.id = record.id

    def update(self, contact: Contact) -> None:
        """UPDATE an existing contact. Raises ValueError if contact.id is None."""
        if contact.id is None:
            raise ValueError("Cannot update a contact that has no id (not yet saved).")
        ContactRecord.update(
            name=contact.name,
            address=contact.address,
            email=contact.email,
            phone=contact.phone,
        ).where(ContactRecord.id == contact.id).execute()

    def delete(self, contact: Contact) -> None:
        """DELETE a contact by id; resets contact.id to None afterward."""
        if contact.id is None:
            raise ValueError("Cannot delete a contact that has no id (not yet saved).")
        ContactRecord.delete().where(ContactRecord.id == contact.id).execute()
        contact.id = None

    def get_all(self) -> list[Contact]:
        """Return all contacts ordered alphabetically by name."""
        return [
            Contact(
                name=r.name,
                address=r.address,
                email=r.email,
                phone=r.phone,
                id=r.id,
            )
            for r in ContactRecord.select().order_by(ContactRecord.name)
        ]
