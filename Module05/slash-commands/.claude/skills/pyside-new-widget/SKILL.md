---
name: pyside-new-widget
description: >
  Use when scaffolding a new PySide6
  QWidget subclass in this project.
---

Widget conventions for this project:

- Subclass QWidget, build layout in a private _build_ui() method.
- Wrap visible strings in self.tr(...).
- self.setProperty("class", "<name>") as the QSS class selector.
- Declare signals as class attributes.
- Remind the user to add a QSS rule for the new class.
