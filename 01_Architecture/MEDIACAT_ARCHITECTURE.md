# MediaCat Architecture

## Status and authority

This document is the authoritative current-state architecture for MediaCat.

The governed visual companion is
[MEDIACAT_ARCHITECTURE.drawio](Diagrams/MEDIACAT_ARCHITECTURE.drawio).
The stored catalogue schema and preventative-validation policy are owned by
[MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md](MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md).
The precise cross-product lookup interface is owned by
[MEDIACAT_ITEM_LOOKUP_INTERFACE.md](../03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md).

Where exact interface semantics matter, the provider-owned contract is
authoritative. Historical migration, deployment and rollback evidence remains
preserved outside this current architecture.

## Product purpose and boundaries

MediaCat is the media-catalogue and route-registry product. It owns:

- catalogue-scoped media identity;
- catalogue structure, membership, metadata and ordering;
- the execution methods available for each item and their route-specific source facts;
- the normalized item-lookup producer boundary; and
- the Home Assistant Media Source view over the playable subset of the catalogue.

MediaCat does **not** own consumer orchestration, execution-method preference or
selection, endpoint selection, fallback policy, playback-profile processing or
final playback execution.

ASTV is an external consumer that owns intent orchestration, method and endpoint
selection and fallback policy. AdvMedia is an external consumer/processor that
operates on caller-selected Home Assistant media context. Their internal
architecture is outside MediaCat and is referenced only where necessary to make
the MediaCat boundary explicit.

## Current runtime architecture

MediaCat runs as the Home Assistant custom integration domain `mediacat`.

The maintained runtime uses:

- integration directory `/config/custom_components/mediacat/`;
- catalogue path `/config/mediacat/catalogue.yaml`;
- Home Assistant action namespace `mediacat`;
- Media Source domain `mediacat`; and
- logical catalogue identity `catalogue_id: curated_media`.

Runtime namespace and logical catalogue identity are deliberately separate.
DDR-03-002 records the durable rationale for that decision.

During setup, MediaCat loads the schema-v3 catalogue, rejects duplicate YAML
mapping keys, validates the complete closed vocabulary and all governed
structural, value, pairing and reference rules, recursively freezes the loaded
mapping, and stores the immutable snapshot under
`hass.data["mediacat"]["catalogue"]`. Authored mapping and category-membership
order are preserved. Setup failure is atomic: if the catalogue cannot be loaded
or accepted, MediaCat does not expose a partially initialized lookup surface.

The maintained runtime accepts only `catalogue_schema_version: 3`.
Schema-v2 runtime compatibility and the raw `mediacat.resolve_item` action are
retired. Their retained code/data exists only as historical or rollback
evidence and does not define current runtime behaviour.

## Current MediaCat interfaces

### Normalized item lookup

`mediacat.resolve_media_record` is the sole current normalized cross-product
lookup producer.

It accepts exact `catalogue_id` and `item_id` inputs matching the schema-v3
identifier rule and returns one complete normalized record containing the item
identity, player-independent metadata and all execution methods available for
that item. The maintained action schema and resolver validate both identifiers
before lookup, so malformed input fails separately from a conforming identifier
that is not found.

MediaCat reports available execution methods; it does not select one. It does
not attach endpoint, fallback or playback-profile context.

Exact request, response, presence, failure and compatibility semantics are
defined by the provider-owned item lookup contract.

### Home Assistant Media Source

The `mediacat` Media Source is a separate Home Assistant browse/search/play
surface over the same loaded catalogue snapshot.

It preserves stored category and item order and currently exposes records that
the Media Source adapter can represent through a usable
`execution_methods.ha_mplayer.source`.

For playable items it:

- supports browse and search using catalogue-facing metadata;
- returns stored direct URL sources with their media type information; and
- delegates an `ha_media_source` URI once to the owning Home Assistant Media
  Source provider, rejecting recursive/self-referential resolution.

Media Source does not select an alternative execution method when an item is not
representable through its supported playback path. Assistant-command-only items
therefore remain outside the Media Source browse/search projection.

