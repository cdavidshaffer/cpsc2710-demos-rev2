import sys

from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class LayoutConstraintsDemo(QWidget):
    """Demo showing layout size constraints and size policies."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layout Constraints Demo")

        # Create the main layout
        layout = QVBoxLayout()

        # Create a line edit with expanding horizontal policy
        edit = QLineEdit()
        edit.setPlaceholderText("Enter text here...")
        # Expands horizontally, fixed vertically
        edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Create an OK button with fixed policy
        ok = QPushButton("OK")
        # Fixed in both directions
        ok.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        layout.addWidget(edit)
        layout.addWidget(ok)

        # Constrain myself to the layout's preferred size
        # If I'm a window, this window will not be resizable.  If
        # I'm nested in another widget, I will occupy a fixed space.
        layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        self.setLayout(layout)


def main():
    """Run the layout constraints demo."""
    app = QApplication(sys.argv)
    demo = LayoutConstraintsDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("LAYOUT CONSTRAINTS DEMO")
    print("=" * 80)
    print("\nKey Concepts:")
    print("  - QSizePolicy: Controls how widgets grow and shrink")
    print("    • Expanding: Widget can grow to fill available space")
    print("    • Fixed: Widget maintains its sizeHint and doesn't resize")
    print("\n  - setSizeConstraint: Controls how the layout affects window size")
    print(
        "    • SetFixedSize: Window sized to layout's preferred size and not resizable"
    )
    print("\nWhat This Demo Shows:")
    print("  • QLineEdit: Expanding horizontal, Fixed vertical")
    print("    - Line edit will grow/shrink horizontally with window width")
    print("    - But maintains fixed height")
    print("\n  • QPushButton: Fixed in both directions")
    print("    - Button stays at its natural size (sizeHint)")
    print("    - Doesn't expand or shrink")
    print("\n  • Layout: SetFixedSize constraint")
    print("    - The dialog cannot be resized by the user")
    print("    - Window is locked to the layout's preferred size")
    print("\nTry:")
    print("  1. Notice you cannot resize this window (SetFixedSize constraint)")
    print("  2. Try commenting out the SetFixedSize constraint to see what happens.")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
