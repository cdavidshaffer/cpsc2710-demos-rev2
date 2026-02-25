# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Human vs AI contributions

This project is part of a course assignment.  The course focuses on UI development in Python + PySide6.  In this assignment the contributions of the human student (me) vs AI (you) are clearly delineated: The entire python source code for the contact user interface must be entirely written by me.  The AI agent should not modify any existing files except contact.py when needed.  The AI's contributions must be limited to the addition of database support to the application.  The AI agent may should also help the user, as needed, with database setup.  The AI agent should not provide suggestions for modifying the UI, particularly for integrating the database support into the UI.  This integration should be completely implemented by me.

## Project Overview

A Python/PySide6 contacts application being developed incrementally as a course demo for CPSC 2710. The `Contact` class in `src/contacts/contact.py` is planned to become a dataclass.

## Commands

This project uses `uv` for dependency and environment management (Python 3.14).

```bash
# Install dependencies / sync environment
uv sync

# Run the application
uv run contacts
# or
uv run python -m contacts.contacts_ui

# Run a specific module directly
uv run python src/contacts/contact.py
```

## Architecture

- **`src/contacts/contact.py`** — `Contact` data model (name, address, email, phone)
- **`src/contacts/contacts_ui.py`** — PySide6 GUI entry point (`main()` function); referenced in `pyproject.toml` but not yet created
- **`src/contacts/__init__.py`** — package init (currently empty)

Entry point declared in `pyproject.toml`: `contacts = "contacts.contacts_ui:main"`

The GUI layer (PySide6) is the only dependency beyond the stdlib.
