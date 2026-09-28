"""Load and validate the MediaCat catalogue."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from io import StringIO
import math
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, cast
from urllib.parse import urlsplit

from homeassistant.core import HomeAssistant
from homeassistant.util.yaml import parse_yaml
import yaml

IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
MIME_TYPE_PATTERN = re.compile(r"^[^\s/]+/[^\s/]+$")

ROOT_FIELDS = frozenset(
    {"catalogue_id", "catalogue_schema_version", "artwork_sources", "items", "categories"}
)
ROOT_REQUIRED_FIELDS = frozenset(
    {"catalogue_id", "catalogue_schema_version", "items", "categories"}
)
ARTWORK_SOURCE_FIELDS = frozenset({"local", "external"})
ITEM_FIELDS = frozenset(
    {
        "catalogue_label",
        "type",
        "description",
        "tags",
        "artwork",
        "content_rating",
        "type_metadata",
        "execution_methods",
    }
)
ITEM_REQUIRED_FIELDS = frozenset(
    {"catalogue_label", "type", "type_metadata", "execution_methods"}
)
ARTWORK_FIELDS = {
    "ha-assets": (
        frozenset({"source_type", "path"}),
        frozenset({"source_type", "path"}),
    ),
    "direct": (
        frozenset({"source_type", "local", "external"}),
        frozenset({"source_type"}),
    ),
}
EXECUTION_METHOD_SOURCE_TYPES = {
    "ha_mplayer": frozenset({"url", "ha_media_source"}),
    "g_home_device": frozenset({"assistant_command"}),
}
SOURCE_FIELDS = {
    "url": (
        frozenset({"source_type", "url", "mime_type", "provider"}),
        frozenset({"source_type", "url", "mime_type"}),
    ),
    "ha_media_source": (
        frozenset({"source_type", "provider", "uri", "media_type"}),
        frozenset({"source_type", "provider", "uri", "media_type"}),
    ),
    "assistant_command": (
        frozenset({"source_type", "provider", "command", "append_target"}),
        frozenset({"source_type", "provider", "command", "append_target"}),
    ),
}
TYPE_METADATA_FIELDS = {
    "radio": (frozenset({"station_name"}), frozenset({"station_name"})),
    "music_track": (
        frozenset(
            {
                "track_title",
                "artist",
                "album_artist",
                "album_title",
                "composer",
                "disc_number",
                "track_number",
                "release_date",
            }
        ),
        frozenset({"track_title"}),
    ),
    "podcast_episode": (
        frozenset(
            {
                "episode_title",
                "podcast_title",
                "creator",
                "publisher",
                "publication_date",
                "episode_number",
            }
        ),
        frozenset({"episode_title"}),
    ),
    "live_tv": (frozenset({"channel_name"}), frozenset({"channel_name"})),
    "tv_episode": (
        frozenset(
            {
                "episode_title",
                "series_title",
                "season_number",
                "episode_number",
                "first_broadcast_date",
            }
        ),
        frozenset({"episode_title"}),
    ),
    "movie": (
        frozenset({"movie_title", "secondary_title", "studio", "release_date"}),
        frozenset({"movie_title"}),
    ),
    "photo": (
        frozenset(
            {
                "image_title",
                "creator",
                "creation_datetime",
                "location",
                "latitude",
                "longitude",
                "width_pixels",
                "height_pixels",
            }
        ),
        frozenset({"image_title"}),
    ),
}


class CatalogueError(Exception):
    """Raised when a catalogue cannot be loaded or validated."""


@dataclass(frozen=True, slots=True)
class CatalogueV4:
    """An immutable schema-v4 stored catalogue."""

    record: Mapping[Any, Any]

    @property
    def catalogue_id(self) -> str:
        """Return the validated catalogue identity."""
        return cast(str, self.record["catalogue_id"])

    @property
    def catalogue_schema_version(self) -> int:
        """Return the stored catalogue schema version."""
        return cast(int, self.record["catalogue_schema_version"])

    @property
    def items(self) -> Mapping[str, Any]:
        """Return the complete immutable item mapping."""
        return cast(Mapping[str, Any], self.record["items"])

    @property
    def categories(self) -> Mapping[str, Any]:
        """Return the complete immutable category mapping."""
        return cast(Mapping[str, Any], self.record["categories"])


async def async_load_catalogue(hass: HomeAssistant, path: str) -> CatalogueV4:
    """Read and validate a catalogue without blocking Home Assistant's event loop."""
    return await hass.async_add_executor_job(_load_catalogue, Path(path))


