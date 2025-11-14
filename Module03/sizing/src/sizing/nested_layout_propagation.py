import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SizeInfoWindow(QWidget):
    """Separate window displaying size information for all tracked widgets."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Size Information")
        self.setMinimumSize(400, 600)

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


class SizeInfoFrame(QFrame):
    """A frame that can report its size information."""

    def __init__(self, label, color, info_window, parent=None):
        super().__init__(parent)
        self.label_text = label
        self.color = color
        self.info_window = info_window

        # Visual styling
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setStyleSheet(f"QFrame {{ border: 2px solid {color}; }}")

    def get_info(self):
        """Get size information as a string."""
        layout = self.layout()
        if layout:
            margins = layout.contentsMargins()
            spacing = layout.spacing()

            info = (
                f"{self.label_text}:\n"
                f"  Size: {self.size().width()}x{self.size().height()}\n"
                f"  sizeHint: {self.sizeHint().width()}x{self.sizeHint().height()}\n"
                f"  Margins: L={margins.left()} T={margins.top()} R={margins.right()} B={margins.bottom()}\n"
                f"  Spacing: {spacing}\n"
            )
            return info
        return f"{self.label_text}: No layout\n"


class PropagationDemo(QWidget):
    """Demo showing how size hints propagate up through nested layouts."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nested Layout Size Propagation Demo")
        self.setMinimumSize(800, 600)

        # Create the separate info window
        self.info_window = SizeInfoWindow()
        self.info_window.show()

        # Position windows side by side
        self.move(100, 100)
        self.info_window.move(920, 100)

        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Nested Layout Size Propagation Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "This demo shows how sizeHint propagates UP from widgets to outer layouts.\n"
            "Watch the separate 'Size Information' window for live size data."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Build the nested structure as specified:
        # Top-level VBox contains:
        #   1) HBox with 3 buttons (default policies)
        #   2) A single button
        #   3) HBox containing a nested VBox with buttons of different policies

        # Main container frame (Purple)
        self.main_frame = SizeInfoFrame("Main VBox (Purple)", "#9c27b0", self.info_window)
        main_container_layout = QVBoxLayout()
        main_container_layout.setContentsMargins(10, 10, 10, 10)
        main_container_layout.setSpacing(8)
        self.main_frame.setLayout(main_container_layout)

        # Part 1: HBox with 3 buttons (Orange)
        self.hbox1_frame = SizeInfoFrame("Part 1: HBox with 3 buttons (Orange)", "#ff9800", self.info_window)
        hbox1_layout = QHBoxLayout()
        hbox1_layout.setContentsMargins(10, 10, 10, 10)
        hbox1_layout.setSpacing(6)
        self.hbox1_frame.setLayout(hbox1_layout)

        self.btn1_1 = QPushButton("Button 1")
        self.btn1_2 = QPushButton("Button 2 (longer text)")
        self.btn1_3 = QPushButton("Btn3")
        hbox1_layout.addWidget(self.btn1_1)
        hbox1_layout.addWidget(self.btn1_2)
        hbox1_layout.addWidget(self.btn1_3)

        main_container_layout.addWidget(self.hbox1_frame)

        # Part 2: Single button
        self.btn2 = QPushButton("Part 2: Single Button")
        main_container_layout.addWidget(self.btn2)

        # Part 3: HBox containing nested VBox (Green outer, Blue inner)
        self.hbox2_frame = SizeInfoFrame("Part 3: HBox (Green)", "#4caf50", self.info_window)
        hbox2_layout = QHBoxLayout()
        hbox2_layout.setContentsMargins(10, 10, 10, 10)
        hbox2_layout.setSpacing(6)
        self.hbox2_frame.setLayout(hbox2_layout)

        # Nested VBox inside Part 3 (Blue)
        self.vbox_nested_frame = SizeInfoFrame("Nested VBox (Blue)", "#2196f3", self.info_window)
        vbox_nested_layout = QVBoxLayout()
        vbox_nested_layout.setContentsMargins(10, 10, 10, 10)
        vbox_nested_layout.setSpacing(6)
        self.vbox_nested_frame.setLayout(vbox_nested_layout)

        # Buttons with different size policies
        self.btn3_1 = QPushButton("Fixed Policy")
        self.btn3_1.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.btn3_2 = QPushButton("Expanding Policy")
        self.btn3_2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.btn3_3 = QPushButton("Minimum Policy")
        self.btn3_3.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.btn3_4 = QPushButton("Preferred (Default)")
        self.btn3_4.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        vbox_nested_layout.addWidget(self.btn3_1)
        vbox_nested_layout.addWidget(self.btn3_2)
        vbox_nested_layout.addWidget(self.btn3_3)
        vbox_nested_layout.addWidget(self.btn3_4)

        hbox2_layout.addWidget(self.vbox_nested_frame)

        # Add additional buttons to the HBox (Part 3)
        self.btn3_5 = QPushButton("Extra 1")
        self.btn3_6 = QPushButton("Extra 2")
        hbox2_layout.addWidget(self.btn3_5)
        hbox2_layout.addWidget(self.btn3_6)

        main_container_layout.addWidget(self.hbox2_frame)

        # Add the main frame to the window
        main_layout.addWidget(self.main_frame)
        main_layout.addSpacing(15)

        # Print info button
        print_button = QPushButton("Print Size Propagation Details to Console")
        print_button.clicked.connect(self.print_propagation_details)
        main_layout.addWidget(print_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        # Track all widgets for info updates
        self.tracked_widgets = [
            self.main_frame,
            self.hbox1_frame,
            self.btn1_1,
            self.btn1_2,
            self.btn1_3,
            self.btn2,
            self.hbox2_frame,
            self.vbox_nested_frame,
            self.btn3_1,
            self.btn3_2,
            self.btn3_3,
            self.btn3_4,
            self.btn3_5,
            self.btn3_6,
        ]

    def update_all_info(self):
        """Update the info window with all widget information."""
        info_lines = []

        info_lines.append(self.main_frame.get_info())
        info_lines.append(self.hbox1_frame.get_info())
        info_lines.append(f"  Button 1: {self.btn1_1.size().width()}x{self.btn1_1.size().height()}, sizeHint: {self.btn1_1.sizeHint().width()}x{self.btn1_1.sizeHint().height()}\n")
        info_lines.append(f"  Button 2: {self.btn1_2.size().width()}x{self.btn1_2.size().height()}, sizeHint: {self.btn1_2.sizeHint().width()}x{self.btn1_2.sizeHint().height()}\n")
        info_lines.append(f"  Button 3: {self.btn1_3.size().width()}x{self.btn1_3.size().height()}, sizeHint: {self.btn1_3.sizeHint().width()}x{self.btn1_3.sizeHint().height()}\n")

        info_lines.append(f"Part 2 Button: {self.btn2.size().width()}x{self.btn2.size().height()}, sizeHint: {self.btn2.sizeHint().width()}x{self.btn2.sizeHint().height()}\n")

        info_lines.append(self.hbox2_frame.get_info())
        info_lines.append(self.vbox_nested_frame.get_info())
        info_lines.append(f"  Fixed: {self.btn3_1.size().width()}x{self.btn3_1.size().height()}, sizeHint: {self.btn3_1.sizeHint().width()}x{self.btn3_1.sizeHint().height()}\n")
        info_lines.append(f"  Expanding: {self.btn3_2.size().width()}x{self.btn3_2.size().height()}, sizeHint: {self.btn3_2.sizeHint().width()}x{self.btn3_2.sizeHint().height()}\n")
        info_lines.append(f"  Minimum: {self.btn3_3.size().width()}x{self.btn3_3.size().height()}, sizeHint: {self.btn3_3.sizeHint().width()}x{self.btn3_3.sizeHint().height()}\n")
        info_lines.append(f"  Preferred: {self.btn3_4.size().width()}x{self.btn3_4.size().height()}, sizeHint: {self.btn3_4.sizeHint().width()}x{self.btn3_4.sizeHint().height()}\n")
        info_lines.append(f"  Extra 1: {self.btn3_5.size().width()}x{self.btn3_5.size().height()}, sizeHint: {self.btn3_5.sizeHint().width()}x{self.btn3_5.sizeHint().height()}\n")
        info_lines.append(f"  Extra 2: {self.btn3_6.size().width()}x{self.btn3_6.size().height()}, sizeHint: {self.btn3_6.sizeHint().width()}x{self.btn3_6.sizeHint().height()}\n")

        self.info_window.update_info("".join(info_lines))

    def print_propagation_details(self):
        """Print detailed size propagation information to console."""
        print("\n" + "=" * 80)
        print("SIZE HINT PROPAGATION DETAILS")
        print("=" * 80)

        print("\n[STRUCTURE]")
        print("Main VBox (Purple) contains:")
        print("  1. HBox (Orange) with 3 buttons (default policies)")
        print("  2. Single button")
        print("  3. HBox (Green) containing VBox (Blue) with 4 buttons (varied policies)")

        print("\n[PART 1: HBox with 3 buttons]")
        print(f"  Button 1 sizeHint: {self.btn1_1.sizeHint().width()}x{self.btn1_1.sizeHint().height()}")
        print(f"  Button 2 sizeHint: {self.btn1_2.sizeHint().width()}x{self.btn1_2.sizeHint().height()}")
        print(f"  Button 3 sizeHint: {self.btn1_3.sizeHint().width()}x{self.btn1_3.sizeHint().height()}")
        print(f"  HBox sizeHint: {self.hbox1_frame.sizeHint().width()}x{self.hbox1_frame.sizeHint().height()}")
        print(f"  HBox actual size: {self.hbox1_frame.size().width()}x{self.hbox1_frame.size().height()}")

        print("\n[PART 2: Single button]")
        print(f"  Button sizeHint: {self.btn2.sizeHint().width()}x{self.btn2.sizeHint().height()}")
        print(f"  Button actual size: {self.btn2.size().width()}x{self.btn2.size().height()}")

        print("\n[PART 3: Nested layouts]")
        print(f"  Fixed button sizeHint: {self.btn3_1.sizeHint().width()}x{self.btn3_1.sizeHint().height()}")
        print(f"  Expanding button sizeHint: {self.btn3_2.sizeHint().width()}x{self.btn3_2.sizeHint().height()}")
        print(f"  Minimum button sizeHint: {self.btn3_3.sizeHint().width()}x{self.btn3_3.sizeHint().height()}")
        print(f"  Preferred button sizeHint: {self.btn3_4.sizeHint().width()}x{self.btn3_4.sizeHint().height()}")
        print(f"  Nested VBox sizeHint: {self.vbox_nested_frame.sizeHint().width()}x{self.vbox_nested_frame.sizeHint().height()}")
        print(f"  Nested VBox actual: {self.vbox_nested_frame.size().width()}x{self.vbox_nested_frame.size().height()}")
        print(f"  Outer HBox sizeHint: {self.hbox2_frame.sizeHint().width()}x{self.hbox2_frame.sizeHint().height()}")
        print(f"  Outer HBox actual: {self.hbox2_frame.size().width()}x{self.hbox2_frame.size().height()}")

        print("\n[MAIN CONTAINER]")
        print(f"  Main VBox sizeHint: {self.main_frame.sizeHint().width()}x{self.main_frame.sizeHint().height()}")
        print(f"  Main VBox actual size: {self.main_frame.size().width()}x{self.main_frame.size().height()}")

        print("\n[KEY OBSERVATIONS]")
        print("  - Button 2 has longest text in Part 1, affecting HBox width")
        print("  - Part 3's nested VBox height = sum of 4 buttons + spacing + margins")
        print("  - Main VBox height = sum of all 3 parts + spacing + margins")
        print("  - Size policies affect how extra space is distributed, not sizeHint")
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
    """Run the size propagation demo."""
    app = QApplication(sys.argv)
    demo = PropagationDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("NESTED LAYOUT SIZE PROPAGATION DEMO")
    print("=" * 80)
    print("\nKey Concepts:")
    print("  - Size hints propagate BOTTOM-UP (from widgets to parent layouts)")
    print("  - Each layout's sizeHint = sum of children's sizeHints + spacing + margins")
    print("  - Size policies control how extra space is distributed, not the sizeHint")
    print("\nStructure:")
    print("  Main VBox (Purple) contains:")
    print("    1. HBox (Orange) with 3 buttons - shows horizontal propagation")
    print("    2. Single button - simplest case")
    print("    3. HBox (Green) with nested VBox (Blue) - shows 2-level nesting")
    print("       The VBox contains buttons with different size policies")
    print("\nTry:")
    print("  1. Resize the window - watch the 'Size Information' window update")
    print("  2. Notice how Button 2's longer text affects Part 1's width")
    print("  3. Observe how Expanding button in Part 3 takes extra space")
    print("  4. Click 'Print...' for detailed propagation calculations")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
