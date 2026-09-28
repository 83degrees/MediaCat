"""Focused non-live coverage for normalized MediaCat record lookup."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
import voluptuous as vol

from homeassistant.exceptions import ServiceValidationError

from custom_components.mediacat import (
    RESOLVE_MEDIA_RECORD_SCHEMA,
    async_setup,
)
from custom_components.mediacat.catalogue import (
    CatalogueError,
    CatalogueV4,
    _load_catalogue,
    _parse_catalogue,
)
from custom_components.mediacat.resolver import CatalogueResolver

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
        "custom_components.mediacat.async_load_catalogue",
        new=AsyncMock(return_value=catalogue),
    ):
        assert asyncio.run(async_setup(hass, {})) is True
    return hass


def _call(handler, **data):
    """Invoke a captured asynchronous action handler."""
    return asyncio.run(handler(SimpleNamespace(data=data)))


def test_schema_v2_is_rejected_as_an_active_catalogue() -> None:
    """Reject the historical schema rather than loading a compatibility model."""
    with pytest.raises(
        CatalogueError,
        match="expected catalogue_schema_version: 4",
    ):
        _parse_catalogue(
            {"version": 2, "items": {}, "categories": {}},
            Path("historical-v2.yaml"),
        )


def test_rejected_schema_prevents_setup_and_action_registration() -> None:
    """Keep catalogue-load failure atomic when the active schema is unsupported."""
    hass = FakeHass()
    with patch(
        "custom_components.mediacat.async_load_catalogue",
        new=AsyncMock(side_effect=CatalogueError("unsupported catalogue schema")),
    ):
        assert asyncio.run(async_setup(hass, {})) is False

    assert hass.data == {}
    assert hass.services.registrations == {}


def test_schema_v4_registers_only_normalized_action() -> None:
    """Expose only the normalized catalogue-scoped lookup action."""
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v4.yaml")
    assert isinstance(catalogue, CatalogueV4)
    hass = _setup_with_catalogue(catalogue)

    assert set(hass.services.registrations) == {"resolve_media_record"}


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
def test_normalized_action_accepts_exactly_two_identifier_inputs(
    request_data,
) -> None:
    """Reject missing, malformed, additional, and compatibility-alias inputs."""
    with pytest.raises(vol.Invalid):
        RESOLVE_MEDIA_RECORD_SCHEMA(request_data)

    assert RESOLVE_MEDIA_RECORD_SCHEMA(
        {"catalogue_id": "curated_media", "item_id": "station_alpha"}
    ) == {"catalogue_id": "curated_media", "item_id": "station_alpha"}


@pytest.mark.parametrize(
    "identifier",
    [
        "a",
        "0",
        "curated_media",
        "station-alpha_2",
        "a" * 1024,
    ],
)
def test_normalized_action_accepts_every_documented_identifier_shape(
    identifier,
) -> None:
    """Accept the complete policy vocabulary without adding a length limit."""
    assert RESOLVE_MEDIA_RECORD_SCHEMA(
        {"catalogue_id": identifier, "item_id": identifier}
    ) == {"catalogue_id": identifier, "item_id": identifier}


@pytest.mark.parametrize(
    "identifier",
    ["", " ", "Uppercase", "-prefix", "_prefix", "has/slash", "has.dot"],
)
def test_normalized_action_rejects_malformed_identifiers(identifier) -> None:
    """Reject only identifiers outside the authoritative lexical rule."""
    with pytest.raises(vol.Invalid, match="value must match"):
        RESOLVE_MEDIA_RECORD_SCHEMA(
            {"catalogue_id": identifier, "item_id": "station_alpha"}
        )


@pytest.mark.parametrize("field", ["catalogue_id", "item_id"])
@pytest.mark.parametrize("identifier", [1, True, 1.5, None])
def test_normalized_action_rejects_non_string_identifiers(
    field, identifier
) -> None:
    """Reject scalar values rather than coercing them to strings."""
    request = {"catalogue_id": "curated_media", "item_id": "station_alpha"}
    request[field] = identifier

    with pytest.raises(vol.Invalid, match="value must be a string"):
        RESOLVE_MEDIA_RECORD_SCHEMA(request)


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
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v4.yaml")
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


def test_response_copy_is_independent_from_validated_catalogue() -> None:
    """Protect catalogue immutability from caller mutation of a response."""
    catalogue = _parse_catalogue(
        {
            "catalogue_id": "curated_media",
            "catalogue_schema_version": 4,
            "items": {
                "station_alpha": {
                    "catalogue_label": "Station Alpha",
                    "type": "radio",
                    "tags": ["radio", "live"],
                    "type_metadata": {"station_name": "Station Alpha"},
                    "execution_methods": {
                        "ha_mplayer": {
                            "source": {
                                "source_type": "url",
                                "url": "https://example.test/live",
                                "mime_type": "audio/aac",
                            }
                        }
                    },
                }
            },
            "categories": {
                "all": {
                    "category_label": "All",
                    "items": ["station_alpha"],
                }
            },
        },
        Path("non-live-v3.yaml"),
    )
    assert isinstance(catalogue, CatalogueV4)
    resolver = CatalogueResolver(catalogue)

    response = resolver.resolve_media_record("curated_media", "station_alpha")

    assert response["returned_record_version"] == 1
    assert response["catalogue_id"] == "curated_media"
    assert response["item_id"] == "station_alpha"
    response["tags"].append("caller-change")
    response["execution_methods"]["ha_mplayer"]["source"]["url"] = "changed"
    assert catalogue.items["station_alpha"]["tags"] == ("radio", "live")
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
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v4.yaml")
    hass = _setup_with_catalogue(catalogue)
    handler = hass.services.registrations["resolve_media_record"]["handler"]

    with pytest.raises(ServiceValidationError, match=message):
        _call(handler, **request_data)


@pytest.mark.parametrize(
    ("request_data", "message"),
    [
        (
            {"catalogue_id": "Invalid", "item_id": "station_alpha"},
            "MediaCat catalogue_id 'Invalid' is invalid",
        ),
        (
            {"catalogue_id": "curated_media", "item_id": "bad/item"},
            "MediaCat item_id 'bad/item' is invalid",
        ),
    ],
)
def test_normalized_action_distinguishes_malformed_identifiers(
    request_data, message
) -> None:
    """Report malformed input separately from a valid identifier not found."""
    catalogue = _load_catalogue(FIXTURE_DIRECTORY / "catalogue_v4.yaml")
    hass = _setup_with_catalogue(catalogue)
    handler = hass.services.registrations["resolve_media_record"]["handler"]

    with pytest.raises(ServiceValidationError, match=re.escape(message)):
        _call(handler, **request_data)
