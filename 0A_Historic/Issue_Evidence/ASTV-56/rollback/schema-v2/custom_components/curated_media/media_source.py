"""Expose the Curated Media catalogue in Home Assistant's Media Browser."""

from __future__ import annotations

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
)
from homeassistant.core import HomeAssistant

from .catalogue import Catalogue, CatalogueCategory, CatalogueItem, CatalogueSource
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


async def async_get_media_source(hass: HomeAssistant) -> CuratedMediaSource:
    """Set up the Curated Media media source."""
    return CuratedMediaSource(hass)


class CuratedMediaSource(MediaSource):
    """Provide the Curated Media catalogue as a media source."""

    name = "Curated Media"

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the media source."""
        super().__init__(DOMAIN)
        self.hass = hass

    def _catalogue(self) -> Catalogue | None:
        """Return the loaded catalogue, if integration setup succeeded."""
        domain_data = self.hass.data.get(DOMAIN)
        if not isinstance(domain_data, dict):
            return None
        catalogue = domain_data.get(DATA_CATALOGUE)
        return catalogue if isinstance(catalogue, Catalogue) else None

    async def async_browse_media(
        self, item: MediaSourceItem
    ) -> BrowseMediaSource:
        """Browse the catalogue root, a category, or a playable item."""
        catalogue = self._catalogue()
        if catalogue is None:
            raise BrowseError("Curated Media catalogue is unavailable")

        identifier = item.identifier or ""

        if not identifier:
            return self._root_node(catalogue)

        if identifier.startswith(CATEGORY_PREFIX):
            category_id = identifier.removeprefix(CATEGORY_PREFIX)
            category = catalogue.categories.get(category_id)
            if category is None:
                raise BrowseError(f"Unknown Curated Media category: {category_id}")
            return self._category_node(
                catalogue, category, include_children=True
            )

        if identifier.startswith(ITEM_PREFIX):
            item_id = identifier.removeprefix(ITEM_PREFIX)
            catalogue_item = catalogue.items.get(item_id)
            if catalogue_item is None:
                raise BrowseError(f"Unknown Curated Media item: {item_id}")
            return self._item_node(catalogue_item)

        raise BrowseError(f"Unknown Curated Media identifier: {identifier}")

    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia:
        """Resolve a playable catalogue item to its stream URL."""
        catalogue = self._catalogue()
        if catalogue is None:
            raise Unresolvable("Curated Media catalogue is unavailable")

        identifier = item.identifier or ""
        if not identifier.startswith(ITEM_PREFIX):
            raise Unresolvable(f"Not a playable Curated Media item: {identifier}")

        item_id = identifier.removeprefix(ITEM_PREFIX)
        catalogue_item = catalogue.items.get(item_id)
        if catalogue_item is None:
            raise Unresolvable(f"Unknown Curated Media item: {item_id}")
        if catalogue_item.item_type != SUPPORTED_ITEM_TYPE:
            raise Unresolvable(
                f"Unsupported Curated Media item type: {catalogue_item.item_type}"
            )

        return self._resolve_source(catalogue_item)

    async def async_search_media(
        self, item: MediaSourceItem, query: SearchMediaQuery
    ) -> SearchMedia:
        """Search canonical catalogue items from the root or a category."""
        catalogue = self._catalogue()
        if catalogue is None:
            raise BrowseError("Curated Media catalogue is unavailable")

        search_text = query.search_query.strip().casefold()
        if not search_text:
            return SearchMedia(result=[])

        identifier = item.identifier or ""
        if not identifier:
            candidates = list(catalogue.items.values())
        elif identifier.startswith(CATEGORY_PREFIX):
            category_id = identifier.removeprefix(CATEGORY_PREFIX)
            category = catalogue.categories.get(category_id)
            if category is None:
                raise BrowseError(f"Unknown Curated Media category: {category_id}")

            candidates = []
            for item_id in category.item_ids:
                catalogue_item = catalogue.items.get(item_id)
                if catalogue_item is None:
                    raise BrowseError(
                        f"Curated Media category {category.category_id!r} "
                        f"references unavailable item {item_id!r}"
                    )
                candidates.append(catalogue_item)
        else:
            raise BrowseError(
                f"Curated Media search is unavailable for: {identifier}"
            )

        results = [
            self._item_node(catalogue_item)
            for catalogue_item in candidates
            if self._item_matches(catalogue_item, search_text)
        ]
        return SearchMedia(result=results)

    def _root_node(self, catalogue: Catalogue) -> BrowseMediaSource:
        """Build the Curated Media root with categories as direct children."""
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
                        f"Curated Media category {category.category_id!r} "
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
                f"Unsupported Curated Media source type: "
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
                f"Unsupported Curated Media stream format: {source.source_format}"
            )
        return PlayMedia(source.url, mime_type)

    @staticmethod
    def _source_media_content_type(source: CatalogueSource) -> str:
        """Return the browse content type for a validated stream source."""
        if source.source_type != SUPPORTED_SOURCE_TYPE:
            raise BrowseError(
                f"Unsupported Curated Media source type: {source.source_type}"
            )
        mime_type = STREAM_FORMAT_MIME_TYPES.get(source.source_format)
        if mime_type is None:
            raise BrowseError(
                f"Unsupported Curated Media stream format: {source.source_format}"
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
