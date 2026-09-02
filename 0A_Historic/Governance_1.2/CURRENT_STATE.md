# MediaCat Current State — Historical Governance 1.2 Restart Index

> Historical and non-authoritative: retained for migration, validation,
> rollback, and knowledge-recovery context. Current authority is defined by
> `CENTRAL_GOVERNANCE.md`, `PROJECT_PROFILE.md`, the current architecture,
> provider-owned contracts, product-owned DDRs, Linear, and Git/GitHub as
> applicable. Statements below record the pre-Governance-2.0-cutover view and
> must not govern current work.

## Metadata

- Project: MediaCat
- Document version: 1.2.0
- Updated (UTC): 2026-08-25
- Approved work instruction: `ASTV-67`
- Governance manifest: `00_Governance/projects/mediacat/manifest.json`
- Current architecture baseline: `ASTV-65`, retaining `ASTV-25` and `ASTV-26` as historical evidence

## Current baseline

MediaCat is the governed product concept for media identity, catalogue data,
metadata, membership, and available delivery-route facts. It is not a separately
deployed Home Assistant runtime or domain in the available evidence. Curated Media
is the current `curated_media` integration and one catalogue within MediaCat; the
two names are not interchangeable.

The current production flow uses the schema-v3 Curated Media catalogue and its
normalized item lookup. ASTV looks up one complete MediaCat record, selects one
execution method, and sends that selected context either through the Home
Assistant / AdvMedia path or the Google Assistant path. AdvMedia prepares the
Home Assistant playback payload, and ASTV performs the single terminal action.
The separate raw `curated_media.resolve_item` action remains available only as a
retained legacy interface.

The proposed model for future cross-catalogue route discovery is not implemented.

## Current schema-v3 data and normalized lookup

Linear issue `ASTV-56` created the 17-item schema-v3 Curated Media
catalogue at `MediaCat/curated_media/catalogue.yaml`. Focused non-live tests pass
against the source-controlled schema-v3 loader and normalized lookup, and the
separate schema-v2 rollback unit has been hash-checked and rehearsed in isolation.
The per-item migration matrix, hashes, test results, evidence limitations, and
rollback instructions are recorded under `MediaCat/evidence/astv-56/`.

`ASTV-65` deployed the complete artifact with the schema-v3 loader and
`curated_media.resolve_media_record`. Immediate live proof at
`2026-08-24T20:09:37.490Z` covered direct URL, Radio Browser, and assistant-command
records. The prepared schema-v2 restoration unit remains the atomic catalogue
rollback path during the retained rollback window.

## Current dual-schema Media Source support

Linear issue `ASTV-57` has added a separate schema-v3 branch to the
source-controlled Curated Media Home Assistant Media Source adapter while
retaining the complete schema-v2 branch. Non-live workspace tests pass for v2
regressions and the completed v3 catalogue's browse, search, direct-URL,
single-delegation, and recursion-boundary behaviour. The v3 `radio` category
keeps all 17 stored members while Media Browser exposes the 14 items with a
usable `execution_methods.ha_mplayer.source`.

`ASTV-65` installed this implementation with the schema-v3 catalogue. Live
backend proof found exactly 14 playable Radio items in stored order, excluded the
three assistant-command-only items, returned the expected 11 BBC search results,
and resolved all 14 playable items to final non-recursive URLs and MIME types.
The user separately confirmed the Media Browser UI smoke test.

## Source-of-truth references

- Governance 2.0 approved target deployment: `MediaCat/CENTRAL_GOVERNANCE.md`,
  `MediaCat/AGENTS.md`, and `MediaCat/PROJECT_PROFILE.md`. Governance 1.2 remains
  operational from `Home_Assistant/00_Governance/` until coordinated cutover.
- Current architecture: `MediaCat/01_Architecture/MEDIACAT_ARCHITECTURE.md`.
- Governed diagram: `MediaCat/01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio`.
- Material rationale: `MediaCat/02_Decisions/DDR-001.md`.
- Current operational contracts: shared Governance 1.2 copies under
  `Home_Assistant/contracts/`.
- Governance 2.0 target provider contract: `MediaCat/03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md`.
- Governance 2.0 external target references: the ASTV execution-dispatch
  contract under `ASTV/03_Contracts/` and the ASTV-AdvMedia and standalone
  gateway contracts under `AdvMedia/03_Contracts/`.
- Historical context: `MediaCat/00_PreProject_History/CONTEXT_HANDOVER.md`.
- Read-only evidence root: `Production_ReadOnly/starburst/`.

## Contract status

