"""The MediaCat integration."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.typing import ConfigType

from .catalogue import (
    CURRENT_CATALOGUE_SCHEMA_VERSION,
    SUPPORTED_CATALOGUE_SCHEMA_VERSIONS,
    CatalogueError,
    CatalogueRegistry,
    CatalogueV4,
    _load_catalogue_text,
    async_load_catalogue_directory,
)
from .const import (
    ATTR_ITEM_ID,
    CATALOGUE_DIRECTORY,
    CATALOGUE_FILE_EXTENSIONS,
    CATALOGUES_DIRECTORY,
    DATA_CATALOGUES,
    DATA_RELOAD_LOCK,
    DOMAIN,
)
from .resolver import (
    IDENTIFIER_PATTERN,
    CatalogueItemNotFoundError,
    CatalogueNotFoundError,
    CatalogueResolver,
    InvalidIdentifierError,
)

_LOGGER = logging.getLogger(__name__)

ATTR_CATALOGUE_ID = "catalogue_id"
SERVICE_RESOLVE_MEDIA_RECORD = "resolve_media_record"
SERVICE_GET_ADMIN_CAPABILITIES = "get_admin_capabilities"
SERVICE_VALIDATE_CATALOGUE = "validate_catalogue"
SERVICE_RELOAD_CATALOGUE = "reload_catalogue"
ATTR_CATALOGUE_YAML = "catalogue_yaml"


def _identifier(value: Any) -> str:
    """Validate a lookup identifier against schema-v4 policy."""
    if not isinstance(value, str):
        raise vol.Invalid("value must be a string")
    if IDENTIFIER_PATTERN.fullmatch(value) is None:
        raise vol.Invalid(
            f"value must match {IDENTIFIER_PATTERN.pattern!r}"
        )
    return value


RESOLVE_MEDIA_RECORD_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CATALOGUE_ID): _identifier,
        vol.Required(ATTR_ITEM_ID): _identifier,
    }
)
VALIDATE_CATALOGUE_SCHEMA = vol.Schema(
    {vol.Required(ATTR_CATALOGUE_YAML): str}
)
EMPTY_SCHEMA = vol.Schema({})


def _registry(hass: HomeAssistant) -> CatalogueRegistry:
    """Return the active immutable catalogue registry."""
    domain_data = hass.data.get(DOMAIN)
    if not isinstance(domain_data, dict):
        raise CatalogueError("MediaCat runtime state is unavailable")
    registry = domain_data.get(DATA_CATALOGUES)
    if not isinstance(registry, CatalogueRegistry):
        raise CatalogueError("MediaCat catalogue registry is unavailable")
    return registry


def _catalogue_summary(catalogue: CatalogueV4) -> dict[str, Any]:
    """Return the stable administrative summary for one validated catalogue."""
    return {
        "catalogue_id": catalogue.catalogue_id,
        "catalogue_schema_version": catalogue.catalogue_schema_version,
        "item_count": len(catalogue.items),
        "category_count": len(catalogue.categories),
    }


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Load the MediaCat catalogue registry and register its actions."""
    catalogue_path = hass.config.path(
        CATALOGUE_DIRECTORY, CATALOGUES_DIRECTORY
    )

    try:
        registry = await async_load_catalogue_directory(hass, catalogue_path)
    except CatalogueError as err:
        _LOGGER.error("Unable to load MediaCat catalogues: %s", err)
        return False

    domain_data: dict[str, Any] = hass.data.setdefault(DOMAIN, {})
    domain_data[DATA_CATALOGUES] = registry
    domain_data[DATA_RELOAD_LOCK] = asyncio.Lock()

    async def async_resolve_media_record(call: ServiceCall) -> dict[str, Any]:
        """Return the normalized v1 record for a catalogue-scoped item."""
        catalogue_id: str = call.data[ATTR_CATALOGUE_ID]
        item_id: str = call.data[ATTR_ITEM_ID]
        try:
            return CatalogueResolver(_registry(hass)).resolve_media_record(
                catalogue_id, item_id
            )
        except (
            CatalogueNotFoundError,
            CatalogueItemNotFoundError,
            InvalidIdentifierError,
        ) as err:
            raise ServiceValidationError(str(err)) from err

    async def async_get_admin_capabilities(
        call: ServiceCall,
    ) -> dict[str, Any]:
        """Return supported schema and transactional administration features."""
        active = _registry(hass)
        return {
            "admin_interface_version": 1,
            "current_catalogue_schema_version": (
                CURRENT_CATALOGUE_SCHEMA_VERSION
            ),
            "supported_catalogue_schema_versions": list(
                SUPPORTED_CATALOGUE_SCHEMA_VERSIONS
            ),
            "catalogue_directory": f"{CATALOGUE_DIRECTORY}/{CATALOGUES_DIRECTORY}",
            "catalogue_file_extensions": list(CATALOGUE_FILE_EXTENSIONS),
            "active_catalogue_ids": list(active.catalogue_ids),
            "validation_supported": True,
            "transactional_reload_supported": True,
        }

    async def async_validate_catalogue(call: ServiceCall) -> dict[str, Any]:
        """Validate supplied YAML without changing disk or active runtime state."""
        try:
            catalogue = await hass.async_add_executor_job(
                _load_catalogue_text,
                call.data[ATTR_CATALOGUE_YAML],
                Path("<admin-request>"),
            )
        except CatalogueError as err:
            return {
                "valid": False,
                "errors": [
                    {"code": "invalid_catalogue", "message": str(err)}
                ],
            }
        return {
            "valid": True,
            **_catalogue_summary(catalogue),
            "errors": [],
        }

    async def async_reload_catalogue(call: ServiceCall) -> dict[str, Any]:
        """Replace the active registry only after full discovery and validation."""
        lock = domain_data[DATA_RELOAD_LOCK]
        async with lock:
            previous = _registry(hass)
            try:
                candidate = await async_load_catalogue_directory(
                    hass, catalogue_path
                )
            except CatalogueError as err:
                return {
                    "reloaded": False,
                    "active_catalogue_ids": list(previous.catalogue_ids),
                    "errors": [
                        {"code": "reload_failed", "message": str(err)}
                    ],
                }
            domain_data[DATA_CATALOGUES] = candidate
            return {
                "reloaded": True,
                "active_catalogue_ids": list(candidate.catalogue_ids),
                "catalogue_count": len(candidate.catalogues),
                "errors": [],
            }

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESOLVE_MEDIA_RECORD,
        async_resolve_media_record,
        schema=RESOLVE_MEDIA_RECORD_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_ADMIN_CAPABILITIES,
        async_get_admin_capabilities,
        schema=EMPTY_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_VALIDATE_CATALOGUE,
        async_validate_catalogue,
        schema=VALIDATE_CATALOGUE_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_RELOAD_CATALOGUE,
        async_reload_catalogue,
        schema=EMPTY_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )

    _LOGGER.info(
        "Loaded %d MediaCat catalogues with %d items and %d categories",
        len(registry.catalogues),
        sum(len(catalogue.items) for catalogue in registry.catalogues.values()),
        sum(
            len(catalogue.categories)
            for catalogue in registry.catalogues.values()
        ),
    )
    return True
