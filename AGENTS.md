# Agent Guidelines for gtk-app-launcher

This document provides essential information for AI coding agents working on this PyGObject + Astal GTK4 application.

## Project Overview

- **Stack**: Python 3.10+, PyGObject, GTK4, Astal
- **Type**: GTK4 desktop application for app launching
- **Entry Point**: `src/main.py`
- **Package Manager**: pip or uv (preferred)

## Build, Run, and Test Commands

### Installation
```bash
# Install system dependencies first (see README.md)
# Then install Python dependencies:
pip install -r requirements.txt
# Or with uv:
uv pip install -r requirements.txt
```

### Running the Application
```bash
# Development mode (from project root):
python -m src.main

# Or directly:
python src/main.py

# Installed mode:
pip install -e .
gtk-app-launcher
```

### Linting and Formatting
```bash
# Format with ruff (if configured):
ruff format .

# Lint with ruff:
ruff check .

# Type checking with mypy (if configured):
mypy src/
```

### Testing
Currently no test suite is configured. When adding tests:
```bash
# Run all tests:
pytest

# Run a single test file:
pytest tests/test_filename.py

# Run a single test function:
pytest tests/test_filename.py::test_function_name

# Run with verbose output:
pytest -v

# Run with coverage:
pytest --cov=src
```

## Code Style Guidelines

### General Principles
- Follow PEP 8 for Python code style
- Write clear, self-documenting code with descriptive names
- Keep functions small and focused (single responsibility)
- Prefer composition over inheritance where appropriate

### Imports
```python
# Order: stdlib, third-party, local, with blank lines between groups
import sys
from pathlib import Path

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Astal", "4.0")

from gi.repository import Gtk, Astal, GLib

from src.utils import helper_function
```

- Always call `gi.require_version()` before importing from `gi.repository`
- Use absolute imports for project modules: `from src.module import Class`
- Avoid wildcard imports (`from module import *`)

### Formatting
- **Indentation**: 4 spaces (no tabs)
- **Line length**: 88-100 characters max (PEP 8 allows up to 99)
- **Quotes**: Double quotes for strings preferred
- **Blank lines**: 2 between top-level definitions, 1 between methods
- **Trailing commas**: Use in multi-line collections

### Type Hints
While not currently enforced, prefer adding type hints for clarity:
```python
def create_window(self, title: str, width: int = 400) -> Gtk.Window:
    """Create a new window with the given title and width"""
    window = Gtk.Window(title=title)
    window.set_default_size(width, 300)
    return window
```

