import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
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


class LayoutFrame(QFrame):
    """A frame that visualizes a layout with its size information."""

    def __init__(self, level_name, level_color, parent=None):
        super().__init__(parent)
        self.level_name = level_name
        self.level_color = level_color

        # Visual styling to show nesting
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setStyleSheet(f"QFrame {{ border: 2px solid {level_color}; }}")

    def get_info(self):
        """Get size information as a string."""
        layout = self.layout()
        if layout:
            margins = layout.contentsMargins()
            spacing = layout.spacing()
            info = (
                f"{self.level_name}:\n"
                f"  Frame size: {self.size().width()}x{self.size().height()}\n"
                f"  sizeHint: {self.sizeHint().width()}x{self.sizeHint().height()}\n"
                f"  Margins: L={margins.left()} T={margins.top()} "
                f"R={margins.right()} B={margins.bottom()}\n"
                f"  Spacing: {spacing}\n"
            )
            return info
        return f"{self.level_name}: No layout\n"


class SizeInfoButton(QPushButton):
    """A button that can report its size information."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)

    def get_info(self):
        """Get size information as a string."""
        info = (
            f"  Button ({self.text()}):\n"
            f"    Size: {self.size().width()}x{self.size().height()}\n"
            f"    sizeHint: {self.sizeHint().width()}x{self.sizeHint().height()}\n"
        )
        return info


class LayoutControlPanel(QWidget):
    """Control panel for adjusting layout margins and spacing."""

    def __init__(self, layout_frame, title, update_callback, parent=None):
        super().__init__(parent)
        self.layout_frame = layout_frame
        self.update_callback = update_callback

        main_layout = QVBoxLayout()
        group = QGroupBox(title)
        group_layout = QVBoxLayout()

        # Margins controls
        margins_label = QLabel("Margins:")
        group_layout.addWidget(margins_label)

        margins_row1 = QHBoxLayout()
        margins_row1.addWidget(QLabel("Left:"))
        self.margin_left_spin = QSpinBox()
        self.margin_left_spin.setRange(0, 100)
        self.margin_left_spin.setValue(0)
        self.margin_left_spin.valueChanged.connect(self.update_layout_properties)
        margins_row1.addWidget(self.margin_left_spin)

        margins_row1.addWidget(QLabel("Top:"))
        self.margin_top_spin = QSpinBox()
        self.margin_top_spin.setRange(0, 100)
        self.margin_top_spin.setValue(0)
        self.margin_top_spin.valueChanged.connect(self.update_layout_properties)
        margins_row1.addWidget(self.margin_top_spin)

        group_layout.addLayout(margins_row1)

        margins_row2 = QHBoxLayout()
        margins_row2.addWidget(QLabel("Right:"))
        self.margin_right_spin = QSpinBox()
        self.margin_right_spin.setRange(0, 100)
        self.margin_right_spin.setValue(0)
        self.margin_right_spin.valueChanged.connect(self.update_layout_properties)
        margins_row2.addWidget(self.margin_right_spin)

        margins_row2.addWidget(QLabel("Bottom:"))
        self.margin_bottom_spin = QSpinBox()
        self.margin_bottom_spin.setRange(0, 100)
        self.margin_bottom_spin.setValue(0)
        self.margin_bottom_spin.valueChanged.connect(self.update_layout_properties)
        margins_row2.addWidget(self.margin_bottom_spin)

        group_layout.addLayout(margins_row2)

        # Spacing control
        spacing_layout = QHBoxLayout()
        spacing_layout.addWidget(QLabel("Spacing:"))
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setRange(0, 100)
        self.spacing_spin.setValue(6)
        self.spacing_spin.valueChanged.connect(self.update_layout_properties)
        spacing_layout.addWidget(self.spacing_spin)

        group_layout.addLayout(spacing_layout)

        group.setLayout(group_layout)
        main_layout.addWidget(group)
        self.setLayout(main_layout)

    def update_layout_properties(self):
        """Update the layout's margins and spacing based on spinbox values."""
        layout = self.layout_frame.layout()
        if layout:
            layout.setContentsMargins(
                self.margin_left_spin.value(),
                self.margin_top_spin.value(),
                self.margin_right_spin.value(),
                self.margin_bottom_spin.value(),
            )
            layout.setSpacing(self.spacing_spin.value())
            self.update_callback()


