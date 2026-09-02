"""Focused model coverage for the stored Curated Media schema v3."""

from __future__ import annotations

from pathlib import Path

import pytest

from custom_components.curated_media.catalogue import (
    CatalogueError,
    CatalogueV3,
    _load_catalogue,
    _parse_catalogue,
)

FIXTURE = Path(__file__).parent / "fixtures" / "catalogue_v3.yaml"


@pytest.fixture
def catalogue() -> CatalogueV3:
    """Load the complete non-live schema-v3 fixture directly."""
    loaded = _load_catalogue(FIXTURE)
    assert isinstance(loaded, CatalogueV3)
    return loaded


def test_loads_complete_v3_fixture_and_preserves_authored_order(catalogue) -> None:
    """Retain every agreed item type and both levels of authored ordering."""
    assert catalogue.catalogue_id == "curated_media"
    assert catalogue.catalogue_schema_version == 3
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


def test_preserves_all_source_shapes_and_multiple_methods(catalogue) -> None:
    """Retain the three source shapes and one source beneath every method."""
    sources = {
        method["source"]["source_type"]: method["source"]
        for item in catalogue.items.values()
        for method in item["execution_methods"].values()
    }
    assert set(sources) == {"url", "ha_media_source", "assistant_command"}
    assert catalogue.items["station_alpha"]["execution_methods"]["ha_mplayer"][
        "source"
    ] == {
        "source_type": "url",
        "url": "https://streams.example.test/station_alpha.m3u8",
        "mime_type": "application/vnd.apple.mpegurl",
        "provider": "example_streams",
        "transport_hint": "live",
    }
    assert sources["ha_media_source"] == {
        "source_type": "ha_media_source",
        "provider": "radio_browser",
        "uri": "media-source://radio_browser/example-track",
        "media_type": "music",
    }
    assert sources["assistant_command"] == {
        "source_type": "assistant_command",
        "provider": "google_assistant",
        "command": "Play Station Alpha",
        "append_target": True,
    }

    methods = catalogue.items["station_alpha"]["execution_methods"]
    assert list(methods) == ["ha_mplayer", "g_home_device"]
    assert all(tuple(method) == ("source",) for method in methods.values())


def test_preserves_type_metadata_and_unknown_additive_fields(catalogue) -> None:
    """Retain representative metadata and additive data at every root level."""
    expected_metadata_fields = {
        "station_alpha": {"station_name"},
        "example_track": {
            "track_title",
            "artist",
            "album_artist",
            "album_title",
            "composer",
            "disc_number",
            "track_number",
            "release_date",
        },
        "example_podcast": {
            "episode_title",
            "podcast_title",
            "creator",
            "publisher",
            "publication_date",
            "episode_number",
        },
        "example_live_tv": {"channel_name"},
        "example_tv_episode": {
            "episode_title",
            "series_title",
            "season_number",
            "episode_number",
            "first_broadcast_date",
        },
        "example_movie": {
            "movie_title",
            "secondary_title",
            "studio",
            "release_date",
        },
        "example_photo": {
            "image_title",
            "creator",
            "creation_datetime",
            "location",
            "latitude",
            "longitude",
            "width_pixels",
            "height_pixels",
        },
    }
    assert {
        item_id: set(item["type_metadata"])
        for item_id, item in catalogue.items.items()
    } == expected_metadata_fields
    assert catalogue.items["example_track"]["type_metadata"] == {
        "track_title": "Example Track",
        "artist": "Example Artist",
        "album_artist": "Example Album Artist",
        "album_title": "Example Album",
        "composer": "Example Composer",
        "disc_number": 1,
        "track_number": 3,
        "release_date": "2026-01-02",
    }
    assert catalogue.record["fixture_note"]["purpose"] == (
        "non-live schema-v3 model coverage"
    )
    station = catalogue.items["station_alpha"]
    assert station["providers"]["legacy_radio"]["service"]["features"] == (
        "live",
        "regional",
    )
    assert station["extension_metadata"]["editorial_note"] == (
        "retained additive item field"
    )
    assert station["execution_methods"]["ha_mplayer"]["source"][
        "transport_hint"
    ] == "live"
    assert catalogue.categories["featured"]["display_hint"] == "hero"


def test_loaded_v3_structure_is_recursively_immutable(catalogue) -> None:
    """Reject mutation of root, item, category, mapping, and list structures."""
    with pytest.raises(TypeError):
        catalogue.record["catalogue_id"] = "changed"
    with pytest.raises(TypeError):
        catalogue.items["station_alpha"]["type_metadata"]["station_name"] = (
            "Changed"
        )
    with pytest.raises(AttributeError):
        catalogue.items["station_alpha"]["tags"].append("changed")
    with pytest.raises(AttributeError):
        catalogue.categories["featured"]["items"].append("changed")


@pytest.mark.parametrize(
    ("root", "message"),
    [
        ([], "must be a mapping"),
        ({"items": {}, "categories": {}}, "unsupported catalogue schema"),
        (
            {"catalogue_schema_version": 3, "items": {}, "categories": {}},
            "catalogue_id must be present",
        ),
        (
            {
                "catalogue_id": "curated_media",
                "catalogue_schema_version": 3,
                "items": [],
                "categories": {},
            },
            "items must be a mapping",
        ),
        (
            {
                "catalogue_id": "curated_media",
                "catalogue_schema_version": 3,
                "items": {},
                "categories": [],
            },
            "categories must be a mapping",
        ),
    ],
)
def test_v3_dispatch_applies_only_the_minimum_structural_boundary(
    root, message
) -> None:
    """Select only an explicit v3 root and enforce its minimum structure."""
    with pytest.raises(CatalogueError, match=message):
        _parse_catalogue(root, Path("non-live-v3.yaml"))


def test_v3_does_not_enforce_deferred_item_or_source_policy() -> None:
    """Avoid turning representative fixture coverage into validation policy."""
    loaded = _parse_catalogue(
        {
            "catalogue_id": None,
            "catalogue_schema_version": 3,
            7: {"additive": "root field"},
            "items": {1: {"type": "future_type", "source": None}},
            "categories": {2: {"items": ["missing", "missing"]}},
        },
        Path("deferred-policy.yaml"),
    )

    assert isinstance(loaded, CatalogueV3)
    assert loaded.catalogue_id is None
    assert loaded.record[7]["additive"] == "root field"
    assert loaded.items[1]["type"] == "future_type"
    assert loaded.categories[2]["items"] == ("missing", "missing")
