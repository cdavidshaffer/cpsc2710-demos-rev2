# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Human vs AI

This project is part of a course assignment.  In this assignment the contributions of the human student (me) vs AI (you) are clearly delineated: The entire python source code for the calculator widget and associated applications must be entirely written by me.  AI contributions can be solicited but only for small technical pieces of advice.  The application may be styled through a Qt stylesheet by an AI agent.

## Build and Run Commands

This project uses `uv` for package management.  Instructions on using uv can be found here: https://docs.astral.sh/uv/.

```bash
# Run the main calculator
uv run pycalc

# Run dual calculator (two side-by-side)
uv run dual_calc

# Run lecture versions
uv run pycalc-lecture-1
uv run pycalc-lecture-2
```

## Architecture

PyCalc is a PySide6 GUI calculator demonstrating widget composition and state management.

### Core Design

The `Pycalc` widget (`src/pycalc/calculator.py`) implements a 4-function calculator using a two-register state machine:

- **x_register**: Current display value (what user is typing)
- **y_register**: Stored value (first operand)
- **operator_register**: Pending operation (+, -, *, /)

State flow example: `3 + 12 =` proceeds as:
1. `3` → (x=3, y=None, op=None)
2. `+` → (x=None, y=3, op=+)
3. `12` → (x=12, y=3, op=+)
4. `=` → (x=15, y=None, op=None)

### Widget Composition

`Pycalc` is a reusable `QWidget` that can be embedded in any layout. `dual_calculator.py` demonstrates this by placing two independent `Pycalc` instances side-by-side.

### Debug Mode

Set `_debug = True` in `calculator.py` to show y_register and operator_register displays for debugging state transitions.
