"""Focused non-live coverage for normalized MediaCat record lookup."""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
import voluptuous as vol

from homeassistant.exceptions import ServiceValidationError

from custom_components.curated_media import (
    RESOLVE_MEDIA_RECORD_SCHEMA,
    async_setup,
)
from custom_components.curated_media.catalogue import (
    CatalogueV3,
    _load_catalogue,
    _parse_catalogue,
)
from custom_components.curated_media.resolver import CatalogueResolver

FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures"


class FakeServices:
    """Capture action registrations without starting Home Assistant."""

    def __init__(self) -> None:
        self.registrations = {}

    def async_register(self, domain, service, handler, **kwargs) -> None:
        """Store one action registration."""
        self.registrations[service] = {
            "domain": domain,
            "handler": handler,
            **kwargs,
        }


class FakeHass:
    """Supply only the Home Assistant surfaces used during setup."""

    def __init__(self) -> None:
        self.config = SimpleNamespace(path=lambda *parts: str(Path(*parts)))
        self.data = {}
        self.services = FakeServices()


def _setup_with_catalogue(catalogue):
    """Run integration setup against an already loaded non-live catalogue."""
    hass = FakeHass()
    with patch(
        "custom_components.curated_media.async_load_catalogue",
        new=AsyncMock(return_value=catalogue),
    ):
        assert asyncio.run(async_setup(hass, {})) is True
    return hass


def _call(handler, **data):
    """Invoke a captured asynchronous action handler."""
    return asyncio.run(handler(SimpleNamespace(data=data)))


def test_schema_v2_registers_only_legacy_raw_item_action() -> None:
    """Keep the current schema-v2 action and response behaviour unchanged."""
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v2.yaml")
    hass = _setup_with_catalogue(catalogue)

    assert set(hass.services.registrations) == {"resolve_item"}
    response = _call(
        hass.services.registrations["resolve_item"]["handler"],
        item_id="station_alpha",
    )
    assert set(response) == set(catalogue.items["station_alpha"].record)
    assert response["title"] == "Station Alpha"
    assert response["tags"] == ["news", "local"]
    assert response["providers"]["radio_music"]["service"]["data"][
        "features"
    ] == ["live", "regional"]
    assert "returned_record_version" not in response
    assert "catalogue_id" not in response
    assert "item_id" not in response


def test_schema_v3_registers_legacy_and_normalized_actions() -> None:
    """Expose both actions while keeping the legacy v3 response raw."""
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v3.yaml")
    assert isinstance(catalogue, CatalogueV3)
    hass = _setup_with_catalogue(catalogue)

    assert set(hass.services.registrations) == {
        "resolve_item",
        "resolve_media_record",
    }
    response = _call(
        hass.services.registrations["resolve_item"]["handler"],
        item_id="station_alpha",
    )
    assert set(response) == set(catalogue.items["station_alpha"])
    assert response["catalogue_label"] == "Station Alpha"
    assert response["tags"] == ["radio", "live"]
    assert response["providers"]["legacy_radio"]["service"]["features"] == [
        "live",
        "regional",
    ]
    assert "returned_record_version" not in response
    assert "catalogue_id" not in response
    assert "item_id" not in response


@pytest.mark.parametrize(
    "request_data",
    [
        {},
        {"catalogue_id": "curated_media"},
        {"item_id": "station_alpha"},
        {"catalogue_id": " ", "item_id": "station_alpha"},
        {"catalogue_id": "curated_media", "item_id": "\t"},
        {
            "catalogue_id": "curated_media",
            "item_id": "station_alpha",
            "media_catalogue": "curated_media",
        },
        {
            "catalogue_id": "curated_media",
            "item_id": "station_alpha",
            "media_item_id": "station_alpha",
        },
    ],
)
def test_normalized_action_accepts_exactly_two_non_blank_inputs(
    request_data,
) -> None:
    """Reject missing, blank, additional, and compatibility-alias inputs."""
    with pytest.raises(vol.Invalid):
        RESOLVE_MEDIA_RECORD_SCHEMA(request_data)

    assert RESOLVE_MEDIA_RECORD_SCHEMA(
        {"catalogue_id": "curated_media", "item_id": "station_alpha"}
    ) == {"catalogue_id": "curated_media", "item_id": "station_alpha"}


