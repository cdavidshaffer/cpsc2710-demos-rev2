import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SpongeBobFormDemo(QWidget):
    """Demo showing a VBox layout with a title label and a form with SpongeBob themed widgets."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpongeBob Form Demo")

        main_layout = QVBoxLayout()

        title = QLabel("Bikini Bottom Employee Registration Form")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Bottom component: Form layout with SpongeBob themed widgets
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )

        name_edit = QLineEdit()
        name_edit.setPlaceholderText("e.g., SpongeBob SquarePants")
        form_layout.addRow("Employee Name:", name_edit)

        position_combo = QComboBox()
        position_combo.addItems(
            [
                "Fry Cook",
                "Cashier",
                "Manager",
                "Jellyfish Hunter",
                "Superhero",
                "Bubble Blower",
            ]
        )
        form_layout.addRow("Position:", position_combo)

        experience_spin = QSpinBox()
        experience_spin.setRange(0, 50)
        experience_spin.setValue(0)
        experience_spin.setSuffix(" years")
        form_layout.addRow("Experience:", experience_spin)

        activity_edit = QLineEdit()
        activity_edit.setText("Jellyfishing")
        form_layout.addRow("Favorite Activity:", activity_edit)

        friend_edit = QLineEdit()
        friend_edit.setText("Patrick Star")
        form_layout.addRow("Best Friend:", friend_edit)

        address_edit = QLineEdit()
        address_edit.setText("124 Conch Street")
        form_layout.addRow("Address:", address_edit)

        pet_combo = QComboBox()
        pet_combo.addItems(
            [
                "Gary (snail)",
                "No pet",
                "Mystery (sea horse)",
                "Rex (worm)",
                "Spot (amoeba)",
            ]
        )
        form_layout.addRow("Pet:", pet_combo)

        skills_layout = QVBoxLayout()
        karate_check = QCheckBox("Karate")
        karate_check.setChecked(True)
        skills_layout.addWidget(karate_check)

        bubble_check = QCheckBox("Bubble Blowing")
        bubble_check.setChecked(True)
        skills_layout.addWidget(bubble_check)

        jellyfishing_check = QCheckBox("Jellyfishing")
        jellyfishing_check.setChecked(True)
        skills_layout.addWidget(jellyfishing_check)

        cooking_check = QCheckBox("Krabby Patty Cooking")
        cooking_check.setChecked(True)
        skills_layout.addWidget(cooking_check)

        form_layout.addRow("Skills:", skills_layout)

        catchphrase_edit = QTextEdit()
        catchphrase_edit.setPlaceholderText("Enter your catchphrase...")
        catchphrase_edit.setText("I'm ready! I'm ready!")
        form_layout.addRow("Catchphrase:", catchphrase_edit)

        # Add the form layout to the main vbox
        main_layout.addLayout(form_layout)

        self.setLayout(main_layout)


def main():
    """Run the SpongeBob form demo."""
    app = QApplication(sys.argv)
    demo = SpongeBobFormDemo()
    demo.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
