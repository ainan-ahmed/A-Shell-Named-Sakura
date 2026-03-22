# A Shell Named Sakura

A GTK4 desktop shell built with PyGObject, Astal, and gtk4-layer-shell.
Currently featuring an application launcher, with plans to expand into a 
full-featured desktop shell environment.

The UI is authored in Blueprint and packaged into a GResource bundle, with SCSS
compiled to CSS during the build step.

## Project Structure

```
gtk_app_launcher/
├── build_scripts/          # SCSS compiler helper
├── data/                   # Desktop entry and bundled assets
├── src/
│   ├── main.py             # Application entry point
│   ├── app.gresource.xml   # Resource manifest
│   ├── ui/                 # Blueprint UI templates
│   │   ├── launcher.blp    # Launcher window template
│   │   └── app_row.blp     # Application row template
│   ├── style.scss          # App styling (compiled to CSS)
│   ├── services/           # Business logic and data services
│   │   └── apps_service.py # Application search using AstalApps
│   ├── utils/              # Resource loading helpers
│   │   └── resource_loader.py  # GResource and CSS loading
│   ├── widgets/            # Reusable UI components
│   │   └── app_row.py      # Application list row widget
│   └── windows/            # Top-level application windows
│       └── launcher.py     # Main launcher window
├── meson.build             # Build configuration
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
├── uv.lock                 # Locked Python dependencies
├── AGENTS.md               # AI agent guidelines
├── INSTALL.md              # System install + shortcut setup
└── README.md               # This file
```

## Features

Currently implemented:
- **Application Launcher**: Fast application search and launch using AstalApps
  - Fuzzy search across app names, descriptions, and executables
  - Keyboard-driven navigation (arrow keys, Enter, Escape)
  - Click-outside-to-close behavior
  - gtk4-layer-shell integration for proper Wayland layer positioning

Planned features:
- Status bar with system indicators (battery, network, audio, etc.)
- Media player controls (MPRIS integration)
- Notification center
- Quick settings panel
- Workspace management
- Custom widgets and plugins

## Dependencies

### System Dependencies
Install these system packages:

- Python 3.10+
- GTK4
- PyGObject
- gtk4-layer-shell (for Wayland layer-shell integration)
- blueprint-compiler (for compiling Blueprint UI files)
- meson + ninja (for building GResource bundles)
- Astal core library:
  - astal4 (required)
- Optional Astal service libraries:
  - astal-apps (required for application launcher)
  - astal-battery (for battery monitoring)
  - astal-wireplumber (for audio control)
  - astal-network (for network status)
  - astal-mpris (for media player control)
  - astal-powerprofiles (for power profile management)
  - astal-tray (for system tray)
  - astal-bluetooth (for Bluetooth management)

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

## Build Resources (Required Before Running)

The shell loads UI and CSS from a compiled GResource bundle. You must build 
resources before running in development mode:

```bash
# Initial setup
meson setup build --prefix=/usr/local

# Compile resources (Blueprint UI + SCSS → GResource bundle)
meson compile -C build
```

This generates:
- Compiled Blueprint UI files (.ui from .blp)
- Compiled CSS (style.css from style.scss)
- GResource bundle (data.gresource) containing all UI assets

Run `meson compile -C build` again after editing any Blueprint (.blp) or SCSS files.

## Running the Shell

### Development Mode
After building resources (see above), run the shell with:

```bash
# From project root:
python -m src.main

# Or directly:
python src/main.py
```

### Installed Mode
For system-wide installation with desktop shortcuts, see [INSTALL.md](INSTALL.md).

If you installed the package in editable mode with pip:

```bash
gtk-app-launcher
```

The launcher window can be activated with a keyboard shortcut (configured in your 
desktop environment or window manager) by running the command above.

## Next Steps

This shell is in active development. You can extend it by:

1. **Adding system indicators**: Integrate Astal services for battery, network, audio monitoring
2. **Custom widgets**: Create reusable UI components in `src/widgets/`
3. **New windows/panels**: Add status bars, notification centers, or quick settings in `src/windows/`
4. **Theme customization**: Edit `src/style.scss` to customize the appearance
5. **Configuration system**: Add user preferences and persistent settings
6. **Animations and effects**: Enhance UI with GTK4 animations and transitions

See [AGENTS.md](AGENTS.md) for detailed development guidelines and project structure information.

## Resources

- [PyGObject Documentation](https://pygobject.gnome.org/tutorials/index.html)
- [Astal GitHub Repository](https://github.com/Aylur/astal)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [Blueprint Language](https://jwestman.pages.gitlab.gnome.org/blueprint-compiler/)
- [gtk4-layer-shell](https://github.com/wmww/gtk4-layer-shell)
