"""Load and validate the Curated Media catalogue."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, cast
from urllib.parse import urlparse

from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import load_yaml

from .const import (
    CATALOGUE_VERSION,
    SUPPORTED_ITEM_TYPE,
    SUPPORTED_SOURCE_FORMATS,
    SUPPORTED_SOURCE_TYPE,
)

IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class CatalogueError(Exception):
    """Raised when a catalogue cannot be loaded or validated."""


@dataclass(frozen=True, slots=True)
class CatalogueSource:
    """A typed view over an immutable validated source record."""

    record: Mapping[str, Any]

    @property
    def source_type(self) -> str:
        """Return the validated source type."""
        return cast(str, self.record["type"])

    @property
    def url(self) -> str:
        """Return the validated source URL."""
        return cast(str, self.record["url"])

    @property
    def source_format(self) -> str:
        """Return the validated source format."""
        return cast(str, self.record["format"])

    @property
    def source_mime_type(self) -> str | None:
        """Return the optional player-facing MIME type."""
        return cast(str | None, self.record.get("mime_type"))


@dataclass(frozen=True, slots=True)
class CatalogueItem:
    """A canonical item backed by its complete immutable catalogue record."""

    item_id: str
    record: Mapping[str, Any]

    @property
    def title(self) -> str:
        """Return the validated item title."""
        return cast(str, self.record["title"])

    @property
    def item_type(self) -> str:
        """Return the validated item type."""
        return cast(str, self.record["type"])

    @property
    def source(self) -> CatalogueSource:
        """Return a typed view over the immutable source record."""
        return CatalogueSource(cast(Mapping[str, Any], self.record["source"]))

    @property
    def artwork(self) -> str | None:
        """Return the optional local artwork used by Media Browser."""
        artwork = cast(Mapping[str, Any] | None, self.record.get("artwork"))
        if artwork is None:
            return None
        return cast(str | None, artwork.get("local"))

    @property
    def artwork_external(self) -> str | None:
        """Return the optional external artwork URL."""
        artwork = cast(Mapping[str, Any] | None, self.record.get("artwork"))
        if artwork is None:
            return None
        return cast(str | None, artwork.get("external"))

    @property
    def description(self) -> str | None:
        """Return the optional item description."""
        return cast(str | None, self.record.get("description"))

    @property
    def tags(self) -> tuple[str, ...]:
        """Return the validated item tags."""
        return cast(tuple[str, ...], self.record.get("tags", ()))


@dataclass(frozen=True, slots=True)
class CatalogueCategory:
    """A category containing references to canonical items."""

    category_id: str
    title: str
    item_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Catalogue:
    """A validated catalogue snapshot."""

    version: int
    items: Mapping[str, CatalogueItem]
    categories: Mapping[str, CatalogueCategory]


async def async_load_catalogue(hass: HomeAssistant, path: str) -> Catalogue:
    """Read and validate a catalogue without blocking Home Assistant's event loop."""
    return await hass.async_add_executor_job(_load_catalogue, Path(path))


def _load_catalogue(path: Path) -> Catalogue:
    """Read and validate a catalogue from disk."""
    try:
        raw = load_yaml(path)
    except Exception as err:
        raise CatalogueError(f"could not read {path}: {err}") from err

    return _parse_catalogue(raw, path)


def _parse_catalogue(raw: Any, path: Path) -> Catalogue:
    """Convert raw YAML data into a validated catalogue snapshot."""
    root = _require_mapping(raw, f"catalogue {path}")

    version = root.get("version")
    if type(version) is not int or version != CATALOGUE_VERSION:
        raise CatalogueError(
            f"catalogue version must be the integer {CATALOGUE_VERSION}, "
            f"got {version!r}"
        )

    raw_items = _require_mapping(root.get("items"), "items")
    raw_categories = _require_mapping(root.get("categories"), "categories")

    items: dict[str, CatalogueItem] = {}
    for item_id, raw_item in raw_items.items():
        _require_identifier(item_id, "item")
        item = _parse_item(item_id, raw_item)
        items[item_id] = item

    categories: dict[str, CatalogueCategory] = {}
    for category_id, raw_category in raw_categories.items():
        _require_identifier(category_id, "category")
        category = _parse_category(category_id, raw_category, items)
        categories[category_id] = category

    return Catalogue(
        version=version,
        items=MappingProxyType(items),
        categories=MappingProxyType(categories),
    )