@pytest.mark.parametrize(
    ("item_id", "method", "expected_source"),
    [
        (
            "station_alpha",
            "ha_mplayer",
            {
                "source_type": "url",
                "url": "https://streams.example.test/station_alpha.m3u8",
                "mime_type": "application/vnd.apple.mpegurl",
                "provider": "example_streams",
                "transport_hint": "live",
            },
        ),
        (
            "example_track",
            "ha_mplayer",
            {
                "source_type": "ha_media_source",
                "provider": "radio_browser",
                "uri": "media-source://radio_browser/example-track",
                "media_type": "music",
            },
        ),
        (
            "station_alpha",
            "g_home_device",
            {
                "source_type": "assistant_command",
                "provider": "google_assistant",
                "command": "Play Station Alpha",
                "append_target": True,
            },
        ),
    ],
)
def test_normalized_action_preserves_complete_items_and_sources(
    item_id, method, expected_source
) -> None:
    """Copy complete items without selecting or translating a method."""
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v3.yaml")
    hass = _setup_with_catalogue(catalogue)
    handler = hass.services.registrations["resolve_media_record"]["handler"]

    response = _call(
        handler, catalogue_id="curated_media", item_id=item_id
    )

    assert response["returned_record_version"] == 1
    assert response["catalogue_id"] == "curated_media"
    assert response["item_id"] == item_id
    assert set(response) == set(catalogue.items[item_id]) | {
        "returned_record_version",
        "catalogue_id",
        "item_id",
    }
    assert response["execution_methods"][method]["source"] == expected_source
    assert set(response["execution_methods"]) == set(
        catalogue.items[item_id]["execution_methods"]
    )
    assert "catalogue_schema_version" not in response
    assert "categories" not in response
    assert "items" not in response
    assert "fixture_note" not in response


def test_response_owned_fields_override_item_fields_and_copy_is_independent() -> None:
    """Protect response identity and catalogue immutability from caller mutation."""
    catalogue = _parse_catalogue(
        {
            "catalogue_id": "curated_media",
            "catalogue_schema_version": 3,
            "items": {
                "station_alpha": {
                    "returned_record_version": 99,
                    "catalogue_id": "falsified",
                    "item_id": "falsified",
                    "execution_methods": {
                        "ha_mplayer": {
                            "source": {
                                "source_type": "url",
                                "url": "https://example.test/live",
                            }
                        }
                    },
                    "additive": {"values": ["retained"]},
                }
            },
            "categories": {"all": {"items": ["station_alpha"]}},
        },
        Path("non-live-v3.yaml"),
    )
    assert isinstance(catalogue, CatalogueV3)
    resolver = CatalogueResolver(catalogue)

    response = resolver.resolve_media_record("curated_media", "station_alpha")

    assert response["returned_record_version"] == 1
    assert response["catalogue_id"] == "curated_media"
    assert response["item_id"] == "station_alpha"
    assert response["additive"] == {"values": ["retained"]}
    response["additive"]["values"].append("caller change")
    response["execution_methods"]["ha_mplayer"]["source"]["url"] = "changed"
    assert catalogue.items["station_alpha"]["additive"]["values"] == (
        "retained",
    )
    assert catalogue.items["station_alpha"]["execution_methods"][
        "ha_mplayer"
    ]["source"]["url"] == "https://example.test/live"


@pytest.mark.parametrize(
    ("request_data", "message"),
    [
        (
            {"catalogue_id": "unknown", "item_id": "station_alpha"},
            "catalogue 'unknown' was not found",
        ),
        (
            {"catalogue_id": "curated_media", "item_id": "unknown"},
            "item 'unknown' was not found in catalogue 'curated_media'",
        ),
    ],
)
def test_normalized_action_reports_lookup_failures_without_a_record(
    request_data, message
) -> None:
    """Translate exact lookup failures to Home Assistant validation errors."""
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v3.yaml")
    hass = _setup_with_catalogue(catalogue)
    handler = hass.services.registrations["resolve_media_record"]["handler"]

    with pytest.raises(ServiceValidationError, match=message):
        _call(handler, **request_data)
