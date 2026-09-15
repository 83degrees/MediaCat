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

from .catalogue import (
    Catalogue,
    CatalogueCategory,
    CatalogueItem,
    CatalogueSource,
    CatalogueV3,
)
from .const import (
    DATA_CATALOGUE,
    DOMAIN,
    SUPPORTED_ITEM_TYPE,
    SUPPORTED_SOURCE_TYPE,
)

CATEGORY_PREFIX = "category/"
ITEM_PREFIX = "item/"
STREAM_FORMAT_MIME_TYPES = {
    "hls": "application/vnd.apple.mpegurl",
    "mp3": "audio/mpeg",
}


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

    def _catalogue(self) -> Catalogue | CatalogueV3 | None:
        """Return the loaded catalogue, if integration setup succeeded."""
        domain_data = self.hass.data.get(DOMAIN)
        if not isinstance(domain_data, dict):
            return None
        catalogue = domain_data.get(DATA_CATALOGUE)
        return (
            catalogue
            if isinstance(catalogue, Catalogue | CatalogueV3)
            else None
        )

    async def async_browse_media(
        self, item: MediaSourceItem
    ) -> BrowseMediaSource:
        """Browse the catalogue root, a category, or a playable item."""
        catalogue = self._catalogue()
        if catalogue is None:
            raise BrowseError("MediaCat catalogue is unavailable")

        identifier = item.identifier or ""
        if isinstance(catalogue, CatalogueV3):
            return self._browse_v3(catalogue, identifier)

        if not identifier:
            return self._root_node(catalogue)

        if identifier.startswith(CATEGORY_PREFIX):
            category_id = identifier.removeprefix(CATEGORY_PREFIX)
            category = catalogue.categories.get(category_id)
            if category is None:
                raise BrowseError(f"Unknown MediaCat category: {category_id}")
            return self._category_node(
                catalogue, category, include_children=True
            )

        if identifier.startswith(ITEM_PREFIX):
            item_id = identifier.removeprefix(ITEM_PREFIX)
            catalogue_item = catalogue.items.get(item_id)
            if catalogue_item is None:
                raise BrowseError(f"Unknown MediaCat item: {item_id}")
            return self._item_node(catalogue_item)

        raise BrowseError(f"Unknown MediaCat identifier: {identifier}")

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve a playable catalogue item to its stream URL."""
        catalogue = self._catalogue()
        if catalogue is None:
            raise Unresolvable("MediaCat catalogue is unavailable")

        identifier = item.identifier or ""
        if isinstance(catalogue, CatalogueV3):
            return await self._resolve_v3(catalogue, item, identifier)

        if not identifier.startswith(ITEM_PREFIX):
            raise Unresolvable(f"Not a playable MediaCat item: {identifier}")

        item_id = identifier.removeprefix(ITEM_PREFIX)
        catalogue_item = catalogue.items.get(item_id)
        if catalogue_item is None:
            raise Unresolvable(f"Unknown MediaCat item: {item_id}")
        if catalogue_item.item_type != SUPPORTED_ITEM_TYPE:
            raise Unresolvable(
                f"Unsupported MediaCat item type: {catalogue_item.item_type}"
            )

        return self._resolve_source(catalogue_item)

    async def async_search_media(
        self, item: MediaSourceItem, query: SearchMediaQuery
    ) -> SearchMedia:
        """Search canonical catalogue items from the root or a category."""
        catalogue = self._catalogue()
        if catalogue is None:
            raise BrowseError("MediaCat catalogue is unavailable")

        search_text = query.search_query.strip().casefold()
        if not search_text:
            return SearchMedia(result=[])

        identifier = item.identifier or ""
        if isinstance(catalogue, CatalogueV3):
            return self._search_v3(catalogue, identifier, search_text)

        if not identifier:
            candidates = list(catalogue.items.values())
        elif identifier.startswith(CATEGORY_PREFIX):
            category_id = identifier.removeprefix(CATEGORY_PREFIX)
            category = catalogue.categories.get(category_id)
            if category is None:
                raise BrowseError(f"Unknown MediaCat category: {category_id}")

            candidates = []
            for item_id in category.item_ids:
                catalogue_item = catalogue.items.get(item_id)
                if catalogue_item is None:
                    raise BrowseError(
                        f"MediaCat category {category.category_id!r} "
                        f"references unavailable item {item_id!r}"
                    )
                candidates.append(catalogue_item)
        else:
            raise BrowseError(
                f"MediaCat search is unavailable for: {identifier}"
            )

        results = [
            self._item_node(catalogue_item)
            for catalogue_item in candidates
            if self._item_matches(catalogue_item, search_text)
        ]
        return SearchMedia(result=results)

    def _root_node(self, catalogue: Catalogue) -> BrowseMediaSource:
        """Build the MediaCat root with categories as direct children."""
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
            children=[
                self._category_node(catalogue, category, include_children=False)
                for category in catalogue.categories.values()
            ],
        )

    def _category_node(
        self,
        catalogue: Catalogue,
        category: CatalogueCategory,
        *,
        include_children: bool,
    ) -> BrowseMediaSource:
        """Build a category node, optionally populated with its items."""
        children = None
        if include_children:
            children = []
            for item_id in category.item_ids:
                item = catalogue.items.get(item_id)
                if item is None:
                    raise BrowseError(
                        f"MediaCat category {category.category_id!r} "
                        f"references unavailable item {item_id!r}"
                    )
                children.append(self._item_node(item))

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{CATEGORY_PREFIX}{category.category_id}",
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.MUSIC,
            title=category.title,
            can_play=False,
            can_expand=True,
            can_search=True,
            children_media_class=MediaClass.MUSIC,
            children=children,
        )

    def _item_node(self, item: CatalogueItem) -> BrowseMediaSource:
        """Build a playable radio item node."""
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{ITEM_PREFIX}{item.item_id}",
            media_class=MediaClass.MUSIC,
            media_content_type=self._source_media_content_type(item.source),
            title=item.title,
            can_play=True,
            can_expand=False,
            thumbnail=item.artwork,
        )

    def _resolve_source(self, item: CatalogueItem) -> PlayMedia:
        """Resolve a catalogue item's source to playable media."""
        if item.source.source_type != SUPPORTED_SOURCE_TYPE:
            raise Unresolvable(
                f"Unsupported MediaCat source type: "
                f"{item.source.source_type}"
            )
        return self._resolve_stream(item.source)

    @staticmethod
    def _resolve_stream(source: CatalogueSource) -> PlayMedia:
        """Resolve a direct stream source."""
        mime_type = source.source_mime_type or STREAM_FORMAT_MIME_TYPES.get(
            source.source_format
        )
        if mime_type is None:
            raise Unresolvable(
                f"Unsupported MediaCat stream format: {source.source_format}"
            )
        return PlayMedia(source.url, mime_type)

    @staticmethod
    def _source_media_content_type(source: CatalogueSource) -> str:
        """Return the browse content type for a validated stream source."""
        if source.source_type != SUPPORTED_SOURCE_TYPE:
            raise BrowseError(
                f"Unsupported MediaCat source type: {source.source_type}"
            )
        mime_type = STREAM_FORMAT_MIME_TYPES.get(source.source_format)
        if mime_type is None:
            raise BrowseError(
                f"Unsupported MediaCat stream format: {source.source_format}"
            )
        return mime_type

    @staticmethod
    def _item_matches(item: CatalogueItem, search_text: str) -> bool:
        """Return whether an item's searchable metadata contains the query."""
        if search_text in item.title.casefold():
            return True
        if item.description and search_text in item.description.casefold():
            return True
        return any(search_text in tag.casefold() for tag in item.tags)

    def _browse_v3(
        self, catalogue: CatalogueV3, identifier: str
    ) -> BrowseMediaSource:
        """Browse a schema-v3 category or playable radio item."""
        if not identifier:
            return self._root_node_v3(catalogue)

        if identifier.startswith(CATEGORY_PREFIX):
            category_id = identifier.removeprefix(CATEGORY_PREFIX)
            category = self._category_v3(catalogue, category_id)
            return self._category_node_v3(
                catalogue, category_id, category, include_children=True
            )

        if identifier.startswith(ITEM_PREFIX):
            item_id = identifier.removeprefix(ITEM_PREFIX)
            record = catalogue.items.get(item_id)
            if not isinstance(record, Mapping):
                raise BrowseError(f"Unknown MediaCat item: {item_id}")
            source = self._playable_source_v3(record)
            if source is None:
                raise BrowseError(f"Unplayable MediaCat item: {item_id}")
            return self._item_node_v3(item_id, record, source)

        raise BrowseError(f"Unknown MediaCat identifier: {identifier}")

    async def _resolve_v3(
        self,
        catalogue: CatalogueV3,
        item: MediaSourceItem,
        identifier: str,
    ) -> PlayMedia:
        """Resolve a schema-v3 radio source without method fallback."""
        if not identifier.startswith(ITEM_PREFIX):
            raise Unresolvable(f"Not a playable MediaCat item: {identifier}")

        item_id = identifier.removeprefix(ITEM_PREFIX)
        record = catalogue.items.get(item_id)
        if not isinstance(record, Mapping):
            raise Unresolvable(f"Unknown MediaCat item: {item_id}")

        source = self._playable_source_v3(record)
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

    def _search_v3(
        self, catalogue: CatalogueV3, identifier: str, search_text: str
    ) -> SearchMedia:
        """Search playable schema-v3 radio items in stored order."""
        candidates: list[tuple[str, Mapping[Any, Any]]] = []
        if not identifier:
            candidates.extend(
                (item_id, record)
                for item_id, record in catalogue.items.items()
                if isinstance(item_id, str) and isinstance(record, Mapping)
            )
        elif identifier.startswith(CATEGORY_PREFIX):
            category_id = identifier.removeprefix(CATEGORY_PREFIX)
            category = self._category_v3(catalogue, category_id)
            for item_id in category["items"]:
                record = catalogue.items.get(item_id)
                if not isinstance(record, Mapping):
                    raise BrowseError(
                        f"MediaCat category {category_id!r} references "
                        f"unavailable item {item_id!r}"
                    )
                candidates.append((item_id, record))
        else:
            raise BrowseError(
                f"MediaCat search is unavailable for: {identifier}"
            )

        results = []
        for item_id, record in candidates:
            source = self._playable_source_v3(record)
            if source is not None and self._item_matches_v3(record, search_text):
                results.append(self._item_node_v3(item_id, record, source))
        return SearchMedia(result=results)

    def _root_node_v3(self, catalogue: CatalogueV3) -> BrowseMediaSource:
        """Build a schema-v3 root preserving category mapping order."""
        children = []
        for category_id in catalogue.categories:
            if not isinstance(category_id, str):
                raise BrowseError("MediaCat category ID is unusable")
            category = self._category_v3(catalogue, category_id)
            children.append(
                self._category_node_v3(
                    catalogue, category_id, category, include_children=False
                )
            )
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

    def _category_node_v3(
        self,
        catalogue: CatalogueV3,
        category_id: str,
        category: Mapping[Any, Any],
        *,
        include_children: bool,
    ) -> BrowseMediaSource:
        """Build a schema-v3 radio category and filter unplayable members."""
        children = None
        if include_children:
            children = []
            for item_id in category["items"]:
                record = catalogue.items.get(item_id)
                if not isinstance(record, Mapping):
                    raise BrowseError(
                        f"MediaCat category {category_id!r} references "
                        f"unavailable item {item_id!r}"
                    )
                source = self._playable_source_v3(record)
                if source is not None:
                    children.append(self._item_node_v3(item_id, record, source))

        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{CATEGORY_PREFIX}{category_id}",
            media_class=MediaClass.DIRECTORY,
            media_content_type=MediaType.MUSIC,
            title=category["category_label"],
            can_play=False,
            can_expand=True,
            can_search=True,
            children_media_class=MediaClass.MUSIC,
            children=children,
        )

    def _item_node_v3(
        self,
        item_id: str,
        record: Mapping[Any, Any],
        source: Mapping[Any, Any],
    ) -> BrowseMediaSource:
        """Build a playable schema-v3 radio item node."""
        artwork = record.get("artwork")
        thumbnail = (
            self._non_empty_string(artwork.get("local"))
            if isinstance(artwork, Mapping)
            else None
        )
        media_content_type = (
            source["mime_type"]
            if source["source_type"] == "url"
            else source["media_type"]
        )
        return BrowseMediaSource(
            domain=DOMAIN,
            identifier=f"{ITEM_PREFIX}{item_id}",
            media_class=MediaClass.MUSIC,
            media_content_type=media_content_type,
            title=record["catalogue_label"],
            can_play=True,
            can_expand=False,
            thumbnail=thumbnail,
        )

    def _category_v3(
        self, catalogue: CatalogueV3, category_id: str
    ) -> Mapping[Any, Any]:
        """Return the interface fields of a usable schema-v3 category."""
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
    def _playable_source_v3(
        cls, record: Mapping[Any, Any]
    ) -> Mapping[Any, Any] | None:
        """Return only a usable ha_mplayer source for a schema-v3 radio item."""
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
    def _item_matches_v3(
        record: Mapping[Any, Any], search_text: str
    ) -> bool:
        """Match only the agreed schema-v3 catalogue search fields."""
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
