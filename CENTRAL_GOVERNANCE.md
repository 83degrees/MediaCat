# Central Governance 2.0

## Status and transition boundary

This document defines the approved Governance 2.0 target rulebook. Governance
1.2 remains operational until the separately governed coordinated cutover.
Creating, reviewing, merging, tagging, or deploying files from this repository
does not by itself activate Governance 2.0 or retire any Governance 1.2
artefact.

During transition, Governance 1.2 material is read-only migration evidence.
Durable knowledge is translated into the Governance 2.0 authority model;
generated instructions, previews, fixtures, baselines, release tooling,
schemas, validation reports, overlays, and release metadata are not inherited
merely because they existed.

## Scope

This rulebook governs central change control and the shared authority boundaries
used by governed products. It does not define product-specific architecture,
implementation, contracts, production state, or diagram styling.

Tool access is capability, not authority. Work must remain within the explicit
scope of its Linear issue and the applicable subject authorities. A missing,
conflicting, or materially ambiguous rule does not grant permission to infer a
new one.

## Authority by subject

Each subject has one authoritative home. Supporting material may explain or
validate an authority but must not become a competing authority.

| Subject | Authority |
| --- | --- |
| Governance rules | `CENTRAL_GOVERNANCE.md` |
| Product identity, purpose, scope, boundaries, implementation namespace, and production/evidence route | Product `PROJECT_PROFILE.md` |
| Product architecture | Approved product `*_ARCHITECTURE.md` |
| Cross-product interface | Provider-owned contract under the provider's `03_Contracts/` |
| Material decision rationale | Product-owned DDR |
| Runtime truth | Current, verified production evidence |
| Work scope and state | Linear |
| Exact repository content and version | Git and GitHub |
| Diagram construction and shared presentation | `Standards/ARCHITECTURE_DIAGRAM_STANDARD.md` |

Git records what version exists; it does not replace semantic authorities.
Linear authorizes and tracks work; it does not override current technical truth
or silently amend governance, architecture, contracts, or DDRs.

When applicable authorities disagree, stop the affected work, identify the
conflict and owners, and record the state as unresolved. Do not resolve a
subject-authority conflict through chat history, working notes, convenience, or
an undocumented implementation.

## Required state language

Governed statements must use the following states deliberately:

| State | Meaning |
| --- | --- |
| Current implemented | Verified behaviour or content that exists now. |
| Current approved | The presently approved authority, whether or not every approved element is deployed. |
| Approved target | Approved future state that is not yet current implemented. |
| Proposed | A candidate that has not been approved. |
| Historical | Retained past context that is not current authority. |
| Unresolved | A material question or conflict awaiting an authoritative decision. |

Never describe approved target or proposed behaviour as current implemented.
Evidence limitations remain explicit and must not be converted into claims of
absence or certainty.

## Core working rules

Before changing a governed artefact:

1. retrieve the approved Linear issue and confirm its classification, scope,
   acceptance criteria, dependencies, and required validation;
2. inspect every applicable subject authority and relevant current evidence;
3. identify affected owners, providers, consumers, boundaries, and repositories;
4. expose conflicts, missing evidence, and material ambiguity rather than
   guessing; and
5. define validation proportionate to the change and its failure modes.

Make the smallest independently reviewable change. Preserve user-authored work
unless the approved issue explicitly supersedes it. Do not opportunistically
rename, move, reformat, relayout, refactor, or broaden unrelated material.

Chat, handovers, and historical notes preserve context but are not durable
authority. Approved knowledge belongs in the applicable product profile,
architecture, contract, DDR, governance rule, production evidence, Linear
record, or Git version.

Git diff and history are the normal technical change record. Do not create
per-file revision logs, before/after copies, `.old`, `.bak`, `.backup`, or other
recovery copies that merely duplicate Git. Governed evidence and DDRs remain
distinct records with distinct purposes.

## Product profiles

