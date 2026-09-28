# PROJECT_PROFILE: MediaCat

## Profile conformance

This profile contains the required product-profile subjects and is current under
the approved Central Governance authority.

## Document status

- Governance state: current approved

## Product identity

- Product name: MediaCat
- Repository: `83degrees/MediaCat`
- DDR origin code: `03`

## Linear work routing

- Default Linear team: `ASTV`

## Purpose

MediaCat is the media-catalogue and route-registry product. It supplies
catalogue-scoped media identity, structure, membership, metadata, available
execution methods, route-specific source facts, and a normalized item lookup for
governed consumers.

## Scope

### In scope

- Media identity and catalogue-scoped item lookup.
- Catalogue structure, metadata, membership, and ordered catalogue content.
- Available execution methods and route-specific source facts for each item.
- The normalized complete returned record and its compatibility version.
- Supported local catalogue capability, validation and transactional reload services.
- The MediaCat Home Assistant integration, Curated Media catalogue, and Media
  Source surface.

### Out of scope

- ASTV request resolution, orchestration, method or route selection, endpoint
  selection, and fallback policy.
- AdvMedia source translation, endpoint/profile processing, playback-payload
  preparation, and execution implementation.
- ASTV-owned `assistant_command` construction or execution.
- Home Assistant, delegated Media Source providers, assistant platforms, or
  media-player ownership.
- Renaming logical `catalogue_id: curated_media` as part of the runtime
  namespace identity.

## Ownership and boundaries

| Boundary or capability | Relationship | Owner | Notes |
| --- | --- | --- | --- |
| Media identity, catalogue structure, metadata, membership, execution methods, and route-specific facts | owned | MediaCat | MediaCat reports all available methods and does not select one. |
| Normalized MediaCat item lookup and returned record | owned | MediaCat | Exact request, record, compatibility, and failure promises are defined by `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md`. |
| Catalogue capability, validation and transactional reload interface | owned | MediaCat | Exact administration promises are defined by `03_Contracts/MEDIACAT_ADMIN_INTERFACE.md`. |
| Catalogue editor, local file writes, snapshots/history and Ingress UI | external | MediaCat Manager | Separate governed admin/client product; consumes MediaCat's supported admin interface. |
| MediaCat integration and Curated Media catalogue | owned | MediaCat | `mediacat` is the runtime namespace; `curated_media` remains the separate logical catalogue ID. |
| ASTV orchestration and selection | external | ASTV | ASTV owns method/endpoint selection and fallback policy. |
| AdvMedia selected-method/profile processing | external | AdvMedia | AdvMedia operates on caller-selected context and does not acquire MediaCat ownership. |
| Home Assistant runtime and Media Source framework | external | Home Assistant | External platform boundary. |
| Delegated Home Assistant Media Source providers | external | Respective providers | MediaCat may delegate an opaque URI once; it does not own the provider. |

## Approved architecture authorities

| Scope | Authoritative location | State |
| --- | --- | --- |
| General MediaCat product and runtime architecture | `01_Architecture/MEDIACAT_ARCHITECTURE.md` | Current approved |
| Stored catalogue schema-v4 authoring, artwork-source resolution and preventative-validation architecture | `01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md` | Current approved |

- Governed diagram: `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio`
- Material DDRs: `DDR-03-001`; `DDR-03-002`; `DDR-03-003`

`MEDIACAT_ARCHITECTURE.md` owns general product responsibilities, runtime
boundaries, interfaces and current architectural meaning. The catalogue schema
architecture owns the schema-v4 stored YAML vocabulary, authoring semantics,
requiredness, preventative-validation rules, and schema evolution. The diagram
is the governed representation of the general architecture and does not replace
either prose authority.

Historical schema-v2, retired-action and retired-namespace material does not
define the current architecture.

## Contracts provided

