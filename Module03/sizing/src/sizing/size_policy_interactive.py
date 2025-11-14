import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SizeInfoWindow(QWidget):
    """Separate window displaying size information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Size Information")
        self.setMinimumSize(500, 500)

        layout = QVBoxLayout()

        title = QLabel("Live Size Information")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        layout.addStretch()

        self.setLayout(layout)

    def update_info(self, info_text):
        """Update the info display."""
        self.info_label.setText(info_text)


class PolicyButton(QPushButton):
    """A button that tracks its size policy settings."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def get_info(self):
        """Get size information as a string."""
        policy = self.sizePolicy()
        h_policy_name = self.get_policy_name(policy.horizontalPolicy())
        v_policy_name = self.get_policy_name(policy.verticalPolicy())

        info = (
            f"{self.text()}:\n"
            f"  Horizontal Policy: {h_policy_name}\n"
            f"  Vertical Policy: {v_policy_name}\n"
            f"  Actual size: {self.size().width()}x{self.size().height()}\n"
            f"  sizeHint: {self.sizeHint().width()}x{self.sizeHint().height()}\n"
            f"  minimumSizeHint: {self.minimumSizeHint().width()}x{self.minimumSizeHint().height()}\n"
        )
        return info

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


class PolicyControlPanel(QWidget):
    """Control panel for adjusting a button's size policy."""

    def __init__(self, button, button_name, update_callback, parent=None):
        super().__init__(parent)
        self.button = button
        self.update_callback = update_callback

        layout = QVBoxLayout()

        # Title
        title = QLabel(f"{button_name} Size Policy")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Horizontal policy
        h_label = QLabel("Horizontal:")
        layout.addWidget(h_label)

        self.h_combo = QComboBox()
        self.h_combo.addItem("Fixed", QSizePolicy.Policy.Fixed)
        self.h_combo.addItem("Minimum", QSizePolicy.Policy.Minimum)
        self.h_combo.addItem("Maximum", QSizePolicy.Policy.Maximum)
        self.h_combo.addItem("Preferred", QSizePolicy.Policy.Preferred)
        self.h_combo.addItem("Expanding", QSizePolicy.Policy.Expanding)
        self.h_combo.addItem("MinimumExpanding", QSizePolicy.Policy.MinimumExpanding)
        self.h_combo.addItem("Ignored", QSizePolicy.Policy.Ignored)
        self.h_combo.setCurrentIndex(3)  # Default to Preferred
        self.h_combo.currentIndexChanged.connect(self.on_policy_changed)
        layout.addWidget(self.h_combo)

        layout.addSpacing(10)

        # Vertical policy
        v_label = QLabel("Vertical:")
        layout.addWidget(v_label)

        self.v_combo = QComboBox()
        self.v_combo.addItem("Fixed", QSizePolicy.Policy.Fixed)
        self.v_combo.addItem("Minimum", QSizePolicy.Policy.Minimum)
        self.v_combo.addItem("Maximum", QSizePolicy.Policy.Maximum)
        self.v_combo.addItem("Preferred", QSizePolicy.Policy.Preferred)
        self.v_combo.addItem("Expanding", QSizePolicy.Policy.Expanding)
        self.v_combo.addItem("MinimumExpanding", QSizePolicy.Policy.MinimumExpanding)
        self.v_combo.addItem("Ignored", QSizePolicy.Policy.Ignored)
        self.v_combo.setCurrentIndex(3)  # Default to Preferred
        self.v_combo.currentIndexChanged.connect(self.on_policy_changed)
        layout.addWidget(self.v_combo)

        self.setLayout(layout)

    def on_policy_changed(self):
        """Handle policy change."""
        h_policy = self.h_combo.currentData()
        v_policy = self.v_combo.currentData()
        self.button.setSizePolicy(h_policy, v_policy)
        self.update_callback()


