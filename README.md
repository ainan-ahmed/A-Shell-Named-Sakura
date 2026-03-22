# A Shell Named Sakura (GTK App Launcher)

A GTK4 application launcher built with PyGObject, Astal, and gtk4-layer-shell.
The UI is authored in Blueprint and packaged into a GResource bundle, with SCSS
compiled to CSS during the build step.

## Project Structure

```
A-Shell-Named-Sakura/
├── build_scripts/          # SCSS compiler helper
├── data/                   # Desktop entry and bundled assets
├── src/
│   ├── main.py             # Application entry point
│   ├── app.gresource.xml   # Resource manifest
│   ├── launcher.blp        # Blueprint template
│   ├── app_row.blp         # Blueprint template
│   ├── style.scss          # App styling
│   ├── services/           # App search + data services
│   ├── utils/              # Resource loading helpers
│   ├── widgets/            # Reusable UI widgets
│   └── windows/            # Top-level launcher window
├── meson.build             # Build configuration
├── pyproject.toml          # Project configuration
├── uv.lock                 # Locked Python dependencies
├── INSTALL.md              # System install + shortcut setup
└── README.md               # This file
```

## Dependencies

### System Dependencies
You need to install these system packages:

- Python 3.10+
- GTK4
- PyGObject
- gtk4-layer-shell (for layer-shell integration)
- blueprint-compiler (for Blueprint UI compilation)
- meson + ninja (for building GResource bundles)
- Astal libraries:
  - astal4
  - astal-battery (optional)
  - astal-wireplumber (optional)
  - astal-network (optional)
  - astal-mpris (optional)
  - astal-powerprofiles (optional)
  - astal-tray (optional)
  - astal-bluetooth (optional)

Package names vary by distro, but ensure gtk4-layer-shell, blueprint-compiler,
meson, and ninja are installed alongside GTK4 and PyGObject.

#### Install on Arch Linux
```bash
sudo pacman -S python python-gobject gtk4
# Install Astal from AUR or build from source
```

#### Install on Ubuntu/Debian
```bash
sudo apt install python3 python3-gi gtk4
# Install Astal from source
```

### Python Virtual Environment Setup

**IMPORTANT**: PyGObject must be installed system-wide and accessed via a virtual environment with `--system-site-packages` enabled.

#### Create Virtual Environment (Recommended)
```bash
# Use system Python (must have PyGObject installed)
/usr/bin/python3 -m venv .venv --system-site-packages

# Activate the virtual environment
source .venv/bin/activate

# Install Python dependencies declared in pyproject.toml
pip install -e .
# Or with uv:
uv pip install -e .
```

#### Why system-site-packages?
PyGObject and GTK4 bindings are typically installed system-wide via your package manager (pacman, apt, etc.). The `--system-site-packages` flag allows your venv to access these system packages while keeping your project dependencies isolated.

#### Alternative: Direct Installation (Not Recommended)
```bash
# This will NOT work for PyGObject - it needs system libraries
pip install -e .
```

## Build Resources (Required for Development)

The app loads UI/CSS from a compiled GResource bundle. Generate it once before
running in development mode:

```bash
meson setup build --prefix=/usr/local
meson compile -C build
```

## Running the Application

### Development Mode
Make sure you have built resources (see above), then run:

```bash
python -m src.main
```

Or:

```bash
python src/main.py
```

### Install and Run
For system-wide install and shortcut setup, see [INSTALL.md](INSTALL.md).

If you have installed the package in editable mode, you can also run:

```bash
gtk-app-launcher
```

## Next Steps

This is a basic skeleton. You can extend it by:

1. Adding custom widgets in separate modules under `src/`
2. Integrating Astal services (battery, network, audio, etc.)
3. Creating a custom CSS theme
4. Adding configuration files
5. Building UI files with Blueprint compiler

## Resources

- [PyGObject Documentation](https://pygobject.gnome.org/tutorials/index.html)
- [Astal GitHub Repository](https://github.com/Aylur/astal)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
