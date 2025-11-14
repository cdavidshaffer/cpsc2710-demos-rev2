"""
Windows Demo Collection

A collection of PySide6 demos for learning QMainWindow and related concepts.
"""

import sys


def main() -> None:
    """
    Main entry point for running demos.

    Usage:
        python -m windows.first_main_window    # Run specific demo
        uv run python -m windows.first_main_window
    """
    if len(sys.argv) > 1:
        print("Windows Demo Collection")
        print("\nAvailable demos:")
        print("  - first_main_window: Basic QMainWindow with menus and forms")
        print("  - second_main_window: QMainWindow with toolbar")
        print("\nUsage:")
        print("  python -m windows.first_main_window")
        print("  python -m windows.second_main_window")
        print("  uv run python -m windows.first_main_window")
    else:
        print("Windows Demo Collection")
        print("\nAvailable demos:")
        print("  - first_main_window: Basic QMainWindow with menus and forms")
        print("  - second_main_window: QMainWindow with toolbar")
        print("\nUsage:")
        print("  python -m windows.first_main_window")
        print("  python -m windows.second_main_window")
