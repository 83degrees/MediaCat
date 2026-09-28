# MediaCat Architecture

## Status and authority

This document is the authoritative current-state architecture for MediaCat.

The governed visual companion is
[MEDIACAT_ARCHITECTURE.drawio](Diagrams/MEDIACAT_ARCHITECTURE.drawio).
The stored catalogue schema and preventative-validation policy are owned by
[MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md](MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md).
The precise cross-product lookup interface is owned by
[MEDIACAT_ITEM_LOOKUP_INTERFACE.md](../03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md).
The supported local-management boundary is owned by
[MEDIACAT_ADMIN_INTERFACE.md](../03_Contracts/MEDIACAT_ADMIN_INTERFACE.md).

Where exact interface semantics matter, the provider-owned contract is
authoritative. Historical migration, deployment and rollback evidence remains
preserved outside this current architecture.

## Product purpose and boundaries

MediaCat is the media-catalogue and route-registry product. It owns:

- catalogue-scoped media identity;
- catalogue structure, membership, metadata and ordering;
- local multi-catalogue discovery and immutable active registry state;
- the execution methods available for each item and their route-specific source facts;
- the normalized item-lookup producer boundary; and
- catalogue capability, validation and transactional reload services; and
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
- catalogue directory `/config/mediacat/catalogues/` with one YAML document per catalogue;
- Home Assistant action namespace `mediacat`;
- Media Source domain `mediacat`; and
- logical catalogue identity `catalogue_id: curated_media`.

Runtime namespace and logical catalogue identity are deliberately separate.
DDR-03-002 records the durable rationale for that decision.

During setup, MediaCat discovers `.yaml` and `.yml` files in filename order,
loads every schema-v4 catalogue, and keys the resulting registry by the
authoritative in-file `catalogue_id`. Filenames are storage convenience and do
not define identity. Duplicate `catalogue_id` values across files reject the
complete candidate registry.

For each file MediaCat rejects duplicate YAML mapping keys, validates the
complete closed vocabulary and all governed structural, value, pairing and
reference rules, resolves authored artwork sources into the common runtime
`artwork.local` / `artwork.external` shape, and recursively freezes the result.
The immutable registry is stored under
`hass.data["mediacat"]["catalogues"]`. Authored mapping and category-membership
order are preserved. Setup failure is atomic: if any discovered catalogue
cannot be loaded or accepted, MediaCat does not expose a partially initialized
runtime surface.

The maintained runtime accepts only `catalogue_schema_version: 4`.
Schema-v2 runtime compatibility and the raw `mediacat.resolve_item` action are
retired. Their retained code/data exists only as historical or rollback
evidence and does not define current runtime behaviour.

## Current MediaCat interfaces

### Normalized item lookup

`mediacat.resolve_media_record` is the sole current normalized cross-product
lookup producer.

It accepts exact `catalogue_id` and `item_id` inputs matching the schema-v4
identifier rule and returns one complete normalized record containing the item
identity, player-independent metadata and all execution methods available for
that item. The maintained action schema and resolver validate both identifiers
before lookup, so malformed input fails separately from a conforming identifier
that is not found.

MediaCat reports available execution methods; it does not select one. It does
not attach endpoint, fallback or playback-profile context.

Exact request, response, presence, failure and compatibility semantics are
defined by the provider-owned item lookup contract.

### Local catalogue administration

MediaCat exposes response-only Home Assistant actions for supported schema and
capability discovery, side-effect-free validation of a supplied YAML document,
and transactional reload of the complete local registry. Validation does not
write files or change active state. Reload discovers and validates the full
directory before one active-registry replacement; any failure retains the
previous immutable registry.

The separate MediaCat Manager product owns editing, atomic filesystem writes,
backups/history and user workflow. It consumes the supported admin interface
and does not duplicate MediaCat schema validation. Exact request, response and
failure semantics are defined by the provider-owned admin contract.

### Home Assistant Media Source

The `mediacat` Media Source is a separate Home Assistant browse/search/play
surface over the same active catalogue registry.

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

With multiple active catalogues, Media Browser identifiers are catalogue-scoped
as `catalogue/<catalogue_id>/category/<category_id>` and
`catalogue/<catalogue_id>/item/<item_id>`. Root search spans every catalogue in
registry order. Catalogue scope is required even when `curated_media` is the
only active catalogue; unscoped `category/<category_id>` and `item/<item_id>`
identifiers are rejected. This retires the former implicit single-catalogue
routing assumption without changing the logical `curated_media` identity.

## MediaCat-owned runtime behaviour

The active immutable catalogue registry is the common source for MediaCat
runtime interfaces:

1. setup loads, validates and freezes every discovered schema-v4 catalogue;
2. normalized lookup resolves a catalogue-scoped item and emits the complete
   consumer-facing record;
3. Media Source projects playable subsets through catalogue-scoped paths; and
4. admin actions report capabilities, validate candidates without mutation and
   transactionally replace the registry after complete revalidation.

The normalized lookup and Media Source are related surfaces over the same
catalogue, but they serve different purposes. The lookup contract exposes all
execution methods to governed consumers. Media Source exposes only what its
Home Assistant playback adapter can directly represent.

Stored catalogue schema version and consumer-facing returned-record version have
independent compatibility lifecycles. Stored authoring and preventative
validation are governed by the catalogue schema architecture; consumer-facing
record compatibility is governed by the lookup contract.

## Responsibilities and ownership boundaries

| Capability | Owner | MediaCat boundary |
| --- | --- | --- |
| Catalogue identity, structure, metadata, membership and order | MediaCat | Owned |
| Catalogue directory discovery and active immutable registry | MediaCat | Owned; identity comes from in-file `catalogue_id` |
| Available execution methods and source facts | MediaCat | Owned; reported without selection |
| Normalized lookup producer | MediaCat | Owned through `mediacat.resolve_media_record` |
| Capability, candidate validation and transactional reload | MediaCat | Owned through the provider admin contract |
| Catalogue editing, file replacement and local history | MediaCat Manager | External client/admin product |
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

The current implemented architecture is schema v4 under the `mediacat`
runtime namespace with logical `catalogue_id: curated_media`.

The following are separate governed compatibility concerns:

- stored catalogue evolution — owned by the catalogue schema architecture, including artwork-source authoring and load-time resolution;
- normalized consumer-record evolution — owned by the item lookup contract;
- local administration interface evolution — owned by the admin contract;
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
- `01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md` — stored schema-v4 authoring and preventative-validation architecture.
- `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio` — governed visual representation of this architecture.
- `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` — normalized lookup interface.
- `03_Contracts/MEDIACAT_ADMIN_INTERFACE.md` — capability, validation and transactional reload interface.
- `02_Decisions/DDR-03-001.md` — schema-v3 transition and historical rollback rationale.
- `02_Decisions/DDR-03-002.md` — runtime namespace and catalogue-identity separation rationale.
- `02_Decisions/DDR-03-004.md` — multi-catalogue registry and admin-boundary rationale.