def _load_catalogue(path: Path) -> CatalogueV4:
    """Read and validate a catalogue from disk."""
    try:
        text = path.read_text(encoding="utf-8")
        _reject_duplicate_keys(text, path)
        raw = parse_yaml(StringIO(text))
    except CatalogueError:
        raise
    except Exception as err:
        raise CatalogueError(f"could not read {path}: {err}") from err
    return _parse_catalogue(raw, path)


def _reject_duplicate_keys(text: str, path: Path) -> None:
    """Reject duplicate YAML mapping keys before construction can overwrite them."""
    try:
        root = yaml.compose(text, Loader=yaml.BaseLoader)
    except yaml.YAMLError as err:
        raise CatalogueError(f"could not read {path}: {err}") from err
    visited: set[int] = set()

    def walk(node: yaml.Node, location: str) -> None:
        if id(node) in visited:
            return
        visited.add(id(node))
        if isinstance(node, yaml.MappingNode):
            seen: dict[tuple[str, str], int] = {}
            for key_node, value_node in node.value:
                key = (key_node.tag, str(getattr(key_node, "value", "<key>")))
                key_text = key[1]
                child = f"{location}.{key_text}" if location else key_text
                line = key_node.start_mark.line + 1
                if key in seen:
                    raise CatalogueError(
                        f"catalogue {path}: {child} is duplicated "
                        f"(lines {seen[key]} and {line})"
                    )
                seen[key] = line
                walk(value_node, child)
        elif isinstance(node, yaml.SequenceNode):
            for index, child_node in enumerate(node.value):
                walk(child_node, f"{location}[{index}]")

    if root is not None:
        walk(root, "")


def _parse_catalogue(raw: Any, path: Path) -> CatalogueV4:
    """Parse the sole active stored catalogue schema."""
    if not isinstance(raw, Mapping):
        raise CatalogueError(f"catalogue {path} must be a mapping")
    if (
        type(raw.get("catalogue_schema_version")) is not int
        or raw.get("catalogue_schema_version") != 4
    ):
        raise CatalogueError(
            "unsupported catalogue schema; expected catalogue_schema_version: 4"
        )
    return _parse_catalogue_v4(raw)


def _parse_catalogue_v4(root: Mapping[Any, Any]) -> CatalogueV4:
    """Validate, resolve artwork, and freeze one complete schema-v4 catalogue."""
    _closed_mapping(root, "root", ROOT_FIELDS)
    _required_fields(root, "root", ROOT_REQUIRED_FIELDS)
    _identifier(root["catalogue_id"], "catalogue_id")

    artwork_sources: Mapping[Any, Any] = {}
    if "artwork_sources" in root:
        artwork_sources = _validate_artwork_sources(root["artwork_sources"])

    items = _mapping(root["items"], "items", allow_empty=False)
    categories = _mapping(root["categories"], "categories", allow_empty=True)

    resolved_items: dict[Any, Any] = {}
    for item_id, item in items.items():
        _identifier(item_id, "items key")
        resolved_items[item_id] = _validate_item(
            item, f"items.{item_id}", artwork_sources
        )
    for category_id, category in categories.items():
        _identifier(category_id, "categories key")
        _validate_category(category, f"categories.{category_id}", items)

    resolved_root = dict(root)
    resolved_root["items"] = resolved_items
    return CatalogueV4(record=_freeze_mapping(resolved_root))


def _validate_artwork_sources(value: Any) -> Mapping[Any, Any]:
    sources = _mapping(value, "artwork_sources", allow_empty=False)
    for source_name, source_value in sources.items():
        if source_name != "ha-assets":
            raise CatalogueError(
                f"artwork_sources.{source_name} is not a supported artwork source"
            )
        source_path = f"artwork_sources.{source_name}"
        source = _mapping(source_value, source_path, allow_empty=False)
        _closed_mapping(source, source_path, ARTWORK_SOURCE_FIELDS)
        _reject_nulls(source, source_path)
        if not source:
            raise CatalogueError(f"{source_path} must not be empty")
        if "local" in source:
            local = _text(source["local"], f"{source_path}.local")
            if not local.startswith("/local/") or not local[len("/local/") :].strip():
                raise CatalogueError(
                    f"{source_path}.local must be a non-empty /local/... reference"
                )
        if "external" in source:
            _http_url(source["external"], f"{source_path}.external")
    return sources


