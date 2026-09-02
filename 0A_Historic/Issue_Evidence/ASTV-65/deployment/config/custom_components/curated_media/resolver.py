"""Reusable catalogue item lookup for Curated Media."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .catalogue import Catalogue, CatalogueItem, CatalogueV3


RETURNED_RECORD_VERSION = 1


class CatalogueNotFoundError(LookupError):
    """Raised when a requested catalogue is not the loaded catalogue."""


class CatalogueItemNotFoundError(LookupError):
    """Raised when an item ID is not present in the loaded catalogue."""


class CatalogueResolver:
    """Resolve canonical item IDs from a loaded catalogue snapshot."""

    def __init__(self, catalogue: Catalogue | CatalogueV3) -> None:
        """Initialize the resolver with an existing loaded catalogue."""
        self._catalogue = catalogue

    def resolve_item(self, item_id: str) -> CatalogueItem | Mapping[Any, Any]:
        """Return the matching stored item or raise a clear lookup error."""
        item = self._catalogue.items.get(item_id)
        if item is None:
            raise CatalogueItemNotFoundError(
                f"Curated Media item {item_id!r} was not found in the catalogue"
            )
        return item

    def resolve_item_record(self, item_id: str) -> dict[Any, Any]:
        """Return a response-safe copy of the matching stored item mapping."""
        item = self.resolve_item(item_id)
        record = item.record if isinstance(item, CatalogueItem) else item
        return _response_safe_mapping(record)

    def resolve_media_record(
        self, catalogue_id: str, item_id: str
    ) -> dict[Any, Any]:
        """Return normalized record v1 for an item in the loaded v3 catalogue."""
        if (
            not isinstance(self._catalogue, CatalogueV3)
            or self._catalogue.catalogue_id != catalogue_id
        ):
            raise CatalogueNotFoundError(
                f"Curated Media catalogue {catalogue_id!r} was not found"
            )

        item = self._catalogue.items.get(item_id)
        if item is None:
            raise CatalogueItemNotFoundError(
                f"Curated Media item {item_id!r} was not found in catalogue "
                f"{catalogue_id!r}"
            )

        record = _response_safe_mapping(item)
        record.update(
            {
                "returned_record_version": RETURNED_RECORD_VERSION,
                "catalogue_id": catalogue_id,
                "item_id": item_id,
            }
        )
        return record


def _response_safe_mapping(value: Mapping[Any, Any]) -> dict[Any, Any]:
    """Copy an immutable mapping into caller-mutable response containers."""
    return {key: _response_safe_value(item) for key, item in value.items()}


def _response_safe_value(value: Any) -> Any:
    """Recursively copy immutable catalogue collections for action responses."""
    if isinstance(value, Mapping):
        return _response_safe_mapping(value)
    if isinstance(value, tuple | list):
        return [_response_safe_value(item) for item in value]
    return value
