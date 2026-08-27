<!-- GENERATED FILE - DO NOT EDIT DIRECTLY.
Governance framework: 1.1.0
Model: baseline-design@1.0.0
Manifest: 00_Governance/projects/mediacat/manifest.json
Rendered payload SHA-256: 3f2ad914b32150a148ec84c9ed3fecaa599d1507c677714fb20f9f9111dfd041
Regenerate with: 00_Governance/tooling/Render-Governance.ps1
-->


# MediaCat Architecture Governance

These instructions apply within `MediaCat/01_Architecture/` and are self-contained;
they do not rely on Git-root instruction inheritance.

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/core/governance.md -->
## Shared governance

Read every applicable `AGENTS.md` before work. A nested file may add stricter
rules but must not silently weaken project-wide safety, architecture, contract,
or authorization controls.

Before changing anything:

1. identify the approved scope and exact files;
2. inspect the applicable sources of truth;
3. identify affected product owners, interfaces, and consumers;
4. expose conflicts, missing evidence, and material ambiguity instead of
   guessing; and
5. define proportionate validation.

User-authored edits are authoritative unless explicitly superseded. Make the
smallest scoped change. Do not opportunistically reformat, relayout, rename,
move, or refactor unrelated material.

Changes to component ownership, subsystem boundaries, inputs or outputs,
routing, external dependencies, or interface meaning are architecture or
contract changes and require explicit approval.

Chat history and historical handovers preserve context but are not the sole
durable record. Promote approved decisions to current architecture, contracts,
governance sources, or Linear as appropriate.

A task is complete only when implementation is in scope, relevant validation
passes, evidence and limitations are recorded, and no unrelated files or system
state changed.

## Governance change requests

When a governance rule appears missing, incorrect, incomplete, or unsuitable,
do not treat a generated `AGENTS.md` as authoritative or edit it directly. Pause
only the affected unsafe or ambiguous work when necessary, record and link a
Governance CR, and follow
`00_Governance/docs/GOVERNANCE_CHANGE_REQUESTS.md`. A temporary restriction may
narrow or pause authority; it must never grant new authority.
<!-- END GOVERNANCE SOURCE: 00_Governance/core/governance.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/core/source-of-truth.md -->
## Source of truth

When sources disagree, use this precedence:

1. current production evidence;
2. current explicit interface contracts;
3. current subsystem architecture documentation and authoritative diagrams;
4. applicable generated governance instructions;
5. project documentation and current-state summaries;
6. historical or pre-project context;
7. temporary working notes and chat history.

A Linear issue is the approved work instruction, not a source of technical
truth. If its scope or acceptance criteria conflict with a higher-precedence
source, stop and record the conflict rather than silently resolving it.

A copied production snapshot is read-only evidence and is authoritative only as
of its recorded capture. Check provenance, timestamp, completeness, exclusions,
and integrity hashes before relying on it. Prefer verified read-only live
evidence when freshness matters and access is authorized.

Current, approved target, proposed, exploratory, historical, and unresolved
states must be labelled distinctly. Never describe a proposed design as current
production behavior.
<!-- END GOVERNANCE SOURCE: 00_Governance/core/source-of-truth.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/models/baseline-design/1.0.0.md -->
## Governance model: baseline-design 1.0.0

This model governs discovery, evidence review, current-state documentation, and
design definition while significant ownership or interface questions remain.

- Prefer analysis and explicit uncertainty over speculative implementation.
- A Linear work instruction is required for changes to implementation,
  architecture, contracts, or production-related configuration.
- Design discussion alone does not authorize implementation.
- Keep current production behavior unchanged until a separate approved work
  instruction defines the change and its validation.
- Record new defects or improvements separately instead of folding them into the
  current task.

The user retains final acceptance. Codex must not move a task to `Done` without
explicit user instruction.
<!-- END GOVERNANCE SOURCE: 00_Governance/models/baseline-design/1.0.0.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/capabilities/architecture/1.0.0.md -->
## Architecture capability 1.0.0

Architecture documentation defines responsibilities, boundaries, major flows,
interfaces, decisions, and constraints. It is not a scratchpad for unlabeled
ideas.

Before an architecture change, read current production evidence, applicable
contracts, current architecture, project governance, and relevant historical
context. Classify the change as current-state correction, approved target
design, or exploratory proposal. Do not invent architecture for implementation
or diagramming convenience.

Written architecture and diagrams must agree. If they do not, identify the
conflict, resolve it against higher-precedence evidence, update only the
appropriate artifact, and leave remaining uncertainty explicit.

