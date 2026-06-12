"""Color themes.  This is a first version.  We'll talk about a better 'design' of
theme classes later.
"""

from abc import ABC, abstractmethod
from typing import Optional, Protocol, Sequence, runtime_checkable

from PySide6.QtCore import QFile, QObject, Signal
from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import QApplication


class ThemeManager(QObject):
    """I hold onto a theme and pass on theme messages to it.  Normally you would access my only instance
    using the module scope variable `theme_manager`."""

    theme_changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._theme: Optional[Theme] = None

    def set_theme(self, theme: Theme):
        self._theme = theme
        self.theme_changed.emit()

    def icon(self, icon_name: str) -> QIcon:
        return self._current_theme().icon(icon_name)

    def install(self, app: QApplication) -> None:
        self._current_theme().install(app)

    def _current_theme(self) -> Theme:
        if self._theme is None:
            raise RuntimeError("Theme was not specified")
        return self._theme


theme_manager = ThemeManager()


class Theme(ABC):
    icon_path = ":/icons/default/"
    style_sheet_paths = [":/styles/default.qss"]

    def install(self, app: QApplication) -> None:
        app.setPalette(self._build_palette())
        app.setStyleSheet(self._load_style_sheets())

    @abstractmethod
    def _build_palette(self) -> QPalette: ...

    def icon(self, icon_name: str) -> QIcon:
        return QIcon(self.icon_path + icon_name)

    def _load_style_sheets(self) -> str:
        result = ""
        for style_sheet_path in self.style_sheet_paths:
            result += self._load_style_sheet(style_sheet_path) + "\n\n"
        return result

    def _load_style_sheet(self, path: str) -> str:
        file = QFile(path)
        if not file.open(QFile.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Failed to open style sheet {path}")
        result = file.readAll().toStdString()
        file.close()
        return self._substitute_theme_paths(result)

    def _substitute_theme_paths(self, input: str) -> str:
        return input.replace("{{icon_path}}", self.icon_path)


@runtime_checkable
class IconTarget(Protocol):
    def setIcon(self, icon: QIcon) -> None: ...


class ThemeableWidgetMixin:
    def _themed_icon_targets(self) -> list[tuple[IconTarget, str]]:
        if not hasattr(self, "_themed_icons"):
            self._themed_icons: list[tuple[IconTarget, str]] = []
        return self._themed_icons

    def _add_themed_icon_target(self, target: IconTarget, icon_name: str) -> None:
        self._themed_icon_targets().append((target, icon_name))
        if not hasattr(self, "_theme_manager_connected"):
            theme_manager.theme_changed.connect(self._update_icons)
            self._theme_manager_connected = True

    def _add_themed_icon_targets(
        self, targets: Sequence[tuple[IconTarget, str]]
    ) -> None:
        for target, name in targets:
            self._add_themed_icon_target(target, name)

    def _update_icons(self) -> None:
        for widget, icon_name in self._themed_icon_targets():
            widget.setIcon(theme_manager.icon(icon_name))


class LightTheme(Theme):
    """Define a light color theme."""

    icon_path = ":/icons/light/"
    style_sheet_paths = [":/styles/default.qss", ":/styles/light.qss"]

    def _build_palette(self) -> QPalette:
        p = QPalette()

        p.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        p.setColor(QPalette.ColorRole.WindowText, QColor("#000000"))
        p.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        p.setColor(QPalette.ColorRole.Text, QColor("#000000"))
        p.setColor(QPalette.ColorRole.Button, QColor("#e0e0e0"))
        p.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
        p.setColor(QPalette.ColorRole.Highlight, QColor("#2a82da"))
        p.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))

        p.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#888888")
        )
        p.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            QColor("#888888"),
        )

        return p


class DarkTheme(Theme):
    """Define a dark color theme"""

    icon_path = ":/icons/dark/"
    style_sheet_paths = [":/styles/default.qss", ":/styles/dark.qss"]

    def _build_palette(self) -> QPalette:
        p = QPalette()

        # Active / general
        p.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
        p.setColor(QPalette.ColorRole.WindowText, QColor("#dddddd"))
        p.setColor(QPalette.ColorRole.Base, QColor("#3c3c3c"))
        p.setColor(QPalette.ColorRole.Text, QColor("#eeeeee"))
        p.setColor(QPalette.ColorRole.Button, QColor("#444444"))
        p.setColor(QPalette.ColorRole.ButtonText, QColor("#dddddd"))
        p.setColor(QPalette.ColorRole.Highlight, QColor("#3d8ec9"))
        p.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))

        # Disabled (explicit!)
        p.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor("#777777")
        )
        p.setColor(
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            QColor("#777777"),
        )

        return p
