"""Interface-behaviour coverage for MediaCat's Media Source adapter."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from homeassistant.components import media_player
from homeassistant.components import media_source as media_source_component
from homeassistant.components.media_player import BrowseError
from homeassistant.components.media_source import (
    MediaSourceItem,
    PlayMedia,
    Unresolvable,
)

# The repository's documented test-only Home Assistant 2024.12.5 baseline predates
# these Media Browser search containers. Supply only their adapter-facing shape so
# this non-live suite can exercise the copied newer Media Source implementation.
if not hasattr(media_player, "SearchMedia"):

    @dataclass(slots=True)
    class BrowseMediaSource:
        """Represent the newer browse result fields used by the adapter."""

        domain: str | None
        identifier: str | None
        media_class: Any
        media_content_type: str
        title: str
        can_play: bool
        can_expand: bool
        can_search: bool = False
        children_media_class: Any | None = None
        children: list[Any] | None = None
        thumbnail: str | None = None

    @dataclass(slots=True)
    class SearchMedia:
        """Represent search results used by the adapter under test."""

        result: list[Any]

    @dataclass(slots=True)
    class SearchMediaQuery:
        """Represent the search query field used by the adapter under test."""

        search_query: str

    media_player.SearchMedia = SearchMedia
    media_player.SearchMediaQuery = SearchMediaQuery
    media_source_component.BrowseMediaSource = BrowseMediaSource

from custom_components.mediacat import media_source as media_source_module
from custom_components.mediacat.catalogue import (
    CatalogueV3,
    _freeze_mapping,
    _load_catalogue,
)
from custom_components.mediacat.const import DATA_CATALOGUE, DOMAIN
from custom_components.mediacat.media_source import MediaCatSource

V3_CATALOGUE = (
    Path(__file__).parents[1]
    / "04_Source"
    / "config"
    / "mediacat"
    / "catalogue.yaml"
)

PLAYABLE_V3_ITEM_IDS = [
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
    "classic_fm",
    "lbc_news",
    "gold_radio",
]
ASSISTANT_ONLY_ITEM_IDS = {"smooth_radio", "lbc_radio", "news_briefing"}


@dataclass
class FakeHass:
    """Provide the Home Assistant state used by the Media Source adapter."""

    data: dict[str, Any]


def _source(catalogue) -> tuple[FakeHass, MediaCatSource]:
    hass = FakeHass(data={DOMAIN: {DATA_CATALOGUE: catalogue}})
    return hass, MediaCatSource(hass)


def _item(
    hass: FakeHass, identifier: str = "", target_media_player: str | None = None
) -> MediaSourceItem:
    return MediaSourceItem(hass, DOMAIN, identifier, target_media_player)


def _run(awaitable):
    return asyncio.run(awaitable)


def _query(search_query: str):
    return media_player.SearchMediaQuery(search_query=search_query)


def _v3_catalogue_with_source(source: dict[str, Any]) -> CatalogueV3:
    return CatalogueV3(
        record=_freeze_mapping(
            {
                "catalogue_id": "curated_media",
                "catalogue_schema_version": 3,
                "items": {
                    "test_radio": {
                        "type": "radio",
                        "catalogue_label": "Test Radio",
                        "execution_methods": {
                            "ha_mplayer": {"source": source},
                            "g_home_device": {
                                "source": {
                                    "source_type": "assistant_command",
                                    "command": "Play Test Radio",
                                }
                            },
                        },
                    }
                },
                "categories": {
                    "radio": {
                        "category_label": "Radio",
                        "items": ["test_radio"],
                    }
                },
            }
        )
    )


def test_schema_v3_browse_filters_assistant_only_items_in_stored_order() -> None:
    """Expose the completed Radio category and its 14 playable members."""
    catalogue = _load_catalogue(V3_CATALOGUE)
    assert isinstance(catalogue, CatalogueV3)
    hass, source = _source(catalogue)

    root = _run(source.async_browse_media(_item(hass)))
    assert [(child.identifier, child.title) for child in root.children] == [
        ("category/radio", "Radio")
    ]

    category = _run(source.async_browse_media(_item(hass, "category/radio")))
    assert [child.identifier.removeprefix("item/") for child in category.children] == (
        PLAYABLE_V3_ITEM_IDS
    )
    assert len(category.children) == 14
    assert not ASSISTANT_ONLY_ITEM_IDS.intersection(
        child.identifier.removeprefix("item/") for child in category.children
    )

    classic = next(
        child
        for child in category.children
        if child.identifier == "item/classic_fm"
    )
    assert classic.title == "Classic FM"
    assert classic.thumbnail == "/local/radio-logos/Classic-FM.png"
    assert classic.media_content_type == "station"


def test_schema_v3_search_uses_only_agreed_fields_and_preserves_order() -> None:
    """Search labels, descriptions, and tags while excluding unplayable items."""
    catalogue = _load_catalogue(V3_CATALOGUE)
    hass, source = _source(catalogue)

    cases = {
        "classic fm": ["item/classic_fm"],
        "contemporary music": ["item/bbc_radio_1"],
        "hiphop": ["item/bbc_radio_1xtra"],
    }
    for query, expected in cases.items():
        root_result = _run(source.async_search_media(_item(hass), _query(query)))
        category_result = _run(
            source.async_search_media(_item(hass, "category/radio"), _query(query))
        )
        assert [item.identifier for item in root_result.result] == expected
        assert [item.identifier for item in category_result.result] == expected

    ordered = _run(source.async_search_media(_item(hass), _query("radio")))
    assert [item.identifier.removeprefix("item/") for item in ordered.result] == (
        [
            item_id
            for item_id in PLAYABLE_V3_ITEM_IDS
            if item_id not in {"classic_fm", "lbc_news"}
        ]
    )
    assistant_only = _run(
        source.async_search_media(_item(hass), _query("smooth radio"))
    )
    assert assistant_only.result == []
    blank = _run(source.async_search_media(_item(hass), _query("  ")))
    assert blank.result == []
    with pytest.raises(BrowseError, match="search is unavailable"):
        _run(
            source.async_search_media(
                _item(hass, "item/bbc_radio_1"), _query("bbc")
            )
        )


def test_schema_v3_direct_url_returns_exact_stored_values() -> None:
    """Resolve only the stored ha_mplayer URL and MIME without inference."""
    catalogue = _load_catalogue(V3_CATALOGUE)
    hass, source = _source(catalogue)

    resolved = _run(
        source.async_resolve_media(_item(hass, "item/bbc_radio_1"))
    )
    stored = catalogue.items["bbc_radio_1"]["execution_methods"]["ha_mplayer"][
        "source"
    ]
    assert resolved == PlayMedia(stored["url"], stored["mime_type"])


def test_schema_v3_media_source_delegates_exactly_once(monkeypatch) -> None:
    """Pass the opaque URI and target through once and return the exact result."""
    catalogue = _load_catalogue(V3_CATALOGUE)
    hass, source = _source(catalogue)
    calls = []
    delegated_result = PlayMedia("https://streams.example.test/classic", "audio/aac")

    async def delegate(hass_arg, uri, target_media_player):
        calls.append((hass_arg, uri, target_media_player))
        return delegated_result

    monkeypatch.setattr(media_source_module, "async_resolve_media_source", delegate)
    resolved = _run(
        source.async_resolve_media(
            _item(hass, "item/classic_fm", "media_player.kitchen")
        )
    )

    stored_uri = catalogue.items["classic_fm"]["execution_methods"]["ha_mplayer"][
        "source"
    ]["uri"]
    assert calls == [(hass, stored_uri, "media_player.kitchen")]
    assert resolved is delegated_result


def test_schema_v3_delegated_failure_is_surfaced(monkeypatch) -> None:
    """Surface the owning Media Source failure without fallback or retry."""
    catalogue = _load_catalogue(V3_CATALOGUE)
    hass, source = _source(catalogue)
    calls = []

    async def delegate(*args):
        calls.append(args)
        raise Unresolvable("Owning Media Source failed")

    monkeypatch.setattr(media_source_module, "async_resolve_media_source", delegate)
    with pytest.raises(Unresolvable, match="Owning Media Source failed"):
        _run(source.async_resolve_media(_item(hass, "item/classic_fm")))
    assert len(calls) == 1


def test_schema_v3_recursion_boundaries_stop_explicitly(monkeypatch) -> None:
    """Reject self-reference and unresolved delegated Media Source output."""
    self_catalogue = _v3_catalogue_with_source(
        {
            "source_type": "ha_media_source",
            "provider": "mediacat",
            "uri": "media-source://mediacat/item/test_radio",
            "media_type": "station",
        }
    )
    hass, source = _source(self_catalogue)
    calls = []

    async def delegate(*args):
        calls.append(args)
        return PlayMedia("media-source://other/item/still-unresolved", "station")

    monkeypatch.setattr(media_source_module, "async_resolve_media_source", delegate)
    with pytest.raises(Unresolvable, match="refers back to MediaCat"):
        _run(source.async_resolve_media(_item(hass, "item/test_radio")))
    assert calls == []

    delegated_catalogue = _v3_catalogue_with_source(
        {
            "source_type": "ha_media_source",
            "provider": "stored_provider_name",
            "uri": "media-source://other/item/test_radio",
            "media_type": "station",
        }
    )
    delegated_hass, delegated_source = _source(delegated_catalogue)
    with pytest.raises(Unresolvable, match="resolved to another Media Source URI"):
        _run(
            delegated_source.async_resolve_media(
                _item(delegated_hass, "item/test_radio")
            )
        )
    assert len(calls) == 1


def test_schema_v3_unplayable_items_have_no_method_fallback() -> None:
    """Do not browse or resolve an unsupported ha_mplayer source via another method."""
    catalogue = _v3_catalogue_with_source(
        {
            "source_type": "assistant_command",
            "command": "Play Test Radio",
        }
    )
    hass, source = _source(catalogue)

    root = _run(source.async_browse_media(_item(hass)))
    assert [(child.identifier, child.title) for child in root.children] == [
        ("category/radio", "Radio")
    ]
    category = _run(source.async_browse_media(_item(hass, "category/radio")))
    assert category.children == []
    with pytest.raises(BrowseError, match="Unplayable MediaCat item"):
        _run(source.async_browse_media(_item(hass, "item/test_radio")))
    with pytest.raises(Unresolvable, match="Unresolvable MediaCat item"):
        _run(source.async_resolve_media(_item(hass, "item/test_radio")))


@pytest.mark.parametrize(
    "source_record",
    [
        {"source_type": "url", "url": "https://streams.example.test/test"},
        {
            "source_type": "ha_media_source",
            "uri": "not-a-media-source-uri",
            "media_type": "station",
        },
    ],
)
def test_schema_v3_unusable_sources_are_explicitly_unresolvable(
    source_record: dict[str, Any]
) -> None:
    """Reject missing direct MIME and unusable delegated URI without inference."""
    catalogue = _v3_catalogue_with_source(source_record)
    hass, source = _source(catalogue)

    with pytest.raises(Unresolvable, match="Unresolvable MediaCat item"):
        _run(source.async_resolve_media(_item(hass, "item/test_radio")))


def test_schema_v3_unknown_and_assistant_only_items_fail_explicitly() -> None:
    """Reject missing identifiers and the three stored assistant-only records."""
    catalogue = _load_catalogue(V3_CATALOGUE)
    hass, source = _source(catalogue)

    with pytest.raises(BrowseError, match="Unknown MediaCat category"):
        _run(source.async_browse_media(_item(hass, "category/missing")))
    with pytest.raises(Unresolvable, match="Unknown MediaCat item"):
        _run(source.async_resolve_media(_item(hass, "item/missing")))

    for item_id in ASSISTANT_ONLY_ITEM_IDS:
        with pytest.raises(BrowseError, match="Unplayable MediaCat item"):
            _run(source.async_browse_media(_item(hass, f"item/{item_id}")))
        with pytest.raises(Unresolvable, match="Unresolvable MediaCat item"):
            _run(source.async_resolve_media(_item(hass, f"item/{item_id}")))
