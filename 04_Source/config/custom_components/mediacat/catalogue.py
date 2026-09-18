"""Load and validate the MediaCat catalogue."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, cast

from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import load_yaml

class CatalogueError(Exception):
    """Raised when a catalogue cannot be loaded or validated."""


@dataclass(frozen=True, slots=True)
class CatalogueV3:
    """An immutable schema-v3 stored catalogue."""

    record: Mapping[Any, Any]

    @property
    def catalogue_id(self) -> Any:
        """Return the stored catalogue identity without interpreting it."""
        return self.record["catalogue_id"]

    @property
    def catalogue_schema_version(self) -> int:
        """Return the stored catalogue schema version."""
        return cast(int, self.record["catalogue_schema_version"])

    @property
    def items(self) -> Mapping[Any, Any]:
        """Return the complete immutable item mapping."""
        return cast(Mapping[Any, Any], self.record["items"])

    @property
    def categories(self) -> Mapping[Any, Any]:
        """Return the complete immutable category mapping."""
        return cast(Mapping[Any, Any], self.record["categories"])


async def async_load_catalogue(
    hass: HomeAssistant, path: str
) -> CatalogueV3:
    """Read and validate a catalogue without blocking Home Assistant's event loop."""
    return await hass.async_add_executor_job(_load_catalogue, Path(path))


def _load_catalogue(path: Path) -> CatalogueV3:
    """Read and validate a catalogue from disk."""
    try:
        raw = load_yaml(path)
    except Exception as err:
        raise CatalogueError(f"could not read {path}: {err}") from err

    return _parse_catalogue(raw, path)


def _parse_catalogue(raw: Any, path: Path) -> CatalogueV3:
    """Parse the sole active stored catalogue schema."""
    if not isinstance(raw, Mapping):
        raise CatalogueError(f"catalogue {path} must be a mapping")
    root = raw
    if (
        type(root.get("catalogue_schema_version")) is not int
        or root.get("catalogue_schema_version") != 3
    ):
        raise CatalogueError(
            "unsupported catalogue schema; expected catalogue_schema_version: 3"
        )
    return _parse_catalogue_v3(root)


def _parse_catalogue_v3(root: Mapping[Any, Any]) -> CatalogueV3:
    """Retain and recursively freeze a minimally checked schema-v3 root."""
    if "catalogue_id" not in root:
        raise CatalogueError("schema-v3 catalogue_id must be present")
    if not isinstance(root.get("items"), Mapping):
        raise CatalogueError("schema-v3 items must be a mapping")
    if not isinstance(root.get("categories"), Mapping):
        raise CatalogueError("schema-v3 categories must be a mapping")

    return CatalogueV3(record=_freeze_mapping(root))


def _freeze_mapping(value: Mapping[Any, Any]) -> Mapping[Any, Any]:
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
