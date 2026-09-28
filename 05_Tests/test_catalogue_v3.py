"""Closed-vocabulary validation coverage for stored MediaCat schema v4."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import pytest

from custom_components.mediacat.catalogue import (
    CatalogueError,
    CatalogueV4,
    _load_catalogue,
    _parse_catalogue,
)

ROOT = Path(__file__).parents[1]
FIXTURE = Path(__file__).parent / "fixtures" / "catalogue_v4.yaml"
MAINTAINED_CATALOGUE = (
    ROOT / "04_Source" / "config" / "mediacat" / "catalogue.yaml"
)


def valid_root() -> dict[str, Any]:
    """Return a small complete schema-v4 catalogue."""
    return {
        "catalogue_id": "curated_media",
        "catalogue_schema_version": 4,
        "items": {
            "station_alpha": {
                "catalogue_label": "Station Alpha",
                "type": "radio",
                "tags": ["radio", "live"],
                "artwork": {
                    "local": "/local/mediacat/station-alpha.png",
                    "external": "https://images.example.test/station-alpha.png",
                },
                "type_metadata": {"station_name": "Station Alpha"},
                "execution_methods": {
                    "ha_mplayer": {
                        "source": {
                            "source_type": "url",
                            "url": "https://streams.example.test/live.aac",
                            "mime_type": "audio/aac",
                            "provider": "example_streams",
                        }
                    }
                },
            }
        },
        "categories": {
            "featured": {
                "category_label": "Featured",
                "items": ["station_alpha"],
            }
        },
    }


def parse(root: dict[str, Any]) -> CatalogueV4:
    """Parse a synthetic catalogue through the production validator."""
    return _parse_catalogue(root, Path("non-live-v3.yaml"))


def delete_path(root: dict[str, Any], path: tuple[str, ...]) -> None:
    """Delete one nested field from a synthetic catalogue."""
    target = root
    for part in path[:-1]:
        target = target[part]
    del target[path[-1]]


@pytest.fixture
def catalogue() -> CatalogueV4:
    """Load the complete representative schema-v4 fixture."""
    return _load_catalogue(FIXTURE)


def test_loads_fixture_and_maintained_catalogue_with_authored_order(catalogue) -> None:
    """Accept both governed catalogues and retain item/category/list order."""
    assert catalogue.catalogue_id == "curated_media"
    assert [item["type"] for item in catalogue.items.values()] == [
        "radio",
        "music_track",
        "podcast_episode",
        "live_tv",
        "tv_episode",
        "movie",
        "photo",
    ]
    assert list(catalogue.categories) == ["featured", "audio", "visual"]
    assert catalogue.categories["featured"]["items"] == (
        "example_movie",
        "station_alpha",
        "example_photo",
    )
    maintained = _load_catalogue(MAINTAINED_CATALOGUE)
    assert maintained.catalogue_id == "curated_media"
    assert next(iter(maintained.items)) == "bbc_radio_1"


def test_accepts_every_type_source_shape_and_optional_value_class(catalogue) -> None:
    """Exercise the rich fixture's complete governed positive vocabulary."""
    sources = {
        method["source"]["source_type"]: method["source"]
        for item in catalogue.items.values()
        for method in item["execution_methods"].values()
    }
    assert set(sources) == {"url", "ha_media_source", "assistant_command"}
    assert sources["ha_media_source"]["provider"] == "radio_browser"
    assert sources["assistant_command"]["append_target"] is True
    assert catalogue.items["example_track"]["type_metadata"]["disc_number"] == 1
    assert catalogue.items["example_photo"]["type_metadata"]["latitude"] == 51.5072


def test_accepts_empty_categories_mapping() -> None:
    """Allow the sole schema exception for an empty required collection."""
    root = valid_root()
    root["categories"] = {}
    assert parse(root).categories == {}


def test_loaded_structure_is_recursively_immutable(catalogue) -> None:
    """Reject mutation of root, nested mappings, and stored lists."""
    with pytest.raises(TypeError):
        catalogue.record["catalogue_id"] = "changed"
    with pytest.raises(TypeError):
        catalogue.items["station_alpha"]["type_metadata"]["station_name"] = "Changed"
    with pytest.raises(AttributeError):
        catalogue.items["station_alpha"]["tags"].append("changed")
    with pytest.raises(AttributeError):
        catalogue.categories["featured"]["items"].append("changed")


