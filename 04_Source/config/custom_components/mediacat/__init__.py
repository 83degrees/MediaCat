"""The MediaCat integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .catalogue import CatalogueError, CatalogueV3, async_load_catalogue
from .const import (
    ATTR_ITEM_ID,
    CATALOGUE_DIRECTORY,
    CATALOGUE_FILENAME,
    DATA_CATALOGUE,
    DOMAIN,
    SERVICE_RESOLVE_ITEM,
)
from .resolver import (
    CatalogueItemNotFoundError,
    CatalogueNotFoundError,
    CatalogueResolver,
)

_LOGGER = logging.getLogger(__name__)

ATTR_CATALOGUE_ID = "catalogue_id"
SERVICE_RESOLVE_MEDIA_RECORD = "resolve_media_record"


def _non_empty_string(value: Any) -> str:
    """Validate a string containing at least one non-whitespace character."""
    value = cv.string(value)
    if not value.strip():
        raise vol.Invalid("value must be a non-empty string")
    return value


RESOLVE_ITEM_SCHEMA = vol.Schema(
    {vol.Required(ATTR_ITEM_ID): _non_empty_string}
)

RESOLVE_MEDIA_RECORD_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CATALOGUE_ID): _non_empty_string,
        vol.Required(ATTR_ITEM_ID): _non_empty_string,
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Load the MediaCat catalogue and register its actions."""
    catalogue_path = hass.config.path(CATALOGUE_DIRECTORY, CATALOGUE_FILENAME)

    try:
        catalogue = await async_load_catalogue(hass, catalogue_path)
    except CatalogueError as err:
        _LOGGER.error("Unable to load MediaCat catalogue: %s", err)
        return False

    domain_data: dict[str, Any] = hass.data.setdefault(DOMAIN, {})
    domain_data[DATA_CATALOGUE] = catalogue

    resolver = CatalogueResolver(catalogue)

    async def async_resolve_item(call: ServiceCall) -> dict[str, Any]:
        """Return the complete canonical item record directly."""
        item_id: str = call.data[ATTR_ITEM_ID]
        try:
            return resolver.resolve_item_record(item_id)
        except CatalogueItemNotFoundError as err:
            raise ServiceValidationError(str(err)) from err

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESOLVE_ITEM,
        async_resolve_item,
        schema=RESOLVE_ITEM_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )

    if isinstance(catalogue, CatalogueV3):

        async def async_resolve_media_record(call: ServiceCall) -> dict[str, Any]:
            """Return the normalized v1 record for a catalogue-scoped item."""
            catalogue_id: str = call.data[ATTR_CATALOGUE_ID]
            item_id: str = call.data[ATTR_ITEM_ID]
            try:
                return resolver.resolve_media_record(catalogue_id, item_id)
            except (CatalogueNotFoundError, CatalogueItemNotFoundError) as err:
                raise ServiceValidationError(str(err)) from err

        hass.services.async_register(
            DOMAIN,
            SERVICE_RESOLVE_MEDIA_RECORD,
            async_resolve_media_record,
            schema=RESOLVE_MEDIA_RECORD_SCHEMA,
            supports_response=SupportsResponse.ONLY,
        )

    _LOGGER.info(
        "Loaded MediaCat catalogue with %d items and %d categories",
        len(catalogue.items),
        len(catalogue.categories),
    )
    return True
