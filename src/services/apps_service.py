"""Service for managing and searching applications using AstalApps."""

import gi

gi.require_version("AstalApps", "0.1")
from gi.repository import AstalApps  # type: ignore  # noqa: E402



class AppsService:
    """Service for querying and managing installed applications."""

    def __init__(
        self,
        name_multiplier: int = 2,
        entry_multiplier: int = 1,
        executable_multiplier: int = 1,
    ):
        """
        Initialize the AppsService.

        Args:
            name_multiplier: Weight for matching app name in fuzzy search
            entry_multiplier: Weight for matching .desktop entry name
            executable_multiplier: Weight for matching executable name
        """
        self._apps = AstalApps.Apps(
            name_multiplier=name_multiplier,
            entry_multiplier=entry_multiplier,
            executable_multiplier=executable_multiplier,
        )

    def search(self, query: str) -> list[AstalApps.Application]:
        """
        Search for applications matching the query.

        Args:
            query: Search query string

        Returns:
            List of matching applications. If query is empty,
            returns all applications sorted by name.
        """
        if not query.strip():
            return sorted(self._apps.get_list(), key=lambda a: a.get_name().lower())
        return self._apps.fuzzy_query(query)

    def get_all_apps(self) -> list[AstalApps.Application]:
        """
        Get all installed applications.

        Returns:
            List of all installed applications
        """
        return self._apps.get_list()


# Global singleton instance
_apps_service_instance = None


def get_apps_service() -> AppsService:
    """
    Get the global AppsService singleton instance.

    Returns:
        The global AppsService instance
    """
    global _apps_service_instance
    if _apps_service_instance is None:
        _apps_service_instance = AppsService()
    return _apps_service_instance
