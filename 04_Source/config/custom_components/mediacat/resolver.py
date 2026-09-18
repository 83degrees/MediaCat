"""Reusable catalogue item lookup for MediaCat."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .catalogue import CatalogueV3


RETURNED_RECORD_VERSION = 1


class CatalogueNotFoundError(LookupError):
    """Raised when a requested catalogue is not the loaded catalogue."""


class CatalogueItemNotFoundError(LookupError):
    """Raised when an item ID is not present in the loaded catalogue."""


class CatalogueResolver:
    """Resolve canonical item IDs from a loaded catalogue snapshot."""

    def __init__(self, catalogue: CatalogueV3) -> None:
        """Initialize the resolver with an existing loaded catalogue."""
        self._catalogue = catalogue

    def resolve_media_record(
        self, catalogue_id: str, item_id: str
    ) -> dict[Any, Any]:
        """Return normalized record v1 for an item in the loaded v3 catalogue."""
        if self._catalogue.catalogue_id != catalogue_id:
            raise CatalogueNotFoundError(
                f"MediaCat catalogue {catalogue_id!r} was not found"
            )

        item = self._catalogue.items.get(item_id)
        if item is None:
            raise CatalogueItemNotFoundError(
                f"MediaCat item {item_id!r} was not found in catalogue "
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
