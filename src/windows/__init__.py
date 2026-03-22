"""Windows module for top-level application windows."""

__all__ = ["Launcher"]


def __getattr__(name):
    """Lazily import window classes to avoid import-time side effects."""
    if name == "Launcher":
        from src.windows.launcher import Launcher

        return Launcher
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