def _validate_item(
    value: Any, path: str, artwork_sources: Mapping[Any, Any]
) -> Mapping[Any, Any]:
    item = _mapping(value, path, allow_empty=False)
    _closed_mapping(item, path, ITEM_FIELDS)
    _required_fields(item, path, ITEM_REQUIRED_FIELDS)
    _text(item["catalogue_label"], f"{path}.catalogue_label")
    item_type = _text(item["type"], f"{path}.type")
    if item_type not in TYPE_METADATA_FIELDS:
        raise CatalogueError(f"{path}.type has unsupported value {item_type!r}")
    for field in ("description", "content_rating"):
        if field in item:
            _text(item[field], f"{path}.{field}")
    if "tags" in item:
        _string_list(item["tags"], f"{path}.tags", identifiers=False)
    resolved = dict(item)
    if "artwork" in item:
        resolved["artwork"] = _validate_artwork(
            item["artwork"], f"{path}.artwork", artwork_sources
        )
    _validate_type_metadata(item["type_metadata"], item_type, f"{path}.type_metadata")
    _validate_execution_methods(item["execution_methods"], f"{path}.execution_methods")
    return resolved


def _validate_artwork(
    value: Any, path: str, artwork_sources: Mapping[Any, Any]
) -> Mapping[str, str]:
    artwork = _mapping(value, path, allow_empty=False)
    if "source_type" not in artwork:
        raise CatalogueError(f"{path}.source_type is required")
    source_type = _text(artwork["source_type"], f"{path}.source_type")
    if source_type not in ARTWORK_FIELDS:
        raise CatalogueError(
            f"{path}.source_type has unsupported value {source_type!r}"
        )
    allowed, required = ARTWORK_FIELDS[source_type]
    _closed_mapping(artwork, path, allowed)
    _required_fields(artwork, path, required)

    if source_type == "direct":
        resolved: dict[str, str] = {}
        if "local" in artwork:
            local = _text(artwork["local"], f"{path}.local")
            if not local.startswith("/local/") or not local[len("/local/") :].strip():
                raise CatalogueError(
                    f"{path}.local must be a non-empty /local/... reference"
                )
            resolved["local"] = local
        if "external" in artwork:
            resolved["external"] = _http_url(
                artwork["external"], f"{path}.external"
            )
        if not resolved:
            raise CatalogueError(
                f"{path} direct artwork requires local and/or external"
            )
        return resolved

    relative_path = _artwork_relative_path(artwork["path"], f"{path}.path")
    source = artwork_sources.get("ha-assets")
    if not isinstance(source, Mapping):
        raise CatalogueError(
            f"{path} references source_type 'ha-assets' but "
            "artwork_sources.ha-assets is missing"
        )
    resolved = {}
    for route in ("local", "external"):
        base = source.get(route)
        if isinstance(base, str):
            resolved[route] = f"{base.rstrip('/')}/{relative_path}"
    return resolved


def _artwork_relative_path(value: Any, path: str) -> str:
    relative = _text(value, path)
    if relative.startswith("/") or "\\" in relative:
        raise CatalogueError(
            f"{path} must be a relative forward-slash path"
        )
    parsed = urlsplit(relative)
    if parsed.scheme or parsed.netloc:
        raise CatalogueError(f"{path} must not be an absolute URL")
    segments = relative.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise CatalogueError(
            f"{path} must not contain empty, current-directory, or traversal segments"
        )
    return relative


