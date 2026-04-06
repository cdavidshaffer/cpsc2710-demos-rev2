"""Color themes.  This is a first version.  We'll talk about a better 'design' of
theme classes later.
"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor, QIcon, QPalette


class ThemeManager(QObject):
    """I hold onto a theme and pass on theme messages to it.  Normally you would access my only instance
    using the module scope variable `theme_manager`."""

    theme_changed = Signal()

    def __init__(self):
        super().__init__()
        self._theme = None

    def set_theme(self, theme):
        self._theme = theme
        self.theme_changed.emit()

    def icon(self, icon_name):
        return self._theme.icon(icon_name)

    def install(self, app):
        self._theme.install(app)


theme_manager = ThemeManager()


class LightTheme:
    """Define a light color theme."""

    icon_path = ":/icons/light/"

    def install(self, app):
        app.setPalette(self._build_palette())

    def _build_palette(self):
        p = QPalette()

        p.setColor(QPalette.Window, QColor("#f0f0f0"))
        p.setColor(QPalette.WindowText, QColor("#000000"))
        p.setColor(QPalette.Base, QColor("#ffffff"))
        p.setColor(QPalette.Text, QColor("#000000"))
        p.setColor(QPalette.Button, QColor("#e0e0e0"))
        p.setColor(QPalette.ButtonText, QColor("#000000"))
        p.setColor(QPalette.Highlight, QColor("#2a82da"))
        p.setColor(QPalette.HighlightedText, QColor("#ffffff"))

        p.setColor(QPalette.Disabled, QPalette.Text, QColor("#888888"))
        p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#888888"))

        return p

    def icon(self, icon_name):
        return QIcon(self.icon_path + icon_name)


class DarkTheme:
    """Define a dark color theme"""

    icon_path = ":/icons/dark/"

    def install(self, app):
        app.setPalette(self._build_palette())

    def _build_palette(self):
        p = QPalette()

        # Active / general
        p.setColor(QPalette.Window, QColor("#2b2b2b"))
        p.setColor(QPalette.WindowText, QColor("#dddddd"))
        p.setColor(QPalette.Base, QColor("#3c3c3c"))
        p.setColor(QPalette.Text, QColor("#eeeeee"))
        p.setColor(QPalette.Button, QColor("#444444"))
        p.setColor(QPalette.ButtonText, QColor("#dddddd"))
        p.setColor(QPalette.Highlight, QColor("#3d8ec9"))
        p.setColor(QPalette.HighlightedText, QColor("#ffffff"))

        # Disabled (explicit!)
        p.setColor(QPalette.Disabled, QPalette.Text, QColor("#777777"))
        p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#777777"))

        return p

    def icon(self, icon_name):
        return QIcon(self.icon_path + icon_name)
