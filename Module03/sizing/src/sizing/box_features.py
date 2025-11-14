import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class SizeInfoWindow(QWidget):
    """Separate window displaying layout information."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Layout Information")
        self.setMinimumSize(500, 600)

        layout = QVBoxLayout()

        title = QLabel("Layout Contents")
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


class BoxFeaturesDemo(QWidget):
    """Demo showing box layout features: addWidget, addStrut, addSpacing, addStretch."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Box Layout Features Demo")
        self.setMinimumSize(900, 700)

        # Create the separate info window
        self.info_window = SizeInfoWindow()
        self.info_window.show()

        # Position windows side by side
        self.move(100, 100)
        self.info_window.move(1020, 100)

        # Counter for button names
        self.button_counter = 1

        # Track items in layout for info display
        self.layout_items = []

        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Box Layout Features Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "Dynamically add items to the HBox below.\n"
            "Experiment with different combinations to see how they interact."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Explanation
        explanation_group = QGroupBox("Box Layout Features")
        explanation_layout = QVBoxLayout()

        explanation_text = QLabel(
            "• addWidget(button): Adds a widget to the layout\n"
            "• addStrut(size): Adds minimum perpendicular dimension (fixed size)\n"
            "• addSpacing(size): Adds fixed spacing (doesn't grow/shrink)\n"
            "• addStretch(factor): Adds flexible space (grows/shrinks)\n"
            "• setContentsMargins(): Sets margins around the layout\n"
            "• setSpacing(): Sets spacing between all items"
        )
        explanation_text.setWordWrap(True)
        explanation_layout.addWidget(explanation_text)

        explanation_group.setLayout(explanation_layout)
        main_layout.addWidget(explanation_group)
        main_layout.addSpacing(15)

        # Layout display area
        demo_label = QLabel("HBox Layout (items added from left to right):")
        main_layout.addWidget(demo_label)

        self.box_container = QFrame()
        self.box_container.setFrameShape(QFrame.Shape.Box)
        self.box_container.setLineWidth(2)
        self.box_layout = QHBoxLayout()
        self.box_layout.setContentsMargins(10, 10, 10, 10)
        self.box_layout.setSpacing(5)
        self.box_container.setLayout(self.box_layout)

        main_layout.addWidget(self.box_container)
        main_layout.addSpacing(15)

        # Controls area
        controls_group = QGroupBox("Add Items to Layout")
        controls_layout = QGridLayout()

        # Row 0: Button
        controls_layout.addWidget(QLabel("Button Stretch:"), 0, 0)
        self.button_stretch_spin = QSpinBox()
        self.button_stretch_spin.setRange(0, 10)
        self.button_stretch_spin.setValue(0)
        controls_layout.addWidget(self.button_stretch_spin, 0, 1)

        add_button_btn = QPushButton("Add Button")
        add_button_btn.clicked.connect(self.add_button)
        controls_layout.addWidget(add_button_btn, 0, 2)

        # Row 1: Strut
        controls_layout.addWidget(QLabel("Strut Size:"), 1, 0)
        self.strut_spin = QSpinBox()
        self.strut_spin.setRange(10, 200)
        self.strut_spin.setValue(50)
        controls_layout.addWidget(self.strut_spin, 1, 1)

        add_strut_btn = QPushButton("Add Strut")
        add_strut_btn.clicked.connect(self.add_strut)
        controls_layout.addWidget(add_strut_btn, 1, 2)

        # Row 2: Spacing
        controls_layout.addWidget(QLabel("Spacing Size:"), 2, 0)
        self.spacing_value_spin = QSpinBox()
        self.spacing_value_spin.setRange(5, 200)
        self.spacing_value_spin.setValue(20)
        controls_layout.addWidget(self.spacing_value_spin, 2, 1)

        add_spacing_btn = QPushButton("Add Spacing")
        add_spacing_btn.clicked.connect(self.add_spacing)
        controls_layout.addWidget(add_spacing_btn, 2, 2)

        # Row 3: Stretch
        controls_layout.addWidget(QLabel("Stretch Factor:"), 3, 0)
        self.stretch_spin = QSpinBox()
        self.stretch_spin.setRange(1, 10)
        self.stretch_spin.setValue(1)
        controls_layout.addWidget(self.stretch_spin, 3, 1)

        add_stretch_btn = QPushButton("Add Stretch")
        add_stretch_btn.clicked.connect(self.add_stretch)
        controls_layout.addWidget(add_stretch_btn, 3, 2)

        # Row 4: Clear button
        clear_btn = QPushButton("Clear All Items")
        clear_btn.clicked.connect(self.clear_layout)
        controls_layout.addWidget(clear_btn, 4, 0, 1, 3)

        controls_group.setLayout(controls_layout)
        main_layout.addWidget(controls_group)
        main_layout.addSpacing(15)

        # Layout property controls
        properties_group = QGroupBox("Layout Properties")
        properties_layout = QVBoxLayout()

        # Margins
        margins_row = QHBoxLayout()
        margins_row.addWidget(QLabel("Contents Margins:"))

        margins_row.addWidget(QLabel("L:"))
        self.margin_left_spin = QSpinBox()
        self.margin_left_spin.setRange(0, 100)
        self.margin_left_spin.setValue(10)
        self.margin_left_spin.valueChanged.connect(self.update_margins)
        margins_row.addWidget(self.margin_left_spin)

        margins_row.addWidget(QLabel("T:"))
        self.margin_top_spin = QSpinBox()
        self.margin_top_spin.setRange(0, 100)
        self.margin_top_spin.setValue(10)
        self.margin_top_spin.valueChanged.connect(self.update_margins)
        margins_row.addWidget(self.margin_top_spin)

        margins_row.addWidget(QLabel("R:"))
        self.margin_right_spin = QSpinBox()
        self.margin_right_spin.setRange(0, 100)
        self.margin_right_spin.setValue(10)
        self.margin_right_spin.valueChanged.connect(self.update_margins)
        margins_row.addWidget(self.margin_right_spin)

        margins_row.addWidget(QLabel("B:"))
        self.margin_bottom_spin = QSpinBox()
        self.margin_bottom_spin.setRange(0, 100)
        self.margin_bottom_spin.setValue(10)
        self.margin_bottom_spin.valueChanged.connect(self.update_margins)
        margins_row.addWidget(self.margin_bottom_spin)

        margins_row.addStretch()

        properties_layout.addLayout(margins_row)

        # Spacing
        spacing_row = QHBoxLayout()
        spacing_row.addWidget(QLabel("Layout Spacing:"))
        self.layout_spacing_spin = QSpinBox()
        self.layout_spacing_spin.setRange(0, 50)
        self.layout_spacing_spin.setValue(5)
        self.layout_spacing_spin.valueChanged.connect(self.update_spacing)
        spacing_row.addWidget(self.layout_spacing_spin)
        spacing_row.addStretch()

        properties_layout.addLayout(spacing_row)

        properties_group.setLayout(properties_layout)
        main_layout.addWidget(properties_group)

        self.setLayout(main_layout)

        # Initial info update
        self.update_info()

    def add_button(self):
        """Add a button to the layout."""
        button = QPushButton(f"Btn {self.button_counter}")
        self.button_counter += 1
        stretch = self.button_stretch_spin.value()
        self.box_layout.addWidget(button, stretch)
        stretch_info = f", stretch={stretch}" if stretch > 0 else ""
        self.layout_items.append(("Widget", f"{button.text()}{stretch_info}", button))
        self.update_info()

    def add_strut(self):
        """Add a strut to the layout."""
        size = self.strut_spin.value()
        self.box_layout.addStrut(size)
        self.layout_items.append(("Strut", f"{size}px", None))
        self.update_info()

    def add_spacing(self):
        """Add spacing to the layout."""
        size = self.spacing_value_spin.value()
        self.box_layout.addSpacing(size)
        self.layout_items.append(("Spacing", f"{size}px", None))
        self.update_info()

    def add_stretch(self):
        """Add stretch to the layout."""
        factor = self.stretch_spin.value()
        self.box_layout.addStretch(factor)
        self.layout_items.append(("Stretch", f"factor={factor}", None))
        self.update_info()

    def clear_layout(self):
        """Clear all items from the layout."""
        # Remove all widgets and items
        while self.box_layout.count():
            item = self.box_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.layout_items.clear()
        self.button_counter = 1
        self.update_info()

    def update_margins(self):
        """Update the layout's contents margins."""
        self.box_layout.setContentsMargins(
            self.margin_left_spin.value(),
            self.margin_top_spin.value(),
            self.margin_right_spin.value(),
            self.margin_bottom_spin.value(),
        )
        self.update_info()

    def update_spacing(self):
        """Update the layout's spacing."""
        self.box_layout.setSpacing(self.layout_spacing_spin.value())
        self.update_info()

    def update_info(self):
        """Update the info window with layout information."""
        margins = self.box_layout.contentsMargins()
        spacing = self.box_layout.spacing()

        info_lines = []
        info_lines.append("Layout Properties:\n")
        info_lines.append(f"  Contents Margins: L={margins.left()}, T={margins.top()}, "
                         f"R={margins.right()}, B={margins.bottom()}\n")
        info_lines.append(f"  Spacing: {spacing}px\n")
        info_lines.append(f"  Container size: {self.box_container.size().width()}x"
                         f"{self.box_container.size().height()}\n\n")

        info_lines.append(f"Layout Items (count={len(self.layout_items)}):\n")

        if not self.layout_items:
            info_lines.append("  (empty - add items using the controls)\n")
        else:
            for i, (item_type, description, widget) in enumerate(self.layout_items, 1):
                info_lines.append(f"  {i}. {item_type}: {description}")
                if widget:
                    info_lines.append(f" - size: {widget.size().width()}x{widget.size().height()}")
                info_lines.append("\n")

        info_lines.append("\nHow Items Work:\n")
        info_lines.append("  • Widgets: Take space based on sizeHint and sizePolicy\n")
        info_lines.append("  • Strut: Sets minimum perpendicular size for layout\n")
        info_lines.append("  • Spacing: Fixed space, never changes\n")
        info_lines.append("  • Stretch: Flexible space, grows/shrinks to fill available space\n")

        self.info_window.update_info("".join(info_lines))

    def resizeEvent(self, event):
        """Update info when window is resized."""
        super().resizeEvent(event)
        self.update_info()

    def showEvent(self, event):
        """Update info when window is shown."""
        super().showEvent(event)
        self.update_info()

    def closeEvent(self, event):
        """Close the info window and exit when main window closes."""
        self.info_window.close()
        event.accept()
        QApplication.quit()