def _validate_type_metadata(value: Any, item_type: str, path: str) -> None:
    metadata = _mapping(value, path, allow_empty=False)
    allowed, required = TYPE_METADATA_FIELDS[item_type]
    _closed_mapping(metadata, path, allowed)
    _required_fields(metadata, path, required)
    numeric_fields = {
        "disc_number", "track_number", "episode_number", "season_number",
        "width_pixels", "height_pixels",
    }
    date_fields = {"release_date", "publication_date", "first_broadcast_date"}
    other_fields = allowed - numeric_fields - date_fields - {
        "creation_datetime", "latitude", "longitude"
    }
    for field in other_fields & metadata.keys():
        _text(metadata[field], f"{path}.{field}")
    for field in numeric_fields & metadata.keys():
        _positive_integer(metadata[field], f"{path}.{field}")
    for field in date_fields & metadata.keys():
        _date(metadata[field], f"{path}.{field}")
    if "creation_datetime" in metadata:
        _datetime(metadata["creation_datetime"], f"{path}.creation_datetime")
    if "latitude" in metadata:
        _finite_number(metadata["latitude"], f"{path}.latitude", -90, 90)
    if "longitude" in metadata:
        _finite_number(metadata["longitude"], f"{path}.longitude", -180, 180)
    _paired_fields(metadata, path, "latitude", "longitude")
    _paired_fields(metadata, path, "width_pixels", "height_pixels")


def _validate_execution_methods(value: Any, path: str) -> None:
    methods = _mapping(value, path, allow_empty=False)
    for method_name, method_value in methods.items():
        _identifier(method_name, f"{path} key")
        if method_name not in EXECUTION_METHOD_SOURCE_TYPES:
            raise CatalogueError(
                f"{path}.{method_name} is not a supported execution method"
            )
        method_path = f"{path}.{method_name}"
        method = _mapping(method_value, method_path, allow_empty=False)
        _closed_mapping(method, method_path, frozenset({"source"}))
        _required_fields(method, method_path, frozenset({"source"}))
        _validate_source(method["source"], method_name, f"{method_path}.source")


def _validate_source(value: Any, method_name: str, path: str) -> None:
    source = _mapping(value, path, allow_empty=False)
    if "source_type" not in source:
        raise CatalogueError(f"{path}.source_type is required")
    source_type = _text(source["source_type"], f"{path}.source_type")
    if source_type not in SOURCE_FIELDS:
        raise CatalogueError(
            f"{path}.source_type has unsupported value {source_type!r}"
        )
    if source_type not in EXECUTION_METHOD_SOURCE_TYPES[method_name]:
        raise CatalogueError(
            f"{path}.source_type {source_type!r} is not permitted for {method_name!r}"
        )
    allowed, required = SOURCE_FIELDS[source_type]
    _closed_mapping(source, path, allowed)
    _required_fields(source, path, required)
    if source_type == "url":
        _http_url(source["url"], f"{path}.url")
        mime_type = _text(source["mime_type"], f"{path}.mime_type")
        if not MIME_TYPE_PATTERN.fullmatch(mime_type):
            raise CatalogueError(f"{path}.mime_type must be a type/subtype value")
        if "provider" in source:
            _identifier(source["provider"], f"{path}.provider")
    elif source_type == "ha_media_source":
        provider = _identifier(source["provider"], f"{path}.provider")
        uri = _text(source["uri"], f"{path}.uri")
        parsed = urlsplit(uri)
        if (
            parsed.scheme != "media-source"
            or parsed.netloc != provider
            or not parsed.path
            or parsed.path == "/"
            or any(character.isspace() for character in uri)
        ):
            raise CatalogueError(
                f"{path}.uri must be an absolute media-source:// URI whose "
                "authority equals provider and whose resource path is non-empty"
            )
        _text(source["media_type"], f"{path}.media_type")
    else:
        _identifier(source["provider"], f"{path}.provider")
        _text(source["command"], f"{path}.command")
        if type(source["append_target"]) is not bool:
            raise CatalogueError(f"{path}.append_target must be a boolean")


def _validate_category(value: Any, path: str, items: Mapping[Any, Any]) -> None:
    category = _mapping(value, path, allow_empty=False)
    fields = frozenset({"category_label", "items"})
    _closed_mapping(category, path, fields)
    _required_fields(category, path, fields)
    _text(category["category_label"], f"{path}.category_label")
    references = _string_list(category["items"], f"{path}.items", identifiers=True)
    for index, item_id in enumerate(references):
        if item_id not in items:
            raise CatalogueError(
                f"{path}.items[{index}] references unknown item {item_id!r}"
            )


