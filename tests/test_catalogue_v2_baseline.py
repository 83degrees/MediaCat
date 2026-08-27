"""Regression coverage for the copied Curated Media schema-v2 baseline."""

from __future__ import annotations

from pathlib import Path

import pytest

from custom_components.curated_media.catalogue import _load_catalogue
from custom_components.curated_media.resolver import CatalogueResolver

FIXTURE = Path(__file__).parent / "fixtures" / "catalogue_v2.yaml"


@pytest.fixture
def catalogue():
    """Load the representative schema-v2 catalogue through the baseline loader."""
    return _load_catalogue(FIXTURE)


def test_load_preserves_complete_records_and_category_order(catalogue) -> None:
    """Preserve opaque fields and the authored category and membership order."""
    assert catalogue.version == 2
    assert list(catalogue.items) == ["station_alpha", "station_beta"]
    assert list(catalogue.categories) == ["favourites", "all_stations"]
    assert catalogue.categories["favourites"].item_ids == (
        "station_beta",
        "station_alpha",
    )

    record = catalogue.items["station_alpha"].record
    assert record["source"]["headers"] == {"User-Agent": "MediaCat test"}
    assert record["providers"]["radio_music"]["service"]["data"][
        "features"
    ] == ("live", "regional")


def test_loaded_data_is_recursively_immutable(catalogue) -> None:
    """Reject mutation of catalogue indexes, records, and nested sequences."""
    with pytest.raises(TypeError):
        catalogue.items["station_gamma"] = catalogue.items["station_alpha"]

    record = catalogue.items["station_alpha"].record
    with pytest.raises(TypeError):
        record["title"] = "Changed"
    with pytest.raises(TypeError):
        record["source"]["headers"]["User-Agent"] = "Changed"
    with pytest.raises(AttributeError):
        record["providers"]["radio_music"]["service"]["data"][
            "features"
        ].append("changed")


def test_resolver_returns_known_complete_item(catalogue) -> None:
    """Resolve a known ID through the current catalogue model."""
    resolved = CatalogueResolver(catalogue).resolve_item("station_alpha")

    assert resolved is catalogue.items["station_alpha"]
    assert resolved.item_id == "station_alpha"
    assert resolved.title == "Station Alpha"
    assert resolved.source.url == "https://streams.example.test/alpha.m3u8"
    assert resolved.record["providers"]["radio_music"]["service"]["domain"] == (
        "media_player"
    )

