# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

`issue-tracker` is a small PySide6 (Qt for Python) desktop application: a single-window issue tracker with an in-memory list of issues shown in a table, plus a detail form for editing the selected issue. It is course demo/example code (CPSC2710), not a production app — there is no persistence layer and no test suite.

## Commands

Dependency management and running are done via `uv` (see `uv.lock`, `pyproject.toml`).

- Install/sync dependencies: `uv sync`
- Run the app: `uv run issue-tracker` (entry point defined in `pyproject.toml` as `issue_tracker.issues_table_window:main`), or `uv run python -m issue_tracker.issues_table_window`
- Regenerate `src/ui/main_window.py` from the Qt Designer file after editing `resources/ui/main_window.ui`:
  `uv run pyside6-uic resources/ui/main_window.ui -o src/ui/main_window.py`

There are no lint/test/type-check scripts configured in this repo (no pytest, no ruff/mypy config files); `ruff` runs only as the VS Code formatter, and `.mypy_cache/` reflects ad hoc editor use of mypy, not a project-wide check.

## Architecture

The `src/` layout contains two separate top-level packages, both put on `sys.path` by the editable install:

- `issue_tracker/` — hand-written application code: the domain model and window logic.
- `ui/` — Qt Designer-generated code only. `main_window.py` is compiled from `resources/ui/main_window.ui` via `pyside6-uic` and carries a "changes will be lost when recompiling" warning in the file header — never hand-edit it; edit the `.ui` file in Qt Designer and regenerate instead.

Within `issue_tracker/`:

- `issue.py` — the domain model: `Issue` (plain data holder: title, status, priority, assigned_to, notes) and the `Status`/`Priority` enums. No validation, no business logic.
- `sample_issues.py` — `get_samples()` returns a hardcoded list of `Issue` objects used to seed the UI. This stands in for a real data source; there is no database or file persistence anywhere in the app, so all edits are lost on exit.
- `issues_table_window.py` — `IssuesTableWindow(QMainWindow, Ui_MainWindow)` is the main window. It inherits from the generated `Ui_MainWindow` (the standard PySide6/Designer pattern: `setupUi(self)` populates widgets as attributes directly on `self`, e.g. `self.issues_table`, `self.save_button`), and adds all interactive behavior — combo box population, table population, signal/slot wiring in `_connect_widgets`, and syncing the detail form to/from the selected `Issue`.

Key implementation detail: the table only has 4 visible columns (title, status, priority, assigned_to); the underlying `Issue` object for a row is stashed on the title cell via `Qt.ItemDataRole.UserRole` (see `_issue_to_table_widget_items` / `_get_selected_issue`) rather than looked up by row index, since row order and the `_issues` list order aren't assumed to stay in sync.