def _mapping(value: Any, path: str, *, allow_empty: bool) -> Mapping[Any, Any]:
    if value is None:
        raise CatalogueError(f"{path} must not be null")
    if not isinstance(value, Mapping):
        raise CatalogueError(f"{path} must be a mapping")
    if not allow_empty and not value:
        raise CatalogueError(f"{path} must not be empty")
    return value


def _closed_mapping(
    value: Mapping[Any, Any], path: str, allowed: frozenset[str]
) -> None:
    for field in value:
        if not isinstance(field, str) or field not in allowed:
            raise CatalogueError(f"{path}.{field} is not a defined field")


def _required_fields(
    value: Mapping[Any, Any], path: str, required: frozenset[str]
) -> None:
    for field in required:
        if field not in value:
            prefix = "" if path == "root" else f"{path}."
            raise CatalogueError(f"{prefix}{field} is required")
    _reject_nulls(value, path)


def _reject_nulls(value: Mapping[Any, Any], path: str) -> None:
    for field, field_value in value.items():
        if field_value is None:
            prefix = "" if path == "root" else f"{path}."
            raise CatalogueError(f"{prefix}{field} must not be null")


def _identifier(value: Any, path: str) -> str:
    text = _text(value, path)
    if not IDENTIFIER_PATTERN.fullmatch(text):
        raise CatalogueError(f"{path} must match ^[a-z0-9][a-z0-9_-]*$")
    return text


def _text(value: Any, path: str) -> str:
    if value is None:
        raise CatalogueError(f"{path} must not be null")
    if not isinstance(value, str) or not value.strip():
        raise CatalogueError(f"{path} must be a non-blank string")
    return value


def _string_list(value: Any, path: str, *, identifiers: bool) -> list[str]:
    if value is None:
        raise CatalogueError(f"{path} must not be null")
    if not isinstance(value, list) or not value:
        raise CatalogueError(f"{path} must be a non-empty list")
    result: list[str] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        result.append(
            _identifier(item, item_path)
            if identifiers
            else _text(item, item_path)
        )
    if len(set(result)) != len(result):
        raise CatalogueError(f"{path} must contain unique values")
    return result


def _positive_integer(value: Any, path: str) -> int:
    if type(value) is not int or value <= 0:
        raise CatalogueError(f"{path} must be an integer greater than zero")
    return value


def _finite_number(value: Any, path: str, minimum: float, maximum: float) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, int | float)
        or not math.isfinite(value)
    ):
        raise CatalogueError(f"{path} must be a finite number")
    if not minimum <= value <= maximum:
        raise CatalogueError(f"{path} must be between {minimum:g} and {maximum:g}")
    return float(value)


def _date(value: Any, path: str) -> None:
    text = _text(value, path)
    if not DATE_PATTERN.fullmatch(text):
        raise CatalogueError(f"{path} must be a valid YYYY-MM-DD date string")
    try:
        date.fromisoformat(text)
    except ValueError as err:
        raise CatalogueError(f"{path} must be a valid YYYY-MM-DD date string") from err


def _datetime(value: Any, path: str) -> None:
    text = _text(value, path)
    if not DATETIME_PATTERN.fullmatch(text):
        raise CatalogueError(
            f"{path} must be an RFC 3339 datetime with an explicit offset"
        )
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as err:
        raise CatalogueError(
            f"{path} must be an RFC 3339 datetime with an explicit offset"
        ) from err


def _http_url(value: Any, path: str) -> str:
    text = _text(value, path)
    try:
        parsed = urlsplit(text)
        host = parsed.hostname
    except ValueError as err:
        raise CatalogueError(f"{path} must be an absolute HTTP(S) URL") from err
    if (
        parsed.scheme not in {"http", "https"}
        or not host
        or any(character.isspace() for character in text)
    ):
        raise CatalogueError(f"{path} must be an absolute HTTP(S) URL")
    return text


def _paired_fields(
    value: Mapping[Any, Any], path: str, first: str, second: str
) -> None:
    if (first in value) != (second in value):
        missing = second if first in value else first
        present = first if first in value else second
        raise CatalogueError(f"{path}.{missing} is required when {present} is present")


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
