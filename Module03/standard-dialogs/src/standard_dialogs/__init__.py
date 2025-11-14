"""
Standard Dialogs Demo Package

This package contains four demo applications showing modal and non-modal dialog usage.
"""

def main() -> None:
    """Main entry point - shows available demos."""
    print("Standard Dialogs Demo Applications")
    print("=" * 50)
    print("\nAvailable demos:")
    print("  1. Modal QMessageBox (static methods)")
    print("  2. Modal QFontDialog (open() and signals)")
    print("  3. Non-Modal QMessageBox (show() method)")
    print("  4. Non-Modal QFontDialog (show() method)")
    print("  5. Standard Dialogs Showcase (all dialog types)")
    print("\nTo run a demo, use:")
    print("  python -m standard_dialogs.modal_messagebox_demo")
    print("  python -m standard_dialogs.modal_fontdialog_demo")
    print("  python -m standard_dialogs.nonmodal_messagebox_demo")
    print("  python -m standard_dialogs.nonmodal_fontdialog_demo")
    print("  python -m standard_dialogs.standard_dialogs_showcase")
