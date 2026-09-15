"""Non-live proof for the parallel MediaCat domain migration."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

from homeassistant.components import media_player
from homeassistant.components import media_source as media_source_component
from homeassistant.util.yaml import load_yaml

# The pinned test-only Home Assistant baseline predates the Media Browser search
# containers used by the maintained adapter. Supply their adapter-facing shape.
if not hasattr(media_player, "SearchMedia"):

    @dataclass(slots=True)
    class BrowseMediaSource:
        """Represent the newer browse fields used by the adapter."""

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
        """Represent search results used by the adapter."""

        result: list[Any]

    @dataclass(slots=True)
    class SearchMediaQuery:
        """Represent a Media Source search query."""

        search_query: str

    media_player.SearchMedia = SearchMedia
    media_player.SearchMediaQuery = SearchMediaQuery
    media_source_component.BrowseMediaSource = BrowseMediaSource

from custom_components import curated_media, mediacat
from custom_components.curated_media.catalogue import _load_catalogue
from custom_components.curated_media.const import DOMAIN as LEGACY_DOMAIN
from custom_components.curated_media.media_source import CuratedMediaSource
from custom_components.mediacat.const import (
    CATALOGUE_DIRECTORY,
    DOMAIN as MEDIACAT_DOMAIN,
)
from custom_components.mediacat.catalogue import (
    _load_catalogue as _load_mediacat_catalogue,
)
from custom_components.mediacat.media_source import MediaCatSource


ROOT = Path(__file__).parents[1]
LEGACY_CATALOGUE = (
    ROOT / "04_Source" / "config" / "curated_media" / "catalogue.yaml"
)
MEDIACAT_CATALOGUE = (
    ROOT / "04_Source" / "config" / "mediacat" / "catalogue.yaml"
)
MEDIACAT_MANIFEST = (
    ROOT
    / "04_Source"
    / "config"
    / "custom_components"
    / "mediacat"
    / "manifest.json"
)


class FakeServices:
    """Capture registrations by domain and action name."""

    def __init__(self) -> None:
        self.registrations = {}

    def async_register(self, domain, service, handler, **kwargs) -> None:
        """Store one action registration without Home Assistant startup."""
        self.registrations[(domain, service)] = {"handler": handler, **kwargs}


class FakeHass:
    """Supply the Home Assistant surfaces used by both integrations."""

    def __init__(self) -> None:
        self.config = SimpleNamespace(path=lambda *parts: str(Path(*parts)))
        self.data = {}
        self.services = FakeServices()


def _call(handler, **data):
    """Invoke a captured asynchronous action handler."""
    return asyncio.run(handler(SimpleNamespace(data=data)))


def test_target_identity_and_catalogue_path_are_distinct_from_legacy() -> None:
    """Expose MediaCat under its new domain while retaining the legacy domain."""
    manifest = json.loads(MEDIACAT_MANIFEST.read_text(encoding="utf-8"))

    assert LEGACY_DOMAIN == "curated_media"
    assert MEDIACAT_DOMAIN == CATALOGUE_DIRECTORY == "mediacat"
    assert manifest["domain"] == "mediacat"
    assert manifest["name"] == "MediaCat"
    assert LEGACY_CATALOGUE.is_file()
    assert MEDIACAT_CATALOGUE.is_file()
    assert MEDIACAT_CATALOGUE.read_bytes() == LEGACY_CATALOGUE.read_bytes()
    assert load_yaml(MEDIACAT_CATALOGUE)["catalogue_id"] == "curated_media"


def test_both_domains_register_equivalent_actions_without_state_collision() -> None:
    """Prove independent namespaces and output parity during parallel running."""
    legacy_catalogue = _load_catalogue(LEGACY_CATALOGUE)
    mediacat_catalogue = _load_mediacat_catalogue(MEDIACAT_CATALOGUE)
    hass = FakeHass()

    legacy_loader = AsyncMock(return_value=legacy_catalogue)
    mediacat_loader = AsyncMock(return_value=mediacat_catalogue)
    with (
        patch(
            "custom_components.curated_media.async_load_catalogue",
            new=legacy_loader,
        ),
        patch(
            "custom_components.mediacat.async_load_catalogue",
            new=mediacat_loader,
        ),
    ):
        assert asyncio.run(curated_media.async_setup(hass, {})) is True
        assert asyncio.run(mediacat.async_setup(hass, {})) is True

    legacy_loader.assert_awaited_once_with(
        hass, str(Path("curated_media", "catalogue.yaml"))
    )
    mediacat_loader.assert_awaited_once_with(
        hass, str(Path("mediacat", "catalogue.yaml"))
    )
    assert set(hass.data) >= {"curated_media", "mediacat"}
    assert hass.data["curated_media"] is not hass.data["mediacat"]
    assert set(hass.services.registrations) == {
        ("curated_media", "resolve_item"),
        ("curated_media", "resolve_media_record"),
        ("mediacat", "resolve_item"),
        ("mediacat", "resolve_media_record"),
    }

    request = {"catalogue_id": "curated_media", "item_id": "classic_fm"}
    legacy_result = _call(
        hass.services.registrations[
            ("curated_media", "resolve_media_record")
        ]["handler"],
        **request,
    )
    mediacat_result = _call(
        hass.services.registrations[("mediacat", "resolve_media_record")][
            "handler"
        ],
        **request,
    )
    assert mediacat_result == legacy_result


def test_media_sources_have_independent_domains_and_self_reference_guards() -> None:
    """Keep each Media Source registered and recursive only to its own domain."""
    hass = FakeHass()
    legacy_source = CuratedMediaSource(hass)
    mediacat_source = MediaCatSource(hass)

    assert legacy_source.name == "Curated Media"
    assert mediacat_source.name == "MediaCat"
    assert legacy_source._is_curated_media_uri(
        "media-source://curated_media/item/test"
    )
    assert not legacy_source._is_curated_media_uri(
        "media-source://mediacat/item/test"
    )
    assert mediacat_source._is_mediacat_uri(
        "media-source://mediacat/item/test"
    )
    assert not mediacat_source._is_mediacat_uri(
        "media-source://curated_media/item/test"
    )
