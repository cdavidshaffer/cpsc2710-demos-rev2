"""Verification script. Run with: uv run python test_contact_db.py"""
import os, sys
sys.path.insert(0, "src")

from contacts.contact import Contact
from contacts.contact_db import ContactDB

DB = "test_contacts_verify.db"
if os.path.exists(DB): os.remove(DB)

with ContactDB(DB) as db:
    assert db.get_all() == []

    fred = Contact("Fred Flintstone", "301 Cobblestone Way", "fred@bedrock.com", "555-0101")
    db.save(fred)
    assert isinstance(fred.id, int), f"Expected int id, got {type(fred.id)}"

    wilma = Contact("Wilma Flintstone", "301 Cobblestone Way", "wilma@bedrock.com", "555-0102")
    db.save(wilma)
    assert wilma.id != fred.id

    assert len(db.get_all()) == 2

    fred.phone = "555-9999"
    db.update(fred)
    saved_fred = next(c for c in db.get_all() if c.id == fred.id)
    assert saved_fred.phone == "555-9999"

    db.delete(fred)
    assert fred.id is None
    assert len(db.get_all()) == 1

    orphan = Contact("Barney", "303 Cobblestone", "b@bedrock.com", "555-0201")
    try:
        db.update(orphan)
        assert False, "should raise ValueError"
    except ValueError:
        pass
    try:
        db.delete(orphan)
        assert False, "should raise ValueError"
    except ValueError:
        pass

os.remove(DB)
print("All checks passed.")
