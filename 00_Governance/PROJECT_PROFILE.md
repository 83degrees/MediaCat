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
- The MediaCat Home Assistant integration, Curated Media catalogue, and Media
  Source surface.

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
| MediaCat integration and Curated Media catalogue | owned | MediaCat | `mediacat` is the runtime namespace; `curated_media` remains the separate logical catalogue ID. |
| ASTV orchestration and selection | external | ASTV | ASTV performs lookup before selecting method and endpoint and owns fallback. |
| AdvMedia execution/profile processing | external | AdvMedia | AdvMedia consumes the selected source and does not acquire MediaCat ownership. |
| Home Assistant runtime and Media Source framework | external | Home Assistant | Runtime truth remains external to this repository. |
| Radio Browser Media Source provider | external | Radio Browser / Home Assistant integration | MediaCat may delegate an opaque URI once; it does not own the provider. |

## Approved architecture authorities

| Scope | Authoritative location | State |
| --- | --- | --- |
| General MediaCat product and runtime architecture | `01_Architecture/MEDIACAT_ARCHITECTURE.md` | Current approved |
| Stored catalogue schema-v3 authoring and preventative-validation architecture | `01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md` | Current approved |

Detailed runtime enforcement of the schema-v3 architecture remains an
implementation concern. Any enforcement lag does not qualify the architecture's
current-approved authority.

- Governed diagram: `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio`
- Material DDRs: `DDR-03-001`; proposed `DDR-03-002`

`MEDIACAT_ARCHITECTURE.md` owns general product responsibilities, runtime
boundaries, flows, and current implementation state. The catalogue schema
architecture owns the schema-v3 stored YAML vocabulary, authoring semantics,
requiredness, preventative-validation rules, and schema evolution. The diagram
is the governed representation of the general architecture and does not replace
either prose authority. Historical `schema-v2` / `resolve_item` material does
not define the current normalized architecture.

## Contracts provided

| Contract | Status/version | Authoritative provider-owned location | Consumers | Notes |
| --- | --- | --- | --- | --- |
| `MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | current v2.1.0 | `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | ASTV; AdvMedia standalone gateway; AdvMedia core downstream | `mediacat.resolve_media_record` namespace with unchanged normalized returned-record v1. |

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
| Home Assistant | platform | Home Assistant | Current verified production evidence | MediaCat integration registration, action registration, and Media Source framework available | Integration setup, lookup, or Media Source operation stops at its documented boundary. |
| Curated Media catalogue data | data | MediaCat | `04_Source/config/mediacat/catalogue.yaml` and normalized lookup contract | Catalogue loads from the active `mediacat` path | Setup fails explicitly; no partial normalized record is returned. |
| Delegated Home Assistant Media Source providers | external service | Respective provider owners | Opaque provider URI and current evidence | Selected provider can resolve its URI for Media Source playback | Provider failure surfaces without retry or another MediaCat route selection. |

ASTV and AdvMedia are governed consumers of MediaCat, not owners of MediaCat or
dependencies required to load its catalogue and lookup surface.

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `mediacat`

MediaCat owns the `mediacat` Home Assistant integration domain, service/action
namespace, Media Source provider identity, and repository paths. It also owns
the separate logical `curated_media` catalogue identity. These identities do
not imply ownership of ASTV, AdvMedia, Home Assistant, delegated providers, or
execution endpoints.

| Identity | Classification | Owner | Permitted use | Evidence |
| --- | --- | --- | --- | --- |
| `mediacat` | owned | MediaCat | Integration, action, Media Source, and configuration-directory namespace | Architecture, DDR-03-002, and repository source |
| `mediacat.resolve_media_record` | owned | MediaCat | Sole normalized lookup producer namespace | Provider-owned lookup contract |
| `catalogue_id: curated_media` | owned | MediaCat | Logical catalogue identity; unchanged by the runtime namespace migration | Provider-owned lookup contract and catalogue source |
| `mediacat.resolve_item` and schema-v2 branches | owned compatibility | MediaCat | Retained raw/model compatibility; not the normalized cross-product interface | Architecture and historical evidence |
| `astv_` and `script.astv_*` | external | ASTV | Governed caller boundary only | ASTV-owned architecture and contracts |
| `advmedia_` and `script.advmedia_*` | external | AdvMedia | Governed caller/processing boundary only | AdvMedia-owned architecture and contracts |
| Home Assistant and delegated provider identities | external | Respective platform/provider owners | Configured platform use | Architecture and production evidence |

The retired `curated_media` runtime namespace remains only in historical and
rollback evidence. It is not a current implementation identity or deployment
source.

## Production and evidence route

- Current implemented production route: MediaCat runs in the Home Assistant
  `starburst` instance under `/config/custom_components/mediacat/` with its
  catalogue at `/config/mediacat/catalogue.yaml`; `mediacat` is the only active
  integration/action and Media Source namespace.
- Pre-retirement evidence: ASTV-221 established parallel `mediacat` and
  `curated_media` deployment; ASTV-223 and ASTV-224 then migrated and validated
  the active AdvMedia and ASTV consumers. ASTV-225 subsequently recorded the
  production-first removal of the legacy component, configuration entry, and
  catalogue path plus successful Home Assistant checks and representative ASTV
  and AdvMedia playback. The repository change under ASTV-225 aligns source and
  governed knowledge with that proven live state.
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
