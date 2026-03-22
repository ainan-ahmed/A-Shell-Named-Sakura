"""Launcher window for searching and launching applications."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Astal", "4.0")
gi.require_version("GLib", "2.0")

from gi.repository import (  # type: ignore  # noqa: E402
    Astal,  # type: ignore
    Gdk,  # type: ignore
    GLib,  # type: ignore
    Gtk,  # type: ignore
)


@Gtk.Template(resource_path="/com/launcher/app/launcher.ui")
class Launcher(Astal.Window):
    """Main launcher window for searching and launching applications."""

    __gtype_name__ = "Launcher"

    _entry = Gtk.Template.Child()
    _list = Gtk.Template.Child()

    def __init__(self, app):
        """
        Initialize the Launcher window.

        Args:
            app: The Gtk.Application instance
        """
        super().__init__(application=app)

        # Delay project imports until the window is constructed so module load
        # order cannot interfere with GI initialization.
        from src.services.apps_service import get_apps_service
        from src.widgets.app_row import AppRow

        self._apps_service = get_apps_service()
        self._app_row_cls = AppRow

        # Signal connections
        self._entry.connect("search-changed", self._on_search_changed)
        self._entry.connect("activate", self._launch_selected)
        self._list.connect("row-activated", self._on_row_activated)

        self._populate("")

    # ── Helper Methods ────────────────────────────────────────────────────────

    def _populate(self, query: str):
        """
        Clear the list and fill it with search results.

        Args:
            query: Search query string
        """
        # Clear existing rows
        while row := self._list.get_row_at_index(0):
            self._list.remove(row)

        # Add new rows (limit to 12 results)
        for app in self._apps_service.search(query)[:12]:
            self._list.append(self._app_row_cls(app))

        # Auto-select the first result
        if first := self._list.get_row_at_index(0):
            self._list.select_row(first)

    def _launch_selected(self, *_):
        """Launch the currently selected application and hide the launcher."""
        if row := self._list.get_selected_row():
            row.launch()
            self._hide()

    def _hide(self):
        """Hide the launcher window."""
        self.set_visible(False)

    def _focus_entry(self):
        """Focus the search entry (used with GLib.timeout_add)."""
        self._entry.grab_focus()
        return False  # run once

    # ── Signal Handlers ───────────────────────────────────────────────────────

    def _on_search_changed(self, entry):
        """
        Handle search entry text changes.

        Args:
            entry: The Gtk.SearchEntry widget
        """
        self._populate(entry.get_text())

    def _on_row_activated(self, _listbox, row):
        """
        Handle row activation (double-click or Enter).

        Args:
            _listbox: The Gtk.ListBox widget
            row: The activated AppRow widget
        """
        row.launch()
        self._hide()

    @Gtk.Template.Callback()
    def _on_key_pressed(self, ctrl, keyval, keycode, state):
        """
        Handle keyboard navigation.

        Args:
            ctrl: The Gtk.EventControllerKey widget
            keyval: The key value
            keycode: The key code
            state: The modifier state

        Returns:
            True if the event was handled, False otherwise
        """
        if keyval == Gdk.KEY_Escape:
            self._hide()
            return True
        elif keyval == Gdk.KEY_Down:
            selected = self._list.get_selected_row()
            if selected:
                idx = selected.get_index() + 1
                if next_row := self._list.get_row_at_index(idx):
                    self._list.select_row(next_row)
            return True
        elif keyval == Gdk.KEY_Up:
            selected = self._list.get_selected_row()
            if selected:
                idx = selected.get_index() - 1
                if idx >= 0 and (prev_row := self._list.get_row_at_index(idx)):
                    self._list.select_row(prev_row)
            return True
        return False

    @Gtk.Template.Callback()
    def _on_overlay_click(self, gesture, n_press, x, y):
        """
        Handle clicks on the overlay (outside the launcher).

        Args:
            gesture: The Gtk.GestureClick widget
            n_press: Number of presses
            x: X coordinate
            y: Y coordinate
        """
        self._hide()

    # ── Public API ────────────────────────────────────────────────────────────

    def show_launcher(self):
        """Reset search and make the launcher visible."""
        self._entry.set_text("")
        self._populate("")
        self.set_visible(True)
        # Focus the search entry after a short delay (GTK needs the window
        # to be mapped before it accepts focus requests)
        GLib.timeout_add(50, self._focus_entry)
