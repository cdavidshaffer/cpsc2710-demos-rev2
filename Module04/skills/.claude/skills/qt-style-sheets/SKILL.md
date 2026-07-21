---
name: qt-style-sheets
description: >
  Use when writing or reviewing Qt Style
  Sheets (QSS) in this project.
---

Remember: QSS is not CSS.

- No !important support.
- Fonts and colors are not inherited automatically.
- Prefer palette(role) over a hard-coded color so themes still work.
- After widget.setProperty("invalid", True), call style().unpolish(widget) then
  style().polish(widget) -- or it won't repaint.