class NestedLayoutDemo(QWidget):
    """Main demo window showing nested layout size computation."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nested Layout Margins & Spacing Demo")
        self.setMinimumSize(800, 600)

        # Create the separate info window
        self.info_window = SizeInfoWindow()
        self.info_window.show()

        # Position windows side by side
        self.move(100, 100)
        self.info_window.move(920, 100)

        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Nested Layout Margins & Spacing Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "This demo shows how margins and spacing accumulate through nested layouts.\n"
            "Adjust the controls to see how they affect total size. Watch the 'Size Information' window."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Main content area
        content_layout = QHBoxLayout()

        # Left side: Nested layout visualization
        left_column_layout = QVBoxLayout()

        viz_label = QLabel("Nested Layout Visualization:")
        left_column_layout.addWidget(viz_label)

        # Create the nested structure
        # Level 1: Outer frame (Red)
        self.outer_frame = LayoutFrame("Level 1 (Outer)", "#cc0000")
        outer_layout = QVBoxLayout()
        self.outer_frame.setLayout(outer_layout)

        # Level 2: Middle frame (Blue)
        self.middle_frame = LayoutFrame("Level 2 (Middle)", "#0000cc")
        middle_layout = QHBoxLayout()
        self.middle_frame.setLayout(middle_layout)

        # Level 3: Inner frame (Green)
        self.inner_frame = LayoutFrame("Level 3 (Inner)", "#00aa00")
        inner_layout = QVBoxLayout()
        self.inner_frame.setLayout(inner_layout)

        # Add buttons to innermost layout
        self.button1 = SizeInfoButton("Button 1")
        self.button2 = SizeInfoButton("Button 2")
        inner_layout.addWidget(self.button1)
        inner_layout.addWidget(self.button2)

        # Nest the layouts
        middle_layout.addWidget(self.inner_frame)
        outer_layout.addWidget(self.middle_frame)

        left_column_layout.addWidget(self.outer_frame)

        content_layout.addLayout(left_column_layout, 3)

        # Right side: Control panels
        controls_layout = QVBoxLayout()

        controls_label = QLabel("Layout Controls:")
        controls_layout.addWidget(controls_label)
        controls_layout.addSpacing(10)

        self.outer_controls = LayoutControlPanel(self.outer_frame, "Level 1 (Red)", self.update_all_info)
        controls_layout.addWidget(self.outer_controls)

        self.middle_controls = LayoutControlPanel(self.middle_frame, "Level 2 (Blue)", self.update_all_info)
        controls_layout.addWidget(self.middle_controls)

        self.inner_controls = LayoutControlPanel(self.inner_frame, "Level 3 (Green)", self.update_all_info)
        controls_layout.addWidget(self.inner_controls)

        controls_layout.addStretch()

        content_layout.addLayout(controls_layout, 2)

        main_layout.addLayout(content_layout)
        main_layout.addSpacing(15)

        # Print info button
        print_button = QPushButton("Print All Size Info to Console")
        print_button.clicked.connect(self.print_all_info)
        main_layout.addWidget(print_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def update_all_info(self):
        """Update the info window with all widget information."""
        info_lines = []

        info_lines.append(self.outer_frame.get_info())
        info_lines.append(self.middle_frame.get_info())
        info_lines.append(self.inner_frame.get_info())
        info_lines.append(self.button1.get_info())
        info_lines.append(self.button2.get_info())

        self.info_window.update_info("".join(info_lines))

    def print_all_info(self):
        """Print detailed size information to console."""
        print("\n" + "=" * 80)
        print("NESTED LAYOUT SIZE COMPUTATION DETAILS")
        print("=" * 80)

        print("\n--- WIDGET LEVEL (Innermost) ---")
        print(f"Button 1: {self.button1.size().width()}x{self.button1.size().height()}")
        print(f"  sizeHint: {self.button1.sizeHint().width()}x{self.button1.sizeHint().height()}")
        print(f"Button 2: {self.button2.size().width()}x{self.button2.size().height()}")
        print(f"  sizeHint: {self.button2.sizeHint().width()}x{self.button2.sizeHint().height()}")

        print("\n--- LEVEL 3 (Inner Frame - Green) ---")
        inner_layout = self.inner_frame.layout()
        inner_margins = inner_layout.contentsMargins()
        print(f"Frame size: {self.inner_frame.size().width()}x{self.inner_frame.size().height()}")
        print(f"sizeHint: {self.inner_frame.sizeHint().width()}x{self.inner_frame.sizeHint().height()}")
        print(f"Margins: L={inner_margins.left()}, T={inner_margins.top()}, R={inner_margins.right()}, B={inner_margins.bottom()}")
        print(f"Spacing: {inner_layout.spacing()}")
        print(f"Total margin contribution: H={inner_margins.left() + inner_margins.right()}, V={inner_margins.top() + inner_margins.bottom()}")

        print("\n--- LEVEL 2 (Middle Frame - Blue) ---")
        middle_layout = self.middle_frame.layout()
        middle_margins = middle_layout.contentsMargins()
        print(f"Frame size: {self.middle_frame.size().width()}x{self.middle_frame.size().height()}")
        print(f"sizeHint: {self.middle_frame.sizeHint().width()}x{self.middle_frame.sizeHint().height()}")
        print(f"Margins: L={middle_margins.left()}, T={middle_margins.top()}, R={middle_margins.right()}, B={middle_margins.bottom()}")
        print(f"Spacing: {middle_layout.spacing()}")
        print(f"Total margin contribution: H={middle_margins.left() + middle_margins.right()}, V={middle_margins.top() + middle_margins.bottom()}")

        print("\n--- LEVEL 1 (Outer Frame - Red) ---")
        outer_layout = self.outer_frame.layout()
        outer_margins = outer_layout.contentsMargins()
        print(f"Frame size: {self.outer_frame.size().width()}x{self.outer_frame.size().height()}")
        print(f"sizeHint: {self.outer_frame.sizeHint().width()}x{self.outer_frame.sizeHint().height()}")
        print(f"Margins: L={outer_margins.left()}, T={outer_margins.top()}, R={outer_margins.right()}, B={outer_margins.bottom()}")
        print(f"Spacing: {outer_layout.spacing()}")
        print(f"Total margin contribution: H={outer_margins.left() + outer_margins.right()}, V={outer_margins.top() + outer_margins.bottom()}")

        print("\n--- SIZE COMPUTATION SUMMARY ---")
        total_h_margins = (
            inner_margins.left() + inner_margins.right() +
            middle_margins.left() + middle_margins.right() +
            outer_margins.left() + outer_margins.right()
        )
        total_v_margins = (
            inner_margins.top() + inner_margins.bottom() +
            middle_margins.top() + middle_margins.bottom() +
            outer_margins.top() + outer_margins.bottom()
        )
        print(f"Total horizontal margins across all levels: {total_h_margins}")
        print(f"Total vertical margins across all levels: {total_v_margins}")
        print(f"Inner frame spacing (between buttons): {inner_layout.spacing()}")
        print(f"\nKey insight: Each nesting level adds its margins to the total size!")
        print("=" * 80 + "\n")

    def resizeEvent(self, event):
        """Update all info when window is resized."""
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
    """Run the nested layout demo."""
    app = QApplication(sys.argv)
    demo = NestedLayoutDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("NESTED LAYOUT SIZE COMPUTATION DEMO")
    print("=" * 80)
    print("\nKey Concepts:")
    print("  - Layouts can be nested inside other layouts")
    print("  - Each layout adds its own margins and spacing to the total size")
    print("  - Size requirements propagate UP from inner widgets to outer layouts")
    print("  - The outer layout's sizeHint includes ALL nested content plus margins")
    print("\nLayout Structure:")
    print("  Level 1 (Red/Outer): VBoxLayout - outermost container")
    print("  Level 2 (Blue/Middle): HBoxLayout - nested inside Level 1")
    print("  Level 3 (Green/Inner): VBoxLayout - contains the actual buttons")
    print("\nTry:")
    print("  1. Start with all margins at 0 - see the baseline sizes")
    print("  2. Add 10px margins to Level 3 - watch how it affects Level 2 and Level 1")
    print("  3. Add 10px margins to Level 2 - see the cumulative effect")
    print("  4. Add 10px margins to Level 1 - observe total size growth")
    print("  5. Increase spacing in Level 3 - see how it affects button arrangement")
    print("  6. Resize the window - see how extra space is distributed")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
