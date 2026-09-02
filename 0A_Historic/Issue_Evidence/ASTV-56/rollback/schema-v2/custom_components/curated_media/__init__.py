"""The Curated Media integration."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .catalogue import CatalogueError, async_load_catalogue
from .const import (
    ATTR_ITEM_ID,
    CATALOGUE_DIRECTORY,
    CATALOGUE_FILENAME,
    DATA_CATALOGUE,
    DOMAIN,
    SERVICE_RESOLVE_ITEM,
)
from .resolver import CatalogueItemNotFoundError, CatalogueResolver

_LOGGER = logging.getLogger(__name__)


def _non_empty_string(value: Any) -> str:
    """Validate a string containing at least one non-whitespace character."""
    value = cv.string(value)
    if not value.strip():
        raise vol.Invalid("value must be a non-empty string")
    return value


RESOLVE_ITEM_SCHEMA = vol.Schema(
    {vol.Required(ATTR_ITEM_ID): _non_empty_string}
)


def _response_safe(value: Any) -> Any:
    """Convert an immutable catalogue record to response-safe containers."""
    if isinstance(value, Mapping):
        return {key: _response_safe(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_response_safe(item) for item in value]
    return value


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Load the Curated Media catalogue and register its actions."""
    catalogue_path = hass.config.path(CATALOGUE_DIRECTORY, CATALOGUE_FILENAME)

    try:
        catalogue = await async_load_catalogue(hass, catalogue_path)
    except CatalogueError as err:
        _LOGGER.error("Unable to load Curated Media catalogue: %s", err)
        return False

    domain_data: dict[str, Any] = hass.data.setdefault(DOMAIN, {})
    domain_data[DATA_CATALOGUE] = catalogue

    resolver = CatalogueResolver(catalogue)

    async def async_resolve_item(call: ServiceCall) -> dict[str, Any]:
        """Return the complete canonical item record directly."""
        item_id: str = call.data[ATTR_ITEM_ID]
        try:
            resolved_item = resolver.resolve_item(item_id)
        except CatalogueItemNotFoundError as err:
            raise ServiceValidationError(str(err)) from err
        return _response_safe(resolved_item.record)

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESOLVE_ITEM,
        async_resolve_item,
        schema=RESOLVE_ITEM_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )

    _LOGGER.info(
        "Loaded Curated Media catalogue with %d items and %d categories",
        len(catalogue.items),
        len(catalogue.categories),
    )
    return True