The MediaCat item-lookup contract is the current producer/consumer boundary for
the normalized record. ASTV-67 added the current AdvMedia standalone gateway as
a direct lookup consumer under its separate v2 gateway contract and retired the
legacy AdvMedia lookup wrapper. The ASTV execution-dispatch and ASTV-AdvMedia
contracts remain current at v2. Governance release 1.1.3 activates the resulting
four-contract central registry, including the standalone gateway entry. Future
route discovery or additional execution interfaces remain separate design work
and must not be invented from architecture discussion or historical notes.

## Evidence index

The following SHA-256 values were rechecked read-only on 2026-08-14. They identify
the static files used by the current architecture baseline; they do not establish
snapshot capture time, completeness, deployment, or runtime activation.

| Home_Assistant-relative path | SHA-256 |
| --- | --- |
| `Production_ReadOnly/starburst/custom_components/curated_media/__init__.py` | `a616d8b31da495b266e015efc8af68610cc9213ee373f27a3a653d63bb643c9e` |
| `Production_ReadOnly/starburst/custom_components/curated_media/const.py` | `3e98b96dbf37f330ae1faf58f3f39b22aaab51e3f054033be0aff9cfe5e1c278` |
| `Production_ReadOnly/starburst/custom_components/curated_media/catalogue.py` | `6eb7ef511483310afea4f9aa53a3546e72a419bd818654cf062dc5eedee5675b` |
| `Production_ReadOnly/starburst/custom_components/curated_media/resolver.py` | `667d2a8fc00e10d292ff235b0bed23f590bb5a9da56086022aef38c20113f0ac` |
| `Production_ReadOnly/starburst/custom_components/curated_media/media_source.py` | `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd` |
| `Production_ReadOnly/starburst/custom_components/curated_media/services.yaml` | `461c093b6bbd82acbffcf5f82bb1cd9462ef9ee0c138891d59850c93cba7e2f4` |
| `Production_ReadOnly/starburst/custom_components/curated_media/manifest.json` | `a9523e1ee385e6ebac055d82d9b169a92fb9a9b273323f6867f808eb9beca566` |
| `Production_ReadOnly/starburst/curated_media/catalogue.yaml` | `5fd55cd35b89b8d1958954173b49c94e3429130aff9766a767b4a223d28f02a8` |
| `Production_ReadOnly/starburst/scripts.yaml` | `f13c5bfaa7e895c1e8bde0202365ecdd31d00d806923f9ae5d2a19d42647277c` |
| `Production_ReadOnly/starburst/packages/astv/astv_scripts.yaml` | `5edb053f79fbd299730d45ac8ac7c29a84456af718159b18136ecd2a565ff5d9` |
| `Production_ReadOnly/starburst/assistive/astv_intent_catalogue.yaml` | `8b99b82a4d2e5c47f787a1393b844486086f726c12b4cefc9eb48b71181ecbd2` |
| `Production_ReadOnly/starburst/assistive/astv_area_endpoints2.yaml` | `34e3b8db445a522487d496fb89c51a5f88a38f485e0cada04c47c79218db369d` |

## Verified status

`ASTV-25` established the historical production baseline and `ASTV-26` produced
the original architecture. `ASTV-65` supplied fresher live evidence after the
coordinated cutover. At `2026-08-24T20:09:37.490Z`, normalized lookups, paused
AdvMedia health checks, seven sequential UID requests with audible confirmation,
Media Browser backend checks, and the user-confirmed UI smoke test all passed.
Relevant Home Assistant logs were clean.

## Known limitations and unresolved items

- The snapshot has no capture manifest, capture timestamp, Home Assistant
  version, `configuration.yaml`, `.storage`, runtime logs, or traces. Relevant
  modification times range from 2026-08-03 to 2026-08-12, but they are not
  provenance evidence.
- The snapshot remains historical static evidence. The scoped ASTV-65 live proof
  supplements it for current activation and the tested runtime paths; it is not a
  continuous monitor or a new complete production capture.
- Media-specific facts remain distributed across ASTV, AdvMedia, and Curated
  Media. No migration or ownership reclassification is authorised.
- Further route schemas, identifiers, and availability semantics remain future
  work outside the current normalized item-lookup contract.
- The optional `source.mime_type` compatibility risk remains separate work under
  `ASTV-27`; it is not a confirmed runtime defect from this static baseline.

## Next authorized step

Review and validate the Governance 2.0 target migration under `ASTV-102` before
merge or coordinated cutover. Any further architecture, contract, schema,
catalogue, or runtime change requires its own approved Linear work instruction
and proportionate validation. The user retains final acceptance.
