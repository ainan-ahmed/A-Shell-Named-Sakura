#!/usr/bin/env python3
"""Entry point for the GTK app launcher application."""

import os
import sys
from ctypes import CDLL

import gi

# Running from XWayland terminals (for example VS Code) can make GTK pick X11,
# which disables gtk4-layer-shell. Prefer Wayland when it is available.
if os.environ.get("WAYLAND_DISPLAY"):
    os.environ.setdefault("GDK_BACKEND", "wayland")

# Load gtk4-layer-shell BEFORE importing gi.repository
CDLL("libgtk4-layer-shell.so")

gi.require_version("Gtk", "4.0")
gi.require_version("Astal", "4.0")

from gi.repository import Astal, Gio  # type: ignore # noqa: E402


class LauncherApplication(Astal.Application):
    """Application class that owns and manages the launcher window."""

    def __init__(self):
        super().__init__(
            application_id="com.launcher.app",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self._launcher = None

    def do_startup(self):
        """Initialize app-wide resources once."""
        Astal.Application.do_startup(self)
        from src.utils.resource_loader import load_css

        load_css()

    def do_activate(self):
        """Create and show the launcher window when app is activated."""
        if self._launcher is None:
            # Import here after resources are loaded to avoid template errors.
            from src.windows.launcher import Launcher

            self._launcher = Launcher(self)
            self.add_window(self._launcher)

        self._launcher.show_launcher()


def main():
    """Main entry point for the application."""
    from src.utils.resource_loader import load_resources

    # Load resources FIRST before any imports with @Gtk.Template
    load_resources()

    application = LauncherApplication()
    application.run(sys.argv)


if __name__ == "__main__":
    main()
