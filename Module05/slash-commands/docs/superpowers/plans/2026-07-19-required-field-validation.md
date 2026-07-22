# Required-Field Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Title and Assigned To required (non-blank) fields on the issue form, with live red-border feedback and Save-button gating, while demonstrating the Qt resource system by compiling the feedback's QSS into the app through a `.qrc` bundle.

**Architecture:** A custom `QValidator` subclass (`NonBlankValidator`) is attached to both `QLineEdit`s. A shared `_update_validation_state()` method reads `hasAcceptableInput()` from both fields, toggles a dynamic `invalid` property that a resource-bundled QSS stylesheet turns into a red border, and gates the Save button — all only while a row is selected.

**Tech Stack:** PySide6 6.11 (Qt for Python), `pyside6-rcc` (the Qt resource compiler) invoked by hand. No test framework exists in this project — verification is manual: ad hoc `python -c` checks for pure logic, and running the app for UI behavior.

## Global Constraints

- This project is **not a git repository** (`git rev-parse --is-inside-work-tree` fails here). Tasks end at a verification step, not a commit — there is nothing to commit to. If a commit step doesn't apply, skip it.
- `requires-python = ">=3.14"`, `pyside6>=6.11.0` (from `pyproject.toml`). Use `.venv/bin/python` and `.venv/bin/pyside6-rcc` for every command below — the project's venv already has `issue_tracker` and `ui` importable as packages (src layout, `ui` is an implicit namespace package with no `__init__.py`).
- Validation only applies while a row is selected; an inactive/cleared form never shows invalid styling and never blocks Save.
- Out of scope: database work, changes to `status_combo`/`priority_combo`, changes to `main()`, app-wide (`QApplication`-level) styling.
- The compiled resource path for the QSS file is `:/styles/qss/validation.qss` (prefix `/styles` + the file's relative path `qss/validation.qss` inside the `.qrc` — Qt does **not** flatten this). Using the wrong path doesn't raise a clean error: `QFile.exists()` silently returns `False`, and reading an unopened/nonexistent resource through `QTextStream` segfaults the interpreter on this PySide6/Python combination. Verified directly — see Task 2.
- On this PySide6 6.11 / Python 3.14 combination, `QTextStream(file).readAll()` **chained as a single expression** (an unbound temporary) reproducibly segfaults the interpreter — confirmed by direct testing, 3/3 runs. Binding it to a variable first (`stream = QTextStream(file); stream.readAll()`) works every time. Likely a shiboken reference-lifetime issue with anonymous temporaries. `_setup_style()` in Task 3 already uses the safe bound-variable form — do not "simplify" it back to a chained call.
- When scripting UI verification with `QTest`/`QT_QPA_PLATFORM=offscreen`, use real focus transfer to another widget (`other_widget.setFocus()`) to simulate blur, not `widget.clearFocus()` — `clearFocus()` under the offscreen platform does not reliably deliver a real focus-out event, so validator `fixup()` never fires and any "trims on blur" check will falsely fail. Confirmed by direct testing: `clearFocus()` never triggered `fixup()` under offscreen; transferring focus to a sibling widget did, both under offscreen and in a real window.

---

### Task 1: NonBlankValidator

**Files:**
- Create: `src/issue_tracker/validators.py`

**Interfaces:**
- Produces: `NonBlankValidator`, a `QValidator` subclass with a no-arg constructor, importable as `from issue_tracker.validators import NonBlankValidator`. `.validate(text: str, pos: int)` returns `(QValidator.State, str, int)`; `.fixup(text: str) -> str`. Task 3 imports this class and calls `NonBlankValidator()` once, then `.setValidator()` on two `QLineEdit`s.

- [ ] **Step 1: Create `src/issue_tracker/validators.py`**

```python
from PySide6.QtGui import QValidator


class NonBlankValidator(QValidator):
    def validate(self, text, pos):
        stripped = text.strip()
        state = (
            QValidator.State.Acceptable
            if stripped and text == stripped
            else QValidator.State.Intermediate
        )
        return state, text, pos

    def fixup(self, text):
        return text.strip()
```

`Acceptable` requires the text to be non-blank **and** already free of leading/trailing whitespace — not just non-blank. This is what makes `fixup()` do real work: a padded string like `"  Bob  "` is `Intermediate` (not yet acceptable), and `fixup()` strips it to `"Bob"`, which validates as `Acceptable` — so Qt actually applies the fixed-up text. (An earlier version of this validator accepted any non-blank string regardless of padding, which meant `fixup()` could never turn a non-acceptable string into an acceptable one — Qt calls `fixup()` but discards results that still don't validate — so it never fired or never stuck. Confirmed by direct testing before settling on this version.) A momentary `Intermediate` state right after typing a trailing space (e.g. mid-typing "Bob Jones") is expected and self-corrects on the next keystroke.

- [ ] **Step 2: Verify the validator's logic**

Run:

```bash
.venv/bin/python -c "
from issue_tracker.validators import NonBlankValidator

v = NonBlankValidator()
assert v.validate('   ', 3)[0].name == 'Intermediate'
assert v.validate('', 0)[0].name == 'Intermediate'
assert v.validate('hello', 5)[0].name == 'Acceptable'
assert v.validate('  hello  ', 5)[0].name == 'Intermediate'
assert v.validate('hello world', 5)[0].name == 'Acceptable'
assert v.fixup('  hi  ') == 'hi'
assert v.fixup('   ') == ''
print('OK')
"
```

Expected output: `OK`

---

### Task 2: QSS resource bundle

**Files:**
- Create: `resources/qss/validation.qss`
- Create: `resources/resources.qrc`
- Create: `src/ui/resources_rc.py` (generated by `pyside6-rcc`, committed like `src/ui/main_window.py`)

**Interfaces:**
- Produces: the Qt resource path `:/styles/qss/validation.qss`, available anywhere in the app once `src/ui/resources_rc.py` has been imported (importing it runs `qInitResources()` at module scope). Task 3 imports this module for that side effect and reads the path via `QFile`/`QTextStream`.

- [ ] **Step 1: Create `resources/qss/validation.qss`**

```css
QLineEdit[invalid="true"] {
    border: 1px solid red;
    background-color: #fff0f0;
}
```

- [ ] **Step 2: Create `resources/resources.qrc`**

```xml
<RCC>
  <qresource prefix="/styles">
    <file>qss/validation.qss</file>
  </qresource>
</RCC>
```

- [ ] **Step 3: Compile the resource bundle**

Run:

```bash
.venv/bin/pyside6-rcc resources/resources.qrc -o src/ui/resources_rc.py
```

Expected: command exits with no output, and `src/ui/resources_rc.py` is created (starts with `# Resource object code (Python 3)` and ends with a call to `qInitResources()`).

- [ ] **Step 4: Verify the resource is readable at the expected path**

Run (from the project root, so `src/ui` is on the import path):

```bash
.venv/bin/python -c "
from ui import resources_rc
from PySide6.QtCore import QFile, QIODevice, QTextStream

assert QFile.exists(':/styles/qss/validation.qss'), 'resource not registered at expected path'
f = QFile(':/styles/qss/validation.qss')
assert f.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
stream = QTextStream(f)
content = stream.readAll()
f.close()
assert 'invalid=\"true\"' in content
print(content)
"
```

Expected output: the CSS content from Step 1 printed back, no errors.

> Notes:
> - Do **not** test with `:/styles/validation.qss` (missing the `qss/` segment) — see the Global Constraints warning above about the silent-failure/segfault behavior of that wrong path.
> - Do **not** chain `QTextStream(f).readAll()` as a single expression — bind `QTextStream(f)` to a variable first. The chained/unbound-temporary form reproducibly segfaults on this PySide6/Python combination; see Global Constraints.

---

### Task 3: Wire validation into the form

**Files:**
- Modify: `src/issue_tracker/issues_table_window.py`

**Interfaces:**
- Consumes: `NonBlankValidator` from Task 1 (`from issue_tracker.validators import NonBlankValidator`); the `resources_rc` module and `:/styles/qss/validation.qss` path from Task 2.
- Produces: `IssuesTableWindow._update_validation_state()` and `IssuesTableWindow._set_invalid(widget, invalid)` — no other task depends on these, they close out the feature.

- [ ] **Step 1: Update the imports at the top of `src/issue_tracker/issues_table_window.py`**

Find:

```python
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from issue_tracker.issue import Issue, Priority, Status
from issue_tracker.sample_issues import get_samples
from ui.main_window import Ui_MainWindow
```

Replace with:

```python
import sys

from PySide6.QtCore import QFile, QIODevice, QTextStream, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

from issue_tracker.issue import Issue, Priority, Status
from issue_tracker.sample_issues import get_samples
from issue_tracker.validators import NonBlankValidator
from ui import resources_rc  # noqa: F401
from ui.main_window import Ui_MainWindow
```

- [ ] **Step 2: Call the two new setup methods from `__init__`**

Find:

```python
        self.setupUi(self)
        self._setup_combo_boxes()
        self._setup_issues_table()
        self._connect_widgets()
```

Replace with:

```python
        self.setupUi(self)
        self._setup_combo_boxes()
        self._setup_issues_table()
        self._setup_validation()
        self._setup_style()
        self._connect_widgets()
```

- [ ] **Step 3: Add `_setup_validation()` and `_setup_style()`**

Find:

```python
    def _setup_issues_table(self):
        self._update_issues_table()
```

Replace with:

```python
    def _setup_issues_table(self):
        self._update_issues_table()

    def _setup_validation(self):
        validator = NonBlankValidator()
        self.title_edit.setValidator(validator)
        self.assigned_to_edit.setValidator(validator)
        self.title_edit.textChanged.connect(self._update_validation_state)
        self.assigned_to_edit.textChanged.connect(self._update_validation_state)

    def _setup_style(self):
        style_file = QFile(":/styles/qss/validation.qss")
        style_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text)
        stream = QTextStream(style_file)
        self.setStyleSheet(stream.readAll())
        style_file.close()
```

- [ ] **Step 4: Call `_update_validation_state()` from `_clear_form()` and `_show_issue()`, and add the two new methods**

Find:

```python
    def _clear_form(self):
        self.title_edit.clear()
        self.status_combo.setCurrentIndex(-1)
        self.priority_combo.setCurrentIndex(-1)
        self.notes_plain_text.clear()
        self.assigned_to_edit.clear()

    def _show_issue(self, issue):
        self.title_edit.setText(issue.title)
        self.status_combo.setCurrentIndex(self.status_combo.findData(issue.status))
        self.priority_combo.setCurrentIndex(
            self.priority_combo.findData(issue.priority)
        )
        self.notes_plain_text.setPlainText(issue.notes)
        self.assigned_to_edit.setText(issue.assigned_to)
```

Replace with:

```python
    def _clear_form(self):
        self.title_edit.clear()
        self.status_combo.setCurrentIndex(-1)
        self.priority_combo.setCurrentIndex(-1)
        self.notes_plain_text.clear()
        self.assigned_to_edit.clear()
        self._update_validation_state()

    def _show_issue(self, issue):
        self.title_edit.setText(issue.title)
        self.status_combo.setCurrentIndex(self.status_combo.findData(issue.status))
        self.priority_combo.setCurrentIndex(
            self.priority_combo.findData(issue.priority)
        )
        self.notes_plain_text.setPlainText(issue.notes)
        self.assigned_to_edit.setText(issue.assigned_to)
        self._update_validation_state()

    def _update_validation_state(self):
        has_selection = self._get_selected_issue() is not None
        title_ok = self.title_edit.hasAcceptableInput()
        assigned_ok = self.assigned_to_edit.hasAcceptableInput()
        self._set_invalid(self.title_edit, has_selection and not title_ok)
        self._set_invalid(self.assigned_to_edit, has_selection and not assigned_ok)
        self.save_button.setEnabled(not has_selection or (title_ok and assigned_ok))

    def _set_invalid(self, widget, invalid):
        widget.setProperty("invalid", invalid)
        widget.style().unpolish(widget)
        widget.style().polish(widget)
```

- [ ] **Step 5: Verify the module imports cleanly**

Run:

```bash
.venv/bin/python -c "from issue_tracker.issues_table_window import IssuesTableWindow; print('OK')"
```

Expected output: `OK` (no `ImportError`, no segfault).

- [ ] **Step 6: Manually verify the full feature by running the app**

Run:

```bash
.venv/bin/issue-tracker
```

Walk through each of these and confirm the observed behavior:

1. Select any sample issue (e.g. "Login page crashes on empty password"). Title and Assigned To show no red border; Save is enabled.
2. Clear the Title field entirely. Title's border turns red; Save becomes disabled.
3. Type any non-whitespace character into Title. The red border clears; Save re-enables.
4. Clear Assigned To on a selected issue. Its border turns red and Save disables, independent of Title's state.
5. Type only spaces into Assigned To, then click elsewhere (or Tab out). It stays invalid (still red, Save still disabled) — `fixup()` runs and reduces it to `""`, but Qt only applies a `fixup()` result when it actually becomes `Acceptable`, and an empty string never is, so the visible text is left as the spaces you typed. It should not become "acceptable" just because it briefly contained space characters.
6. Type "  Bob  " (with surrounding spaces) into Assigned To, then click elsewhere. The field's text is trimmed to "Bob" (visible in the field) and the border clears.
7. Click "New". A new row is added and selected; Assigned To is empty (`assigned_to=None` renders as `''`), so its border is red and Save is disabled until you type an assignee.
8. With a row selected and made invalid (per step 2), click "Cancel". The form reloads the selected issue's saved values (not the invalid edits) and the red border clears, since the reloaded values are the original valid ones.
9. Click on the selected row's own row again to deselect it (or otherwise clear the table selection so nothing is selected). Confirm no field shows a red border regardless of contents, and clicking Save does nothing (matches today's behavior).
10. Close the app (Cmd+Q or window close) — no crash on exit.

If any of these diverge from the description, stop and report exactly which step and what was observed instead.

---

## Post-plan note

No commit step is included anywhere in this plan because the project directory is not a git repository (confirmed in Global Constraints). If you want these changes under version control, that's a separate decision — ask before running `git init`, since creating a new repository here is a choice for you to make, not an implied part of this feature.
