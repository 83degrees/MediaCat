"""Reusable catalogue item lookup for MediaCat."""

from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any

from .catalogue import CatalogueRegistry, CatalogueV4


RETURNED_RECORD_VERSION = 1
IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class CatalogueNotFoundError(LookupError):
    """Raised when a requested catalogue is not the loaded catalogue."""


class CatalogueItemNotFoundError(LookupError):
    """Raised when an item ID is not present in the loaded catalogue."""


class InvalidIdentifierError(ValueError):
    """Raised when a lookup identifier violates schema-v4 policy."""


def validate_lookup_identifier(identifier: str, field_name: str) -> str:
    """Return an identifier after applying the schema-v4 lexical rule."""
    if (
        not isinstance(identifier, str)
        or IDENTIFIER_PATTERN.fullmatch(identifier) is None
    ):
        raise InvalidIdentifierError(
            f"MediaCat {field_name} {identifier!r} is invalid; identifiers "
            f"must match {IDENTIFIER_PATTERN.pattern!r}"
        )
    return identifier


class CatalogueResolver:
    """Resolve canonical item IDs from a loaded catalogue snapshot."""

    def __init__(
        self, registry: CatalogueRegistry | Mapping[str, CatalogueV4] | CatalogueV4
    ) -> None:
        """Initialize the resolver with an immutable catalogue registry."""
        if isinstance(registry, CatalogueRegistry):
            self._catalogues = registry.catalogues
        elif isinstance(registry, CatalogueV4):
            self._catalogues = {registry.catalogue_id: registry}
        else:
            self._catalogues = registry

    def resolve_media_record(
        self, catalogue_id: str, item_id: str
    ) -> dict[Any, Any]:
        """Return normalized record v1 for an item in an active catalogue."""
        catalogue_id = validate_lookup_identifier(catalogue_id, "catalogue_id")
        item_id = validate_lookup_identifier(item_id, "item_id")

        catalogue = self._catalogues.get(catalogue_id)
        if catalogue is None:
            raise CatalogueNotFoundError(
                f"MediaCat catalogue {catalogue_id!r} was not found"
            )

        item = catalogue.items.get(item_id)
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
