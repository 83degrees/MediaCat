# ASTV-221 Cross-Product Namespace Impact Assessment

## Assessment record

- Assessment date: 2026-09-15
- Governing issue: `ASTV-221`
- Search terms: `curated_media`, `Curated Media`,
  `custom_components/curated_media`, `/config/curated_media`,
  `curated_media.*`, and `media-source://curated_media`
- Repositories/search roots: MediaCat, AdvMedia, ASTV, central Governance,
  and the retained `Production_ReadOnly/starburst` baseline
- Method: read-only `rg` scans of the available working checkouts, targeted
  inspection of authoritative architecture/contracts, and a live read-only
  Home Assistant configuration-body search
- Limitation: sibling repository checkouts and the retained production snapshot
  are evidence of the local states inspected, not proof of their latest remote
  commits. The retained production snapshot has no capture manifest. The live
  Home Assistant search was partial: four YAML automations and 31 YAML scripts
  were not exposed by per-object configuration endpoints.

Logical `catalogue_id: curated_media` occurrences are intentionally excluded
from required rename work unless the same line is also an integration-domain,
service, Media Source, or configuration-path reference. ASTV-221 explicitly
preserves the logical catalogue identifier.

## MediaCat

### References and classification

| Location | Classification | Finding and required change |
| --- | --- | --- |
| `04_Source/config/custom_components/curated_media/**` | Runtime-critical | Current legacy integration declares domain/path `curated_media` and user-facing name `Curated Media`. Retain unchanged during parallel migration. Add equivalent `custom_components/mediacat/**` with domain/path `mediacat` and name `MediaCat`. |
| `04_Source/config/curated_media/catalogue.yaml` | Deployment/configuration | Current catalogue path. Retain for rollback and add byte-identical `04_Source/config/mediacat/catalogue.yaml`. Keep `catalogue_id: curated_media`. |
| `05_Tests/test_*.py` and fixtures | Test-only | Existing suite imports and verifies the legacy implementation and catalogue identity. Retain legacy coverage; add explicit dual-domain identity, isolation, Media Source recursion, registration, and normalized-output parity coverage. |
| `00_Governance/PROJECT_PROFILE.md` | Authoritative product context | Previously declared only the current legacy namespace. Record `mediacat` as the approved target, `curated_media` as logical catalogue identity and temporary runtime compatibility, and distinguish current production evidence from the migration target. |
| `01_Architecture/MEDIACAT_ARCHITECTURE.md` | Authoritative architecture | Previously described only current legacy production. Add the approved parallel namespace architecture while preserving the verified legacy state as current implemented evidence. |
| `01_Architecture/Diagrams/MEDIACAT_ARCHITECTURE.drawio` | Governed diagram | Previously presented `curated_media` as the only current runtime. Update the existing topology minimally to show the approved `mediacat` target and explicitly state that the legacy domain remains parallel during migration. |
| `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | Provider-owned contract | Producer endpoint changes to `mediacat.resolve_media_record`; request/response semantics and returned-record version remain unchanged. Record the temporary legacy producer and proposed breaking namespace revision `2.0.0`. |
| `02_Decisions/DDR-03-001.md` | Historical accepted DDR | References the legacy schema-v2 action in its historical rationale. Preserve unchanged. |
| `0A_Historic/**` | Historical evidence | Preserve unchanged; these references identify actual past artefacts and rollback evidence. |

### Sequencing, validation, and rollback

MediaCat must deploy first, with both domains and catalogue paths present.
Source validation must prove distinct Home Assistant service, Media Source, and
`hass.data` namespaces and equivalent action results. Runtime validation must
then prove both integrations load and expose equivalent behaviour before any
consumer migrates. Rollback leaves consumers on or returns them to
`curated_media.*` while the legacy implementation and catalogue path remain.

## AdvMedia

### References and classification

| Location | Classification | Finding and required change |
| --- | --- | --- |
| `04_Source/config/packages/advmedia/advmedia_scripts.yaml:654` | Runtime-critical | Standalone gateway calls `curated_media.resolve_media_record`. Change to `mediacat.resolve_media_record` under `ASTV-223`; keep the request `catalogue_id` unchanged. |
| `05_Tests/test_advmedia_process_media_record.py` | Test-only | Harness registrations and assertions use the legacy action name, including lines 887 and 1011–1360. Update with the product implementation under `ASTV-223`. |
| `01_Architecture/ADVMEDIA_ARCHITECTURE.md` and `01_Architecture/Diagrams/ADVMEDIA_ARCHITECTURE.drawio` | Authoritative architecture/diagram | Current external MediaCat boundary names the legacy action. Update under `ASTV-223`. |
| `03_Contracts/ADVMEDIA_MEDIACAT_GATEWAY_INTERFACE.md` | Provider-owned consumer contract | Lines 52 and 112 name the legacy producer. Update its referenced producer namespace under `ASTV-223` without redefining the MediaCat returned record. |
| `0A_Historic/**` | Historical/rollback | Preserve legacy action and path references as evidence of the state they record. |

### Sequencing, validation, and rollback

Migrate only after parallel MediaCat deployment and parity proof. Run AdvMedia's
package/harness tests, deploy while both domains exist, then validate one lookup
and one core call with unchanged three-field gateway result. Rollback changes
the gateway action back to `curated_media.resolve_media_record`.

## ASTV / Assistive TV

### References and classification

| Location | Classification | Finding and required change |
| --- | --- | --- |
| `04_Source/config/packages/astv/astv_scripts.yaml:257` | Runtime-critical | Media intent engine calls `curated_media.resolve_media_record`. Change only the action domain under `ASTV-224`; retain `catalogue_id: curated_media` values in `04_Source/config/assistive/astv_intent_catalogue.yaml`. |
| `01_Architecture/ASTV_ARCHITECTURE.md:216` and `01_Architecture/Diagrams/ASTV_ARCHITECTURE.drawio:216` | Authoritative architecture/diagram | External MediaCat boundary names the legacy action. Update under `ASTV-224`. |
| `00_Governance/PROJECT_PROFILE.md:119` | Authoritative product context | Consumed namespace is recorded as `curated_media`; update the runtime namespace declaration under `ASTV-224` while retaining logical catalogue identity where documented. |
| Maintained ASTV tests/fixtures | Test-only | No additional active `curated_media.*` test invocation was found outside the package reference in the inspected checkout. Product validation must still exercise the changed media intent path. |
| `0A_Historic/**` | Historical | Preserve unchanged. |

### Sequencing, validation, and rollback

Migrate after parallel MediaCat deployment; it may proceed independently of
AdvMedia because the legacy domain remains available. Validate lookup before
method/endpoint selection and both ASTV execution paths. Rollback changes the
action domain back while preserving the same catalogue request values.

## Home Assistant production deployment target

### References and classification

| Location/evidence | Classification | Finding and required change |
| --- | --- | --- |
| `Production_ReadOnly/starburst/custom_components/curated_media/**` | Deployed integration baseline | Retained snapshot contains only the legacy component. Parallel deployment must add `custom_components/mediacat/**` without altering the snapshot. |
| `Production_ReadOnly/starburst/curated_media/catalogue.yaml` | Deployed catalogue baseline | Retained snapshot contains only the legacy catalogue path. Parallel deployment must add `/config/mediacat/catalogue.yaml` and retain the old path. |
| `Production_ReadOnly/starburst/scripts.yaml:756` | Active deployed consumer baseline | ASTV media intent engine calls the legacy action. Migrate through ASTV-224 after provider parity proof. |
| `Production_ReadOnly/starburst/scripts.yaml:1509` | Active deployed consumer baseline | AdvMedia standalone gateway calls the legacy action. Migrate through ASTV-223 after provider parity proof. |
| Live Home Assistant configuration-body search on 2026-09-15 | Current but partial read-only evidence | No exposed object matched `curated_media`; four YAML automations and 31 YAML scripts were unscannable, so this does not contradict the retained YAML references and does not prove absence. |

The baseline does not establish current configuration entries, include order,
startup logs, backup state, or deployed file hashes for a future candidate.
Before Beta, record a fresh backup/rollback point, install both directories and
catalogues, validate Home Assistant configuration/startup, verify both action
sets and Media Source roots, and compare representative direct URL, delegated
Media Source, and normalized lookup results. No separate product issue is
created for this deployment target.

## Central/shared Governance and contracts

No active `curated_media` runtime/domain reference was found in the inspected
central Governance repository outside product projections. Central Governance
controls and Standards do not require content change. The MediaCat
provider-owned contract changes in this issue; AdvMedia and ASTV
provider/consumer authorities change under ASTV-223 and ASTV-224. Any external
contract registry entry must be checked during cutover because the proposed
provider endpoint and contract version change, even though no matching legacy
domain text was found in the inspected Governance checkout.

## Tests, CI, fixtures, and deployment tooling

- MediaCat CI discovers `05_Tests/` through `pyproject.toml`; no workflow text
  contains the legacy domain. Add dual-run tests to the existing suite.
- MediaCat fixture `catalogue_id: curated_media` values remain correct.
- AdvMedia's maintained harness contains multiple action-name assertions and
  changes with ASTV-223.
- ASTV's maintained package is the direct test/validation target for ASTV-224.
- No active `08_Deployment/` namespace-specific tooling was present in the
  inspected MediaCat checkout. Production deployment therefore requires an
  explicit, evidenced copy/validation/rollback procedure at Beta rather than an
  inferred repository script.

## Additional consumers and issue routing

No additional product or repository with an active service, component,
catalogue-path, or Media Source dependency was found in the available search
roots. This is bounded by the checkout and live-search limitations above.

- MediaCat provider implementation and cross-product control: `ASTV-221`
- AdvMedia migration: `ASTV-223`
- ASTV migration: `ASTV-224`
- Home Assistant production baseline: deployment target/evidence source only;
  no separate product issue

## Retirement readiness and rollback gate

Do not remove `curated_media` until both consumer issues have completed their
runtime validation and a fresh active-reference scan finds no remaining
runtime/deployment dependency. Preserve the legacy component, catalogue path,
and an attributable pre-change backup until that gate passes. After removal,
validate `mediacat` startup, action registration, Media Source behaviour,
representative catalogue resolution, both consumer paths, and the absence of
legacy registration. Any failure before retirement returns the affected
consumer to the legacy action; any retirement failure restores the legacy
component/path/configuration from the recorded rollback state.