def main():
    """Run the box features demo."""
    app = QApplication(sys.argv)
    demo = BoxFeaturesDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("BOX LAYOUT FEATURES DEMO")
    print("=" * 80)
    print("\nBox Layout Methods:")
    print("  addWidget(widget): Adds a widget to the layout")
    print("  addStrut(size): Adds minimum perpendicular dimension")
    print("    - In HBox: sets minimum height")
    print("    - In VBox: sets minimum width")
    print("  addSpacing(size): Adds fixed spacing that never changes")
    print("  addStretch(factor): Adds flexible space that grows/shrinks")
    print("\nLayout Properties:")
    print("  setContentsMargins(l,t,r,b): Sets margins around layout edges")
    print("  setSpacing(size): Sets spacing between ALL items in layout")
    print("\nKey Differences:")
    print("  - Spacing vs Stretch:")
    print("    Spacing = fixed size, never changes")
    print("    Stretch = flexible, grows to fill available space")
    print("  - Layout spacing vs addSpacing:")
    print("    Layout spacing affects space between ALL items")
    print("    addSpacing adds ONE fixed-size spacer item")
    print("\nExperiments to Try:")
    print("  1. Add several buttons - see them arranged horizontally")
    print("  2. Add stretch before/after buttons - see buttons pushed to edges")
    print("  3. Add spacing - see fixed gaps that don't change on resize")
    print("  4. Add strut - see how it sets minimum height for the layout")
    print("  5. Adjust contents margins - see space around all items")
    print("  6. Adjust layout spacing - see space between items change")
    print("  7. Try: Button, Stretch(1), Button, Spacing(50), Button")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