class SizePolicyInteractiveDemo(QWidget):
    """Interactive demo for exploring size policies."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Size Policy Demo")
        self.setMinimumSize(900, 700)

        # Create the separate info window
        self.info_window = SizeInfoWindow()
        self.info_window.show()

        # Position windows side by side
        self.move(100, 100)
        self.info_window.move(1020, 100)

        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Interactive Size Policy Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "Change the size policies using the dropdown menus below.\n"
            "Resize the window to see how different policies affect widget sizes.\n"
            "Watch the 'Size Information' window for details."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Explanation
        explanation_group = QGroupBox("Size Policy Types")
        explanation_layout = QVBoxLayout()

        explanation_text = QLabel(
            "• Fixed: Widget has fixed size (sizeHint), won't grow or shrink\n"
            "• Minimum: Can grow larger than sizeHint, won't shrink below it\n"
            "• Maximum: Can shrink smaller than sizeHint, won't grow beyond it\n"
            "• Preferred: Prefers sizeHint, but can grow or shrink (default)\n"
            "• Expanding: Like Preferred, but greedily takes available space\n"
            "• MinimumExpanding: Like Expanding, but won't shrink below sizeHint\n"
            "• Ignored: sizeHint is ignored, can be any size"
        )
        explanation_text.setWordWrap(True)
        explanation_layout.addWidget(explanation_text)

        explanation_group.setLayout(explanation_layout)
        main_layout.addWidget(explanation_group)
        main_layout.addSpacing(15)

        # Button display area
        demo_label = QLabel("Button Layout (VBox):")
        main_layout.addWidget(demo_label)

        self.button_container = QFrame()
        self.button_container.setFrameShape(QFrame.Shape.Box)
        self.button_container.setLineWidth(2)
        self.button_layout = QVBoxLayout()
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.setSpacing(8)
        self.button_container.setLayout(self.button_layout)

        # Create three buttons with different default text
        self.button1 = PolicyButton("Button 1 (short text)")
        self.button2 = PolicyButton("Button 2 with much longer text to show size differences")
        self.button3 = PolicyButton("Btn3")

        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)

        main_layout.addWidget(self.button_container)
        main_layout.addSpacing(15)

        # Control panels
        controls_label = QLabel("Size Policy Controls:")
        main_layout.addWidget(controls_label)
        main_layout.addSpacing(10)

        controls_layout = QHBoxLayout()

        self.control1 = PolicyControlPanel(self.button1, "Button 1", self.update_all_info)
        controls_layout.addWidget(self.control1)

        self.control2 = PolicyControlPanel(self.button2, "Button 2", self.update_all_info)
        controls_layout.addWidget(self.control2)

        self.control3 = PolicyControlPanel(self.button3, "Button 3", self.update_all_info)
        controls_layout.addWidget(self.control3)

        main_layout.addLayout(controls_layout)
        main_layout.addSpacing(15)

        # Print info button
        print_button = QPushButton("Print Size Info to Console")
        print_button.clicked.connect(self.print_info)
        main_layout.addWidget(print_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def update_all_info(self):
        """Update the info window with all button information."""
        container_height = self.button_container.size().height()
        margins = self.button_layout.contentsMargins()
        spacing = self.button_layout.spacing()

        available_height = container_height - margins.top() - margins.bottom() - (2 * spacing)

        info_lines = []
        info_lines.append("Layout Information:\n")
        info_lines.append(f"  Container size: {self.button_container.size().width()}x{container_height}\n")
        info_lines.append(f"  Available height for buttons: {available_height}\n")
        info_lines.append(f"  Spacing between buttons: {spacing}\n\n")

        info_lines.append(self.button1.get_info())
        info_lines.append("\n")
        info_lines.append(self.button2.get_info())
        info_lines.append("\n")
        info_lines.append(self.button3.get_info())

        self.info_window.update_info("".join(info_lines))

    def print_info(self):
        """Print detailed information to console."""
        print("\n" + "=" * 80)
        print("SIZE POLICY DETAILS")
        print("=" * 80)

        print(f"\nContainer size: {self.button_container.size().width()}x{self.button_container.size().height()}")

        print("\nButton 1:")
        policy1 = self.button1.sizePolicy()
        print(f"  Horizontal Policy: {self.button1.get_policy_name(policy1.horizontalPolicy())}")
        print(f"  Vertical Policy: {self.button1.get_policy_name(policy1.verticalPolicy())}")
        print(f"  sizeHint: {self.button1.sizeHint().width()}x{self.button1.sizeHint().height()}")
        print(f"  Actual size: {self.button1.size().width()}x{self.button1.size().height()}")

        print("\nButton 2:")
        policy2 = self.button2.sizePolicy()
        print(f"  Horizontal Policy: {self.button2.get_policy_name(policy2.horizontalPolicy())}")
        print(f"  Vertical Policy: {self.button2.get_policy_name(policy2.verticalPolicy())}")
        print(f"  sizeHint: {self.button2.sizeHint().width()}x{self.button2.sizeHint().height()}")
        print(f"  Actual size: {self.button2.size().width()}x{self.button2.size().height()}")

        print("\nButton 3:")
        policy3 = self.button3.sizePolicy()
        print(f"  Horizontal Policy: {self.button3.get_policy_name(policy3.horizontalPolicy())}")
        print(f"  Vertical Policy: {self.button3.get_policy_name(policy3.verticalPolicy())}")
        print(f"  sizeHint: {self.button3.sizeHint().width()}x{self.button3.sizeHint().height()}")
        print(f"  Actual size: {self.button3.size().width()}x{self.button3.size().height()}")

        print("\n" + "=" * 80 + "\n")

    def resizeEvent(self, event):
        """Update info when window is resized."""
        super().resizeEvent(event)
        self.update_all_info()

    def showEvent(self, event):
        """Update info when window is shown."""
        super().showEvent(event)
        self.update_all_info()

    def closeEvent(self, event):
        """Close the info window and exit when main window closes."""
        self.info_window.close()
        event.accept()
        QApplication.quit()


def main():
    """Run the interactive size policy demo."""
    app = QApplication(sys.argv)
    demo = SizePolicyInteractiveDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("INTERACTIVE SIZE POLICY DEMO")
    print("=" * 80)
    print("\nKey Concepts:")
    print("  - Size policies control how widgets respond to available space")
    print("  - Horizontal and vertical policies are set independently")
    print("  - Policies affect whether widgets grow/shrink, not their sizeHint")
    print("\nPolicy Behaviors:")
    print("  Fixed: Never changes from sizeHint")
    print("  Minimum: Can grow, won't shrink below sizeHint")
    print("  Maximum: Can shrink, won't grow beyond sizeHint")
    print("  Preferred: Can grow/shrink (default behavior)")
    print("  Expanding: Like Preferred but greedily takes space")
    print("\nExperiments to Try:")
    print("  1. Set Button 1 vertical to Fixed - it won't grow when you resize")
    print("  2. Set Button 2 vertical to Expanding - it takes most of the extra space")
    print("  3. Set all horizontal to Fixed - buttons become narrow (sizeHint width)")
    print("  4. Set Button 3 horizontal to Expanding - it grows to fill window width")
    print("  5. Compare Preferred vs Expanding - Expanding is greedier")
    print("\nTry:")
    print("  - Change policies using the dropdown menus")
    print("  - Resize the window to see how widgets respond")
    print("  - Watch the info window for exact size calculations")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
