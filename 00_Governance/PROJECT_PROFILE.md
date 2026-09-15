# PROJECT_PROFILE: MediaCat

## Profile conformance

This profile contains the required product-profile subjects and
is current under the approved Central Governance authority.

## Document status

- Governance state: current approved
- Exact migration baseline: `c1d5f5c7a895456b1f81f7a48d3ca2c8a65c407d`

## Product identity

- Product name: MediaCat
- Repository: `83degrees/MediaCat`
- DDR origin code: `03`

## Linear work routing

- Default Linear team: `ASTV`

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
- The MediaCat Home Assistant integration, catalogue, and Media Source surface,
  including the temporary legacy Curated Media compatibility deployment during
  the governed namespace migration.

### Out of scope

- ASTV request resolution, orchestration, method or route selection, endpoint
  selection, and fallback policy.
- AdvMedia source translation, endpoint/profile processing, playback-payload
  preparation, and execution implementation.
- ASTV-owned `assistant_command` construction or execution.
- Home Assistant, Radio Browser, Google Assistant, or media-player ownership.
- Renaming the logical `catalogue_id: curated_media` identity as part of the
  Home Assistant integration/domain migration.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| Media identity, catalogue structure, metadata, membership, routes, and route-specific facts | owned | MediaCat | MediaCat reports all available methods and does not select one. |
| Normalized MediaCat item lookup and returned record | owned | MediaCat | Exact request, record, compatibility, and failure promises are defined by `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md`. |
| MediaCat integration and Curated Media catalogue | owned | MediaCat | `mediacat` is the approved runtime namespace; `curated_media` remains the logical catalogue ID and a temporary legacy runtime namespace during migration. |
| ASTV orchestration and selection | external | ASTV | ASTV performs lookup before selecting method and endpoint and owns fallback. |
| AdvMedia execution/profile processing | external | AdvMedia | AdvMedia consumes the selected source and does not acquire MediaCat ownership. |
| Home Assistant runtime and Media Source framework | external | Home Assistant | Runtime truth remains external to this repository. |
| Radio Browser Media Source provider | external | Radio Browser / Home Assistant integration | MediaCat may delegate an opaque URI once; it does not own the provider. |

## Approved architecture location

- Approved architecture location: `01_Architecture/MEDIACAT_ARCHITECTURE.md`
- Governed diagram: `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio`
- Architecture state: current approved
- Material DDRs: `DDR-03-001`; proposed `DDR-03-002`

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
| Home Assistant | platform | Home Assistant | Current verified production evidence | MediaCat and temporary legacy Curated Media integration registration, action registration, and Media Source framework available during migration | Integration setup, lookup, or Media Source operation stops at its documented boundary. |
| Curated Media catalogue data | data | MediaCat | Repository implementation baseline under `04_Source/config/` and normalized lookup contract | Identical catalogue content loads from the active and temporary legacy paths during migration | Setup fails explicitly; no partial normalized record is returned. |
| Delegated Home Assistant Media Source providers | external service | Respective provider owners | Opaque provider URI and current evidence | Selected provider can resolve its URI for Media Source playback | Provider failure surfaces without retry or another MediaCat route selection. |

ASTV and AdvMedia are governed consumers of MediaCat, not owners of MediaCat or
dependencies required to load its catalogue and lookup surface.

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `mediacat`

MediaCat owns the approved `mediacat` Home Assistant integration domain,
service/action namespace, Media Source provider identity, and repository paths.
It also owns the separate logical `curated_media` catalogue identity. The
legacy `curated_media` runtime namespace remains temporarily owned and operated
only as migration compatibility. These identities do not imply ownership of
ASTV, AdvMedia, Home Assistant, delegated providers, or execution endpoints.

| Identity | Classification | Owner | Permitted use | Evidence |
| --- | --- | --- | --- | --- |
| `mediacat` | owned | MediaCat | Approved integration, action, Media Source, and configuration-directory namespace | Architecture, DDR-03-002, and repository source |
| `mediacat.resolve_media_record` | owned | MediaCat | Approved normalized lookup producer namespace | Provider-owned lookup contract |
| `catalogue_id: curated_media` | owned | MediaCat | Logical catalogue identity; unchanged by the runtime namespace migration | Provider-owned lookup contract and catalogue source |
| `curated_media` runtime namespace | owned legacy compatibility | MediaCat | Temporary parallel integration, action, Media Source, and configuration path until consumer migration and retirement readiness pass | ASTV-221 and DDR-03-002 |
| `curated_media.resolve_item` and schema-v2 branches | owned legacy compatibility | MediaCat | Retained raw compatibility; not the normalized cross-product interface | Architecture and historical evidence |
| `astv_` and `script.astv_*` | external | ASTV | Governed caller boundary only | ASTV-owned architecture and contracts |
| `advmedia_` and `script.advmedia_*` | external | AdvMedia | Governed caller/processing boundary only | AdvMedia-owned architecture and contracts |
| Home Assistant and delegated provider identities | external | Respective platform/provider owners | Configured platform use | Architecture and production evidence |

The `mediacat` domain is the approved target. Current production evidence still
shows only `curated_media`; parallel deployment and runtime proof remain WF-01
Beta obligations under ASTV-221.

## Production and evidence route

- Current implemented production route: MediaCat runs in the Home Assistant
  `starburst` instance as the legacy Curated Media custom integration under
  `/config/custom_components/curated_media/` with its catalogue at
  `/config/curated_media/catalogue.yaml`.
- Approved migration target: deploy `/config/custom_components/mediacat/` and
  `/config/mediacat/catalogue.yaml` in parallel, migrate consumers to
  `mediacat.*`, then retire the legacy paths only after readiness proof.
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

## Repository source baseline

The current MediaCat implementation baseline is held under `04_Source/config/`.
Maintained tests and fixtures remain under `05_Tests/`. Their Home Assistant
deployment paths and runtime behaviour are not changed by this repository-
structure migration.
