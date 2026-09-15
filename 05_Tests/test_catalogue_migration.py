"""Focused non-live proof for the ASTV-56 Curated Media migration."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from homeassistant.util.yaml import load_yaml

from custom_components.curated_media.catalogue import CatalogueV3, _load_catalogue
from custom_components.curated_media.resolver import CatalogueResolver


ROOT = Path(__file__).parents[1]
TARGET = ROOT / "04_Source" / "config" / "curated_media" / "catalogue.yaml"
ROLLBACK_ROOT = (
    ROOT
    / "0A_Historic"
    / "Issue_Evidence"
    / "ASTV-56"
    / "rollback"
    / "schema-v2"
)
ROLLBACK_CATALOGUE = ROLLBACK_ROOT / "curated_media" / "catalogue.yaml"

EXISTING_ITEM_IDS = [
    "bbc_radio_1",
    "bbc_radio_1xtra",
    "bbc_radio_2",
    "bbc_radio_3",
    "bbc_radio_4",
    "bbc_radio_4_extra",
    "bbc_radio_5_live",
    "bbc_radio_5_sports_extra",
    "bbc_radio_6_music",
    "bbc_world_service",
    "bbc_radio_scotland",
]
NEW_ITEM_IDS = [
    "classic_fm",
    "lbc_news",
    "gold_radio",
    "smooth_radio",
    "lbc_radio",
    "news_briefing",
]
EXPECTED_ITEM_IDS = EXISTING_ITEM_IDS + NEW_ITEM_IDS

EXPECTED_NEW_ITEMS = {
    "classic_fm": {
        "type": "radio",
        "catalogue_label": "Classic FM",
        "type_metadata": {"station_name": "Classic FM"},
        "artwork": {"local": "/local/radio-logos/Classic-FM.png"},
        "execution_methods": {
            "ha_mplayer": {
                "source": {
                    "source_type": "ha_media_source",
                    "provider": "radio_browser",
                    "uri": (
                        "media-source://radio_browser/"
                        "bd1c441c-132a-4d48-a3f3-bdb386f4b09a"
                    ),
                    "media_type": "station",
                }
            }
        },
    },
    "lbc_news": {
        "type": "radio",
        "catalogue_label": "LBC News",
        "type_metadata": {"station_name": "LBC News"},
        "artwork": {"local": "/local/radio-logos/LBC-News.png"},
        "execution_methods": {
            "ha_mplayer": {
                "source": {
                    "source_type": "ha_media_source",
                    "provider": "radio_browser",
                    "uri": (
                        "media-source://radio_browser/"
                        "8e32c763-b926-4e57-9b8f-d60f1c5b48e3"
                    ),
                    "media_type": "station",
                }
            }
        },
    },
    "gold_radio": {
        "type": "radio",
        "catalogue_label": "Gold Radio",
        "type_metadata": {"station_name": "Gold Radio"},
        "artwork": {"local": "/local/radio-logos/Gold-Radio.png"},
        "execution_methods": {
            "ha_mplayer": {
                "source": {
                    "source_type": "ha_media_source",
                    "provider": "radio_browser",
                    "uri": (
                        "media-source://radio_browser/"
                        "9b3a5084-91ba-4d90-ac06-3e0ba8c50d67"
                    ),
                    "media_type": "station",
                }
            }
        },
    },
    "smooth_radio": {
        "type": "radio",
        "catalogue_label": "Smooth Radio",
        "type_metadata": {"station_name": "Smooth Radio"},
        "execution_methods": {
            "g_home_device": {
                "source": {
                    "source_type": "assistant_command",
                    "provider": "google_assistant",
                    "command": "Play Smooth Radio on Global Player",
                    "append_target": True,
                }
            }
        },
    },
    "lbc_radio": {
        "type": "radio",
        "catalogue_label": "LBC",
        "type_metadata": {"station_name": "LBC"},
        "execution_methods": {
            "g_home_device": {
                "source": {
                    "source_type": "assistant_command",
                    "provider": "google_assistant",
                    "command": "play LBC Radio on Global Player",
                    "append_target": True,
                }
            }
        },
    },
    "news_briefing": {
        "type": "radio",
        "catalogue_label": "My News Briefing",
        "type_metadata": {"station_name": "My News Briefing"},
        "execution_methods": {
            "g_home_device": {
                "source": {
                    "source_type": "assistant_command",
                    "provider": "google_assistant",
                    "command": "Play my news briefing",
                    "append_target": True,
                }
            }
        },
    },
}


def test_complete_v3_catalogue_loads_with_exact_root_population_and_order() -> None:
    """Load the cutover artifact and prove its exact identity and membership."""
    raw = load_yaml(TARGET)
    loaded = _load_catalogue(TARGET)

    assert isinstance(loaded, CatalogueV3)
    assert list(raw) == [
        "catalogue_id",
        "catalogue_schema_version",
        "items",
        "categories",
    ]
    assert raw["catalogue_id"] == "curated_media"
    assert raw["catalogue_schema_version"] == 3
    assert list(raw["items"]) == EXPECTED_ITEM_IDS
    assert len(raw["items"]) == len(set(raw["items"])) == 17
    assert list(raw["categories"]) == ["radio"]
    assert raw["categories"]["radio"] == {
        "category_label": "Radio",
        "items": EXPECTED_ITEM_IDS,
    }


def test_existing_items_preserve_v2_data_with_only_approved_changes() -> None:
    """Compare every migrated schema-v2 item with its preserved source record."""
    source = load_yaml(ROLLBACK_CATALOGUE)
    target = load_yaml(TARGET)

    assert source["version"] == 2
    assert list(source["items"]) == EXISTING_ITEM_IDS
    assert source["categories"]["radio"]["items"] == EXISTING_ITEM_IDS

    for item_id in EXISTING_ITEM_IDS:
        old = source["items"][item_id]
        new = target["items"][item_id]
        assert set(new) == {
            "type",
            "catalogue_label",
            "type_metadata",
            "artwork",
            "description",
            "tags",
            "execution_methods",
        }
        assert new["type"] == old["type"] == "radio"
        assert new["catalogue_label"] == old["title"]
        assert new["type_metadata"] == {"station_name": old["title"]}
        assert new["description"] == old["description"]
        assert new["tags"] == old["tags"]
        if item_id == "bbc_radio_4":
            assert new["artwork"] == {
                "local": "/local/curated_media/artwork/radio/BBC-Radio-4.png",
                "external": (
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/"
                    "BBC_Radio_4_2022.svg/960px-BBC_Radio_4_2022.svg.png"
                ),
            }
        else:
            assert new["artwork"] == old["artwork"]

        migrated_source = new["execution_methods"]["ha_mplayer"]["source"]
        assert set(new["execution_methods"]) == {"ha_mplayer"}
        assert migrated_source == {
            "source_type": "url",
            "url": old["source"]["url"],
            "mime_type": old["source"].get("mime_type", "audio/aac"),
        }


def test_six_astv_derived_items_match_the_approved_item_specific_values() -> None:
    """Prove every non-mechanical ASTV-derived target record exactly."""
    target = load_yaml(TARGET)
    assert {item_id: target["items"][item_id] for item_id in NEW_ITEM_IDS} == (
        EXPECTED_NEW_ITEMS
    )


def test_execution_methods_are_complete_without_legacy_or_inferred_fields() -> None:
    """Retain exactly one approved source per approved method and no v2 envelope."""
    items = load_yaml(TARGET)["items"]
    for item in items.values():
        assert "providers" not in item
        assert "source" not in item
        assert len(item["execution_methods"]) == 1
        for method in item["execution_methods"].values():
            assert list(method) == ["source"]
            assert "type" not in method["source"]
            assert "format" not in method["source"]

    assert items["bbc_radio_scotland"]["execution_methods"]["ha_mplayer"][
        "source"
    ]["mime_type"] == "audio/aac"
    assert "Kitchen Speaker" not in json.dumps(items["lbc_radio"])
    assert "artwork" not in items["smooth_radio"]
    assert "artwork" not in items["lbc_radio"]
    assert "artwork" not in items["news_briefing"]


def test_normalized_lookup_preserves_all_three_representative_source_shapes() -> None:
    """Return complete normalized records for the three migrated source types."""
    loaded = _load_catalogue(TARGET)
    assert isinstance(loaded, CatalogueV3)
    resolver = CatalogueResolver(loaded)

    representatives = {
        "bbc_radio_1": ("ha_mplayer", "url"),
        "classic_fm": ("ha_mplayer", "ha_media_source"),
        "smooth_radio": ("g_home_device", "assistant_command"),
    }
    for item_id, (method, source_type) in representatives.items():
        record = resolver.resolve_media_record("curated_media", item_id)
        assert record["returned_record_version"] == 1
        assert record["catalogue_id"] == "curated_media"
        assert record["item_id"] == item_id
        assert record["execution_methods"][method]["source"][
            "source_type"
        ] == source_type
        assert "catalogue_schema_version" not in record
        assert "providers" not in record

    assert resolver.resolve_media_record("curated_media", "classic_fm")[
        "execution_methods"
    ]["ha_mplayer"]["source"]["provider"] == "radio_browser"
    assert resolver.resolve_media_record("curated_media", "smooth_radio")[
        "execution_methods"
    ]["g_home_device"]["source"]["provider"] == "google_assistant"


def test_preserved_v2_package_loads_with_its_compatible_implementation() -> None:
    """Rehearse the rollback lookup in an isolated Python subprocess."""
    expected_hash = "5fd55cd35b89b8d1958954173b49c94e3429130aff9766a767b4a223d28f02a8"
    repository_path = ROLLBACK_CATALOGUE.relative_to(ROOT).as_posix()
    governed_blob = subprocess.run(
        ["git", "show", f"HEAD:{repository_path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    assert hashlib.sha256(governed_blob).hexdigest() == expected_hash
    assert subprocess.run(
        ["git", "diff", "--quiet", "--", repository_path],
        cwd=ROOT,
        check=False,
    ).returncode == 0

    script = """
import json
from pathlib import Path
from custom_components.curated_media.catalogue import _load_catalogue
from custom_components.curated_media.resolver import CatalogueResolver

catalogue = _load_catalogue(Path('curated_media/catalogue.yaml'))
record = CatalogueResolver(catalogue).resolve_item('bbc_radio_1').record
print(json.dumps({
    'version': catalogue.version,
    'item_count': len(catalogue.items),
    'provider': record['providers']['radio_music']['service'],
}))
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROLLBACK_ROOT,
        check=True,
        capture_output=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
    )
    rehearsal = json.loads(completed.stdout)
    assert rehearsal == {
        "version": 2,
        "item_count": 11,
        "provider": "bbc_radio_one",
    }