## MediaCat-owned runtime behaviour

The loaded catalogue snapshot is the common source for both current MediaCat
interfaces:

1. setup loads and freezes the current schema-v3 catalogue;
2. normalized lookup resolves a catalogue-scoped item and emits the complete
   consumer-facing record;
3. Media Source projects the playable subset for Home Assistant browse/search
   and resolves the selected playable item.

The normalized lookup and Media Source are related surfaces over the same
catalogue, but they serve different purposes. The lookup contract exposes all
execution methods to governed consumers. Media Source exposes only what its
Home Assistant playback adapter can directly represent.

Stored catalogue schema version and consumer-facing returned-record version have
independent compatibility lifecycles. Stored authoring and preventative
validation are governed by the catalogue schema architecture; consumer-facing
record compatibility is governed by the lookup contract.

## Public artwork delivery

MediaCat may store both Home Assistant-local and public artwork references for an
item. The stored schema and exact field rules remain owned by the catalogue
schema architecture.

Where an Internet-reachable artwork URL is required, MediaCat uses a public
Cloudflare R2 delivery surface and stores the resulting absolute HTTPS URL in
`artwork.external`. Stable object keys are grouped by media type, for example
`radio/classic-fm.png` and `tv/bbc-iplayer.png`.

The public asset host is a delivery dependency, not part of the Home Assistant
runtime. MediaCat catalogue loading and normalized lookup do not fetch the
artwork object. Consumers retrieve the published URL independently.

Home Assistant-local artwork may continue to be represented separately through
`artwork.local`. Public artwork hosting must not require exposing a Home
Assistant instance to the public Internet.

DDR-03-003 records the hosting decision and trade-offs. Operational publication
and replacement steps are documented in
`08_Deployment/MEDIACAT_ARTWORK_HOSTING.md`.

## Responsibilities and ownership boundaries

| Capability | Owner | MediaCat boundary |
| --- | --- | --- |
| Catalogue identity, structure, metadata, membership and order | MediaCat | Owned |
| Available execution methods and source facts | MediaCat | Owned; reported without selection |
| Normalized lookup producer | MediaCat | Owned through `mediacat.resolve_media_record` |
| Media Source browse/search/play projection | MediaCat | Owned adapter over the loaded catalogue |
| Method preference and selection | ASTV | External |
| Endpoint selection and fallback policy | ASTV | External |
| Selected-method/profile processing | AdvMedia | External |
| Home Assistant runtime/framework | Home Assistant | External |
| Delegated Media Source providers | Respective provider owners | External |

External consumers may depend only on governed MediaCat interfaces, not on the
stored YAML shape, loader internals, `hass.data` representation, category
implementation details or other undocumented runtime internals.

## Compatibility and evolution boundaries

The current implemented architecture is schema v3 under the `mediacat`
runtime namespace with logical `catalogue_id: curated_media`.

The following are separate governed compatibility concerns:

- stored catalogue evolution — owned by the catalogue schema architecture;
- normalized consumer-record evolution — owned by the item lookup contract;
- runtime namespace identity — durable rationale recorded in DDR-03-002; and
- historical schema-v2 / retired-action recovery evidence — preserved outside
  the maintained runtime.

DDR-03-001 records the rationale for the schema-v3 transition and the preserved
historical schema-v2 rollback package.

A material change to MediaCat responsibilities, ownership boundaries or current
runtime architecture requires governed architecture work. Exact contract changes
must be made in the provider-owned contract rather than being introduced only
through this document.

## Authoritative references

- `00_Governance/PROJECT_PROFILE.md` — product identity, scope and declared dependencies.
- `01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md` — stored schema-v3 authoring and preventative-validation architecture.
- `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio` — governed visual representation of this architecture.
- `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` — normalized lookup interface.
- `02_Decisions/DDR-03-001.md` — schema-v3 transition and historical rollback rationale.
- `02_Decisions/DDR-03-002.md` — runtime namespace and catalogue-identity separation rationale.
