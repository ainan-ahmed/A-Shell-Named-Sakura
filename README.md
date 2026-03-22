# GTK App Launcher

A simple GTK4 application using PyGObject and Astal.

## Project Structure

```
gtk_app_launcher/
├── src/
│   ├── __init__.py
│   └── main.py          # Main application code
├── main.py              # Legacy entry point (can be removed)
├── pyproject.toml       # Project configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Dependencies

### System Dependencies
You need to install these system packages:

- Python 3.10+
- GTK4
- PyGObject
- Astal libraries:
  - astal4
  - astal-battery (optional)
  - astal-wireplumber (optional)
  - astal-network (optional)
  - astal-mpris (optional)
  - astal-powerprofiles (optional)
  - astal-tray (optional)
  - astal-bluetooth (optional)

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

# Install any additional Python dependencies
pip install -r requirements.txt
```

#### Why system-site-packages?
PyGObject and GTK4 bindings are typically installed system-wide via your package manager (pacman, apt, etc.). The `--system-site-packages` flag allows your venv to access these system packages while keeping your project dependencies isolated.

#### Alternative: Direct Installation (Not Recommended)
```bash
# This will NOT work for PyGObject - it needs system libraries
pip install -r requirements.txt
```

## Running the Application

### Development Mode
```bash
python -m src.main
```

Or:

```bash
python src/main.py
```

### Install and Run
```bash
pip install -e .
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
