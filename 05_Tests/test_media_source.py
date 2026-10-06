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
    CatalogueRegistry,
    CatalogueV4,
    _freeze_mapping,
    _load_catalogue,
)
from custom_components.mediacat.const import DATA_CATALOGUES, DOMAIN
from custom_components.mediacat.media_source import MediaCatSource

V4_CATALOGUE = (
    Path(__file__).parents[1]
    / "04_Implementation"
    / "haos"
    / "source"
    / "config"
    / "mediacat"
    / "catalogues"
    / "curated-media.yaml"
)

PLAYABLE_V4_ITEM_IDS = [
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
CURATED_ROOT = "catalogue/curated_media"
CURATED_CATEGORY = "registry/category/radio"
CURATED_ITEM_PREFIX = f"{CURATED_ROOT}/item/"


@dataclass
class FakeHass:
    """Provide the Home Assistant state used by the Media Source adapter."""

    data: dict[str, Any]


def _source(catalogue) -> tuple[FakeHass, MediaCatSource]:
    registry = CatalogueRegistry(
        catalogues={catalogue.catalogue_id: catalogue},
        source_paths={catalogue.catalogue_id: "fixture.yaml"},
    )
    hass = FakeHass(data={DOMAIN: {DATA_CATALOGUES: registry}})
    return hass, MediaCatSource(hass)


def _source_registry(*catalogues) -> tuple[FakeHass, MediaCatSource]:
    registry = CatalogueRegistry(
        catalogues={catalogue.catalogue_id: catalogue for catalogue in catalogues},
        source_paths={
            catalogue.catalogue_id: f"{catalogue.catalogue_id}.yaml"
            for catalogue in catalogues
        },
    )
    hass = FakeHass(data={DOMAIN: {DATA_CATALOGUES: registry}})
    return hass, MediaCatSource(hass)


def _item(
    hass: FakeHass, identifier: str = "", target_media_player: str | None = None
) -> MediaSourceItem:
    return MediaSourceItem(hass, DOMAIN, identifier, target_media_player)


def _run(awaitable):
    return asyncio.run(awaitable)


def _query(search_query: str):
    return media_player.SearchMediaQuery(search_query=search_query)


def _v4_catalogue_with_source(
    source: dict[str, Any], catalogue_id: str = "curated_media"
) -> CatalogueV4:
    return CatalogueV4(
        record=_freeze_mapping(
            {
                "catalogue_id": catalogue_id,
                "catalogue_schema_version": 4,
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


def _projection_catalogue(
    catalogue_id: str,
    categories: list[tuple[str, str, list[tuple[str, str]]]],
) -> CatalogueV4:
    """Build a catalogue with explicit category and item ordering."""
    items = {}
    category_records = {}
    for category_id, category_label, members in categories:
        category_records[category_id] = {
            "category_label": category_label,
            "items": [item_id for item_id, _ in members],
        }
        for item_id, item_label in members:
            items[item_id] = {
                "type": "radio",
                "catalogue_label": item_label,
                "execution_methods": {
                    "ha_mplayer": {
                        "source": {
                            "source_type": "url",
                            "url": f"https://example.test/{catalogue_id}/{item_id}",
                            "mime_type": "audio/aac",
                        }
                    }
                },
            }
    return CatalogueV4(
        record=_freeze_mapping(
            {
                "catalogue_id": catalogue_id,
                "catalogue_schema_version": 4,
                "items": items,
                "categories": category_records,
            }
        )
    )


def test_schema_v4_browse_filters_assistant_only_items_in_stored_order() -> None:
    """Expose the completed Radio category and its 14 playable members."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    assert isinstance(catalogue, CatalogueV4)
    hass, source = _source(catalogue)

    root = _run(source.async_browse_media(_item(hass)))
    assert [(child.identifier, child.title) for child in root.children] == [
        (CURATED_CATEGORY, "Radio")
    ]

    category = _run(source.async_browse_media(_item(hass, CURATED_CATEGORY)))
    assert [
        child.identifier.removeprefix(CURATED_ITEM_PREFIX)
        for child in category.children
    ] == PLAYABLE_V4_ITEM_IDS
    assert len(category.children) == 14
    assert not ASSISTANT_ONLY_ITEM_IDS.intersection(
        child.identifier.removeprefix(CURATED_ITEM_PREFIX)
        for child in category.children
    )

    classic = next(
        child
        for child in category.children
        if child.identifier == f"{CURATED_ITEM_PREFIX}classic_fm"
    )
    assert classic.title == "Classic FM"
    assert classic.thumbnail == "/local/ha-assets/media-assets/radio/images/128x128/Classic-FM.png"
    assert classic.media_content_type == "station"


def test_multi_catalogue_projection_merges_categories_and_scopes_items() -> None:
    """Hide catalogues while preserving defined category and item ordering."""
    first = _projection_catalogue(
        "first_catalogue",
        [
            (
                "radio",
                "Radio",
                [("first", "First"), ("shared_one", "Shared")],
            ),
            ("podcasts", "Podcasts", [("podcast", "Podcast")]),
        ],
    )
    second = _projection_catalogue(
        "second_catalogue",
        [
            (
                "radio",
                "Radio",
                [("second", "Second"), ("shared_two", "Shared")],
            ),
            ("audiobooks", "Audiobooks", [("book", "Book")]),
        ],
    )
    hass, source = _source_registry(first, second)

    root = _run(source.async_browse_media(_item(hass)))
    assert [(child.identifier, child.title) for child in root.children] == [
        ("registry/category/radio", "Radio"),
        ("registry/category/podcasts", "Podcasts"),
        ("registry/category/audiobooks", "Audiobooks"),
    ]

    category = _run(
        source.async_browse_media(_item(hass, "registry/category/radio"))
    )
    assert [(child.identifier, child.title) for child in category.children] == [
        ("catalogue/first_catalogue/item/first", "First"),
        ("catalogue/first_catalogue/item/shared_one", "Shared"),
        ("catalogue/second_catalogue/item/second", "Second"),
        ("catalogue/second_catalogue/item/shared_two", "Shared"),
    ]

    result = _run(
        source.async_search_media(
            _item(hass, "registry/category/radio"), _query("shared")
        )
    )
    assert [item.identifier for item in result.result] == [
        "catalogue/first_catalogue/item/shared_one",
        "catalogue/second_catalogue/item/shared_two",
    ]
    root_result = _run(
        source.async_search_media(_item(hass), _query("shared"))
    )
    assert [item.identifier for item in root_result.result] == [
        "catalogue/first_catalogue/item/shared_one",
        "catalogue/second_catalogue/item/shared_two",
    ]

    played = _run(
        source.async_resolve_media(
            _item(hass, "catalogue/second_catalogue/item/second")
        )
    )
    assert played.url == "https://example.test/second_catalogue/second"


def test_multi_catalogue_projection_rejects_conflicting_category_labels() -> None:
    """Fail explicitly when one category ID has multiple visible labels."""
    first = _projection_catalogue("first", [("radio", "Radio", [])])
    second = _projection_catalogue("second", [("radio", "Wireless", [])])
    hass, source = _source_registry(first, second)

    with pytest.raises(BrowseError, match="conflicting labels"):
        _run(source.async_browse_media(_item(hass)))


def test_single_curated_catalogue_rejects_legacy_media_source_paths() -> None:
    """Reject legacy unscoped paths and catalogue directories."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    hass, source = _source(catalogue)

    for identifier in ("category/radio", "item/bbc_radio_1"):
        with pytest.raises(
            BrowseError,
            match="catalogue-scoped MediaCat identifier is required",
        ):
            _run(source.async_browse_media(_item(hass, identifier)))

    for identifier in (CURATED_ROOT, f"{CURATED_ROOT}/category/radio"):
        with pytest.raises(BrowseError, match="Unknown MediaCat identifier"):
            _run(source.async_browse_media(_item(hass, identifier)))

    with pytest.raises(
        BrowseError,
        match="catalogue-scoped MediaCat identifier is required",
    ):
        _run(
            source.async_search_media(
                _item(hass, "category/radio"), _query("radio")
            )
        )

    with pytest.raises(BrowseError, match="search is unavailable"):
        _run(
            source.async_search_media(
                _item(hass, f"{CURATED_ROOT}/category/radio"),
                _query("radio"),
            )
        )

    with pytest.raises(
        Unresolvable,
        match="catalogue-scoped MediaCat identifier is required",
    ):
        _run(source.async_resolve_media(_item(hass, "item/bbc_radio_1")))


def test_schema_v4_search_uses_only_agreed_fields_and_preserves_order() -> None:
    """Search labels, descriptions, and tags while excluding unplayable items."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    hass, source = _source(catalogue)

    cases = {
        "classic fm": [f"{CURATED_ITEM_PREFIX}classic_fm"],
        "contemporary music": [f"{CURATED_ITEM_PREFIX}bbc_radio_1"],
        "hiphop": [f"{CURATED_ITEM_PREFIX}bbc_radio_1xtra"],
    }
    for query, expected in cases.items():
        root_result = _run(source.async_search_media(_item(hass), _query(query)))
        category_result = _run(
            source.async_search_media(_item(hass, CURATED_CATEGORY), _query(query))
        )
        assert [item.identifier for item in root_result.result] == expected
        assert [item.identifier for item in category_result.result] == expected

    ordered = _run(source.async_search_media(_item(hass), _query("radio")))
    assert [
        item.identifier.removeprefix(CURATED_ITEM_PREFIX)
        for item in ordered.result
    ] == (
        [
            item_id
            for item_id in PLAYABLE_V4_ITEM_IDS
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
                _item(hass, f"{CURATED_ITEM_PREFIX}bbc_radio_1"),
                _query("bbc"),
            )
        )


def test_schema_v4_direct_url_returns_exact_stored_values() -> None:
    """Resolve only the stored ha_mplayer URL and MIME without inference."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    hass, source = _source(catalogue)

    resolved = _run(
        source.async_resolve_media(
            _item(hass, f"{CURATED_ITEM_PREFIX}bbc_radio_1")
        )
    )
    stored = catalogue.items["bbc_radio_1"]["execution_methods"]["ha_mplayer"][
        "source"
    ]
    assert resolved == PlayMedia(stored["url"], stored["mime_type"])


def test_schema_v4_media_source_delegates_exactly_once(monkeypatch) -> None:
    """Pass the opaque URI and target through once and return the exact result."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    hass, source = _source(catalogue)
    calls = []
    delegated_result = PlayMedia("https://streams.example.test/classic", "audio/aac")

    async def delegate(hass_arg, uri, target_media_player):
        calls.append((hass_arg, uri, target_media_player))
        return delegated_result

    monkeypatch.setattr(media_source_module, "async_resolve_media_source", delegate)
    resolved = _run(
        source.async_resolve_media(
            _item(
                hass,
                f"{CURATED_ITEM_PREFIX}classic_fm",
                "media_player.kitchen",
            )
        )
    )

    stored_uri = catalogue.items["classic_fm"]["execution_methods"]["ha_mplayer"][
        "source"
    ]["uri"]
    assert calls == [(hass, stored_uri, "media_player.kitchen")]
    assert resolved is delegated_result


def test_schema_v4_delegated_failure_is_surfaced(monkeypatch) -> None:
    """Surface the owning Media Source failure without fallback or retry."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    hass, source = _source(catalogue)
    calls = []

    async def delegate(*args):
        calls.append(args)
        raise Unresolvable("Owning Media Source failed")

    monkeypatch.setattr(media_source_module, "async_resolve_media_source", delegate)
    with pytest.raises(Unresolvable, match="Owning Media Source failed"):
        _run(
            source.async_resolve_media(
                _item(hass, f"{CURATED_ITEM_PREFIX}classic_fm")
            )
        )
    assert len(calls) == 1


def test_schema_v4_recursion_boundaries_stop_explicitly(monkeypatch) -> None:
    """Reject self-reference and unresolved delegated Media Source output."""
    self_catalogue = _v4_catalogue_with_source(
        {
            "source_type": "ha_media_source",
            "provider": "mediacat",
            "uri": "media-source://mediacat/catalogue/curated_media/item/test_radio",
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
        _run(
            source.async_resolve_media(
                _item(hass, f"{CURATED_ITEM_PREFIX}test_radio")
            )
        )
    assert calls == []

    delegated_catalogue = _v4_catalogue_with_source(
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
                _item(
                    delegated_hass,
                    f"{CURATED_ITEM_PREFIX}test_radio",
                )
            )
        )
    assert len(calls) == 1


def test_schema_v4_unplayable_items_have_no_method_fallback() -> None:
    """Do not browse or resolve an unsupported ha_mplayer source via another method."""
    catalogue = _v4_catalogue_with_source(
        {
            "source_type": "assistant_command",
            "command": "Play Test Radio",
        }
    )
    hass, source = _source(catalogue)

    root = _run(source.async_browse_media(_item(hass)))
    assert [(child.identifier, child.title) for child in root.children] == [
        (CURATED_CATEGORY, "Radio")
    ]
    category = _run(source.async_browse_media(_item(hass, CURATED_CATEGORY)))
    assert category.children == []
    with pytest.raises(BrowseError, match="Unplayable MediaCat item"):
        _run(
            source.async_browse_media(
                _item(hass, f"{CURATED_ITEM_PREFIX}test_radio")
            )
        )
    with pytest.raises(Unresolvable, match="Unresolvable MediaCat item"):
        _run(
            source.async_resolve_media(
                _item(hass, f"{CURATED_ITEM_PREFIX}test_radio")
            )
        )


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
def test_schema_v4_unusable_sources_are_explicitly_unresolvable(
    source_record: dict[str, Any]
) -> None:
    """Reject missing direct MIME and unusable delegated URI without inference."""
    catalogue = _v4_catalogue_with_source(source_record)
    hass, source = _source(catalogue)

    with pytest.raises(Unresolvable, match="Unresolvable MediaCat item"):
        _run(
            source.async_resolve_media(
                _item(hass, f"{CURATED_ITEM_PREFIX}test_radio")
            )
        )


def test_schema_v4_unknown_and_assistant_only_items_fail_explicitly() -> None:
    """Reject missing identifiers and the three stored assistant-only records."""
    catalogue = _load_catalogue(V4_CATALOGUE)
    hass, source = _source(catalogue)

    with pytest.raises(BrowseError, match="Unknown MediaCat category"):
        _run(
            source.async_browse_media(
                _item(hass, "registry/category/missing")
            )
        )
    with pytest.raises(Unresolvable, match="Unknown MediaCat item"):
        _run(
            source.async_resolve_media(
                _item(hass, f"{CURATED_ITEM_PREFIX}missing")
            )
        )

    for item_id in ASSISTANT_ONLY_ITEM_IDS:
        with pytest.raises(BrowseError, match="Unplayable MediaCat item"):
            _run(
                source.async_browse_media(
                    _item(hass, f"{CURATED_ITEM_PREFIX}{item_id}")
                )
            )
        with pytest.raises(Unresolvable, match="Unresolvable MediaCat item"):
            _run(
                source.async_resolve_media(
                    _item(hass, f"{CURATED_ITEM_PREFIX}{item_id}")
                )
            )


def _v4_catalogue_with_resolved_artwork(artwork: dict[str, str]) -> CatalogueV4:
    return CatalogueV4(
        record=_freeze_mapping(
            {
                "catalogue_id": "curated_media",
                "catalogue_schema_version": 4,
                "items": {
                    "test_radio": {
                        "type": "radio",
                        "catalogue_label": "Test Radio",
                        "artwork": artwork,
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
                "categories": {
                    "radio": {
                        "category_label": "Radio",
                        "items": ["test_radio"],
                    }
                },
            }
        )
    )


def test_schema_v4_thumbnail_prefers_local_then_external_then_none() -> None:
    cases = [
        (
            {
                "local": "/local/ha-assets/media-assets/radio/local.png",
                "external": "https://example.test/external.png",
            },
            "/local/ha-assets/media-assets/radio/local.png",
        ),
        (
            {"external": "https://example.test/external.png"},
            "https://example.test/external.png",
        ),
        ({}, None),
    ]

    for artwork, expected in cases:
        catalogue = _v4_catalogue_with_resolved_artwork(artwork)
        hass, source = _source(catalogue)
        category = _run(
            source.async_browse_media(_item(hass, CURATED_CATEGORY))
        )
        assert len(category.children) == 1
        assert category.children[0].thumbnail == expected
