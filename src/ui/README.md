# UI Blueprint Files

This directory contains GTK Blueprint (`.blp`) files that define the UI structure for windows and widgets.

## What are Blueprint files?

Blueprint is a markup language for GTK user interfaces, similar to GtkBuilder XML but with cleaner, more concise syntax. Blueprint files are compiled to `.ui` files (GtkBuilder XML) during the build process.

## How they're used

1. **Build Time**: Meson compiles `.blp` files to `.ui` files using `blueprint-compiler`
2. **Package Time**: The `.ui` files are bundled into a GResource binary (see `app.gresource.xml`)
3. **Runtime**: Python classes load the UI templates using `@Gtk.Template(resource_path=...)`

## File Organization

- `launcher.blp` - Main launcher window UI template (used by `windows/launcher.py`)
- `app_row.blp` - Application row widget template (used by `widgets/app_row.py`)

## Adding New UI Templates

1. Create a new `.blp` file in this directory
2. Add it to `blueprint_sources` in `meson.build`
3. Add the corresponding `.ui` file to `app.gresource.xml`
4. Reference it in your Python class using `@Gtk.Template(resource_path="/com/launcher/app/your_template.ui")`

## Resources

- [Blueprint Documentation](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/)
- [GTK4 Widget Gallery](https://docs.gtk.org/gtk4/visual_index.html)
