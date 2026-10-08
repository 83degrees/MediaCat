# ASTV-328 MediaCat Administration Interface Conformance Review

## Review record

| Property | Value |
| --- | --- |
| Governing issue | `ASTV-328` |
| Review date | 2026-10-08 |
| Change class / workflow | `Change: Documentation`; `WF-02` |
| MediaCat state reviewed | `83degrees/MediaCat` `main` at `e9a00bce4edb7d418af3e08d58019435698abdf6` |
| MediaCat Manager state reviewed | `83degrees/MediaCat-Manager` `main` at `9711e760344517cd3af0d108933877120e28b04f` |
| Common standard | `PRODUCT_ADMINISTRATION_INTERFACE_STANDARD.md` v1.0.0 |
| Provider contract | `MEDIACAT_ADMIN_INTERFACE.md` v1.0.0 |
| Result | Pre-existing interface is compatible in design but does not yet satisfy or claim the complete mandatory conformance baseline. Additive remediation is required. |

This is an evidence-backed compatibility assessment. It does not modify the
MediaCat or MediaCat Manager runtime, redefine the provider-owned contract, or
transfer persistence ownership from MediaCat Manager to MediaCat.

## Authority and evidence

The review applies these authorities and current implementation sources:

- `AGENTS.md`, which routes work to Central Governance and the Project Profile.
- `00_Governance/01_Central/CENTRAL_GOVERNANCE.md` v11.14.0, especially
  Sections 2.5, 4-7, 10-17 and Appendices A, B and E. Linear is workflow truth;
  the provider-owned contract is interface truth; Git identifies exact states;
  a documentation-only assessment follows `WF-02` and must stop for human review.
- `00_Governance/PROJECT_PROFILE.md`, which assigns MediaCat ownership of the
  catalogue administration interface and assigns editing, local file writes,
  snapshots/history and Ingress UI to the separate MediaCat Manager product.
- `00_Governance/01_Central/01_Standards/PRODUCT_ADMINISTRATION_INTERFACE_STANDARD.md`
  v1.0.0 (the Standard), including its explicit Section 14.1 assessment of the
  pre-existing MediaCat interface.
- `03_Contracts/MEDIACAT_ADMIN_INTERFACE.md` v1.0.0 (the Contract), the sole
  provider-owned administration boundary.
- `01_Architecture/MEDIACAT_ARCHITECTURE.md` and
  `01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md`, including the
  schema-v4 validation rules and complete-registry failure boundary.
- `custom_components/mediacat/__init__.py`, especially `_registry`,
  `async_get_admin_capabilities`, `async_validate_catalogue`,
  `async_reload_catalogue`, and the four `hass.services.async_register` calls.
- `custom_components/mediacat/catalogue.py`, especially `CatalogueRegistry`,
  `_load_catalogue_text`, `_load_catalogue_directory`, and the immutable
  `MappingProxyType` construction.
- `custom_components/mediacat/services.yaml`, which publishes the three current
  administration actions as response-only Home Assistant services.
- The MediaCat Manager Project Profile and
  `01_Architecture/MEDIACAT_MANAGER_ARCHITECTURE.md` at the reviewed Manager
  state.
- MediaCat Manager implementation evidence in `app/admin_client.py`,
  `app/catalogues.py`, `app/storage.py`, and `app/main.py` below
  `04_Implementation/haos/source/apps/mediacat_manager/`.

The Standard is intentionally about external interoperability. Different
transport, code structure, storage and UI are permitted and are not gaps.

## Clause-by-clause conformance matrix

Assessment terms:

- **Conformant**: the current contract and implementation satisfy the clause.
- **Permitted variation**: implementation differs without violating a mandatory
  interoperability invariant.
- **Partial / gap**: useful current behavior exists, but the complete mandatory
  baseline is not exposed or documented.
- **Not applicable**: an optional capability is not advertised or the condition
  does not arise.

