import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SizePolicyButton(QPushButton):
    """A button that displays its size and size policy."""

    def __init__(self, text, h_policy, v_policy, parent=None):
        super().__init__(text, parent)
        self.h_policy = h_policy
        self.v_policy = v_policy
        self.info_label = None

        # Set the size policy
        self.setSizePolicy(h_policy, v_policy)

        # Store policy names for display
        self.h_policy_name = self.get_policy_name(h_policy)
        self.v_policy_name = self.get_policy_name(v_policy)

    def get_policy_name(self, policy):
        """Convert QSizePolicy.Policy enum to readable name."""
        policy_map = {
            QSizePolicy.Policy.Fixed: "Fixed",
            QSizePolicy.Policy.Minimum: "Minimum",
            QSizePolicy.Policy.Maximum: "Maximum",
            QSizePolicy.Policy.Preferred: "Preferred",
            QSizePolicy.Policy.Expanding: "Expanding",
            QSizePolicy.Policy.MinimumExpanding: "MinimumExpanding",
            QSizePolicy.Policy.Ignored: "Ignored",
        }
        return policy_map.get(policy, str(policy))

    def set_info_label(self, label):
        """Set the label that will display this button's size info."""
        self.info_label = label
        self.update_info()

    def update_info(self):
        """Update the info label with current size information."""
        if self.info_label:
            info = (
                f"H: {self.h_policy_name}\n"
                f"V: {self.v_policy_name}\n"
                f"Size: {self.size().width()}x{self.size().height()}\n"
                f"Hint: {self.sizeHint().width()}x{self.sizeHint().height()}"
            )
            self.info_label.setText(info)

    def resizeEvent(self, event):
        """Override to update info when button is resized."""
        super().resizeEvent(event)
        self.update_info()