| Contract | Status/version | Authoritative provider-owned location | Consumers | Notes |
| --- | --- | --- | --- | --- |
| `MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | current v2.2.0 | `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | ASTV; AdvMedia standalone gateway; AdvMedia core downstream | `mediacat.resolve_media_record` with returned-record version 1. |
| `MEDIACAT_ADMIN_INTERFACE.md` | current v1.0.0 | `03_Contracts/MEDIACAT_ADMIN_INTERFACE.md` | MediaCat Manager; operational callers | Capability discovery, side-effect-free validation and transactional complete-registry reload. |

The provider-owned file above is the sole operational interface authority.

## Contracts consumed

None.

MediaCat provides the normalized lookup contract. References to external
consumer-owned contracts document topology only and do not transfer ownership or
create a dependency on another product's undocumented internals.

## Product dependencies

| Dependency | Type | Owner | Governed interface/evidence | Required state | Failure boundary |
| --- | --- | --- | --- | --- | --- |
| Home Assistant | platform | Home Assistant | Current production evidence and runtime integration surface | MediaCat integration/action and Media Source framework available | Failure stops at the affected MediaCat integration/interface boundary. |
| Local catalogue files | data | MediaCat | `04_Source/config/mediacat/catalogues/`, schema architecture, lookup contract, and admin contract | At least one valid schema-v4 catalogue; unique in-file catalogue IDs | Setup fails explicitly; failed runtime reload retains the prior active registry. |
| Delegated Home Assistant Media Source providers | external service | Respective provider owners | Opaque provider URI and provider-owned Media Source interface | Selected provider can resolve its URI | Provider failure surfaces without MediaCat route fallback. |

ASTV and AdvMedia are governed consumers of MediaCat, not dependencies required
to load its catalogue and lookup surface.

## Implementation namespace / naming identity

- Implementation namespace / naming identity: `mediacat`

MediaCat owns the `mediacat` Home Assistant integration domain, action
namespace, Media Source identity, and configuration directory. It also owns the
separate logical `curated_media` catalogue identity.

| Identity | Classification | Owner | Permitted use | Evidence |
| --- | --- | --- | --- | --- |
| `mediacat` | owned | MediaCat | Integration, action, Media Source, and configuration-directory namespace | Architecture and DDR-03-002 |
| `mediacat.resolve_media_record` | owned | MediaCat | Sole normalized lookup producer | Provider-owned lookup contract |
| `catalogue_id: curated_media` | owned | MediaCat | Logical catalogue identity | Provider-owned lookup contract and catalogue source |
| `mediacat.resolve_item` | owned historical | MediaCat | Retired action retained only in historical/rollback evidence | Historical evidence |
| Schema-v2 package | owned historical | MediaCat | Read-only historical/rollback evidence; not accepted by maintained runtime | DDR-03-001 and historical evidence |
| `astv_` and `script.astv_*` | external | ASTV | Governed caller boundary only | ASTV-owned architecture/contracts |
| `advmedia_` and `script.advmedia_*` | external | AdvMedia | Governed caller/processing boundary only | AdvMedia-owned architecture/contracts |
| Home Assistant and delegated provider identities | external | Respective platform/provider owners | Configured external platform/provider use | Architecture and current evidence |

The retired `curated_media` runtime namespace remains historical only.

## Production and evidence route

- Maintained deployment route: Home Assistant `starburst`, using
  `/config/custom_components/mediacat/` and
  `/config/mediacat/catalogues/`.
- Current runtime namespace: `mediacat`.
- Production activation truth, including completion of the single-file to
  directory migration, comes only from approved current production evidence.
- Validation/workflow truth: Linear records governed work and validation;
  Git/GitHub records exact candidate and accepted repository states.
- Secrets, mutable Home Assistant state, and production snapshots remain outside
  this repository.

## Repository source baseline

The current MediaCat implementation baseline is under `04_Source/config/`.
Maintained tests and fixtures are under `05_Tests/`.
