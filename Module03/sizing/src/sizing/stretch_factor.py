import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class SizeInfoWindow(QWidget):
    """Separate window displaying size information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Size Information")
        self.setMinimumSize(500, 600)

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


class StretchButton(QPushButton):
    """A button that tracks its stretch factor."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.stretch_factor = 0

    def set_stretch_factor(self, stretch):
        """Set the stretch factor for this button."""
        self.stretch_factor = stretch

    def get_info(self):
        """Get size information as a string."""
        info = (
            f"{self.text()}:\n"
            f"  Stretch factor: {self.stretch_factor}\n"
            f"  Actual size: {self.size().width()}x{self.size().height()}\n"
            f"  sizeHint: {self.sizeHint().width()}x{self.sizeHint().height()}\n"
            f"  sizePolicy: H={self.sizePolicy().horizontalPolicy()}, "
            f"V={self.sizePolicy().verticalPolicy()}\n"
        )
        return info


class StretchControlPanel(QWidget):
    """Control panel for adjusting a button's stretch factor."""

    def __init__(self, button, button_name, update_callback, parent=None):
        super().__init__(parent)
        self.button = button
        self.update_callback = update_callback

        layout = QVBoxLayout()

        # Title
        title = QLabel(f"{button_name} Stretch Factor:")
        layout.addWidget(title)

        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.on_stretch_changed)
        layout.addWidget(self.slider)

        # Value label
        self.value_label = QLabel("0")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)

        self.setLayout(layout)

    def on_stretch_changed(self, value):
        """Handle stretch factor change."""
        self.value_label.setText(str(value))
        self.button.set_stretch_factor(value)
        self.update_callback()