Show product boundaries, ownership, calls, return data, external systems, and
data sources clearly. Preserve established visual conventions and manual layout.
Architecture determines canvas size; canvas size never determines architecture.
<!-- END GOVERNANCE SOURCE: 00_Governance/capabilities/architecture/1.0.0.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/capabilities/contracts/1.0.0.md -->
## Contract capability 1.0.0

Cross-product interfaces are explicit contracts. A consumer must not depend on
another product's undocumented internals.

Do not rename, add, remove, normalize, reinterpret, or change the requiredness of
fields without reviewing the authoritative contract and every known producer and
consumer. A caller capture-variable name and a child return-field name are
different concepts and must not be made identical merely for consistency.

If a boundary change is required:

1. identify ownership and all known consumers;
2. update the shared contract first or as one coordinated change;
3. keep each product's implementation work separately authorized; and
4. validate compatibility and failure behavior.

Use the central contract registry to record ownership, producers, consumers,
status, version, and relative source path. Architecture may explain a boundary,
but the contract remains authoritative for its precise interface.
<!-- END GOVERNANCE SOURCE: 00_Governance/capabilities/contracts/1.0.0.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/capabilities/linear-workflow/1.0.0.md -->
## Linear workflow capability 1.0.0

All three products use the shared Linear team `astv` and the intentional shared
`ASTV-...` issue namespace.

Durable roles are separate:

- **Design task:** discusses requirements, inspects evidence read-only, develops
  design, and prepares or refines the work instruction. It stops after handing
  back the issue identifier.
- **Approved Linear work instruction:** carries scope, acceptance criteria,
  dependencies, and required validation. It does not override technical sources
  of truth.
- **Separate implementation task:** retrieves the issue, satisfies the selected
  model's pickup gate, implements only the approved scope, validates it, and
  records evidence.

Use the shared status meanings:

- `Ready`: approved and eligible for pickup where the model permits.
- `In Progress`: picked up by the implementation task.
- `Review / Test`: implementation and Codex validation complete; ready for user
  review or testing.
- `Done`: final user acceptance only.

Conversational phrases such as “agreed”, “continue”, “go ahead”, or “approved”
approve design or work definition only. They never bypass the Linear boundary.
<!-- END GOVERNANCE SOURCE: 00_Governance/capabilities/linear-workflow/1.0.0.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/capabilities/production-evidence/1.0.0.md -->
## Production evidence capability 1.0.0

Production evidence is held outside product repositories under
`Production_ReadOnly/` and must remain read-only. Never modify, rename, delete,
reformat, regenerate, or use it as a working directory. Never sync local changes
back to production.

Before relying on evidence, check its capture timestamp, source, procedure,
included and excluded areas, freshness, and hashes. If evidence is missing,
stale, incomplete, or ambiguous, say so and do not invent behavior. A missing
capture manifest is a limitation to fix in a future capture process, not by
retrospectively editing an existing snapshot.

Governance stores only metadata, SHA-256 hashes, relative references, and compact
validation notes. Credentials, secrets, mutable state, production snapshots, and
large rollback payloads remain outside future version-controlled governance.

Use the production-capture manifest and evidence-index schemas for new captures.
Record exactly what was inspected, what was verified, what remains unverified,
and whether any live read-only evidence supplemented the snapshot.
<!-- END GOVERNANCE SOURCE: 00_Governance/capabilities/production-evidence/1.0.0.md -->

<!-- BEGIN GOVERNANCE SOURCE: 00_Governance/projects/mediacat/architecture-overlay.md -->
## MediaCat architecture overlay

Document the current production interaction before target redesign. Keep current
production, approved target, and proposed/exploratory architecture visibly
distinct.

A logical media item may have several delivery methods such as tuner, provider,
stream, or future mechanisms. The current normalized record and consumer
interfaces are defined by the active contracts. Any different future route
schema, consumer boundary, or fallback behavior remains unresolved until
formally approved and contracted.

Current production uses the schema-v3
`curated_media.resolve_media_record(catalogue_id, item_id)` boundary. ASTV
performs one normalized lookup before method and endpoint selection. The direct
AdvMedia path receives the complete record and selected method without a second
lookup; the standalone AdvMedia gateway performs one lookup and one core call.
ASTV-owned `assistant_command` execution remains wholly inside ASTV. These
current paths are governed by the MediaCat lookup, ASTV execution,
ASTV-AdvMedia, and AdvMedia-MediaCat gateway contracts. Retained schema-v2
`resolve_item` topology and pre-contract descriptions are historical or
compatibility material, not the current normalized architecture.

Show product boundaries, calls, returns, and ownership without implying that
layout settles unresolved responsibility. Cite evidence, mark gaps, and do not
rename current production artifacts solely to align them with newer terminology.
<!-- END GOVERNANCE SOURCE: 00_Governance/projects/mediacat/architecture-overlay.md -->