def _parse_item(item_id: str, raw: Any) -> CatalogueItem:
    """Parse one canonical media item."""
    item = _require_mapping(raw, f"item {item_id!r}")
    title = _require_non_empty_string(item.get("title"), f"item {item_id!r} title")
    item_type = _require_non_empty_string(
        item.get("type"), f"item {item_id!r} type"
    )
    if item_type != SUPPORTED_ITEM_TYPE:
        raise CatalogueError(
            f"item {item_id!r} has unsupported item.type {item_type!r}; "
            f"expected {SUPPORTED_ITEM_TYPE!r}"
        )

    _parse_artwork(item.get("artwork"), item_id)
    _parse_optional_string(
        item.get("description"), f"item {item_id!r} description"
    )
    _parse_tags(item.get("tags"), item_id)

    raw_source = _require_mapping(item.get("source"), f"item {item_id!r} source")
    source_type = _require_non_empty_string(
        raw_source.get("type"), f"item {item_id!r} source.type"
    )
    if source_type != SUPPORTED_SOURCE_TYPE:
        raise CatalogueError(
            f"item {item_id!r} has unsupported source.type {source_type!r}; "
            f"expected {SUPPORTED_SOURCE_TYPE!r}"
        )

    url = _require_non_empty_string(
        raw_source.get("url"), f"item {item_id!r} source.url"
    )
    parsed_url = urlparse(url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise CatalogueError(
            f"item {item_id!r} source.url must be an absolute HTTP or HTTPS URL"
        )

    source_format = _require_non_empty_string(
        raw_source.get("format"), f"item {item_id!r} source.format"
    )
    if source_format not in SUPPORTED_SOURCE_FORMATS:
        raise CatalogueError(
            f"item {item_id!r} has unsupported source.format "
            f"{source_format!r}; expected one of: "
            f"{', '.join(sorted(SUPPORTED_SOURCE_FORMATS))}"
        )
    _parse_optional_string(
        raw_source.get("mime_type"), f"item {item_id!r} source.mime_type"
    )

    return CatalogueItem(
        item_id=item_id,
        record=_freeze_mapping(item),
    )


def _parse_category(
    category_id: str, raw: Any, items: Mapping[str, CatalogueItem]
) -> CatalogueCategory:
    """Parse one category and validate all of its item references."""
    category = _require_mapping(raw, f"category {category_id!r}")
    title = _require_non_empty_string(
        category.get("title"), f"category {category_id!r} title"
    )

    raw_item_ids = category.get("items")
    if not isinstance(raw_item_ids, list):
        raise CatalogueError(f"category {category_id!r} items must be a list")

    item_ids: list[str] = []
    seen: set[str] = set()
    for item_id in raw_item_ids:
        _require_identifier(item_id, f"category {category_id!r} item reference")
        if item_id not in items:
            raise CatalogueError(
                f"category {category_id!r} references unknown item {item_id!r}"
            )
        if item_id in seen:
            raise CatalogueError(
                f"category {category_id!r} references item {item_id!r} more than once"
            )
        seen.add(item_id)
        item_ids.append(item_id)

    return CatalogueCategory(
        category_id=category_id,
        title=title,
        item_ids=tuple(item_ids),
    )


def _require_mapping(value: Any, location: str) -> Mapping[str, Any]:
    """Require a mapping with string keys."""
    if not isinstance(value, dict):
        raise CatalogueError(f"{location} must be a mapping")
    if any(not isinstance(key, str) for key in value):
        raise CatalogueError(f"{location} keys must be strings")
    return value


def _require_identifier(value: Any, location: str) -> str:
    """Require a non-empty identifier that is safe in a media-source path."""
    identifier = _require_non_empty_string(value, f"{location} ID")
    if IDENTIFIER_PATTERN.fullmatch(identifier) is None:
        raise CatalogueError(
            f"{location} ID {identifier!r} is invalid; IDs must match "
            "^[a-z0-9][a-z0-9_-]*$"
        )
    return identifier


def _require_non_empty_string(value: Any, location: str) -> str:
    """Require a non-empty string."""
    if not isinstance(value, str) or not value.strip():
        raise CatalogueError(f"{location} must be a non-empty string")
    return value


def _parse_artwork(value: Any, item_id: str) -> tuple[str | None, str | None]:
    """Validate an optional artwork mapping."""
    if value is None:
        return None, None

    if not isinstance(value, dict):
        raise CatalogueError(
            f"item {item_id!r} artwork must be a mapping with local and/or "
            "external"
        )

    unknown_keys = set(value) - {"local", "external"}
    if unknown_keys:
        raise CatalogueError(
            f"item {item_id!r} artwork contains unknown keys: "
            f"{', '.join(sorted(str(key) for key in unknown_keys))}"
        )
    if not value:
        raise CatalogueError(
            f"item {item_id!r} artwork must contain local or external"
        )

    local = None
    external = None
    if "local" in value:
        local = _require_non_empty_string(
            value["local"], f"item {item_id!r} artwork.local"
        )
        if not local.startswith("/local/") or len(local) == len("/local/"):
            raise CatalogueError(
                f"item {item_id!r} artwork.local must be a /local/... URL"
            )
    if "external" in value:
        external = _require_non_empty_string(
            value["external"], f"item {item_id!r} artwork.external"
        )
        parsed_external = urlparse(external)
        if (
            parsed_external.scheme not in {"http", "https"}
            or not parsed_external.netloc
        ):
            raise CatalogueError(
                f"item {item_id!r} artwork.external must be an absolute "
                "http:// or https:// URL"
            )
    return local, external


def _parse_optional_string(value: Any, location: str) -> str | None:
    """Validate an optional non-empty string."""
    if value is None:
        return None
    return _require_non_empty_string(value, location)


def _parse_tags(value: Any, item_id: str) -> tuple[str, ...]:
    """Validate optional item tags."""
    if value is None:
        return ()
    if not isinstance(value, list):
        raise CatalogueError(f"item {item_id!r} tags must be a list")
    return tuple(
        _require_non_empty_string(tag, f"item {item_id!r} tag") for tag in value
    )


def _freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return an immutable, recursively frozen copy of a catalogue mapping."""
    return MappingProxyType(
        {key: _freeze_value(item_value) for key, item_value in value.items()}
    )


def _freeze_value(value: Any) -> Any:
    """Recursively freeze mappings and sequences from a catalogue record."""
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _freeze_value(item_value) for key, item_value in value.items()}
        )
    if isinstance(value, list | tuple):
        return tuple(_freeze_value(item_value) for item_value in value)
    return value