| Standard clause | Exact contract and implementation evidence | Assessment | Compatibility consequence |
| --- | --- | --- | --- |
| Section 2 — existing-interface adoption | The Contract is v1.0.0 from `ASTV-276` and predates the Standard. Standard 2 says a pre-existing interface is not silently redefined and cannot claim conformance until its provider contract exposes the mandatory baseline and common error mapping. Standard 14.1 names the MediaCat gaps. | **Conformant process; non-conformant claim state.** The current Contract does not claim full Standard conformance. | Adopt through additive fields/operations or a documented compatibility profile. Do not reinterpret existing fields or codes. |
| Section 3 — provider ownership and boundary | Project Profile and Contract assign schema meaning, validation and runtime activation to MediaCat. The Contract assigns editing, file writes, replacement, history and restoration to MediaCat Manager. Manager `admin_client.py` calls only the published `mediacat` actions. | **Conformant / permitted variation.** Separate Manager-owned persistence is intentional. | No ownership transfer or common manager is required. Consumers must continue to avoid MediaCat internals. |
| Section 4 — mandatory baseline | Contract publishes discovery, interface/schema versions, validation and activation. It lacks the complete structured outcome convention and normalized administration status required by Standard 4. | **Partial / gap.** | Full conformance cannot yet be claimed. |
| Section 5 — interface identity | `get_admin_capabilities` returns `admin_interface_version: 1`; `async_get_admin_capabilities` implements that field. No provider-unique `interface_id` is returned. | **Gap.** Version exists, but identity is implicit in the Home Assistant domain/action names rather than explicitly discovered. | Add a stable `interface_id` without removing `admin_interface_version`. |
| Section 5 — operation/capability discovery | Contract and code return `validation_supported: true` and `transactional_reload_supported: true`; `services.yaml` publishes the concrete actions. There is no general stable operation identifier list, and the response does not explicitly classify the interface as read-only versus managed mutation/activation. | **Partial / gap.** | Add stable capability/operation identifiers and an explicit management/activation mode. Preserve the two booleans for current consumers. |
| Section 5 — independent versions | Contract Common rules separate `admin_interface_version`, stored `catalogue_schema_version` and lookup `returned_record_version`. Capabilities expose interface major 1 plus current/supported schema version 4. `catalogue.py` independently defines `CURRENT_CATALOGUE_SCHEMA_VERSION = 4`. | **Conformant in principle.** | Additive normalized names may alias existing identities; no major version increase is required. |
| Section 5 — revision identity | Neither Contract nor `async_get_admin_capabilities` exposes persisted or active revisions. `CatalogueRegistry` is immutable but has no external state identity. | **Gap where Standard status/concurrency applies.** | Introduce opaque persisted and active identities. Do not reuse interface or schema versions as revisions. |
| Section 6 — successful outcomes | Validation uses `valid: true/false`; reload uses `reloaded: true/false`; both return `errors: []` on success. These are clear provider-owned equivalents for current clients, but there is no documented common `ok` equivalence for every operation, including discovery/status. | **Partial / gap.** | Add an `ok`-equivalent field or document deterministic equivalence while retaining `valid` and `reloaded`. |
| Section 6 — stable errors | Validation returns `invalid_catalogue`; reload returns `reload_failed`. `__init__.py` emits those exact codes. Input-schema rejection and unavailable runtime state can also escape through Home Assistant service/transport errors rather than a common structured envelope. | **Gap.** Current stable codes lack a documented common-category mapping. | Preserve `invalid_catalogue` and `reload_failed`; add/map common categories such as `invalid_request`, `dependency_unavailable`, and `activation_failed`. Existing consumers must not be forced to switch codes. |
| Section 6 — no partial success | Rejected validation omits summary fields. `_load_catalogue_directory` constructs a complete candidate or raises. Reload publishes the new registry only after complete discovery/validation. | **Conformant.** | Preserve these guarantees. |
| Section 7 — provider availability/status | Capability discovery succeeds only while `_registry(hass)` can obtain the active registry. There is no normalized `available` status or last material activation failure. | **Gap.** | Add administration status that can describe unavailable persisted state, invalid candidate state and retained active state without collapsing them. |
| Section 7 — persisted versus active | Capabilities return only `active_catalogue_ids`. Manager `_save` and `_restore` atomically replace a file before calling reload; on reload failure they return `saved/restored: true` with `runtime_active: false`, while MediaCat retains the prior registry. No shared persisted/active revisions or activation-required indicator exist. | **Gap, with compatible underlying behavior.** | A status/revision design must span the provider boundary truthfully while leaving filesystem/history ownership with Manager. |
| Section 8 — read/manage authorization | Contract says actions expose no secrets or caller-selected paths. MediaCat registers discovery, validation and reload as ordinary response-only Home Assistant services with no explicit provider-side read/manage authorization check. Manager uses `SUPERVISOR_TOKEN`; its UI is protected by Home Assistant Ingress, but that is consumer/platform authentication rather than a documented MediaCat authorization split. | **Gap requiring platform-specific design.** | Define and enforce read versus manage authority at the MediaCat boundary where Home Assistant permits. Map denial to `permission_denied`. Do not rely on Manager UI authentication as the sole enforcement point. |
| Section 9 — side-effect-free validation | Contract states validation does not write, inspect a caller path, alter active state or test liveness. `async_validate_catalogue` calls `_load_catalogue_text` on supplied content and only returns a summary/error. | **Conformant.** | No change required. |
| Section 9 — optional mutation and concurrency | MediaCat advertises no CRUD/persistence operation. Standard 9 explicitly permits an external provider-owned client to manage storage. Manager serializes in-process mutation with `RLock`, snapshots the current file and uses same-directory `os.replace`, but it has no opaque expected-revision guard against another writer. | **Permitted variation for MediaCat; follow-up risk for the combined management path.** | Do not add MediaCat CRUD merely for uniformity. A remediation design should decide whether Manager save/restore needs a persisted expected revision to prevent cross-writer lost updates. |
| Section 10 — save versus activation | Manager `_save` validates, snapshots, atomically replaces, then calls reload. It reports `runtime_active` from `reloaded`. The architecture explicitly says reload failure leaves the new file and history evidence while MediaCat retains the previous in-memory registry. | **Behaviorally conformant.** Save is not represented as activation. | Standardized status/revisions are still required so a separate consumer can discover the pending activation state later. |
| Section 10 — atomic activation and retained state | Contract promises complete-registry replacement; `async_reload_catalogue` loads the complete directory under a reload lock and assigns `DATA_CATALOGUES` only on success. Failure returns the prior active catalogue IDs. Registry/catalogues are recursively immutable. | **Conformant.** | Preserve transaction and retained-active-state guarantees. Map reload failure compatibly to `activation_failed`. |
| Section 10 — restoration ownership | Contract says reload does not roll back external writes and Manager owns snapshots/restoration. Manager `snapshot_catalogue` keeps bounded history and restore repeats validation, replacement and reload. | **Conformant / permitted variation.** | No provider-owned backup feature is required. |
| Section 11 — cross-product references | Schema architecture validates catalogue-internal category/item references and structurally validates external source identities/URIs. It explicitly does not test external liveness. MediaCat stores no reverse-reference state in ASTV, AdvMedia or external providers and advertises no cross-product query. | **Conformant; optional query not applicable.** | No reverse-state or mandatory cross-product query should be added. |
| Section 12 — optional-provider failure isolation | Project Profile states ASTV and AdvMedia are consumers, not MediaCat load dependencies. Validation does not dereference external URLs/providers. Manager architecture keeps its shell reachable but prevents writes if the MediaCat admin provider is unavailable. | **Conformant.** | If a future optional dependency blocks an operation, expose `dependency_unavailable`; do not delete stored references. |
| Section 13 — backward-compatible evolution | Contract explicitly permits additive response fields and requires consumers to ignore unknown fields. Manager reads named fields with `.get`, returns the full capabilities response, and requires interface major 1/schema 4 plus the two required booleans. | **Conformant adoption route.** | Additive discovery, status and error detail can remain interface major 1. Removing/renaming existing fields/codes or weakening atomicity would require a new major and coordinated consumer work. |
| Section 15 — conformance record | Project Profile records the current provider contract but the Contract does not identify a Standard conformance profile. | **Gap.** | After implementation and consumer validation, update the provider Contract/Profile to state the supported conformance profile and interface version. |

