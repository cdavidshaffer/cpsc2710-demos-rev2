#!/usr/bin/env python3
"""Generate a pytest-qt test skeleton for a widget class."""

import ast
import sys
from pathlib import Path


def public_methods(source: str, class_name: str) -> list[str]:
    tree = ast.parse(source)
    node = next(n for n in ast.walk(tree) if getattr(n, "name", "") == class_name)
    return [
        member.name
        for member in node.body
        if isinstance(member, ast.FunctionDef) and not member.name.startswith("_")
    ]


def test_stub(class_name: str, method: str) -> str:
    return (
        f"def test_{method}(qtbot):\n"
        f"    widget = {class_name}()\n"
        f"    qtbot.addWidget(widget)\n"
        f"    widget.{method}()"
    )


if __name__ == "__main__":
    path, class_name = Path(sys.argv[1]), sys.argv[2]
    for method in public_methods(path.read_text(), class_name):
        print(test_stub(class_name, method) + "\n")
