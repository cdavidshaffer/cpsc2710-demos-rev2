# Contacts Database

SQLite persistence layer for the Contacts application, implemented using the [Peewee ORM](https://docs.peewee-orm.com/).

---

## Overview

The database layer lives in `src/contacts/contact_db.py` and provides two classes:

| Class | Role |
|---|---|
| `ContactRecord` | Peewee model; owns the table schema |
| `ContactDB` | Public API; translates between `Contact` and `ContactRecord` |

The `Contact` class (domain model) and the `ContactRecord` class (persistence model) are kept separate. `ContactDB` is the only bridge between them.

---

## Database Schema

**File:** `contacts.db` (SQLite, created automatically on first use)

**Table:** `contacts`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, auto-incremented by SQLite |
| `name` | TEXT | Required |
| `address` | TEXT | Defaults to `""` |
| `email` | TEXT | Defaults to `""` |
| `phone` | TEXT | Defaults to `""` |

---

## Contact ID Lifecycle

The `Contact` domain object gains database awareness through its `id` field:

- **`id = None`** — contact exists only in memory; not yet saved
- **`id = <integer>`** — contact has a corresponding row in the database

`ContactDB.save()` mutates `contact.id` in place after INSERT so the caller's reference immediately reflects the assigned id. `ContactDB.delete()` resets `contact.id` back to `None` after DELETE.

---

## API Reference

### `ContactDB(db_path="contacts.db")`

Opens (or creates) the SQLite database at `db_path`, connects, and creates the `contacts` table if it does not already exist.

Supports use as a context manager:

```python
with ContactDB() as db:
    ...
# connection closed automatically
```

---

### `db.save(contact)`

Inserts a new contact and assigns the generated id back to `contact.id`.

```python
c = Contact("Fred Flintstone", "301 Cobblestone Way", "fred@bedrock.com", "555-0101")
db.save(c)
print(c.id)  # e.g. 1
```

Raises `ValueError` if `contact.id` is already set (use `update()` instead).

---

### `db.update(contact)`

Updates the database row for an existing contact.

```python
c.phone = "555-9999"
db.update(c)
```

Raises `ValueError` if `contact.id` is `None`.

---

### `db.delete(contact)`

Deletes the database row and resets `contact.id` to `None`.

```python
db.delete(c)
print(c.id)  # None
```

Raises `ValueError` if `contact.id` is `None`.

---

### `db.get_all() -> list[Contact]`

Returns all contacts as a list of `Contact` objects, ordered alphabetically by name.

```python
contacts = db.get_all()
for c in contacts:
    print(c.name, c.id)
```

---

### `db.close()`

Closes the database connection. Called automatically when using the context manager.

---

## Usage Examples

### Load all contacts on startup

```python
from contacts.contact_db import ContactDB

db = ContactDB()
contacts = db.get_all()
```

### Add a new contact

```python
from contacts.contact import Contact

c = Contact("Barney Rubble", "303 Cobblestone Way", "barney@bedrock.com", "555-0201")
db.save(c)
# c.id is now set
```

### Edit an existing contact

```python
c.phone = "555-1234"
db.update(c)
```

### Delete a contact

```python
db.delete(c)
# c.id is now None
```

---

## Utilities

### `load_sample_data.py`

Inserts the six sample Flintstones contacts from `sample_data.py` into the database.

```bash
uv run python load_sample_data.py
```

### `test_contact_db.py`

Runs a self-contained verification suite against a temporary database (deleted on completion).

```bash
uv run python test_contact_db.py
# Expected output: All checks passed.
```

---

## File Locations

| Path | Description |
|---|---|
| `src/contacts/contact.py` | `Contact` domain model |
| `src/contacts/contact_db.py` | `ContactRecord` and `ContactDB` |
| `src/contacts/sample_data.py` | Sample contact data |
| `contacts.db` | SQLite database file (runtime, not checked in) |
| `load_sample_data.py` | Utility to seed the database |
| `test_contact_db.py` | Verification script |
