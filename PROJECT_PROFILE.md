# PROJECT_PROFILE: MediaCat

## Profile conformance

This profile contains the required Governance 2.0 product-profile subjects and
is current under the operational Governance 2.0 authority.

## Document status

- Governance state: current approved
- Exact migration baseline: `c1d5f5c7a895456b1f81f7a48d3ca2c8a65c407d`

## Product identity

- Product name: MediaCat
- Repository: `83degrees/MediaCat`

## Purpose

MediaCat is the media-catalogue and route-registry product. It supplies
catalogue-scoped media identity, structure, membership, metadata, available
delivery routes, route-specific facts, and a normalized item lookup for
governed consumers.

## Scope

### In scope

- Media identity and catalogue-scoped item lookup.
- Catalogue structure, metadata, membership, and ordered catalogue content.
- Available execution methods and route-specific source facts for each item.
- The normalized complete returned record and its compatibility version.
- The Curated Media Home Assistant integration, catalogue, and Media Source
  surface as the current deployed MediaCat implementation.

### Out of scope

- ASTV request resolution, orchestration, method or route selection, endpoint
  selection, and fallback policy.
- AdvMedia source translation, endpoint/profile processing, playback-payload
  preparation, and execution implementation.
- ASTV-owned `assistant_command` construction or execution.
- Home Assistant, Radio Browser, Google Assistant, or media-player ownership.
- Treating Curated Media as the whole MediaCat product or assuming a separate
  deployed `mediacat` Home Assistant domain.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| Media identity, catalogue structure, metadata, membership, routes, and route-specific facts | owned | MediaCat | MediaCat reports all available methods and does not select one. |
| Normalized MediaCat item lookup and returned record | owned | MediaCat | Exact request, record, compatibility, and failure promises are defined by `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md`. |
| Curated Media integration and catalogue | owned | MediaCat | Curated Media is one catalogue and the current deployed implementation, not the product itself. |
| ASTV orchestration and selection | external | ASTV | ASTV performs lookup before selecting method and endpoint and owns fallback. |
| AdvMedia execution/profile processing | external | AdvMedia | AdvMedia consumes the selected source and does not acquire MediaCat ownership. |
| Home Assistant runtime and Media Source framework | external | Home Assistant | Runtime truth remains external to this repository. |
| Radio Browser Media Source provider | external | Radio Browser / Home Assistant integration | Curated Media may delegate an opaque URI once; it does not own the provider. |

## Approved architecture location

- Approved architecture location: `01_Architecture/MEDIACAT_ARCHITECTURE.md`
- Governed diagram: `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio`
- Architecture state: current approved
- Material DDRs: `DDR-001`

The Markdown file is the semantic architecture authority. The diagram is its
governed representation. Historical `schema-v2` / `resolve_item` material does
not define the current normalized architecture.

## Contracts provided

| Contract | Status/version | Authoritative provider-owned location | Consumers | Notes |
| --- | --- | --- | --- | --- |
| `MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | current deployed v1.0.0 | `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | ASTV; AdvMedia standalone gateway; AdvMedia core downstream | Normalized catalogue/item lookup and complete returned-record v1. |

The provider-owned file above is the sole operational authority. The former
shared Governance 1.2 copy under `Home_Assistant/contracts/` is retired and
non-authoritative; any temporarily retained recovery copy must not be used for
current work.

## Contracts consumed

None. MediaCat provides the normalized lookup contract and does not consume the
ASTV execution-dispatch, ASTV-AdvMedia, or AdvMedia standalone-gateway
interfaces. References to those external provider-owned contracts document
consumer topology without transferring ownership or creating a dependency on
their undocumented internals.

## Product dependencies

| Dependency | Type | Owner | Governed interface/evidence | Required state | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| Home Assistant | platform | Home Assistant | Current verified production evidence | Curated Media integration, action registration, and Media Source framework available | Integration setup, lookup, or Media Source operation stops at its documented boundary. |
| Curated Media catalogue data | data | MediaCat | `curated_media/catalogue.yaml` and normalized lookup contract | Catalogue loads as the supported immutable model | Setup fails explicitly; no partial normalized record is returned. |
| Delegated Home Assistant Media Source providers | external service | Respective provider owners | Opaque provider URI and current evidence | Selected provider can resolve its URI for Media Source playback | Provider failure surfaces without retry or another MediaCat route selection. |

ASTV and AdvMedia are governed consumers of MediaCat, not owners of MediaCat or
dependencies required to load its catalogue and lookup surface.

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `curated_media`

MediaCat owns the deployed `curated_media` Home Assistant integration domain,
service/action namespace, Media Source provider identity, catalogue identity,
and repository paths used by the current Curated Media implementation. This
implementation identity does not make Curated Media synonymous with the
MediaCat product and does not imply ownership of ASTV, AdvMedia, Home Assistant,
delegated providers, or execution endpoints.

| Identity | Classification | Owner | Permitted use | Evidence |
| --- | --- | --- | --- | --- |
| `curated_media`, `custom_components/curated_media`, `curated_media/catalogue.yaml` | owned | MediaCat | Current integration, catalogue, action, and Media Source implementation | Architecture and repository source |
| `curated_media.resolve_media_record` | owned | MediaCat | Governed normalized lookup | Provider-owned lookup contract |
| `curated_media.resolve_item` and schema-v2 branches | owned | MediaCat | Retained legacy/raw compatibility only; not the current cross-product interface | Architecture and historical evidence |
| `astv_` and `script.astv_*` | external | ASTV | Governed caller boundary only | ASTV-owned architecture and contracts |
| `advmedia_` and `script.advmedia_*` | external | AdvMedia | Governed caller/processing boundary only | AdvMedia-owned architecture and contracts |
| Home Assistant and delegated provider identities | external | Respective platform/provider owners | Configured platform use | Architecture and production evidence |

There is no separate current deployed `mediacat` Home Assistant domain.

## Production and evidence route

- Production route: MediaCat runs in the Home Assistant `starburst` instance as
  the Curated Media custom integration under
  `/config/custom_components/curated_media/` with its active catalogue at
  `/config/curated_media/catalogue.yaml`.
- Evidence route: sibling read-only evidence under
  `Production_ReadOnly/starburst/`, supplemented where authorized by verified
  live read-only Home Assistant inspection.
- Provenance and freshness requirement: verify source, capture time, procedure,
  included/excluded content, integrity, and freshness before relying on a
  snapshot. The retained static snapshot has no capture manifest, so its
  provenance, completeness, and freshness are not independently established.
- Secrets and mutable-state boundary: credentials, secrets, mutable Home
  Assistant state, and production snapshots remain outside this repository.
- Validation evidence route: Linear records governed work and validation;
  Git/GitHub records the exact candidate and accepted repository SHAs.
- Known limitations: live configuration search is partial for YAML-defined
  objects, and retained completed traces are finite evidence rather than a
  continuous monitor.

Current runtime-sensitive source remains at `custom_components/curated_media/`,
the active catalogue remains at `curated_media/catalogue.yaml`, and maintained
tests and fixtures remain under `tests/`. Their loading, discovery, and import
paths are not changed by this governance migration.
