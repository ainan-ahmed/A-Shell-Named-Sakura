"""AppRow widget for displaying application entries in the launcher."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("AstalApps", "0.1")

from gi.repository import Gtk, AstalApps  # type: ignore  # noqa: E402


@Gtk.Template(resource_path="/com/launcher/app/app_row.ui")
class AppRow(Gtk.ListBoxRow):
    """A single row in the application launcher list."""

    __gtype_name__ = "AppRow"

    _icon = Gtk.Template.Child()
    _name_label = Gtk.Template.Child()
    _desc_label = Gtk.Template.Child()

    def __init__(self, app: AstalApps.Application):
        """
        Initialize an AppRow widget.

        Args:
            app: The AstalApps.Application instance to display
        """
        super().__init__()
        self._app = app

        self._icon.set_from_icon_name(app.get_icon_name() or "application-x-executable")
        self._name_label.set_label(app.get_name())
        self._desc_label.set_label(app.get_description() or "")

    def launch(self):
        """Launch the application associated with this row."""
        self._app.launch()

    @property
    def app(self) -> AstalApps.Application:
        """Get the underlying application object."""
        return self._app
