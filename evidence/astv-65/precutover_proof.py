"""Reproducible non-live ASTV-65 cross-product readiness proof."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from custom_components.curated_media.catalogue import _load_catalogue  # noqa: E402
from custom_components.curated_media.resolver import CatalogueResolver  # noqa: E402


HOME_ASSISTANT_ROOT = ROOT.parent
ASTV_ROOT = HOME_ASSISTANT_ROOT / "ASTV"
ADVMEDIA_ROOT = HOME_ASSISTANT_ROOT / "AdvMedia"
PRODUCTION_EVIDENCE_ROOT = HOME_ASSISTANT_ROOT / "Production_ReadOnly" / "starburst"

MEDIA_IDS = (
    "classic_fm",
    "lbc_news",
    "gold_radio",
    "bbc_radio_2",
    "smooth_radio",
    "lbc_radio",
    "news_briefing",
)
ASSISTANT_ONLY = ("smooth_radio", "lbc_radio", "news_briefing")
KITCHEN_AREA = "5fa17a3cccaf4af0a5daef18141375fd"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def iter_actions(value: Any):
    if isinstance(value, dict):
        action = value.get("action")
        if isinstance(action, str):
            yield action
        for child in value.values():
            yield from iter_actions(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_actions(child)


def main() -> None:
    target_intents = load_yaml(ASTV_ROOT / "assistive" / "astv_intent_catalogue.yaml")
    legacy_intents = load_yaml(
        ASTV_ROOT
        / "ASTV-64_Rollback"
        / "starburst"
        / "assistive"
        / "astv_intent_catalogue.yaml"
    )
    endpoints = load_yaml(
        PRODUCTION_EVIDENCE_ROOT / "assistive" / "astv_area_endpoints2.yaml"
    )
    advmedia_package = load_yaml(
        ADVMEDIA_ROOT / "packages" / "advmedia" / "advmedia_scripts.yaml"
    )["script"]

    assert tuple(target_intents) == MEDIA_IDS + ("morning_routine",)
    assert target_intents["morning_routine"] == legacy_intents["morning_routine"]

    catalogue = _load_catalogue(ROOT / "curated_media" / "catalogue.yaml")
    resolver = CatalogueResolver(catalogue)
    radio_members = tuple(catalogue.categories["radio"]["items"])
    playable_members = tuple(
        item_id
        for item_id in radio_members
        if "ha_mplayer" in catalogue.items[item_id]["execution_methods"]
    )
    assert len(radio_members) == 17
    assert len(playable_members) == 14
    assert all(item_id not in playable_members for item_id in ASSISTANT_ONLY)

    area_audio = endpoints[KITCHEN_AREA]["playback"]["audio"]
    preferences = tuple(area_audio["preference"])
    rows: list[dict[str, Any]] = []
    lookup_count = 0
    method_selection_count = 0
    advmedia_handoffs = 0
    assistant_commands = 0

    for intent_id in MEDIA_IDS:
        request = target_intents[intent_id]
        params = request["params"]
        assert tuple(params) == ("output", "catalogue_id", "item_id")
        assert params["output"] == {"domain": "audio"}
        assert params["catalogue_id"] == "curated_media"
        assert params["item_id"] == intent_id
        assert "sources" not in params

        lookup_count += 1
        media_record = resolver.resolve_media_record(
            params["catalogue_id"], params["item_id"]
        )
        record_before_dispatch = copy.deepcopy(media_record)
        available_methods = tuple(media_record["execution_methods"])
        selected_method = next(
            (method for method in preferences if method in available_methods), None
        )
        assert selected_method is not None
        method_selection_count += 1
        selected_endpoint = area_audio[selected_method]
        source = media_record["execution_methods"][selected_method]["source"]

        if selected_method == "ha_mplayer":
            assert selected_endpoint == {"media_entity": "media_player.kitchen_speaker"}
            assert source["source_type"] in {"url", "ha_media_source"}
            if source["source_type"] == "url":
                assert source["url"] and source["mime_type"]
            else:
                assert source["provider"] == "radio_browser"
                assert source["uri"].startswith("media-source://radio_browser/")
                assert source["media_type"] == "station"
            outcome = "AdvMedia core handoff intercepted"
            advmedia_handoffs += 1
        else:
            assert selected_method == "g_home_device"
            assert selected_endpoint == {"phrase": "Kitchen Speaker"}
            assert source["source_type"] == "assistant_command"
            assert source["provider"] == "google_assistant"
            command = source["command"]
            if source["append_target"]:
                command = f"{command} on {selected_endpoint['phrase']}"
            outcome = command
            assistant_commands += 1

        assert media_record == record_before_dispatch
        rows.append(
            {
                "intent_id": intent_id,
                "lookup_count": 1,
                "method_selection_count": 1,
                "selected_method": selected_method,
                "selected_endpoint": selected_endpoint,
                "source_type": source["source_type"],
                "intercepted_outcome": outcome,
            }
        )

    assert lookup_count == 7
    assert method_selection_count == 7
    assert advmedia_handoffs == 4
    assert assistant_commands == 3

    expected_advmedia = {
        "advmedia_prepare_playback",
        "advmedia_find_media_record",
        "advmedia_process_media_record",
        "advmedia_translate_media_source",
        "advmedia_resolve_player_mediaprofile",
        "advmedia_mediaprofile_handler",
        "advmedia_mediaprofile_generic",
        "advmedia_mediaprofile_googlecast",
    }
    assert set(advmedia_package) == expected_advmedia
    direct_core_actions = list(
        iter_actions(advmedia_package["advmedia_process_media_record"]["sequence"])
    )
    assert direct_core_actions.count("script.advmedia_translate_media_source") == 1
    assert direct_core_actions.count("script.advmedia_mediaprofile_handler") == 1
    assert not any(action.startswith("curated_media.") for action in direct_core_actions)

    compatibility_actions = list(
        iter_actions(advmedia_package["advmedia_prepare_playback"]["sequence"])
    )
    assert compatibility_actions.count("script.advmedia_find_media_record") == 1
    assert compatibility_actions.count("script.advmedia_process_media_record") == 2
    lookup_actions = list(
        iter_actions(advmedia_package["advmedia_find_media_record"]["sequence"])
    )
    assert lookup_actions.count("curated_media.resolve_media_record") == 1
    assert "curated_media.resolve_item" not in lookup_actions

    result = {
        "status": "passed",
        "records": rows,
        "totals": {
            "media_records": len(rows),
            "lookups": lookup_count,
            "method_selections": method_selection_count,
            "advmedia_handoffs_intercepted": advmedia_handoffs,
            "assistant_commands_intercepted": assistant_commands,
            "external_actions_executed": 0,
        },
        "media_browser": {
            "stored_radio_members": len(radio_members),
            "playable_members": len(playable_members),
            "playable_order": playable_members,
            "assistant_only_excluded": ASSISTANT_ONLY,
        },
        "advmedia": {
            "script_count": len(advmedia_package),
            "direct_core_lookup_count": 0,
            "compatibility_lookup_count": 1,
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
