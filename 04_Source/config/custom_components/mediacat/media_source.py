"""Expose the MediaCat catalogue in Home Assistant's Media Browser."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from homeassistant.components.media_player import (
    BrowseError,
    MediaClass,
    MediaType,
    SearchMedia,
    SearchMediaQuery,
)
from homeassistant.components.media_source import (
    BrowseMediaSource,
    MediaSource,
    MediaSourceItem,
    PlayMedia,
    Unresolvable,
    async_resolve_media as async_resolve_media_source,
)
from homeassistant.core import HomeAssistant

from .catalogue import CatalogueRegistry, CatalogueV4
from .const import DATA_CATALOGUES, DOMAIN, SUPPORTED_ITEM_TYPE

ITEM_PREFIX = "item/"
CATALOGUE_PREFIX = "catalogue/"
REGISTRY_CATEGORY_PREFIX = "registry/category/"


async def async_get_media_source(hass: HomeAssistant) -> MediaCatSource:
    """Set up the MediaCat media source."""
    return MediaCatSource(hass)


class MediaCatSource(MediaSource):
    """Provide the MediaCat catalogue as a media source."""

    name = "MediaCat"

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the media source."""
        super().__init__(DOMAIN)
        self.hass = hass

    def _registry(self) -> CatalogueRegistry | None:
        """Return the active registry, if integration setup succeeded."""
        domain_data = self.hass.data.get(DOMAIN)
        if not isinstance(domain_data, dict):
            return None
        registry = domain_data.get(DATA_CATALOGUES)
        return registry if isinstance(registry, CatalogueRegistry) else None

    @staticmethod
    def _catalogue(
        registry: CatalogueRegistry, catalogue_id: str
    ) -> CatalogueV4:
        """Return one active catalogue or fail at the Media Source boundary."""
        catalogue = registry.get(catalogue_id)
        if catalogue is None:
            raise BrowseError(f"Unknown MediaCat catalogue: {catalogue_id}")
        return catalogue

    def _route(
        self, registry: CatalogueRegistry, identifier: str
    ) -> tuple[CatalogueV4, str, str]:
        """Resolve an explicitly catalogue-scoped identifier."""
        if not identifier.startswith(CATALOGUE_PREFIX):
            raise BrowseError(
                "A catalogue-scoped MediaCat identifier is required"
            )
        remainder = identifier.removeprefix(CATALOGUE_PREFIX)
        catalogue_id, separator, child = remainder.partition("/")
        if not catalogue_id:
            raise BrowseError("MediaCat catalogue identifier is missing")
        catalogue = self._catalogue(registry, catalogue_id)
        return catalogue, child if separator else "", (
            f"{CATALOGUE_PREFIX}{catalogue_id}/"
        )

    async def async_browse_media(
        self, item: MediaSourceItem
    ) -> BrowseMediaSource:
        """Browse the catalogue root, a category, or a playable item."""
        registry = self._registry()
        if registry is None:
            raise BrowseError("MediaCat catalogue registry is unavailable")

        identifier = item.identifier or ""
        if not identifier:
            return self._registry_root(registry)
        if identifier.startswith(REGISTRY_CATEGORY_PREFIX):
            category_id = identifier.removeprefix(REGISTRY_CATEGORY_PREFIX)
            return self._registry_category_node(
                registry, category_id, include_children=True
            )
        catalogue, child_identifier, prefix = self._route(
            registry, identifier
        )
        return self._browse_v4(catalogue, child_identifier, prefix)

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve a playable catalogue item to its stream URL."""
        registry = self._registry()
        if registry is None:
            raise Unresolvable("MediaCat catalogue registry is unavailable")

        identifier = item.identifier or ""
        try:
            catalogue, child_identifier, _ = self._route(
                registry, identifier
            )
        except BrowseError as err:
            raise Unresolvable(str(err)) from err
        return await self._resolve_v4(catalogue, item, child_identifier)

    async def async_search_media(
        self, item: MediaSourceItem, query: SearchMediaQuery
    ) -> SearchMedia:
        """Search canonical catalogue items from the root or a category."""
        registry = self._registry()
        if registry is None:
            raise BrowseError("MediaCat catalogue registry is unavailable")

        search_text = query.search_query.strip().casefold()
        if not search_text:
            return SearchMedia(result=[])

        identifier = item.identifier or ""
        if not identifier:
            results = []
            for catalogue_id, catalogue in registry.catalogues.items():
                prefix = f"{CATALOGUE_PREFIX}{catalogue_id}/"
                results.extend(
                    self._search_v4(
                        catalogue, "", search_text, prefix
                    ).result
                )
            return SearchMedia(result=results)
        if identifier.startswith(REGISTRY_CATEGORY_PREFIX):
            category_id = identifier.removeprefix(REGISTRY_CATEGORY_PREFIX)
            return self._search_registry_category(
                registry, category_id, search_text
            )
        catalogue, child_identifier, prefix = self._route(
            registry, identifier
        )
        return self._search_v4(
            catalogue, child_identifier, search_text, prefix
        )

    def _browse_v4(
        self, catalogue: CatalogueV4, identifier: str, prefix: str = ""
    ) -> BrowseMediaSource:
        """Browse a catalogue-scoped playable radio item."""
        if identifier.startswith(ITEM_PREFIX):
            item_id = identifier.removeprefix(ITEM_PREFIX)
            record = catalogue.items.get(item_id)
            if not isinstance(record, Mapping):
                raise BrowseError(f"Unknown MediaCat item: {item_id}")
            source = self._playable_source_v4(record)
            if source is None:
                raise BrowseError(f"Unplayable MediaCat item: {item_id}")
            return self._item_node_v4(item_id, record, source, prefix=prefix)

        raise BrowseError(f"Unknown MediaCat identifier: {identifier}")

    async def _resolve_v4(
        self,
        catalogue: CatalogueV4,
        item: MediaSourceItem,
        identifier: str,
    ) -> PlayMedia:
        """Resolve a schema-v4 radio source without method fallback."""
        if not identifier.startswith(ITEM_PREFIX):
            raise Unresolvable(f"Not a playable MediaCat item: {identifier}")

        item_id = identifier.removeprefix(ITEM_PREFIX)
        record = catalogue.items.get(item_id)
        if not isinstance(record, Mapping):
            raise Unresolvable(f"Unknown MediaCat item: {item_id}")

        source = self._playable_source_v4(record)
        if source is None:
            raise Unresolvable(f"Unresolvable MediaCat item: {item_id}")

        source_type = source["source_type"]
        if source_type == "url":
            return PlayMedia(source["url"], source["mime_type"])

        uri = source["uri"]
        if self._is_mediacat_uri(uri):
            raise Unresolvable(
                f"MediaCat item {item_id!r} refers back to MediaCat"
            )

        resolved = await async_resolve_media_source(
            self.hass, uri, item.target_media_player
        )
        if self._is_media_source_uri(resolved.url):
            raise Unresolvable(
                f"MediaCat item {item_id!r} resolved to another "
                "Media Source URI"
            )
        return resolved

    def _search_v4(
        self,
        catalogue: CatalogueV4,
        identifier: str,
        search_text: str,
        prefix: str = "",
    ) -> SearchMedia:
        """Search playable schema-v4 radio items in stored order."""
        if identifier:
            raise BrowseError(
                f"MediaCat search is unavailable for: {identifier}"
            )
        candidates = [
            (item_id, record)
            for item_id, record in catalogue.items.items()
            if isinstance(item_id, str) and isinstance(record, Mapping)
        ]

        results = []
        for item_id, record in candidates:
            source = self._playable_source_v4(record)
            if source is not None and self._item_matches_v4(record, search_text):
                results.append(
                    self._item_node_v4(
                        item_id, record, source, prefix=prefix
                    )
                )
        return SearchMedia(result=results)

    def _registry_root(
        self, registry: CatalogueRegistry
    ) -> BrowseMediaSource:
        """Build the catalogue-blind root from merged registry categories."""
        children = [
            self._registry_category_node(
                registry, category_id, include_children=False
            )
            for category_id in self._registry_categories(registry)
        ]
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=None,
            media_class=MediaClass.APP,
            media_content_type="",
            title=self.name,
            can_play=False,
            can_expand=True,
            can_search=True,
            children_media_class=MediaClass.DIRECTORY,
            children=children,
        )

    def _registry_categories(
        self, registry: CatalogueRegistry
    ) -> dict[str, tuple[str, list[tuple[str, CatalogueV4, str]]]]:
        """Merge categories in registry order while retaining item identity."""
        categories: dict[
            str, tuple[str, list[tuple[str, CatalogueV4, str]]]
        ] = {}
        for catalogue_id, catalogue in registry.catalogues.items():
            for category_id in catalogue.categories:
                if not isinstance(category_id, str):
                    raise BrowseError("MediaCat category ID is unusable")
                category = self._category_v4(catalogue, category_id)
                label = category["category_label"]
                existing = categories.get(category_id)
                if existing is None:
                    members: list[tuple[str, CatalogueV4, str]] = []
                    categories[category_id] = (label, members)
                else:
                    existing_label, members = existing
                    if label != existing_label:
                        raise BrowseError(
                            f"MediaCat category {category_id!r} has "
                            f"conflicting labels {existing_label!r} and "
                            f"{label!r}"
                        )
                members.extend(
                    (catalogue_id, catalogue, item_id)
                    for item_id in category["items"]
                )
        return categories

    def _registry_category_node(
        self,
        registry: CatalogueRegistry,
        category_id: str,
        *,
        include_children: bool,
    ) -> BrowseMediaSource:
        """Build one merged category while keeping item routes scoped."""
        category = self._registry_categories(registry).get(category_id)
        if category is None:
            raise BrowseError(f"Unknown MediaCat category: {category_id}")
        label, members = category
        children = None
        if include_children:
            children = []
            for catalogue_id, catalogue, item_id in members:
                record = catalogue.items.get(item_id)
                if not isinstance(record, Mapping):
                    raise BrowseError(
                        f"MediaCat category {category_id!r} references "
                        f"unavailable item {item_id!r}"
                    )
                source = self._playable_source_v4(record)
                if source is not None:
                    children.append(
                        self._item_node_v4(
                            item_id,
                            record,
                            source,
                            prefix=f"{CATALOGUE_PREFIX}{catalogue_id}/",
                        )
                    )

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{REGISTRY_CATEGORY_PREFIX}{category_id}",
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.MUSIC,
            title=label,
            can_play=False,
            can_expand=True,
            can_search=True,
            children_media_class=MediaClass.MUSIC,
            children=children,
        )

    def _search_registry_category(
        self,
        registry: CatalogueRegistry,
        category_id: str,
        search_text: str,
    ) -> SearchMedia:
        """Search one merged category in registry and authored item order."""
        category = self._registry_categories(registry).get(category_id)
        if category is None:
            raise BrowseError(f"Unknown MediaCat category: {category_id}")
        _, members = category
        results = []
        for catalogue_id, catalogue, item_id in members:
            record = catalogue.items.get(item_id)
            if not isinstance(record, Mapping):
                raise BrowseError(
                    f"MediaCat category {category_id!r} references "
                    f"unavailable item {item_id!r}"
                )
            source = self._playable_source_v4(record)
            if source is not None and self._item_matches_v4(record, search_text):
                results.append(
                    self._item_node_v4(
                        item_id,
                        record,
                        source,
                        prefix=f"{CATALOGUE_PREFIX}{catalogue_id}/",
                    )
                )
        return SearchMedia(result=results)

    def _item_node_v4(
        self,
        item_id: str,
        record: Mapping[Any, Any],
        source: Mapping[Any, Any],
        *,
        prefix: str = "",
    ) -> BrowseMediaSource:
        """Build a playable schema-v4 radio item node."""
        artwork = record.get("artwork")
        thumbnail = None
        if isinstance(artwork, Mapping):
            thumbnail = self._non_empty_string(artwork.get("local"))
            if thumbnail is None:
                thumbnail = self._non_empty_string(artwork.get("external"))
        media_content_type = (
            source["mime_type"]
            if source["source_type"] == "url"
            else source["media_type"]
        )
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{prefix}{ITEM_PREFIX}{item_id}",
            media_class=MediaClass.MUSIC,
            media_content_type=media_content_type,
            title=record["catalogue_label"],
            can_play=True,
            can_expand=False,
            thumbnail=thumbnail,
        )

    def _category_v4(
        self, catalogue: CatalogueV4, category_id: str
    ) -> Mapping[Any, Any]:
        """Return the interface fields of a usable schema-v4 category."""
        category = catalogue.categories.get(category_id)
        if category is None:
            raise BrowseError(f"Unknown MediaCat category: {category_id}")
        if not isinstance(category, Mapping):
            raise BrowseError(f"Unusable MediaCat category: {category_id}")
        if self._non_empty_string(category.get("category_label")) is None:
            raise BrowseError(f"Unusable MediaCat category: {category_id}")
        item_ids = category.get("items")
        if not isinstance(item_ids, list | tuple) or any(
            not isinstance(item_id, str) or not item_id for item_id in item_ids
        ):
            raise BrowseError(f"Unusable MediaCat category: {category_id}")
        return category

    @classmethod
    def _playable_source_v4(
        cls, record: Mapping[Any, Any]
    ) -> Mapping[Any, Any] | None:
        """Return only a usable ha_mplayer source for a schema-v4 radio item."""
        if record.get("type") != SUPPORTED_ITEM_TYPE:
            return None
        if cls._non_empty_string(record.get("catalogue_label")) is None:
            return None
        methods = record.get("execution_methods")
        if not isinstance(methods, Mapping):
            return None
        method = methods.get("ha_mplayer")
        if not isinstance(method, Mapping):
            return None
        source = method.get("source")
        if not isinstance(source, Mapping):
            return None

        source_type = source.get("source_type")
        if source_type == "url":
            if (
                cls._non_empty_string(source.get("url")) is not None
                and cls._non_empty_string(source.get("mime_type")) is not None
            ):
                return source
            return None
        if source_type == "ha_media_source":
            uri = cls._non_empty_string(source.get("uri"))
            if (
                uri is not None
                and cls._is_media_source_uri(uri)
                and cls._non_empty_string(source.get("media_type")) is not None
            ):
                return source
        return None

    @staticmethod
    def _item_matches_v4(
        record: Mapping[Any, Any], search_text: str
    ) -> bool:
        """Match only the agreed schema-v4 catalogue search fields."""
        label = record["catalogue_label"]
        if search_text in label.casefold():
            return True
        description = record.get("description")
        if isinstance(description, str) and search_text in description.casefold():
            return True
        tags = record.get("tags")
        if isinstance(tags, list | tuple):
            return any(
                isinstance(tag, str) and search_text in tag.casefold()
                for tag in tags
            )
        return False

    @staticmethod
    def _non_empty_string(value: Any) -> str | None:
        """Return a stored non-blank string without normalizing it."""
        return value if isinstance(value, str) and value.strip() else None

    @staticmethod
    def _is_media_source_uri(value: Any) -> bool:
        """Return whether a value is a syntactically usable Media Source URI."""
        if not isinstance(value, str):
            return False
        try:
            parsed = urlsplit(value)
        except ValueError:
            return False
        return parsed.scheme.casefold() == "media-source" and bool(parsed.netloc)

    @classmethod
    def _is_mediacat_uri(cls, value: Any) -> bool:
        """Return whether a Media Source URI points back to this domain."""
        if not cls._is_media_source_uri(value):
            return False
        return urlsplit(value).netloc.casefold() == DOMAIN.casefold()