### Naming Conventions
- **Classes**: PascalCase (e.g., `AppLauncher`, `MainWindow`)
- **Functions/Methods**: snake_case (e.g., `on_button_clicked`, `create_window`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_WIDTH`, `APP_ID`)
- **Private members**: prefix with single underscore (e.g., `_internal_method`)
- **Widget callbacks**: prefix with `on_` (e.g., `on_button_clicked`)

### Docstrings
Use docstrings for all public modules, classes, and functions:
```python
def process_data(data: list) -> dict:
    """
    Process raw data and return structured results.
    
    Args:
        data: List of raw data items to process
        
    Returns:
        Dictionary with processed results
        
    Raises:
        ValueError: If data is empty or invalid
    """
    pass
```

### Error Handling
- Use specific exceptions, not bare `except:`
- Log errors appropriately (use Python logging module)
- Handle GTK/GLib errors gracefully
```python
try:
    result = perform_operation()
except GLib.Error as e:
    print(f"GTK error occurred: {e}")
    # Handle appropriately
```

## GTK4/PyGObject Specific Guidelines

### Widget Creation
- Use `Gtk.Box` with orientation for layouts
- Set margins using `set_margin_*` methods consistently
- Apply CSS classes with `add_css_class()` for styling
- Connect signals with `connect()` method

### Signal Handlers
```python
# Method signature for signal handlers:
def on_signal_name(self, widget, *args):
    """Handle the signal_name signal"""
    pass

# Connect:
widget.connect("signal-name", self.on_signal_name)
```

### Application Structure
- Extend `Gtk.Application` for main app class
- Use `application_id` in reverse domain format (e.g., `com.example.app_name`)
- Implement `do_activate()` for window creation
- Store window reference to avoid recreating on reactivation

## Project Structure

The project follows a modular architecture with clear separation of concerns:

```
gtk_app_launcher/
├── src/                    # Main source code
│   ├── __init__.py
│   ├── main.py             # Application entry point (minimal, just initialization)
│   ├── widgets/            # Reusable UI components
│   │   ├── __init__.py
│   │   └── app_row.py      # Example: application list row widget
│   ├── windows/            # Top-level application windows
│   │   ├── __init__.py
│   │   └── launcher.py     # Example: main launcher window
│   ├── services/           # Business logic and data services
│   │   ├── __init__.py
│   │   └── apps_service.py # Example: application search and management
│   └── utils/              # Utility functions and helpers
│       ├── __init__.py
│       └── resource_loader.py  # Example: GResource and CSS loading
├── data/                   # UI files (.blp, .ui), resources, icons
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
├── README.md               # User documentation
└── AGENTS.md               # This file (agent guidelines)
```

### Module Organization Principles

#### widgets/
**Purpose**: Reusable, self-contained UI components that can be used across different windows.

**Guidelines**:
- Each widget should be in its own file
- Extend GTK base classes (e.g., `Gtk.ListBoxRow`, `Gtk.Box`, `Gtk.Button`)
- Use `@Gtk.Template` decorator with Blueprint UI files when appropriate
- Keep widgets focused on presentation logic
- Widgets should not contain business logic or direct service access (pass data via properties/methods)

**Examples**:
- `app_row.py`: A single application entry in a list
- `status_bar.py`: A status bar showing system information
- `menu_item.py`: A custom menu item with icon and label

#### windows/
**Purpose**: Top-level application windows that compose widgets and handle window-level logic.

**Guidelines**:
- Each major window should be in its own file
- Extend `Gtk.Window`, `Gtk.ApplicationWindow`, or `Astal.Window`
- Use `@Gtk.Template` decorator with Blueprint UI files when appropriate
- Windows coordinate between widgets and services
- Handle window-level shortcuts and events
- Keep business logic minimal; delegate to services

**Examples**:
- `launcher.py`: Main application launcher window
- `settings.py`: Settings/preferences window
- `about.py`: About dialog window

#### services/
**Purpose**: Business logic, data management, and state that needs to be shared across the application.

**Guidelines**:
- Each major functional area should have its own service
- Services should be stateful and often singleton instances
- Provide clean public APIs for windows/widgets to use
- Handle data processing, external API calls, file I/O
- Implement search, filtering, and data transformation logic
- Services should not import or create GTK widgets

**Examples**:
- `apps_service.py`: Application search and management using AstalApps
- `settings_service.py`: Application settings persistence
- `notification_service.py`: System notifications
- `theme_service.py`: Theme and appearance management

**Singleton Pattern**:
```python
# Preferred pattern for services
_service_instance = None

def get_service() -> MyService:
    """Get the global MyService singleton instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = MyService()
    return _service_instance
```

#### utils/
**Purpose**: Stateless utility functions and helpers that don't fit elsewhere.

**Guidelines**:
- Small, focused utility functions
- Should be stateless (pure functions preferred)
- No GTK widget creation (except for helpers like CSS loading)
- Group related utilities in the same file

**Examples**:
- `resource_loader.py`: GResource and CSS loading utilities
- `format.py`: String formatting helpers
- `path.py`: Path manipulation utilities

### Adding New Modules

#### Adding a New Widget
1. Create `src/widgets/widget_name.py`
2. Define the widget class extending a GTK base class
3. Optionally create `data/widget_name.blp` for the UI template
4. Add widget to `src/widgets/__init__.py`:
   ```python
   from src.widgets.widget_name import WidgetName
   __all__ = [..., "WidgetName"]
   ```
5. Import in windows where needed: `from src.widgets import WidgetName`

#### Adding a New Window
1. Create `src/windows/window_name.py`
2. Define the window class extending `Gtk.Window`, `Gtk.ApplicationWindow`, or `Astal.Window`
3. Optionally create `data/window_name.blp` for the UI template
4. Add window to `src/windows/__init__.py`
5. Import in `main.py` or where needed: `from src.windows import WindowName`

#### Adding a New Service
1. Create `src/services/service_name.py`
2. Define the service class
3. Implement singleton getter function: `get_service_name()`
4. Add service to `src/services/__init__.py`
5. Import where needed: `from src.services import get_service_name`

#### Adding Utility Functions
1. Create or update a file in `src/utils/`
2. Define utility functions (prefer stateless functions)
3. Add to `src/utils/__init__.py` if part of public API
4. Import where needed: `from src.utils import utility_function`

## Dependencies

### Adding New Dependencies
1. Add to `pyproject.toml` under `[project.dependencies]`
2. Update `requirements.txt`
3. Document any system-level dependencies in `README.md`

### Astal Integration
When using Astal services:
```python
gi.require_version("AstalBattery", "0.1")
from gi.repository import AstalBattery

battery = AstalBattery.get_default()
```

## Common Pitfalls

1. **Forgetting `gi.require_version()`**: Always call before importing from `gi.repository`
2. **Signal handler signatures**: Must accept widget as first argument after self
3. **Window recreation**: Check if window exists in `do_activate()` before creating
4. **GTK main loop**: Don't block the main loop with long-running operations
5. **Memory leaks**: Properly disconnect signals when destroying widgets

## Resources

- [PyGObject Documentation](https://pygobject.gnome.org/)
- [GTK4 Documentation](https://docs.gtk.org/gtk4/)
- [Astal GitHub](https://github.com/Aylur/astal)
- [Python PEP 8](https://pep8.org/)
