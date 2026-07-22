from PySide6.QtGui import QValidator


class NonBlankValidator(QValidator):
    def validate(self, text, pos):
        stripped = text.strip()
        state = (
            QValidator.State.Acceptable
            if stripped and text == stripped
            else QValidator.State.Intermediate
        )
        return state, text, pos

    def fixup(self, text):
        return text.strip()