@pytest.mark.parametrize(
    ("location", "field", "expected_path"),
    [
        ((), "fixture_note", "root.fixture_note"),
        (
            ("items", "station_alpha"),
            "catalogue_lable",
            "items.station_alpha.catalogue_lable",
        ),
        (
            ("items", "station_alpha", "artwork"),
            "caption",
            "items.station_alpha.artwork.caption",
        ),
        (
            ("items", "station_alpha", "type_metadata"),
            "genre",
            "items.station_alpha.type_metadata.genre",
        ),
        (
            ("items", "station_alpha", "execution_methods", "ha_mplayer"),
            "priority",
            "execution_methods.ha_mplayer.priority",
        ),
        (
            (
                "items",
                "station_alpha",
                "execution_methods",
                "ha_mplayer",
                "source",
            ),
            "transport_hint",
            "source.transport_hint",
        ),
        (
            ("categories", "featured"),
            "display_hint",
            "categories.featured.display_hint",
        ),
    ],
)
def test_rejects_unknown_field_at_every_structural_level(
    location: tuple[str, ...], field: str, expected_path: str
) -> None:
    """Enforce the closed vocabulary with correction-ready paths."""
    root = valid_root()
    target: dict[str, Any] = root
    for part in location:
        target = target[part]
    target[field] = "unknown"
    with pytest.raises(CatalogueError, match=re.escape(expected_path)):
        parse(root)


def test_rejects_duplicate_yaml_key_before_overwrite(tmp_path: Path) -> None:
    """Report both lines and the nested path for a duplicate key."""
    candidate = tmp_path / "duplicate.yaml"
    candidate.write_text(
        """catalogue_id: curated_media
catalogue_schema_version: 4
items:
  station_alpha:
    catalogue_label: Station Alpha
    catalogue_label: Overwritten
categories: {}
""",
        encoding="utf-8",
    )
    with pytest.raises(
        CatalogueError, match=r"items\.station_alpha\.catalogue_label is duplicated"
    ):
        _load_catalogue(candidate)


@pytest.mark.parametrize(
    ("path", "message"),
    [
        (("items",), "items is required"),
        (("items", "station_alpha", "catalogue_label"), "catalogue_label is required"),
        (
            ("items", "station_alpha", "type_metadata", "station_name"),
            "type_metadata must not be empty",
        ),
        (
            ("items", "station_alpha", "execution_methods", "ha_mplayer", "source"),
            "ha_mplayer must not be empty",
        ),
        (
            (
                "items",
                "station_alpha",
                "execution_methods",
                "ha_mplayer",
                "source",
                "mime_type",
            ),
            "mime_type is required",
        ),
        (("categories", "featured", "category_label"), "category_label is required"),
    ],
)
def test_rejects_missing_required_fields_with_structural_paths(
    path: tuple[str, ...], message: str
) -> None:
    """Reject required-field omission at every governed object level."""
    root = valid_root()
    delete_path(root, path)
    with pytest.raises(CatalogueError, match=message):
        parse(root)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda root: root.__setitem__("catalogue_id", "Invalid"), "catalogue_id must match"),
        (lambda root: root.__setitem__("items", {}), "items must not be empty"),
        (lambda root: root["items"]["station_alpha"].__setitem__("catalogue_label", " "), "catalogue_label must be a non-blank"),
        (lambda root: root["items"]["station_alpha"].__setitem__("description", None), "description must not be null"),
        (lambda root: root["items"]["station_alpha"].__setitem__("tags", []), "tags must be a non-empty list"),
        (lambda root: root["items"]["station_alpha"].__setitem__("tags", ["radio", "radio"]), "tags must contain unique"),
        (lambda root: root["items"]["station_alpha"].__setitem__("artwork", {}), "artwork must not be empty"),
        (lambda root: root["items"]["station_alpha"]["artwork"].__setitem__("local", "/local/"), "artwork.local must be a non-empty"),
        (lambda root: root["items"]["station_alpha"]["artwork"].__setitem__("external", "ftp://example.test/a"), "artwork.external must be an absolute HTTP"),
        (lambda root: root["items"]["station_alpha"].__setitem__("type", "future_type"), "type has unsupported value"),
        (lambda root: root["items"]["station_alpha"].__setitem__("execution_methods", {}), "execution_methods must not be empty"),
        (lambda root: root["categories"]["featured"].__setitem__("items", ["missing"]), "references unknown item"),
        (lambda root: root["categories"]["featured"].__setitem__("items", ["station_alpha", "station_alpha"]), "items must contain unique"),
    ],
)
def test_requiredness_empty_null_identifier_reference_and_uniqueness_rules(
    mutate, message: str
) -> None:
    """Reject representative cross-cutting structural and value violations."""
    root = valid_root()
    mutate(root)
    with pytest.raises(CatalogueError, match=message):
        parse(root)


