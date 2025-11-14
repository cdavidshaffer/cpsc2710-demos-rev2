import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
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

        title = QLabel("Size Conflict Analysis")
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


class ConflictScenario(QWidget):
    """Widget displaying a single conflict scenario."""

    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        self.scenario_title = title
        self.scenario_description = description
        self.setup_ui()

    def setup_ui(self):
        """Set up the scenario UI."""
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Title
        title_label = QLabel(self.scenario_title)
        title_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(self.scenario_description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #555; font-size: 11px;")
        layout.addWidget(desc_label)

        # Container for the actual conflict demonstration
        self.demo_container = QFrame()
        self.demo_container.setFrameShape(QFrame.Shape.Box)
        self.demo_container.setLineWidth(1)
        self.demo_container.setMinimumHeight(150)
        layout.addWidget(self.demo_container)

        # Info display
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 10px; color: #666;")
        layout.addWidget(self.info_label)

        self.setLayout(layout)

    def update_info(self):
        """Update the info label with current sizes."""
        # Override in subclasses
        pass


class Scenario1_ParentMaxLessThanChildMin(ConflictScenario):
    """Scenario: Parent maximum size < child minimum size."""

    def __init__(self, parent=None):
        super().__init__(
            "Scenario 1: Parent Max < Child Min",
            "Parent has maximum size of 200x100, child button has minimum size of 300x150. "
            "What happens?",
            parent,
        )
        self.create_conflict()

    def create_conflict(self):
        """Create the conflict scenario."""
        layout = QVBoxLayout()
        self.demo_container.setLayout(layout)

        # Set parent constraints
        self.demo_container.setMaximumSize(200, 100)

        # Create child with conflicting constraints
        self.child_button = QPushButton("Child Button\n(minSize: 300x150)")
        self.child_button.setMinimumSize(300, 150)

        layout.addWidget(self.child_button)

        self.update_info()

    def update_info(self):
        """Update size information."""
        parent_max = self.demo_container.maximumSize()
        child_min = self.child_button.minimumSize()
        child_actual = self.child_button.size()

        info = (
            f"Parent maximum: {parent_max.width()}x{parent_max.height()}\n"
            f"Child minimum: {child_min.width()}x{child_min.height()}\n"
            f"Child actual size: {child_actual.width()}x{child_actual.height()}\n\n"
            f"Result: Parent constraint wins. Child is forced smaller than its minimum."
        )
        self.info_label.setText(info)

    def resizeEvent(self, event):
        """Update info on resize."""
        super().resizeEvent(event)
        self.update_info()


class Scenario2_ParentMinGreaterThanChildMax(ConflictScenario):
    """Scenario: Parent minimum size > child maximum size."""

    def __init__(self, parent=None):
        super().__init__(
            "Scenario 2: Parent Min > Child Max",
            "Parent has minimum size of 400x200, child button has maximum size of 200x100. "
            "What happens?",
            parent,
        )
        self.create_conflict()

    def create_conflict(self):
        """Create the conflict scenario."""
        layout = QVBoxLayout()
        self.demo_container.setLayout(layout)

        # Set parent constraints
        self.demo_container.setMinimumSize(400, 200)

        # Create child with conflicting constraints
        self.child_button = QPushButton("Child Button\n(maxSize: 200x100)")
        self.child_button.setMaximumSize(200, 100)

        layout.addWidget(self.child_button)

        self.update_info()

    def update_info(self):
        """Update size information."""
        parent_min = self.demo_container.minimumSize()
        child_max = self.child_button.maximumSize()
        child_actual = self.child_button.size()

        info = (
            f"Parent minimum: {parent_min.width()}x{parent_min.height()}\n"
            f"Child maximum: {child_max.width()}x{child_max.height()}\n"
            f"Child actual size: {child_actual.width()}x{child_actual.height()}\n\n"
            f"Result: Child stays at its maximum. Parent has extra space."
        )
        self.info_label.setText(info)

    def resizeEvent(self, event):
        """Update info on resize."""
        super().resizeEvent(event)
        self.update_info()


class Scenario3_MultipleChildrenExceedParent(ConflictScenario):
    """Scenario: Multiple children's combined minimum exceeds parent maximum."""

    def __init__(self, parent=None):
        super().__init__(
            "Scenario 3: Children Combined Min > Parent Max",
            "Parent has maximum width of 300px. Three buttons each want minimum 150px width. "
            "Total needed: 450px. What happens?",
            parent,
        )
        self.create_conflict()

    def create_conflict(self):
        """Create the conflict scenario."""
        layout = QHBoxLayout()
        self.demo_container.setLayout(layout)

        # Set parent constraints
        self.demo_container.setMaximumWidth(300)
        self.demo_container.setMinimumHeight(80)

        # Create children with conflicting constraints
        self.button1 = QPushButton("Button 1\n(min: 150)")
        self.button1.setMinimumWidth(150)

        self.button2 = QPushButton("Button 2\n(min: 150)")
        self.button2.setMinimumWidth(150)

        self.button3 = QPushButton("Button 3\n(min: 150)")
        self.button3.setMinimumWidth(150)

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.update_info()

    def update_info(self):
        """Update size information."""
        parent_max = self.demo_container.maximumWidth()
        total_min = sum([
            self.button1.minimumWidth(),
            self.button2.minimumWidth(),
            self.button3.minimumWidth(),
        ])

        info = (
            f"Parent maximum width: {parent_max}px\n"
            f"Children combined minimum: {total_min}px\n"
            f"Button 1 actual: {self.button1.width()}px\n"
            f"Button 2 actual: {self.button2.width()}px\n"
            f"Button 3 actual: {self.button3.width()}px\n\n"
            f"Result: All children are squeezed below their minimums proportionally."
        )
        self.info_label.setText(info)

    def resizeEvent(self, event):
        """Update info on resize."""
        super().resizeEvent(event)
        self.update_info()


class Scenario4_FixedParentFlexibleChild(ConflictScenario):
    """Scenario: Fixed-size parent with expanding child."""

    def __init__(self, parent=None):
        super().__init__(
            "Scenario 4: Fixed Parent with Expanding Child",
            "Parent has fixed size of 250x120. Child has Expanding size policy and wants more space. "
            "What happens?",
            parent,
        )
        self.create_conflict()

    def create_conflict(self):
        """Create the conflict scenario."""
        layout = QVBoxLayout()
        self.demo_container.setLayout(layout)

        # Set parent constraints
        self.demo_container.setFixedSize(250, 120)

        # Create child that wants to expand
        self.child_button = QPushButton("Expanding Child\n(wants all available space)")
        from PySide6.QtWidgets import QSizePolicy
        self.child_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.child_button)

        self.update_info()

    def update_info(self):
        """Update size information."""
        parent_size = self.demo_container.size()
        child_size = self.child_button.size()
        child_hint = self.child_button.sizeHint()

        info = (
            f"Parent fixed size: {parent_size.width()}x{parent_size.height()}\n"
            f"Child sizeHint: {child_hint.width()}x{child_hint.height()}\n"
            f"Child actual size: {child_size.width()}x{child_size.height()}\n\n"
            f"Result: Child fills parent (minus margins). Parent size is absolute."
        )
        self.info_label.setText(info)

    def resizeEvent(self, event):
        """Update info on resize."""
        super().resizeEvent(event)
        self.update_info()


