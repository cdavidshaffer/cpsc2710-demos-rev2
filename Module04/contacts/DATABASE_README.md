# Contacts Database Support

This document describes the SQLite database support added to the contacts application.

## Overview

The database layer provides a repository-style interface for persisting contacts to a SQLite database. The implementation uses SQLAlchemy ORM for database operations.

## Components

### 1. Database Model (`src/contacts/db_models.py`)
- `ContactModel`: SQLAlchemy model representing the contacts table
- Fields: id (primary key), name, address, email, phone

### 2. Repository (`src/contacts/repository.py`)
- `ContactRepository`: Main interface for database operations
- Provides CRUD operations:
  - `create(contact)`: Create a new contact
  - `get_all()`: Retrieve all contacts
  - `get_by_id(id)`: Retrieve a specific contact
  - `update(contact)`: Update an existing contact
  - `save(contact)`: Save contact (automatically creates or updates based on id)
  - `delete(id)`: Delete a contact
  - `seed_sample_data(contacts)`: Populate database with initial data

### 3. Database Setup (`src/contacts/db_setup.py`)
- `initialize_database()`: Convenience function to initialize the database
- Can be run as a script to set up the database with sample data

### 4. Contact Model Updates (`src/contacts/contact.py`)
- Added optional `id` field to support database persistence

## Usage

### Initialize the Database

```python
from contacts.db_setup import initialize_database

# Initialize with default path (contacts.db) and seed with sample data
repo = initialize_database()
```

Or run directly:
```bash
python -m contacts.db_setup
```

### Basic Operations

```python
from contacts.repository import ContactRepository
from contacts.contact import Contact

# Create repository instance
repo = ContactRepository("contacts.db")

# Get all contacts
contacts = repo.get_all()

# Create a new contact
new_contact = Contact(
    name="John Doe",
    address="123 Main St",
    email="john@example.com",
    phone="555-1234"
)
created = repo.create(new_contact)
print(f"Created contact with id: {created.id}")

# Update a contact
created.email = "john.doe@example.com"
repo.update(created)

# Or use save (automatically creates or updates)
contact = Contact(name="Jane Doe", address="456 Oak Ave",
                 email="jane@example.com", phone="555-5678")
saved = repo.save(contact)  # Creates new contact

saved.phone = "555-0000"
repo.save(saved)  # Updates existing contact

# Delete a contact
repo.delete(created.id)
```

### Integration with UI

To integrate the database with the existing UI (`contacts_ui`), you would need to:

1. Replace the `sample_data.get_samples()` call with repository initialization:
```python
from contacts.db_setup import initialize_database

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Instead of: self._contacts = sample_data.get_samples()
        self.repo = initialize_database()
        self._contacts = self.repo.get_all()
        # ... rest of initialization
```

2. Implement the `_save_button_clicked` method to persist changes:
```python
def _save_button_clicked(self):
    # Get current selection
    selection = self._list.selectedItems()
    if len(selection) == 0:
        return

    # Get the contact from the selected item
    item = selection[0]
    contact = item.data(Qt.ItemDataRole.UserRole)

    # Update contact with form values
    contact.name = self._name_edit.text()
    contact.address = self._address_edit.toPlainText()
    contact.phone = self._phone_edit.text()
    contact.email = self._email_edit.text()

    # Save to database (automatically creates or updates)
    saved = self.repo.save(contact)

    # Update the contact reference and list item display
    item.setData(Qt.ItemDataRole.UserRole, saved)
    item.setText(saved.name)
```

## Database File

By default, the database file is named `contacts.db` and is created in the current working directory. You can specify a different path when creating the repository:

```python
repo = ContactRepository("path/to/my/database.db")
```

## Dependencies

- SQLAlchemy 2.0.44 (installed via `uv add sqlalchemy`)

## Notes

- The database is automatically created if it doesn't exist
- Sample data (Flintstones characters) is seeded only if the database is empty
- All database operations use context managers for proper connection handling
- The Contact dataclass maintains backward compatibility with the existing UI code
