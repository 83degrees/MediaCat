"""Non-live proof for the post-retirement MediaCat domain state."""

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

from custom_components import mediacat
from custom_components.mediacat.catalogue import _load_catalogue
from custom_components.mediacat.const import CATALOGUE_DIRECTORY, DOMAIN
from custom_components.mediacat.media_source import MediaCatSource


ROOT = Path(__file__).parents[1]
SOURCE_CONFIG = ROOT / "04_Source" / "config"
CATALOGUE = SOURCE_CONFIG / "mediacat" / "catalogue.yaml"
MANIFEST = SOURCE_CONFIG / "custom_components" / "mediacat" / "manifest.json"
LEGACY_COMPONENT = SOURCE_CONFIG / "custom_components" / "curated_media"
LEGACY_CATALOGUE = SOURCE_CONFIG / "curated_media" / "catalogue.yaml"


class FakeServices:
    """Capture registrations by domain and action name."""

    def __init__(self) -> None:
        self.registrations = {}

    def async_register(self, domain, service, handler, **kwargs) -> None:
        """Store one action registration without Home Assistant startup."""
        self.registrations[(domain, service)] = {"handler": handler, **kwargs}


class FakeHass:
    """Supply the Home Assistant surfaces used by the integration."""

    def __init__(self) -> None:
        self.config = SimpleNamespace(path=lambda *parts: str(Path(*parts)))
        self.data = {}
        self.services = FakeServices()


def _call(handler, **data):
    """Invoke a captured asynchronous action handler."""
    return asyncio.run(handler(SimpleNamespace(data=data)))


def test_source_contains_only_the_mediacat_runtime_namespace() -> None:
    """Retire legacy runtime paths while preserving catalogue identity."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert DOMAIN == CATALOGUE_DIRECTORY == "mediacat"
    assert manifest["domain"] == "mediacat"
    assert manifest["name"] == "MediaCat"
    assert CATALOGUE.is_file()
    assert not LEGACY_COMPONENT.exists()
    assert not LEGACY_CATALOGUE.exists()
    assert load_yaml(CATALOGUE)["catalogue_id"] == "curated_media"


def test_only_mediacat_registers_actions_and_domain_state() -> None:
    """Register both supported actions in the sole active runtime domain."""
    catalogue = _load_catalogue(CATALOGUE)
    hass = FakeHass()
    loader = AsyncMock(return_value=catalogue)

    with patch("custom_components.mediacat.async_load_catalogue", new=loader):
        assert asyncio.run(mediacat.async_setup(hass, {})) is True

    loader.assert_awaited_once_with(hass, str(Path("mediacat", "catalogue.yaml")))
    assert set(hass.data) == {"mediacat"}
    assert set(hass.services.registrations) == {
        ("mediacat", "resolve_item"),
        ("mediacat", "resolve_media_record"),
    }

    response = _call(
        hass.services.registrations[("mediacat", "resolve_media_record")][
            "handler"
        ],
        catalogue_id="curated_media",
        item_id="classic_fm",
    )
    assert response["returned_record_version"] == 1
    assert response["catalogue_id"] == "curated_media"
    assert response["item_id"] == "classic_fm"


def test_media_source_uses_only_the_mediacat_domain() -> None:
    """Keep Media Source identity and recursion protection on mediacat."""
    source = MediaCatSource(FakeHass())

    assert source.name == "MediaCat"
    assert source._is_mediacat_uri("media-source://mediacat/item/test")
    assert not source._is_mediacat_uri(
        "media-source://curated_media/item/test"
    )