class StretchFactorDemo(QWidget):
    """Demo showing how stretch factors affect space distribution."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stretch Factor Demo")
        self.setMinimumSize(800, 600)

        # Create the separate info window
        self.info_window = SizeInfoWindow()
        self.info_window.show()

        # Position windows side by side
        self.move(100, 100)
        self.info_window.move(920, 100)

        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Stretch Factor Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "Stretch factors control how extra space is distributed among widgets.\n"
            "Adjust the sliders to see how buttons with different stretch factors share available space.\n"
            "Watch the 'Size Information' window for details."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Explanation box
        explanation_group = QGroupBox("How Stretch Factors Work")
        explanation_layout = QVBoxLayout()

        explanation_text = QLabel(
            "• Stretch factor = 0: Widget gets its sizeHint, no extra space\n"
            "• Stretch factor > 0: Widget shares extra space proportionally\n"
            "• Example: If Button 1 has stretch=1 and Button 2 has stretch=2,\n"
            "  Button 2 gets twice as much extra space as Button 1\n"
            "• All buttons have Expanding horizontal policy for this demo"
        )
        explanation_text.setWordWrap(True)
        explanation_layout.addWidget(explanation_text)

        explanation_group.setLayout(explanation_layout)
        main_layout.addWidget(explanation_group)
        main_layout.addSpacing(15)

        # Main demonstration area
        demo_label = QLabel("Button Layout (HBox):")
        main_layout.addWidget(demo_label)

        # Create the HBox with buttons
        self.button_container = QFrame()
        self.button_container.setFrameShape(QFrame.Shape.Box)
        self.button_container.setLineWidth(2)
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(10, 10, 10, 10)
        self.button_layout.setSpacing(8)
        self.button_container.setLayout(self.button_layout)

        # Create three buttons
        self.button1 = StretchButton("Button 1")
        self.button2 = StretchButton("Button 2 (longer text)")
        self.button3 = StretchButton("Btn3")

        # Add buttons to layout with initial stretch of 0
        self.button_layout.addWidget(self.button1, 0)
        self.button_layout.addWidget(self.button2, 0)
        self.button_layout.addWidget(self.button3, 0)

        main_layout.addWidget(self.button_container)
        main_layout.addSpacing(15)

        # Control panels
        controls_label = QLabel("Stretch Factor Controls:")
        main_layout.addWidget(controls_label)
        main_layout.addSpacing(10)

        controls_layout = QHBoxLayout()

        self.control1 = StretchControlPanel(self.button1, "Button 1", self.update_stretch_factors)
        controls_layout.addWidget(self.control1)

        self.control2 = StretchControlPanel(self.button2, "Button 2", self.update_stretch_factors)
        controls_layout.addWidget(self.control2)

        self.control3 = StretchControlPanel(self.button3, "Button 3", self.update_stretch_factors)
        controls_layout.addWidget(self.control3)

        main_layout.addLayout(controls_layout)
        main_layout.addSpacing(15)

        # Print info button
        print_button = QPushButton("Print Size Info to Console")
        print_button.clicked.connect(self.print_info)
        main_layout.addWidget(print_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def update_stretch_factors(self):
        """Update the stretch factors in the layout."""
        # Remove all widgets from layout
        for i in reversed(range(self.button_layout.count())):
            self.button_layout.itemAt(i).widget().setParent(None)

        # Re-add with new stretch factors
        self.button_layout.addWidget(self.button1, self.button1.stretch_factor)
        self.button_layout.addWidget(self.button2, self.button2.stretch_factor)
        self.button_layout.addWidget(self.button3, self.button3.stretch_factor)

        # Update info display
        self.update_all_info()

    def update_all_info(self):
        """Update the info window with all button information."""
        total_width = self.button_container.size().width()
        margins = self.button_layout.contentsMargins()
        spacing = self.button_layout.spacing()

        # Calculate available width
        available_width = total_width - margins.left() - margins.right() - (2 * spacing)

        # Calculate total sizeHint width
        total_hint = (self.button1.sizeHint().width() +
                     self.button2.sizeHint().width() +
                     self.button3.sizeHint().width())

        extra_space = max(0, available_width - total_hint)

        total_stretch = (self.button1.stretch_factor +
                        self.button2.stretch_factor +
                        self.button3.stretch_factor)

        info_lines = []
        info_lines.append("Layout Information:\n")
        info_lines.append(f"  Container width: {total_width}\n")
        info_lines.append(f"  Available width for buttons: {available_width}\n")
        info_lines.append(f"  Total sizeHint width: {total_hint}\n")
        info_lines.append(f"  Extra space to distribute: {extra_space}\n")
        info_lines.append(f"  Total stretch factors: {total_stretch}\n\n")

        info_lines.append(self.button1.get_info())
        if self.button1.stretch_factor > 0 and total_stretch > 0:
            share = (self.button1.stretch_factor / total_stretch) * extra_space
            info_lines.append(f"  Extra space allocated: {share:.1f}\n")
        info_lines.append("\n")

        info_lines.append(self.button2.get_info())
        if self.button2.stretch_factor > 0 and total_stretch > 0:
            share = (self.button2.stretch_factor / total_stretch) * extra_space
            info_lines.append(f"  Extra space allocated: {share:.1f}\n")
        info_lines.append("\n")

        info_lines.append(self.button3.get_info())
        if self.button3.stretch_factor > 0 and total_stretch > 0:
            share = (self.button3.stretch_factor / total_stretch) * extra_space
            info_lines.append(f"  Extra space allocated: {share:.1f}\n")

        self.info_window.update_info("".join(info_lines))

    def print_info(self):
        """Print detailed information to console."""
        print("\n" + "=" * 80)
        print("STRETCH FACTOR DETAILS")
        print("=" * 80)

        total_width = self.button_container.size().width()
        margins = self.button_layout.contentsMargins()
        spacing = self.button_layout.spacing()

        print(f"\nContainer width: {total_width}")
        print(f"Margins: L={margins.left()}, R={margins.right()}")
        print(f"Spacing: {spacing}")

        available_width = total_width - margins.left() - margins.right() - (2 * spacing)
        print(f"Available width for buttons: {available_width}")

        print(f"\nButton 1:")
        print(f"  Stretch factor: {self.button1.stretch_factor}")
        print(f"  sizeHint: {self.button1.sizeHint().width()}x{self.button1.sizeHint().height()}")
        print(f"  Actual size: {self.button1.size().width()}x{self.button1.size().height()}")

        print(f"\nButton 2:")
        print(f"  Stretch factor: {self.button2.stretch_factor}")
        print(f"  sizeHint: {self.button2.sizeHint().width()}x{self.button2.sizeHint().height()}")
        print(f"  Actual size: {self.button2.size().width()}x{self.button2.size().height()}")

        print(f"\nButton 3:")
        print(f"  Stretch factor: {self.button3.stretch_factor}")
        print(f"  sizeHint: {self.button3.sizeHint().width()}x{self.button3.sizeHint().height()}")
        print(f"  Actual size: {self.button3.size().width()}x{self.button3.size().height()}")

        total_stretch = (self.button1.stretch_factor +
                        self.button2.stretch_factor +
                        self.button3.stretch_factor)

        total_hint = (self.button1.sizeHint().width() +
                     self.button2.sizeHint().width() +
                     self.button3.sizeHint().width())

        extra_space = max(0, available_width - total_hint)

        print(f"\nTotal stretch factors: {total_stretch}")
        print(f"Total sizeHint width: {total_hint}")
        print(f"Extra space to distribute: {extra_space}")

        if total_stretch > 0:
            print(f"\nSpace distribution:")
            print(f"  Button 1 gets: {(self.button1.stretch_factor / total_stretch) * extra_space:.1f} pixels")
            print(f"  Button 2 gets: {(self.button2.stretch_factor / total_stretch) * extra_space:.1f} pixels")
            print(f"  Button 3 gets: {(self.button3.stretch_factor / total_stretch) * extra_space:.1f} pixels")

        print("=" * 80 + "\n")

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
    """Run the stretch factor demo."""
    app = QApplication(sys.argv)
    demo = StretchFactorDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("STRETCH FACTOR DEMO")
    print("=" * 80)
    print("\nKey Concepts:")
    print("  - Stretch factors control how EXTRA space is distributed")
    print("  - They don't affect the minimum size (sizeHint) of widgets")
    print("  - Stretch factor of 0 means 'don't give me extra space'")
    print("  - Higher stretch factors get proportionally more space")
    print("\nHow It Works:")
    print("  1. Layout calculates total space needed (sum of sizeHints + spacing)")
    print("  2. If container is larger, there's 'extra space' to distribute")
    print("  3. Extra space is divided proportionally by stretch factors")
    print("  4. Widget final width = sizeHint + (stretch_factor/total_stretch) * extra_space")
    print("\nExamples to Try:")
    print("  - All stretch = 0: Buttons stay at sizeHint, centered in container")
    print("  - All stretch = 1: Extra space divided equally among all buttons")
    print("  - Stretch 1,2,1: Middle button gets twice as much extra space")
    print("  - Stretch 0,1,0: Only middle button grows, others stay at sizeHint")
    print("\nTry:")
    print("  1. Start with all sliders at 0 - resize window, buttons don't grow")
    print("  2. Set all to 1 - resize window, all buttons grow equally")
    print("  3. Set to 1,2,3 - see proportional distribution")
    print("  4. Watch the info window for exact calculations!")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
