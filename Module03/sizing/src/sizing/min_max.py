import argparse
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

NO_MIN = -1
NO_MAX = -1


class SizeDisplayButton(QPushButton):
    """A button that displays its size information."""

    def __init__(self, text, parent=None, set_expanding_policy=True):
        super().__init__(text, parent)
        self.info_label = None
        # Set size policy to Expanding in both directions to better demonstrate min/max constraints
        if set_expanding_policy:
            self.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

    def set_info_label(self, label):
        """Set the label that will display this button's size info."""
        self.info_label = label
        self.update_info()

    def update_info(self):
        """Update the info label with current size information."""
        if self.info_label:
            info = (
                f"size: {self.size().width()}x{self.size().height()}\n"
                f"minimumSize: {self.minimumSize().width()}x{self.minimumSize().height()}\n"
                f"maximumSize: {self.maximumSize().width()}x{self.maximumSize().height()}\n"
                f"minimumSizeHint: {self.minimumSizeHint().width()}x{self.minimumSizeHint().height()}\n"
                f"sizeHint: {self.sizeHint().width()}x{self.sizeHint().height()}\n"
                f"sizePolicy: H={self.sizePolicy().horizontalPolicy()}, V={self.sizePolicy().verticalPolicy()}"
            )
            self.info_label.setText(info)

    def resizeEvent(self, event):
        """Override to update info when button is resized."""
        super().resizeEvent(event)
        self.update_info()


class InteractiveControlPanel(QWidget):
    """A control panel for adjusting button min/max sizes."""

    def __init__(self, button, title, parent=None):
        super().__init__(parent)
        self.button = button

        layout = QVBoxLayout()
        group = QGroupBox(title)
        group_layout = QVBoxLayout()

        # Minimum size controls
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("Min Width:"))
        self.min_width_spin = QSpinBox()
        self.min_width_spin.setRange(0, 1000)
        self.min_width_spin.setValue(0)
        self.min_width_spin.valueChanged.connect(self.update_button_size)
        min_layout.addWidget(self.min_width_spin)

        min_layout.addWidget(QLabel("Min Height:"))
        self.min_height_spin = QSpinBox()
        self.min_height_spin.setRange(0, 1000)
        self.min_height_spin.setValue(0)
        self.min_height_spin.valueChanged.connect(self.update_button_size)
        min_layout.addWidget(self.min_height_spin)

        group_layout.addLayout(min_layout)

        # Maximum size controls
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("Max Width:"))
        self.max_width_spin = QSpinBox()
        self.max_width_spin.setRange(0, 16777215)  # Qt's QWIDGETSIZE_MAX
        self.max_width_spin.setValue(16777215)
        self.max_width_spin.valueChanged.connect(self.update_button_size)
        max_layout.addWidget(self.max_width_spin)

        max_layout.addWidget(QLabel("Max Height:"))
        self.max_height_spin = QSpinBox()
        self.max_height_spin.setRange(0, 16777215)
        self.max_height_spin.setValue(16777215)
        self.max_height_spin.valueChanged.connect(self.update_button_size)
        max_layout.addWidget(self.max_height_spin)

        group_layout.addLayout(max_layout)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)

    def update_button_size(self):
        """Update the button's min/max size based on spinbox values."""
        self.button.setMinimumSize(
            QSize(self.min_width_spin.value(), self.min_height_spin.value())
        )
        self.button.setMaximumSize(
            QSize(self.max_width_spin.value(), self.max_height_spin.value())
        )
        self.button.update_info()


class ScenarioWindow(QWidget):
    """A window displaying only a button for demonstrating min/max size constraints."""

    def __init__(
        self,
        title,
        button_text,
        min_w,
        min_h,
        max_w,
        max_h,
        set_expanding_policy=True,
    ):
        super().__init__()
        self.setWindowTitle(title)

        main_layout = QVBoxLayout()

        # Button with size constraints - this is the ONLY widget in the window
        self.button = SizeDisplayButton(
            button_text, set_expanding_policy=set_expanding_policy
        )
        if min_w != NO_MIN:
            self.button.setMinimumSize(QSize(min_w, min_h))
        if max_w != NO_MAX:
            self.button.setMaximumSize(QSize(max_w, max_h))

        main_layout.addWidget(self.button)
        self.setLayout(main_layout)


