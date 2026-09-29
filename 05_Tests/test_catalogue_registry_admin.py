"""Acceptance coverage for multi-catalogue discovery and admin actions."""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest

from custom_components import mediacat
from custom_components.mediacat.catalogue import (
    CatalogueError,
    CatalogueRegistry,
    _load_catalogue_directory,
)
from custom_components.mediacat.const import DATA_CATALOGUES, DOMAIN


FIXTURE = Path(__file__).parent / "fixtures" / "catalogue_v4.yaml"


class FakeServices:
    """Capture service registrations for direct handler invocation."""

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
    """Supply the Home Assistant surfaces used by MediaCat setup and reload."""

    def __init__(self, config_root: Path) -> None:
        self.config = SimpleNamespace(
            path=lambda *parts: str(config_root.joinpath(*parts))
        )
        self.data = {}
        self.services = FakeServices()

    async def async_add_executor_job(self, target, *args):
        """Run deterministic test I/O without a Home Assistant executor."""
        return target(*args)


def _catalogue_text(catalogue_id: str) -> str:
    """Return the maintained fixture with a distinct in-file identity."""
    return FIXTURE.read_text(encoding="utf-8").replace(
        "catalogue_id: curated_media",
        f"catalogue_id: {catalogue_id}",
        1,
    )


def _write_catalogue(directory: Path, filename: str, catalogue_id: str) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    directory.joinpath(filename).write_text(
        _catalogue_text(catalogue_id), encoding="utf-8"
    )


def _call(handler, **data):
    """Invoke an asynchronous registered action handler."""
    return asyncio.run(handler(SimpleNamespace(data=data)))


def test_directory_discovery_uses_in_file_identity_not_filename(
    tmp_path: Path,
) -> None:
    """Discover all YAML files and key them by authoritative catalogue_id."""
    directory = tmp_path / "catalogues"
    _write_catalogue(directory, "friendly-name.yaml", "curated_media")
    _write_catalogue(directory, "unrelated-storage-name.yml", "second_catalogue")
    directory.joinpath("ignored.txt").write_text("not yaml", encoding="utf-8")

    registry = _load_catalogue_directory(directory)

    assert registry.catalogue_ids == ("curated_media", "second_catalogue")
    assert registry.get("curated_media").catalogue_id == "curated_media"
    assert registry.get("second_catalogue").catalogue_id == "second_catalogue"


def test_directory_discovery_rejects_duplicate_catalogue_ids(
    tmp_path: Path,
) -> None:
    """Reject a complete candidate registry when two files claim one identity."""
    directory = tmp_path / "catalogues"
    _write_catalogue(directory, "one.yaml", "duplicate")
    _write_catalogue(directory, "two.yaml", "duplicate")

    with pytest.raises(
        CatalogueError, match="duplicate catalogue_id 'duplicate'"
    ):
        _load_catalogue_directory(directory)


def test_admin_actions_report_capabilities_and_validate_without_mutation(
    tmp_path: Path,
) -> None:
    """Expose schema capabilities and side-effect-free candidate validation."""
    directory = tmp_path / "mediacat" / "catalogues"
    _write_catalogue(directory, "current.yaml", "curated_media")
    hass = FakeHass(tmp_path)

    assert asyncio.run(mediacat.async_setup(hass, {})) is True
    active = hass.data[DOMAIN][DATA_CATALOGUES]

    capabilities = _call(
        hass.services.registrations["get_admin_capabilities"]["handler"]
    )
    assert capabilities == {
        "admin_interface_version": 1,
        "current_catalogue_schema_version": 4,
        "supported_catalogue_schema_versions": [4],
        "catalogue_directory": "mediacat/catalogues",
        "catalogue_file_extensions": [".yaml", ".yml"],
        "active_catalogue_ids": ["curated_media"],
        "validation_supported": True,
        "transactional_reload_supported": True,
    }

    validation = _call(
        hass.services.registrations["validate_catalogue"]["handler"],
        catalogue_yaml=_catalogue_text("candidate_identity"),
    )
    assert validation["valid"] is True
    assert validation["catalogue_id"] == "candidate_identity"
    assert validation["catalogue_schema_version"] == 4
    assert validation["errors"] == []

    invalid = _call(
        hass.services.registrations["validate_catalogue"]["handler"],
        catalogue_yaml="catalogue_id: invalid\n",
    )
    assert invalid["valid"] is False
    assert invalid["errors"][0]["code"] == "invalid_catalogue"
    assert hass.data[DOMAIN][DATA_CATALOGUES] is active


def test_reload_is_transactional_across_the_complete_registry(
    tmp_path: Path,
) -> None:
    """Keep the old registry on failure and swap once after full success."""
    directory = tmp_path / "mediacat" / "catalogues"
    _write_catalogue(directory, "current.yaml", "curated_media")
    hass = FakeHass(tmp_path)
    assert asyncio.run(mediacat.async_setup(hass, {})) is True
    previous = hass.data[DOMAIN][DATA_CATALOGUES]
    assert isinstance(previous, CatalogueRegistry)

    _write_catalogue(directory, "duplicate.yaml", "curated_media")
    reload_handler = hass.services.registrations["reload_catalogue"]["handler"]
    failed = _call(reload_handler)
    assert failed["reloaded"] is False
    assert failed["active_catalogue_ids"] == ["curated_media"]
    assert failed["errors"][0]["code"] == "reload_failed"
    assert hass.data[DOMAIN][DATA_CATALOGUES] is previous

    directory.joinpath("duplicate.yaml").write_text(
        _catalogue_text("second_catalogue"), encoding="utf-8"
    )
    succeeded = _call(reload_handler)
    assert succeeded == {
        "reloaded": True,
        "active_catalogue_ids": ["curated_media", "second_catalogue"],
        "catalogue_count": 2,
        "errors": [],
    }
    current = hass.data[DOMAIN][DATA_CATALOGUES]
    assert current is not previous
    assert current.catalogue_ids == ("curated_media", "second_catalogue")

    lookup = _call(
        hass.services.registrations["resolve_media_record"]["handler"],
        catalogue_id="second_catalogue",
        item_id="station_alpha",
    )
    assert lookup["catalogue_id"] == "second_catalogue"