@pytest.mark.parametrize(
    ("location", "old_key", "new_key", "message"),
    [
        (("items",), "station_alpha", "Station Alpha", "items key must match"),
        (("categories",), "featured", "featured/all", "categories key must match"),
    ],
)
def test_rejects_invalid_dynamic_mapping_identifiers(
    location: tuple[str, ...], old_key: str, new_key: str, message: str
) -> None:
    """Apply the identifier grammar to item and category mapping keys."""
    root = valid_root()
    target = root
    for part in location:
        target = target[part]
    target[new_key] = target.pop(old_key)
    with pytest.raises(CatalogueError, match=message):
        parse(root)


def test_rejects_invalid_provider_identifier() -> None:
    """Apply the identifier grammar to source providers."""
    root = valid_root()
    source = root["items"]["station_alpha"]["execution_methods"]["ha_mplayer"][
        "source"
    ]
    source["provider"] = "Example Streams"
    with pytest.raises(CatalogueError, match="source.provider must match"):
        parse(root)


@pytest.mark.parametrize(
    ("item_type", "metadata", "message"),
    [
        ("radio", {}, "type_metadata must not be empty"),
        ("music_track", {"track_title": "Track", "disc_number": 0}, "disc_number must be an integer greater"),
        ("music_track", {"track_title": "Track", "release_date": "2026-02-30"}, "release_date must be a valid"),
        ("photo", {"image_title": "Photo", "creation_datetime": "2026-01-01T00:00:00"}, "creation_datetime must be an RFC 3339"),
        ("photo", {"image_title": "Photo", "latitude": 91, "longitude": 0}, "latitude must be between"),
        ("photo", {"image_title": "Photo", "latitude": 51.5}, "longitude is required when latitude"),
        ("photo", {"image_title": "Photo", "width_pixels": 100}, "height_pixels is required when width_pixels"),
        ("photo", {"image_title": "Photo", "width_pixels": True, "height_pixels": 10}, "width_pixels must be an integer"),
    ],
)
def test_type_selected_metadata_value_and_pairing_rules(
    item_type: str, metadata: dict[str, Any], message: str
) -> None:
    """Apply exact metadata vocabularies and type-specific constraints."""
    root = valid_root()
    item = root["items"]["station_alpha"]
    item["type"] = item_type
    item["type_metadata"] = metadata
    with pytest.raises(CatalogueError, match=message):
        parse(root)


@pytest.mark.parametrize(
    ("method", "source", "message"),
    [
        (
            "ha_mplayer",
            {"source_type": "assistant_command", "provider": "google_assistant", "command": "Play", "append_target": True},
            "is not permitted for 'ha_mplayer'",
        ),
        (
            "ha_mplayer",
            {"source_type": "url", "url": "relative", "mime_type": "audio/aac"},
            "url must be an absolute HTTP",
        ),
        (
            "ha_mplayer",
            {"source_type": "url", "url": "https://example.test/live", "mime_type": "aac"},
            "mime_type must be a type/subtype",
        ),
        (
            "ha_mplayer",
            {"source_type": "ha_media_source", "provider": "radio_browser", "uri": "media-source://other/item", "media_type": "station"},
            "authority equals provider",
        ),
        (
            "g_home_device",
            {"source_type": "assistant_command", "provider": "google_assistant", "command": " ", "append_target": True},
            "command must be a non-blank",
        ),
        (
            "g_home_device",
            {"source_type": "assistant_command", "provider": "google_assistant", "command": "Play", "append_target": 1},
            "append_target must be a boolean",
        ),
    ],
)
def test_method_source_pairing_and_source_value_rules(
    method: str, source: dict[str, Any], message: str
) -> None:
    """Reject invalid method/source combinations and malformed source values."""
    root = valid_root()
    root["items"]["station_alpha"]["execution_methods"] = {
        method: {"source": source}
    }
    with pytest.raises(CatalogueError, match=message):
        parse(root)


def test_schema_dispatch_remains_v3_only() -> None:
    """Do not reintroduce executable schema-v2 compatibility."""
    with pytest.raises(CatalogueError, match="expected catalogue_schema_version: 4"):
        _parse_catalogue(
            {"catalogue_schema_version": 2, "items": {}, "categories": {}},
            Path("historical-v2.yaml"),
        )