## Findings

### Genuine gaps

The current interface must not claim full Product Administration Interface
Standard v1.0.0 conformance because it lacks:

1. an explicit provider-unique interface identity;
2. stable general operation/capability identifiers and explicit
   read-only/manage/activation classification;
3. a documented common success/error mapping across all administration
   operations and transport-level failures;
4. normalized administration status, including provider availability,
   persisted versus active state, activation-required state, opaque revisions
   and the last relevant activation failure;
5. a documented and enforced read-versus-manage authorization boundary; and
6. a provider-contract conformance profile that identifies how the mandatory
   Standard fields and common error categories are exposed.

The combined MediaCat/Manager management path also has no cross-writer expected
revision. This is not a violation of an advertised MediaCat mutation operation,
because MediaCat advertises none, but it is a credible lost-update risk that the
remediation design must explicitly accept or close.

### Permitted independent implementation

The following are not gaps:

- Home Assistant response-only actions as the transport;
- MediaCat Manager as a separate product and UI;
- Manager-owned YAML persistence, atomic file replacement, bounded history and
  restore;
- MediaCat-owned schema validation and complete-registry activation;
- provider-specific `valid`, `reloaded`, `invalid_catalogue` and
  `reload_failed` fields/codes, provided compatible common mappings are added;
- omission of CRUD, staging and cross-product query operations when they are
  not advertised; and