class Scenario5_NestedConflicts(ConflictScenario):
    """Scenario: Nested layouts with cascading conflicts."""

    def __init__(self, parent=None):
        super().__init__(
            "Scenario 5: Nested Layout Conflicts",
            "Outer parent max=200px, middle child min=250px, inner child min=300px. "
            "Conflicts cascade through nesting levels.",
            parent,
        )
        self.create_conflict()

    def create_conflict(self):
        """Create the conflict scenario."""
        outer_layout = QVBoxLayout()
        self.demo_container.setLayout(outer_layout)

        # Outer parent constraint
        self.demo_container.setMaximumWidth(200)
        self.demo_container.setMinimumHeight(150)

        # Middle frame with conflicting constraint
        self.middle_frame = QFrame()
        self.middle_frame.setFrameShape(QFrame.Shape.Box)
        self.middle_frame.setStyleSheet("border: 1px dashed blue;")
        self.middle_frame.setMinimumWidth(250)
        middle_layout = QVBoxLayout()
        self.middle_frame.setLayout(middle_layout)

        # Inner button with even more conflicting constraint
        self.inner_button = QPushButton("Inner\n(min: 300px)")
        self.inner_button.setMinimumWidth(300)

        middle_layout.addWidget(self.inner_button)
        outer_layout.addWidget(self.middle_frame)

        self.update_info()

    def update_info(self):
        """Update size information."""
        outer_max = self.demo_container.maximumWidth()
        middle_min = self.middle_frame.minimumWidth()
        inner_min = self.inner_button.minimumWidth()

        info = (
            f"Outer max width: {outer_max}px\n"
            f"Middle min width: {middle_min}px\n"
            f"Inner min width: {inner_min}px\n"
            f"Middle actual: {self.middle_frame.width()}px\n"
            f"Inner actual: {self.inner_button.width()}px\n\n"
            f"Result: Outer constraint wins. All descendants are squeezed."
        )
        self.info_label.setText(info)

    def resizeEvent(self, event):
        """Update info on resize."""
        super().resizeEvent(event)
        self.update_info()


