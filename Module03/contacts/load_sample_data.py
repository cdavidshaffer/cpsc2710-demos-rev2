"""Insert sample contacts into the database. Run with: uv run python load_sample_data.py"""
import sys
sys.path.insert(0, "src")

from contacts.contact_db import ContactDB
from contacts.sample_data import get_samples

with ContactDB() as db:
    for contact in get_samples():
        db.save(contact)
        print(f"Inserted: {contact.name} (id={contact.id})")

print("Done.")