- structural validation without external target liveness checks.

## Backward compatibility and consumer impact

### MediaCat provider

The gaps can be remediated additively within administration interface major 1:

- retain every current required field and its meaning;
- retain `validation_supported` and `transactional_reload_supported`;
- retain `valid`, `reloaded`, `errors[]`, `invalid_catalogue` and
  `reload_failed` for existing consumers;
- add normalized identity, capability, status, revision, outcome and common
  category fields;
- add a status operation, or extend discovery, without changing the behavior
  of validation or reload; and
- keep reload atomicity and prior-active-registry retention unchanged.

A major version would be required only if remediation removes/renames existing
fields or operations, changes their type/meaning, replaces stable codes without
a mapping, changes revision comparison semantics after publication, or weakens
the current transaction guarantees.

### MediaCat Manager consumer

MediaCat Manager currently requires interface major 1, schema 4, validation and
transactional reload. Additive fields are tolerated. It should be updated in
the remediation work to:

- negotiate using the normalized `interface_id`, interface major and advertised
  operation identifiers while retaining compatibility with the current v1
  profile during transition;
- consume normalized status and show saved-versus-active/pending activation
  explicitly after reload failure and on later bootstrap;
- branch on common categories while preserving provider-specific diagnostic
  detail;
- handle `permission_denied` and `dependency_unavailable` distinctly; and
- use an expected persisted revision for save/restore if the governed design
  selects guarded multi-writer behavior.

No ASTV or AdvMedia runtime change is required: they consume MediaCat lookup,
not this administration interface. Home Assistant service registration and
Manager authorization behavior require focused validation because those are
the actual enforcement and transport surfaces.

## Separately scoped remediation proposal

Create a new governed multi-repository issue after this review is accepted:

**Proposed title:** Adopt Product Administration Interface Standard v1 in
MediaCat administration and MediaCat Manager

**Proposed change classes:** `Change: Code`, `Change: Contract`, and, only if
approved responsibilities/boundaries change, `Change: Architecture`.
Because runtime code is involved, use `WF-01` and the governed `beta` route in
each affected product repository.

**Scope:**

1. Design and approve the additive major-1 conformance profile, including exact
   normalized discovery fields, capability identifiers, common error mapping,
   status/revision semantics and Home Assistant authorization model.
2. Implement the provider additions without changing existing v1 fields,
   validation semantics, persistence ownership or reload atomicity.
3. Update MediaCat Manager to negotiate the new profile, consume status/error
   fields and preserve compatibility with the existing v1 response during an
   agreed transition.
4. Decide and test the cross-writer concurrency policy. If guarded mutation is
   selected, define the opaque persisted revision and stale-write behavior
   before implementation.
5. Update the provider Contract, MediaCat and Manager architecture/profile
   artefacts only where their approved meaning changes.
6. Validate existing consumer behavior, authorization denial, invalid
   persisted candidate, retained active registry, reload failure, unavailable
   provider and successful activation against exact Beta candidates.

**Explicit non-scope:** common UI, shared database, MediaCat-owned file writes
or history, schema-v4 redesign, lookup-contract changes, ASTV/AdvMedia runtime
changes, and refactoring solely for visual or structural uniformity.

## Acceptance-criteria disposition

| ASTV-328 acceptance criterion | Result |
| --- | --- |
| Matrix cites exact contract and implementation evidence | Satisfied by the clause matrix and Authority and evidence section. |
| Genuine gaps distinguished from permitted independent implementation | Satisfied by the matrix and Findings section. |
| Required remediation issues and backward-compatibility impacts identified, or explicitly none | Satisfied by Backward compatibility and consumer impact plus the separately scoped remediation proposal. |
| Approved documentation and governance evidence captured | Satisfied by the review record, exact repository states and authority list. |

## Review conclusion

MediaCat's current administration design is compatible with the common
Standard's intended model: validation is side-effect free, persistence remains
separate, activation is complete-registry and atomic, failure retains the prior
active state, and optional products do not become runtime dependencies. The
interface is nevertheless only partially conformant because normalized
discovery, outcomes/errors, status/revisions and authorization are incomplete.

The correct next step is the separately governed, backward-compatible
remediation above. No runtime or provider-contract modification is authorized
or performed by `ASTV-328`.
