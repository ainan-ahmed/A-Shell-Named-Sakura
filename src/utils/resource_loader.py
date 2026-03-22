"""Utility functions for loading GResource files and CSS."""

import os
import sys

import gi

gi.require_version("Gio", "2.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gdk, Gio, Gtk  # type: ignore  # noqa: E402


def load_resources():
    """
    Load GResource from either build dir (dev) or install dir (production).

    Searches for data.gresource in the following locations:
    1. build/ directory (development mode)
    2. /usr/local/share/gtk-app-launcher/ (installed mode)
    3. /usr/share/gtk-app-launcher/ (installed mode)

    Exits with error if resource file cannot be found.
    """
    # Check if running from source tree
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    builddir_gresource = os.path.join(project_root, "builddir", "data.gresource")
    build_gresource = os.path.join(project_root, "build", "data.gresource")

    if os.path.exists(builddir_gresource):
        # Development mode: prefer Meson's default builddir output
        resource = Gio.Resource.load(builddir_gresource)
        resource._register()
        src_dir = os.path.join(project_root, "src")
        sys.path.insert(0, src_dir)
        return

    if os.path.exists(build_gresource):
        # Development mode: load the newest generated resource bundle
        resource = Gio.Resource.load(build_gresource)
        resource._register()
        src_dir = os.path.join(project_root, "src")
        sys.path.insert(0, src_dir)
        return

    # Production mode: try to find installed gresource
    installed_gresource = None
    for prefix in ["/usr/local", "/usr"]:
        candidate = os.path.join(prefix, "share", "gtk-app-launcher", "data.gresource")
        if os.path.exists(candidate):
            installed_gresource = candidate
            sys.path.insert(0, os.path.join(prefix, "share", "gtk-app-launcher"))
            break

    if installed_gresource:
        resource = Gio.Resource.load(installed_gresource)
        resource._register()
    else:
        print("Error: Could not find data.gresource", file=sys.stderr)
        sys.exit(1)


def load_css(resource_path: str = "/com/launcher/app/style.css"):
    """
    Load CSS from a GResource and apply it to the default display.

    Args:
        resource_path: The GResource path to the CSS file
    """
    provider = Gtk.CssProvider()
    provider.load_from_resource(resource_path)
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
