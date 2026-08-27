"""Reusable catalogue item lookup for Curated Media."""

from __future__ import annotations

from .catalogue import Catalogue, CatalogueItem


class CatalogueItemNotFoundError(LookupError):
    """Raised when an item ID is not present in the loaded catalogue."""


class CatalogueResolver:
    """Resolve canonical item IDs from a loaded catalogue snapshot."""

    def __init__(self, catalogue: Catalogue) -> None:
        """Initialize the resolver with an existing loaded catalogue."""
        self._catalogue = catalogue

    def resolve_item(self, item_id: str) -> CatalogueItem:
        """Return the matching canonical item or raise a clear lookup error."""
        item = self._catalogue.items.get(item_id)
        if item is None:
            raise CatalogueItemNotFoundError(
                f"Curated Media item {item_id!r} was not found in the catalogue"
            )
        return item