Every governed product must maintain a `PROJECT_PROFILE.md` based on
`Templates/PROJECT_PROFILE.template.md`. The profile is authoritative for:

- product name, purpose, and scope;
- ownership and explicit boundaries;
- the approved architecture location;
- contracts provided and consumed;
- product dependencies;
- implementation namespace and naming identity; and
- the production and evidence route.

Implementation namespace identifies ownership and legitimate reuse. A name,
prefix, integration domain, service name, package, or reused component must not
imply ownership that the product does not possess. The profile must distinguish
owned, consumed, shared, and external identities.

## Architecture governance

The approved product `*_ARCHITECTURE.md` is the semantic architecture authority.
It defines responsibilities, boundaries, major flows, interfaces, dependencies,
constraints, and applicable material decisions. It is not a scratchpad for
unlabelled ideas.

Before an architecture change, inspect current production evidence, applicable
contracts, the current approved architecture, materially applicable DDRs, and
relevant historical context. Classify the result using the required state
language. Do not invent architecture for implementation or diagramming
convenience.

Architecture diagrams represent the approved semantic architecture and must
conform to the Architecture Diagram Standard. A diagram does not become an
independent source of product architecture. Architecture correctness and
diagram-standard conformity are separate review checks; both must pass when a
diagram changes.

A product boundary, ownership, input, output, routing rule, external dependency,
or interface meaning may change only through explicitly classified and approved
architecture and/or contract work. Where material rationale must outlive the
change, the applicable DDR must also be current.

## Contract governance

The provider owns each authoritative cross-product contract under its product
`03_Contracts/`. Consumers declare consumed contracts in their
`PROJECT_PROFILE.md`. Do not create authoritative duplicate copies.

Dependencies must use governed interfaces, not undocumented provider internals.
Before changing a field, requiredness, meaning, routing behaviour, or failure
behaviour:

1. identify the authoritative provider and every known producer and consumer;
2. update the provider-owned contract through coordinated authorized work;
3. keep each affected product implementation separately authorized; and
4. validate compatibility and failure behaviour.

Caller capture names and returned field names are different concepts and must
not be normalized merely for consistency. A temporary interface exception
requires explicit human override and must be recorded with scope, owner,
expiry/review condition, and resolution route.

Known contract ownership for product migration is:

| Contract | Provider/owner |
| --- | --- |
| `ASTV_ADVMEDIA_INTERFACE.md` | AdvMedia |
| `ADVMEDIA_MEDIACAT_GATEWAY_INTERFACE.md` | AdvMedia |
| `MEDIACAT_ITEM_LOOKUP_INTERFACE.md` | MediaCat |
| `ASTV_EXECUTION_DISPATCH_INTERFACE.md` | ASTV |

## DDR governance

Create a DDR when material rationale, alternatives, or consequences must be
preserved. Architecture states approved product truth; a DDR records why a
material decision was made. Routine implementation, refactoring, wording, and
diagram layout do not normally require a DDR.

Use the global `DDR-###` sequence and record issued DDRs in `DDR_REGISTRY.md`.
Governance 2.0 has no reservation spreadsheet. Product-owned DDRs remain in the
product repository; the central registry points to them without duplicating
their authority.

Allowed statuses are `Proposed`, `Accepted`, and `Superseded`. An Accepted DDR
is substantively immutable. A later decision supersedes it through a new DDR;
historical rationale is not rewritten to fit a later model.

## Production and validation evidence

Production evidence establishes runtime truth and must remain read-only. Never
edit, rename, delete, reformat, regenerate, or use a production snapshot as a
working directory, and never sync local changes back to production.

Before relying on evidence, verify its capture time, source, procedure,
included and excluded areas, freshness, integrity, and material limitations.
Prefer authorized, verified read-only live evidence when freshness matters.
Missing or incomplete evidence is a limitation to record, not a fact to invent.