class SizePolicyDemo(QWidget):
    """Main demo window showing size policy effects."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Size Policy Demo")
        self.setMinimumSize(1200, 900)

        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Size Policy Interactive Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "Size policies control how widgets grow/shrink when space is available.\n"
            "Resize the window to see how different policies behave.\n"
            "All buttons have the same sizeHint - only the policies differ!"
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(10)

        # Legend
        legend = QLabel(
            "Fixed: Never grows/shrinks | Minimum: Can grow, won't shrink below sizeHint | "
            "Maximum: Can shrink, won't grow beyond sizeHint\n"
            "Preferred: Can grow/shrink (default) | Expanding: Like Preferred but takes more space | "
            "Ignored: SizeHint is ignored"
        )
        legend.setWordWrap(True)
        main_layout.addWidget(legend)
        main_layout.addSpacing(15)

        # Create grid of buttons with different size policies
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # Define common size policies to demonstrate
        policies = [
            (QSizePolicy.Policy.Fixed, "Fixed"),
            (QSizePolicy.Policy.Minimum, "Minimum"),
            (QSizePolicy.Policy.Maximum, "Maximum"),
            (QSizePolicy.Policy.Preferred, "Preferred"),
            (QSizePolicy.Policy.Expanding, "Expanding"),
        ]

        # Row 1: Horizontal policies (vary horizontal, keep vertical as Preferred)
        row = 0
        header = QLabel("Horizontal Size Policies\n(Vertical: Preferred)")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(header, row, 0, 1, len(policies))
        row += 1

        for col, (policy, name) in enumerate(policies):
            button = SizePolicyButton(
                name, policy, QSizePolicy.Policy.Preferred
            )
            info_label = QLabel()
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button.set_info_label(info_label)

            grid_layout.addWidget(button, row, col)
            grid_layout.addWidget(info_label, row + 1, col)

        # Row 2: Vertical policies (vary vertical, keep horizontal as Preferred)
        row += 2
        header = QLabel("Vertical Size Policies\n(Horizontal: Preferred)")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(header, row, 0, 1, len(policies))
        row += 1

        for col, (policy, name) in enumerate(policies):
            button = SizePolicyButton(
                name, QSizePolicy.Policy.Preferred, policy
            )
            info_label = QLabel()
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button.set_info_label(info_label)

            grid_layout.addWidget(button, row, col)
            grid_layout.addWidget(info_label, row + 1, col)

        # Row 3: Common combinations
        row += 2
        header = QLabel("Common Size Policy Combinations")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(header, row, 0, 1, len(policies))
        row += 1

        combinations = [
            (QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed, "Fixed/Fixed"),
            (QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding, "Expanding/Expanding"),
            (QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred, "Preferred/Preferred"),
            (QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum, "Minimum/Minimum"),
            (QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed, "Expanding/Fixed"),
        ]

        for col, (h_policy, v_policy, label) in enumerate(combinations):
            button = SizePolicyButton(label, h_policy, v_policy)
            info_label = QLabel()
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button.set_info_label(info_label)

            grid_layout.addWidget(button, row, col)
            grid_layout.addWidget(info_label, row + 1, col)

        main_layout.addLayout(grid_layout)
        main_layout.addSpacing(15)

        # Print info button
        print_button = QPushButton("Print All Size Info to Console")
        print_button.clicked.connect(self.print_all_info)
        print_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(print_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def print_all_info(self):
        """Print size information for all buttons to console."""
        print("\n" + "=" * 80)
        print("CURRENT SIZE INFORMATION FOR ALL BUTTONS")
        print("=" * 80)

        for i, button in enumerate(self.findChildren(SizePolicyButton)):
            print(f"\nButton {i + 1}: '{button.text()}'")
            print(f"  Horizontal Policy: {button.h_policy_name}")
            print(f"  Vertical Policy: {button.v_policy_name}")
            print(f"  Actual size: {button.size().width()}x{button.size().height()}")
            print(f"  sizeHint: {button.sizeHint().width()}x{button.sizeHint().height()}")
            print(
                f"  minimumSizeHint: {button.minimumSizeHint().width()}x{button.minimumSizeHint().height()}"
            )
            h_stretch = button.sizePolicy().horizontalStretch()
            v_stretch = button.sizePolicy().verticalStretch()
            print(f"  Stretch factors: H={h_stretch}, V={v_stretch}")

        print("\n" + "=" * 80 + "\n")

    def resizeEvent(self, event):
        """Update all button info when window is resized."""
        super().resizeEvent(event)
        # Force update of all size display buttons
        for button in self.findChildren(SizePolicyButton):
            button.update_info()


def main():
    """Run the size policy demo."""
    app = QApplication(sys.argv)
    demo = SizePolicyDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("SIZE POLICY DEMO")
    print("=" * 80)
    print("\nSize Policy Types:")
    print("  - Fixed: Widget has fixed size (sizeHint), cannot grow or shrink")
    print("  - Minimum: Widget can grow larger than sizeHint, but not smaller")
    print("  - Maximum: Widget can shrink smaller than sizeHint, but not larger")
    print("  - Preferred: Widget prefers sizeHint, but can grow or shrink (default)")
    print("  - Expanding: Like Preferred, but greedily takes available space")
    print("  - MinimumExpanding: Like Expanding, but won't shrink below sizeHint")
    print("  - Ignored: SizeHint is ignored, widget can be any size")
    print("\nKey Points:")
    print("  - Size policies control how widgets respond to available space")
    print("  - Horizontal and vertical policies are independent")
    print("  - Layout managers use policies to distribute space among widgets")
    print("  - All buttons start with same sizeHint - only policies differ!")
    print("\nTry:")
    print("  1. Resize the window horizontally - watch Fixed vs Expanding")
    print("  2. Resize vertically - see how vertical policies behave")
    print("  3. Compare Preferred vs Expanding - Expanding takes more space")
    print("  4. Notice Minimum widgets won't shrink below sizeHint")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
