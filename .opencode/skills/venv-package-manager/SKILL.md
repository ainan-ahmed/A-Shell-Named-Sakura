---
name: venv-package-manager
description: |
  Manages Python packages in the project's venv (.venv/). Uses uv/pip for package operations.
  Always checks Context7 for up-to-date documentation when working with Python packages.
triggers:
  - pip install
  - uv pip
  - requirements
  - pyproject.toml
  - venv
  - package management
  - dependencies
---

When working with Python package management in this project, use the following workflow:

## Project Environment

- **Venv path**: `.venv/` (in project root)
- **Python**: uv-managed virtual environment
- **Package files**: `requirements.txt`, `pyproject.toml`

## Package Operations

### Check installed packages
```bash
.venv/bin/pip list
```

### Install package
```bash
.venv/bin/pip install <package>
# or with uv:
.venv/bin/uv pip install <package>
```

### Add to requirements.txt and install
1. Edit `requirements.txt` to add the package
2. Run `.venv/bin/pip install -r requirements.txt`

### Update pyproject.toml dependencies
1. Edit the `[project.dependencies]` section
2. Run `.venv/bin/pip install -e .` to reinstall in editable mode

## Context7 Integration

Before performing package operations or when unsure about package APIs, use Context7:

1. Call `context7_resolve-library-id` with the package name and query
2. Call `context7_query-docs` with the library ID and specific question
3. Use the documentation to ensure correct package versions and API usage

Example:
```
context7_resolve-library-id: {query: "PyGObject GTK4 bindings", libraryName: "PyGObject"}
context7_query-docs: {libraryId: "/pygobject/pygobject", query: "How to install and use PyGObject with GTK4"}
```

## Common Packages in This Project

- `pygobject` - Python bindings for GTK/GObject
- `pycairo` - Python bindings for cairo
- `sass` (libsass-python) - SCSS compilation