Credentials, secrets, mutable state, and bulk production snapshots do not
belong in governed repositories. Store only appropriate references, hashes,
provenance, and compact validation results.

Production evidence, Git state, and validation evidence are distinct. Final
validation must address the exact accepted or candidate SHA being reviewed. A
push proves remote presence only; it does not prove approval, validation,
deployment, activation, or completion.

## Linear and change classification

Linear is the work-control record. GitHub Issues must not become a parallel
product backlog. Classification is cumulative and is required before `Ready`:

- `Change: Code`
- `Change: Architecture`
- `Change: Contract`
- `Change: Governance`
- `Change: DDR`
- `Change: Documentation`
- `Change: Diagram`

The non-code workflow is:

`Backlog → Ready → In Progress → Ready for Review → Ready for Validation → Done`

Code work adds `Beta` before `Done`. `Blocked` and `Changes Requested` are also
available. `Done` represents final human acceptance after all cumulative gates
pass; an agent must not declare or perform that acceptance on the user's behalf.

An issue authorizes only its stated scope. Design agreement, conversational
approval, tool availability, an existing working context, or a status change
does not silently authorize additional implementation or production mutation.

## Git, PR, and repository protection

`main` is the accepted integrated development state; it is not necessarily a
stable release and does not by itself prove validation, deployment, activation,
or Linear completion.

The normal change unit is one independently reviewable Linear issue, one issue
branch, and one linked pull request in each changed repository. Substantive
governance, documentation, architecture, contract, and DDR changes normally use
PR review. Squash merge is the required normal merge method.

Direct changes to `main` require explicit human-approved exception. At least one
human approval is required before merge, and agents must not merge their own
PRs. Force-push or deletion of `main` is prohibited. Record the accepted merge
SHA. Any bypass requires explicit human authority.

Use platform branch protection or rulesets when the repository visibility and
GitHub plan support them. When technical enforcement is unavailable, the same
controls remain procedurally mandatory and the transition is not blocked. Do
not change repository visibility or GitHub plan merely to obtain enforcement
without separate authorization. Enable technical enforcement if it becomes
available later.

No automated status check is mandatory unless a product or later governance
decision explicitly defines it.

Version identifiers are:

- stable product/repository release: `vX.Y.Z`;
- central governance release: `governance-vX.Y.Z`;
- Architecture Diagram Standard release: `diagram-standard-vX.Y.Z`.

Beta uses the exact SHA and has no beta tag. Create stable, governance, and
standard tags only after the applicable human review, validation, merge, and
governed approval point.

## Central governance change and deployment

Central governance changes follow:

`Linear issue → governance branch → PR → human review → validation → squash merge → appropriate tag`

Every intentionally preserved durable rule must have a clear Governance 2.0
home. If a significant rule does not fit the approved authority model and would
require a new decision, stop and return it for human governance review.

Deploying exact approved central governance files into product repositories is
deployment, not reapproval. Product deployment occurs through separately
authorized migration/cutover work and must preserve exact version/SHA evidence.
No partial or implied deployment is operational authority.

An urgent restriction may narrow or pause existing authority while a formal
change is prepared; it must never grant new authority. Urgency does not remove
scope, human review, validation, evidence, or rollback duties unless an explicit
human-approved exception says exactly which control is overridden.

## Audit and knowledge retention

Audits are periodic backstops, not the primary authority mechanism. The Review
Log is authoritative for audit population and progress. `Reviewed` does not
mean `Archive Ready`.

Completed historical audit material does not need to be copied into a new
product `07_Audit/`. Substantive findings become normal classified Linear and
Git work. Migrate durable knowledge, not obsolete containers.

## Completion boundary

Work is ready for human review only when the authorized implementation is
complete, relevant validation has passed against the exact candidate state,
changed files and limitations are recorded, and no unrelated repository or
system state changed.

Governance 2.0 remains an approved target until the separately authorized T7/T8
coordinated cutover. No artefact in this repository may claim otherwise before
that cutover.
