"""Focused schema-v4 artwork source and resolution coverage."""

from pathlib import Path

import pytest

from custom_components.mediacat.catalogue import CatalogueError, _parse_catalogue


def base_root():
    return {
        "catalogue_id": "curated_media",
        "catalogue_schema_version": 4,
        "items": {
            "station": {
                "catalogue_label": "Station",
                "type": "radio",
                "type_metadata": {"station_name": "Station"},
                "execution_methods": {
                    "ha_mplayer": {
                        "source": {
                            "source_type": "url",
                            "url": "https://streams.example.test/live",
                            "mime_type": "audio/aac",
                        }
                    }
                },
            }
        },
        "categories": {},
    }


def parse(root):
    return _parse_catalogue(root, Path("artwork-v4.yaml"))


def test_ha_assets_artwork_resolves_local_and_external_routes():
    root = base_root()
    root["artwork_sources"] = {
        "ha-assets": {
            "local": "/local/ha-assets/",
            "external": "https://83degrees.github.io/ha-assets",
        }
    }
    root["items"]["station"]["artwork"] = {
        "source_type": "ha-assets",
        "path": "media-assets/radio/images/128x128/station.png",
    }

    catalogue = parse(root)
    assert dict(catalogue.items["station"]["artwork"]) == {
        "local": "/local/ha-assets/media-assets/radio/images/128x128/station.png",
        "external": "https://83degrees.github.io/ha-assets/media-assets/radio/images/128x128/station.png",
    }


def test_direct_artwork_resolves_without_source_metadata():
    root = base_root()
    root["items"]["station"]["artwork"] = {
        "source_type": "direct",
        "external": "https://images.example.test/station.png",
    }

    catalogue = parse(root)
    assert dict(catalogue.items["station"]["artwork"]) == {
        "external": "https://images.example.test/station.png"
    }


def test_item_without_artwork_remains_valid():
    assert "artwork" not in parse(base_root()).items["station"]


@pytest.mark.parametrize(
    "path",
    [
        "/media-assets/radio/image.png",
        "../image.png",
        "media-assets/../image.png",
        r"media-assets\\radio\\image.png",
        "https://example.test/image.png",
        "media-assets//image.png",
    ],
)
def test_ha_assets_rejects_unsafe_or_non_relative_path(path):
    root = base_root()
    root["artwork_sources"] = {"ha-assets": {"local": "/local/ha-assets/"}}
    root["items"]["station"]["artwork"] = {
        "source_type": "ha-assets",
        "path": path,
    }
    with pytest.raises(CatalogueError):
        parse(root)


def test_ha_assets_reference_requires_catalogue_source():
    root = base_root()
    root["items"]["station"]["artwork"] = {
        "source_type": "ha-assets",
        "path": "media-assets/radio/image.png",
    }
    with pytest.raises(CatalogueError, match="artwork_sources.ha-assets is missing"):
        parse(root)


def test_v4_rejects_legacy_v3_artwork_shape():
    root = base_root()
    root["items"]["station"]["artwork"] = {
        "local": "/local/legacy.png",
        "external": "https://images.example.test/legacy.png",
    }
    with pytest.raises(CatalogueError, match="source_type is required"):
        parse(root)


def test_unknown_artwork_source_type_is_rejected():
    root = base_root()
    root["items"]["station"]["artwork"] = {
        "source_type": "future",
        "path": "image.png",
    }
    with pytest.raises(CatalogueError, match="unsupported value"):
        parse(root)


def test_reparse_rebuilds_resolved_urls_from_current_source_bases():
    root = base_root()
    root["artwork_sources"] = {
        "ha-assets": {"local": "/local/ha-assets/"}
    }
    root["items"]["station"]["artwork"] = {
        "source_type": "ha-assets",
        "path": "media-assets/radio/image.png",
    }
    first = parse(root)
    assert first.items["station"]["artwork"]["local"] == (
        "/local/ha-assets/media-assets/radio/image.png"
    )

    root["artwork_sources"]["ha-assets"]["local"] = "/local/repointed-assets"
    second = parse(root)
    assert second.items["station"]["artwork"]["local"] == (
        "/local/repointed-assets/media-assets/radio/image.png"
    )