class SizeInfoWindow(QWidget):
    """A dedicated window that displays size information for all scenario buttons."""

    def __init__(self, scenario_windows):
        super().__init__()
        self.setWindowTitle("Size Information Display")
        self.scenario_windows = scenario_windows

        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Button Size Information")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title.font()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        main_layout.addWidget(title)
        main_layout.addSpacing(10)

        # Instructions
        instructions = QLabel(
            "This window displays size information for all scenario buttons.\n"
            "Information updates automatically as you resize the scenario windows."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(15)

        # Info labels for each scenario
        self.info_labels = []
        for scenario in scenario_windows:
            # Scenario title
            scenario_title = QLabel(scenario.windowTitle())
            scenario_title.setStyleSheet("font-weight: bold; font-size: 11pt;")
            main_layout.addWidget(scenario_title)

            # Info label
            info_label = QLabel()
            info_label.setWordWrap(True)
            info_label.setStyleSheet("padding-left: 15px; margin-bottom: 10px;")
            self.info_labels.append(info_label)
            main_layout.addWidget(info_label)

            # Connect button to update this info label
            scenario.button.set_info_label(info_label)

        main_layout.addSpacing(10)

        # Buttons
        button_layout = QHBoxLayout()

        refresh_button = QPushButton("Refresh All")
        refresh_button.clicked.connect(self.refresh_all)
        button_layout.addWidget(refresh_button)

        print_button = QPushButton("Print All to Console")
        print_button.clicked.connect(self.print_all_info)
        button_layout.addWidget(print_button)

        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.resize(500, 700)

    def refresh_all(self):
        """Refresh size information for all buttons."""
        for scenario in self.scenario_windows:
            scenario.button.update_info()

    def print_all_info(self):
        """Print size information for all buttons to console."""
        print("\n" + "=" * 80)
        print("SIZE INFORMATION FOR ALL SCENARIO BUTTONS")
        print("=" * 80)

        for scenario in self.scenario_windows:
            button = scenario.button
            print(f"\n{scenario.windowTitle()}")
            print(f"  Button text: '{button.text()}'")
            print(f"  Actual size: {button.size().width()}x{button.size().height()}")
            print(
                f"  minimumSize: {button.minimumSize().width()}x{button.minimumSize().height()}"
            )
            print(
                f"  maximumSize: {button.maximumSize().width()}x{button.maximumSize().height()}"
            )
            print(
                f"  minimumSizeHint: {button.minimumSizeHint().width()}x{button.minimumSizeHint().height()}"
            )
            print(
                f"  sizeHint: {button.sizeHint().width()}x{button.sizeHint().height()}"
            )
            print(
                f"  sizePolicy: H={button.sizePolicy().horizontalPolicy()}, V={button.sizePolicy().verticalPolicy()}"
            )

        print("\n" + "=" * 80 + "\n")


class InteractiveWindow(QWidget):
    """Interactive window with controls to adjust min/max constraints in real-time."""

    def __init__(self, set_expanding_policy=True):
        super().__init__()
        self.setWindowTitle("Interactive Min/Max Controls")

        main_layout = QVBoxLayout()

        # Instructions
        instructions = QLabel(
            "Use the controls below to adjust minimum and maximum size constraints.\n"
            "Resize the window to see how the button responds to your settings."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        main_layout.addSpacing(10)

        # Button
        self.button = SizeDisplayButton(
            "Interactive Button - Adjust Me!", set_expanding_policy=set_expanding_policy
        )
        main_layout.addWidget(self.button)
        main_layout.addSpacing(10)

        # Info label
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.button.set_info_label(self.info_label)
        main_layout.addWidget(self.info_label)
        main_layout.addSpacing(10)

        # Control panel
        control_panel = InteractiveControlPanel(self.button, "Adjust Constraints")
        main_layout.addWidget(control_panel)

        self.setLayout(main_layout)
        self.resize(700, 500)


def main():
    """Run the interactive min/max size demo with separate windows."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Min/Max size demonstration")
    parser.add_argument(
        "--no-policy",
        action="store_true",
        help="Don't set button size policy to Expanding, Expanding (leave at default)",
    )
    args = parser.parse_args()

    # Determine whether to set expanding policy
    set_expanding_policy = not args.no_policy

    app = QApplication(sys.argv)

    # Create scenario windows (each in its own window to avoid interference)
    scenario_windows = []

    # Scenario 1: No constraints
    scenario1 = ScenarioWindow(
        "Scenario 1: No Constraints",
        "This button has long text impacting minimumSizeHint",
        NO_MIN,
        NO_MIN,
        NO_MAX,
        NO_MAX,
        set_expanding_policy=set_expanding_policy,
    )
    scenario_windows.append(scenario1)

    # Scenario 2: Minimum size explicitly set to 1x1
    scenario2 = ScenarioWindow(
        "Scenario 2: Minimum Size 1x1 (Overrides minimumSizeHint)",
        "This button has long text but minimum size 1, 1",
        1,
        1,
        NO_MAX,
        NO_MAX,
        set_expanding_policy=set_expanding_policy,
    )
    scenario_windows.append(scenario2)

    # Scenario 3: Only minimum size
    scenario3 = ScenarioWindow(
        "Scenario 3: Only Minimum Size (150x50)",
        "Short",
        150,
        50,
        NO_MAX,
        NO_MAX,
        set_expanding_policy=set_expanding_policy,
    )
    scenario_windows.append(scenario3)

    # Scenario 4: Only maximum size
    scenario4 = ScenarioWindow(
        "Scenario 4: Only Maximum Size (200x40)",
        "This button has a long label that would normally be wider",
        NO_MIN,
        NO_MIN,
        200,
        40,
        set_expanding_policy=set_expanding_policy,
    )
    scenario_windows.append(scenario4)

    # Scenario 5: Both min and max
    scenario5 = ScenarioWindow(
        "Scenario 5: Both Min (100x30) and Max (300x60)",
        "Medium Label",
        100,
        30,
        300,
        60,
        set_expanding_policy=set_expanding_policy,
    )
    scenario_windows.append(scenario5)

    # Create size info window that displays information for all scenarios
    info_window = SizeInfoWindow(scenario_windows)

    # Position scenario windows in a vertical column on the left
    scenario_x = 350
    scenario_y = 200
    scenario_spacing = 250  # Vertical spacing between scenario windows

    for index, window in enumerate(scenario_windows):
        window.move(scenario_x, scenario_y + index * scenario_spacing)
        window.show()

    # Position info window to the right of scenarios
    info_window.move(scenario_x + 450, scenario_y)
    info_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
