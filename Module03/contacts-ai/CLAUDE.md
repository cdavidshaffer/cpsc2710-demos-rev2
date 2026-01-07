# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Human vs AI contributions

This project is part of a course assignment.  In this assignment the contributions of the human student (me) vs AI (you) are clearly delineated: The entire python source code for the contact user interface must be entirely written by me.  AI contributions can be solicited for the UI portion but only for small technical pieces of advice.  The AI agent should not modify any existing files except contact.py when needed.  The AI's contributions must be limited to the addition of database support to the application.  The AI agent may should also help the user, as needed, with database setup.

## Project Overview

This is a PySide6-based desktop application for managing contacts. It's a simple CRUD application with a split-pane interface: a list of contacts on the left and an editable form on the right.

## Technology Stack

- **Python**: 3.14+ (specified in pyproject.toml)
- **UI Framework**: PySide6 (Qt for Python)
- **Package Manager**: uv
- **Build System**: uv_build

## Running the Application

```bash
# Run the contacts UI directly
python src/contacts/contacts_ui
```

Note: The contacts_ui file is an executable Python script (not a .py extension), but it can be run directly.

## Development Setup

```bash
# Install dependencies
uv sync

# Activate virtual environment (if needed)
source .venv/bin/activate  # On Unix/macOS
```

## Code Architecture

### Core Data Model

- **Contact** (`src/contacts/contact.py`): Simple dataclass with fields: name, address, email, phone

### UI Architecture

- **MainWindow** (`src/contacts/contacts_ui`): The main application window using PySide6
  - Uses a `QSplitter` to create a two-pane layout
  - Left pane: `QListWidget` displaying contact names
  - Right pane: Form with `QLineEdit` and `QPlainTextEdit` for editing contact details

### Key UI Components

1. **Contact List** (`_create_list`):
   - Single selection mode
   - Stores Contact objects in `Qt.ItemDataRole.UserRole` for each list item
   - Selection changes trigger form updates via `_list_item_selection_changed`

2. **Contact Form** (`_create_form`):
   - Form fields: name (QLineEdit), address (QPlainTextEdit), phone (QLineEdit), email (QLineEdit)
   - Save button: Currently not implemented (marked TBD in `_save_button_clicked`)
   - Cancel button: Reverts form to show currently selected contact

### Data Flow

- Initial contact data is loaded from `sample_data.get_samples()` (Flintstones characters)
- When a list item is selected, the form is populated from the Contact object stored in the item's UserRole
- Form editing is functional, but the Save button has no implementation yet

## Code Style

- Uses Ruff for formatting and linting (configured in .vscode/settings.json)
- Format on save is enabled
- Auto-organize imports on save
- Docstring format: Sphinx style
