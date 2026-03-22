# Development shortcuts for gtk-app-launcher

# Build resources and run
run: build
    python -m src.main

# Run without rebuilding (Python changes only)
quick:
    python -m src.main

# Auto-rebuild on .blp/.scss changes (requires entr)
watch:
    find src/ui -name '*.blp' src -name '*.scss' | entr -r meson compile -C builddir

# Build Blueprint and SCSS resources
build:
    meson compile -C builddir