class SizeConflictsDemo(QWidget):
    """Main demo showing parent-child size conflicts."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parent-Child Size Conflicts Demo")
        self.setMinimumSize(900, 800)

        # Create the separate info window
        self.info_window = SizeInfoWindow()
        self.info_window.show()

        # Position windows side by side
        self.move(100, 100)
        self.info_window.move(1020, 100)

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        main_layout = QVBoxLayout()

        # Title and instructions
        title = QLabel("Parent-Child Size Conflicts Demo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        instructions = QLabel(
            "This demo shows what happens when parent and child widget size constraints conflict.\n"
            "Resize the window to see how Qt resolves these conflicts."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Key principles
        principles_group = QGroupBox("Key Principles")
        principles_layout = QVBoxLayout()

        principles_text = QLabel(
            "1. Parent constraints generally win over child constraints\n"
            "2. Children can be forced smaller than their minimum size\n"
            "3. Children may not be able to reach their maximum size\n"
            "4. Multiple children share available space when constrained\n"
            "5. Nested conflicts cascade from outermost parent down"
        )
        principles_layout.addWidget(principles_text)
        principles_group.setLayout(principles_layout)
        main_layout.addWidget(principles_group)
        main_layout.addSpacing(15)

        # Scenarios
        scenarios_label = QLabel("Conflict Scenarios:")
        scenarios_label.setStyleSheet("font-weight: bold;")
        main_layout.addWidget(scenarios_label)

        # Create all scenarios
        self.scenario1 = Scenario1_ParentMaxLessThanChildMin()
        main_layout.addWidget(self.scenario1)

        self.scenario2 = Scenario2_ParentMinGreaterThanChildMax()
        main_layout.addWidget(self.scenario2)

        self.scenario3 = Scenario3_MultipleChildrenExceedParent()
        main_layout.addWidget(self.scenario3)

        self.scenario4 = Scenario4_FixedParentFlexibleChild()
        main_layout.addWidget(self.scenario4)

        self.scenario5 = Scenario5_NestedConflicts()
        main_layout.addWidget(self.scenario5)

        main_layout.addStretch()

        self.setLayout(main_layout)

        # Update info window
        self.update_info_window()

    def update_info_window(self):
        """Update the info window with general information."""
        info = (
            "CONFLICT RESOLUTION RULES:\n\n"
            "When parent and child constraints conflict, Qt follows these rules:\n\n"
            "1. PARENT WINS: Parent's maximum size is enforced even if children need more\n"
            "2. CHILDREN SQUEEZED: Children can be forced below their minimum size\n"
            "3. PROPORTIONAL: Multiple children share limited space proportionally\n"
            "4. NO OVERFLOW: Children cannot overflow parent boundaries\n"
            "5. CASCADE: Constraints propagate through nesting levels\n\n"
            "PRACTICAL IMPLICATIONS:\n\n"
            "• Always test your UI with different window sizes\n"
            "• Be careful with fixed sizes - they're absolute\n"
            "• Use minimum/maximum carefully in nested layouts\n"
            "• Parent size policies affect all descendants\n"
            "• Scroll areas can help when content exceeds available space\n\n"
            "BEST PRACTICES:\n\n"
            "• Use size policies over hard constraints when possible\n"
            "• Test edge cases (very small/large windows)\n"
            "• Consider using QScrollArea for large content\n"
            "• Set sensible minimums on top-level windows\n"
            "• Remember: layout margins and spacing also consume space"
        )
        self.info_window.update_info(info)

    def resizeEvent(self, event):
        """Update on resize."""
        super().resizeEvent(event)
        # Scenarios update themselves

    def closeEvent(self, event):
        """Close the info window and exit when main window closes."""
        self.info_window.close()
        event.accept()
        QApplication.quit()


def main():
    """Run the size conflicts demo."""
    app = QApplication(sys.argv)
    demo = SizeConflictsDemo()
    demo.show()

    print("\n" + "=" * 80)
    print("PARENT-CHILD SIZE CONFLICTS DEMO")
    print("=" * 80)
    print("\nThis demo illustrates what happens when size constraints conflict:")
    print("\nConflict Types:")
    print("  1. Parent max < child min")
    print("  2. Parent min > child max")
    print("  3. Multiple children's combined min > parent max")
    print("  4. Fixed parent with expanding children")
    print("  5. Nested layouts with cascading conflicts")
    print("\nKey Takeaways:")
    print("  • Parent constraints take precedence")
    print("  • Children can be forced below their minimum size")
    print("  • Qt does its best to accommodate all constraints")
    print("  • When impossible, parent wins and children adapt")
    print("\nTry:")
    print("  • Resize the window to see how conflicts resolve")
    print("  • Notice how children are squeezed in Scenarios 1 and 3")
    print("  • Observe how parent minimums create extra space in Scenario 2")
    print("  • See how fixed sizes are absolute in Scenario 4")
    print("  • Watch conflicts cascade through nesting in Scenario 5")
    print("=" * 80 + "\n")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
