# Required-Field Validation Design

## Purpose

The issue form currently accepts a blank Title and blank Assigned To with no
feedback — an issue can be saved with either field empty. This adds real
validation for those two fields, using the opportunity to also demonstrate
the Qt resource system: the QSS used for the invalid-field styling is
compiled into the app via a `.qrc` resource bundle rather than loaded as a
loose file.

Database persistence is explicitly out of scope for this feature (planned
for a later module).

## Scope

- `title_edit` and `assigned_to_edit` become required (non-blank) fields.
- Validation only applies while a row is selected (i.e. the form is
  "active"). An empty, inactive form (nothing selected) never shows invalid
  styling and never blocks Save — this matches today's behavior where Save
  is a no-op with no selection.
- `save_button` is disabled live whenever a row is selected and either
  required field is not currently acceptable; it re-enables the instant both
  fields become acceptable.
- No changes to `status_combo` / `priority_combo` validation — they're
  already constrained to enum values by construction.
- Creating a new issue (`new_issue_button`) defaults `assigned_to=None`,
  which renders as an empty string in the field. This means Save will be
  disabled immediately after clicking "New" until an assignee is typed in —
  intentional, not a bug to work around.

## Validator

New module `src/issue_tracker/validators.py`:

```python
class NonBlankValidator(QValidator):
    def validate(self, text, pos):
        state = QValidator.State.Acceptable if text.strip() else QValidator.State.Intermediate
        return state, text, pos

    def fixup(self, text):
        return text.strip()
```

- `Acceptable` when the field has at least one non-whitespace character,
  otherwise `Intermediate` (never `Invalid` — the field is always
  completable by typing more).
- `fixup()` trims leading/trailing whitespace; Qt calls this automatically
  when the field loses focus while not `Acceptable` but a validator is
  attached.

One shared `NonBlankValidator` instance is created and attached to both
`title_edit` and `assigned_to_edit` (validators are stateless, so sharing is
safe).

## Form wiring (`issues_table_window.py`)

- `_setup_validation()` (new, called from `__init__` alongside the other
  `_setup_*` calls): creates the shared validator, calls `setValidator()` on
  both fields, and connects both fields' `textChanged` to
  `_update_validation_state`.
- `_update_validation_state(self)` (new):
  ```python
  has_selection = self._get_selected_issue() is not None
  title_ok = self.title_edit.hasAcceptableInput()
  assigned_ok = self.assigned_to_edit.hasAcceptableInput()
  self._set_invalid(self.title_edit, has_selection and not title_ok)
  self._set_invalid(self.assigned_to_edit, has_selection and not assigned_ok)
  self.save_button.setEnabled(not has_selection or (title_ok and assigned_ok))
  ```
- `_set_invalid(self, widget, invalid)` (new): sets the dynamic property
  `invalid` (bool) on `widget`, then calls
  `widget.style().unpolish(widget)` / `widget.style().polish(widget)` so the
  QSS re-evaluates.
- `_update_validation_state()` is also called at the end of `_show_issue()`
  and `_clear_form()`. Those two methods already run on every path that
  changes what's displayed in the form — selection change, new issue,
  delete issue, cancel — so no other call sites need to change.

## QSS + resource bundle

`resources/qss/validation.qss`:

```css
QLineEdit[invalid="true"] {
    border: 1px solid red;
    background-color: #fff0f0;
}
```

`resources/resources.qrc` (new; top-level under `resources/` so future
resource work — icons, additional themes — can extend the same manifest
with more `<qresource>` blocks):

```xml
<RCC>
  <qresource prefix="/styles">
    <file>qss/validation.qss</file>
  </qresource>
</RCC>
```

Compiled by hand:

```
pyside6-rcc resources/resources.qrc -o src/ui/resources_rc.py
```

This mirrors the existing convention where `resources/ui/main_window.ui` is
compiled to `src/ui/main_window.py` — a generated file that gets committed
and manually regenerated when its source changes. There's no build-time
generation step in this project today, so this feature doesn't add one.

`src/ui/resources_rc.py` is imported for its side effect (registering
`:/styles/qss/validation.qss` with Qt's resource system):

```python
from ui import resources_rc  # noqa: F401
```

added near the other imports at the top of `issues_table_window.py`.

`IssuesTableWindow` gets a new `_setup_style()` method (called from
`__init__`) that reads `:/styles/qss/validation.qss` via `QFile`/`QTextStream`
and calls `self.setStyleSheet(...)`. This is scoped to the window (and
propagates to its child widgets, including both `QLineEdit`s) rather than
applied at the `QApplication` level — keeps the feature self-contained in
one file without touching `main()`. App-wide theming is future scope for
the QSS/palette topics, not this feature.

## File layout summary

New files:
- `src/issue_tracker/validators.py`
- `resources/qss/validation.qss`
- `resources/resources.qrc`
- `src/ui/resources_rc.py` (generated by `pyside6-rcc`, committed)

Modified files:
- `src/issue_tracker/issues_table_window.py`: import `resources_rc`, add
  `_setup_validation()`, `_setup_style()`, `_update_validation_state()`,
  `_set_invalid()`; call the two new `_setup_*` methods from `__init__`;
  call `_update_validation_state()` from `_show_issue()` and
  `_clear_form()`.

## Testing

No automated test suite exists in this project. Verification is manual:
run the app and confirm —
- Selecting an issue with a valid Title/Assigned To shows no red border and
  Save is enabled.
- Clearing Title or Assigned To on a selected issue turns that field's
  border red and disables Save; restoring non-blank text re-enables Save
  and clears the border.
- Clicking "New" shows Assigned To as invalid (empty) with Save disabled
  until an assignee is entered.
- Deselecting (Cancel with nothing selected, or no row selected) shows no
  red border regardless of field contents, and Save remains a no-op as
  today.
- Leading/trailing whitespace typed into either field is trimmed when the
  field loses focus (`fixup()`).
