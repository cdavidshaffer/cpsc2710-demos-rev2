from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QValidator
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)


class RequiredFieldValidator(QValidator):
    """Validator that requires non-empty input."""

    def validate(self, input_str, pos):
        if not input_str.strip():
            return (QValidator.State.Intermediate, input_str, pos)
        return (QValidator.State.Acceptable, input_str, pos)


class AddCatDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Cat")
        self.setMinimumWidth(400)
        self.validation_attempted = False

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("Add a New Cat to Gallery")
        header.setObjectName("dialogHeader")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Form section
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter cat's name")
        self.name_input.setObjectName("nameInput")
        self.name_input.setValidator(RequiredFieldValidator())
        form_layout.addRow("Name:", self.name_input)

        self.breed_combo = QComboBox()
        self.breed_combo.addItem("")  # Empty default selection
        self.breed_combo.addItems(
            ["Persian", "Siamese", "Maine Coon", "Bengal", "Ragdoll", "Mixed"]
        )
        form_layout.addRow("Breed:", self.breed_combo)

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Age in years")
        self.age_input.setValidator(QIntValidator(0, 99))
        form_layout.addRow("Age:", self.age_input)

        self.description_input = QPlainTextEdit()
        self.description_input.setPlaceholderText("Describe your cat...")
        self.description_input.setMaximumHeight(100)
        # Note: QPlainTextEdit doesn't natively support validators, but we'll attach one for manual checking
        self.description_validator = RequiredFieldValidator()
        form_layout.addRow("Description:", self.description_input)

        layout.addLayout(form_layout)

        # Store all validated widgets for easy access
        self.validated_widgets = [
            self.name_input,
            self.breed_combo,
            self.age_input,
            self.description_input,
        ]

        # Checkboxes
        checkbox_layout = QHBoxLayout()

        self.favorite_check = QCheckBox("Mark as Favorite")
        checkbox_layout.addWidget(self.favorite_check)

        self.adopted_check = QCheckBox("Already Adopted")
        checkbox_layout.addWidget(self.adopted_check)

        checkbox_layout.addStretch()
        layout.addLayout(checkbox_layout)

        # Dialog buttons
        button_box = QDialogButtonBox()

        self.save_button = QPushButton("Save Cat")
        self.save_button.setObjectName("saveButton")
        self.save_button.setDefault(True)
        button_box.addButton(self.save_button, QDialogButtonBox.ButtonRole.AcceptRole)

        self.cancel_button = QPushButton("Cancel")
        button_box.addButton(self.cancel_button, QDialogButtonBox.ButtonRole.RejectRole)

        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)

        # Connect input changes to validation (only after first attempt)
        self.name_input.textChanged.connect(self.on_input_changed)
        self.age_input.textChanged.connect(self.on_input_changed)
        self.description_input.textChanged.connect(self.on_input_changed)
        self.breed_combo.currentTextChanged.connect(self.on_input_changed)

    def get_cat_name(self):
        return self.name_input.text() or "Unnamed Cat"

    def get_cat_breed(self):
        return self.breed_combo.currentText()

    def validate_widget(self, widget):
        """Validate a single widget and update its invalid property."""
        is_valid = False

        # Use hasAcceptableInput() for QLineEdit widgets with validators
        if hasattr(widget, "hasAcceptableInput") and widget.validator():
            is_valid = widget.hasAcceptableInput()

        # QComboBox: check if selection is not empty
        elif isinstance(widget, QComboBox):
            is_valid = bool(widget.currentText().strip())

        # QPlainTextEdit: use manual validator check
        elif widget == self.description_input:
            state, _, _ = self.description_validator.validate(widget.toPlainText(), 0)
            is_valid = state == QValidator.State.Acceptable

        # Set the invalid property based on validation result
        widget.setProperty("invalid", "false" if is_valid else "true")

        # Force style refresh for this widget
        widget.style().unpolish(widget)
        widget.style().polish(widget)

        return is_valid

    def validate_inputs(self):
        """Validate all required inputs and set invalid property."""
        is_valid = True

        # Validate all widgets
        for widget in self.validated_widgets:
            if not self.validate_widget(widget):
                is_valid = False

        return is_valid

    def on_input_changed(self):
        """Re-validate inputs when they change (only after first save attempt)."""
        if self.validation_attempted:
            # Only validate the widget that changed
            sender = self.sender()
            if sender in self.validated_widgets:
                self.validate_widget(sender)

    def validate_and_accept(self):
        """Validate inputs before accepting the dialog."""
        self.validation_attempted = True

        if self.validate_inputs():
            self.accept()
        else:
            QMessageBox.warning(
                self, "Validation Error", "Please fill in all required fields."
            )
