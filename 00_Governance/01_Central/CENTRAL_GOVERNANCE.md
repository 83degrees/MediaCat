# CENTRAL_GOVERNANCE.md

**Governance version:** 9.0.1
**Status:** Approved
**Approval tag:** `governance-v9.0.1`
**Approval date:** 2026-09-05

**Authority of appendices:**  
All appendices form an integral part of this governance book and carry the same authority as the main body unless an appendix explicitly states otherwise. Agents must apply applicable appendix requirements together with the relevant body sections and must not treat appendices as optional or supplementary guidance.

---

# Contents

## Part I — Governance Foundations

1. Objective  
2. Governance Model  
3. Standard Repository Model  

## Part II — Work Management and Execution

4. Linear as the Workflow Authority  
5. Change Classes  
6. Sub-Issues and Issue Decomposition  
7. Execution Routes  

## Part III — Durable Product Knowledge

8. Knowledge Retention  
9. Design Decision Records  
10. Contract Ownership and Compatibility  

## Part IV — Git, Review and Change Acceptance

11. Git Working Model and Linear Alignment  
12. Branch and Pull Request Rules  
13. Code Review  
14. Non-Code Review  

## Part V — Validation and Completion

15. Validation Model  
16. Validation Failure Handling  
17. Non-Code Completion  
18. Code Completion and Beta  

## Part VI — Stable Product Release

19. Stable Release  
20. Release Modes  

## Part VII — Assurance and Governance Operations

21. Audit Model  
22. Central Governance Change, Release and Distribution Lifecycle  
23. Validation Tooling Lifecycle  
24. Production Evidence Authority  
25. Agent Execution Efficiency  
26. Monitoring and Continuous Improvement  

## Appendices

- Appendix A — Authoritative Workflow Gate Matrix
- Appendix B — Authoritative Change-Class Control Matrix
- Appendix C — Governance Change Approval Checklist
- Appendix D — Historical provenance pointer — DDR Standard extraction (non-operative)
- Appendix E — Historical provenance pointer — Audit controls consolidation (non-operative)
- Appendix F — Monitoring Register
- Appendix G — Historical provenance pointer — Governance Distribution Standard extraction (non-operative)
- Appendix H — Authoritative Repository Structure and Artefact Placement

---

## Part I — Governance Foundations

### 1. Objective

Governance 2.0 provides the minimum effective controls needed to protect product integrity, architecture, contracts, durable decisions, recoverability and auditability, while making normal development and maintenance straightforward to execute.

The operating model favours:

- one authoritative source for each kind of truth;
- convention over repeated configuration;
- proportionate controls based on change type and risk;
- lightweight handling of non-code artefacts;
- Git-native history, provenance and rollback;
- clear human approval points;
- automation where it removes repetitive work;
- reuse of valid evidence rather than unnecessary revalidation;
- low execution, runtime and agent-context overhead.

Execution method is interchangeable.

Governance controls apply to the change and its risk, not to whether the work is performed by an agent or manually by the user.

The same required control gates therefore apply regardless of execution method, while the actor and mechanics used to perform the work may differ.

Governance must not become more burdensome than the risks it is intended to control.

#### 1.1 Governed Execution Path

For normal governed work, use the following navigation sequence to identify the applicable authority without treating this map as a separate source of control:

1. **Establish authority and product context** — use Sections 2–3 and the applicable Project Profile, architecture, contracts and evidence sources.
2. **Classify the work and select the workflow** — use Sections 4–5 together with Appendix A for workflow gates and Appendix B for change-class-specific controls.
3. **Define the executable scope and route** — use Sections 6–7 for issue decomposition and execution route.
4. **Identify durable product-knowledge obligations early** — use Sections 8–10 for architecture, DDR and contract obligations that may need to be satisfied during the same logical work.
5. **Execute through Git and human review** — use Sections 11–14 where the normal Git/review route applies.
6. **Validate and complete the issue** — use Sections 15–18, including any applicable durable-knowledge obligations identified above.
7. **Promote a stable product release only where separately applicable** — use Sections 19–20; stable release is not implied by issue completion.
8. **Apply assurance and Governance-operations controls where relevant** — use Sections 21–26 for audit, central Governance lifecycle/distribution, validation tooling, production evidence, execution efficiency and continuous improvement.

This routing map is navigation only. It does not create, weaken, duplicate or replace any requirement in the cited sections or appendices. Where a cited section or appendix applies, that source remains authoritative for the control itself.

---

### 2. Governance Model

#### 2.1 One Central Governance Book

There is one authoritative central governance book:

`CENTRAL_GOVERNANCE.md`

The central governance repository owns and approves this artefact.

Once approved, the exact approved file is deployed unchanged into each product repository as part of the centrally managed governance projection defined in Appendix H.2.

Product repositories must not locally modify the deployed central governance book.

Any change to central governance must first be made and approved in the central governance repository and then distributed as a new approved version.

There shall be:

- no project-specific rendering of the central governance book;
- no generated project governance book;
- no local tailoring of the deployed central governance copy;
- no duplicate substantive validation merely because the approved book has been distributed into another repository.

#### 2.2 Central Governance Repository

The central governance model is maintained in its own independent Git/GitHub repository.

Its authoritative central artefacts include:

- `/CENTRAL_GOVERNANCE.md`
- `/Standards/Product/ARCHITECTURE_DIAGRAM_STANDARD.md`
- `/Standards/Product/DDR_STANDARD.md`
- `/Standards/Product/PRODUCTION_EVIDENCE_STANDARD.md`
- `/Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md`
- `/Templates/PROJECT_PROFILE.template.md`
- `/Templates/DIAGRAM_CONVENTION_LEARNING.md`
- `/Templates/DDR.template.md`
- `/Templates/AUDIT_REVIEW_LOG.template.md`

Central governance artefacts required locally by product agents are deployed through the centrally managed governance projection defined in Appendix H.2.

The repository's `main` branch represents the accepted integrated governance state.

The central governance repository is not required to use the standard product-repository folder structure.

GitHub hosts the repository and may technically enforce branch, pull-request and merge controls.

`CENTRAL_GOVERNANCE.md` remains authoritative for what those controls mean and when they apply.

GitHub configuration does not replace or independently redefine central governance.

#### Centrally Governed Standards

Governance may define centrally governed standards for subjects that require specialised consistent rules but are expected to evolve as a distinct governed discipline.

A centrally governed standard:

- is authoritative within its defined scope;
- is maintained in the central Governance repository;
- has one fixed authoritative filename and path;
- must not contradict `CENTRAL_GOVERNANCE.md`; and
- follows the lifecycle and applicability rules defined in Section 22.14.

Centrally governed Standards have one of two applicability categories:

- **Product-applicable** — the Standard is required as product-local working authority and is projected unchanged to every product to which it applies;
- **Central-only** — the Standard governs central Governance operations only and is not part of the product projection unless its applicability is deliberately changed through governed work.

Repository structure makes applicability visible. Central-only Standards are stored under:

`/Standards/Central/`

Product-applicable Standards are stored under:

`/Standards/Product/`

The centrally governed standards are:

- `ARCHITECTURE_DIAGRAM_STANDARD.md`
  - applicability: Product-applicable
  - authoritative central path: `/Standards/Product/ARCHITECTURE_DIAGRAM_STANDARD.md`
  - deployed product path: `00_Governance/01_Central/01_Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`
- `DDR_STANDARD.md`
  - applicability: Product-applicable
  - authoritative central path: `/Standards/Product/DDR_STANDARD.md`
  - deployed product path: `00_Governance/01_Central/01_Standards/DDR_STANDARD.md`
- `PRODUCTION_EVIDENCE_STANDARD.md`
  - applicability: Product-applicable
  - authoritative central path: `/Standards/Product/PRODUCTION_EVIDENCE_STANDARD.md`
  - deployed product path: `00_Governance/01_Central/01_Standards/PRODUCTION_EVIDENCE_STANDARD.md`
- `GOVERNANCE_DISTRIBUTION_STANDARD.md`
  - applicability: Central-only
  - authoritative central path: `/Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md`
  - no deployed product path

Where `CENTRAL_GOVERNANCE.md` and a centrally governed standard conflict, `CENTRAL_GOVERNANCE.md` prevails and the conflict must be surfaced for resolution.

#### 2.3 Root `AGENTS.md`

Every product repository contains a small, stable root:

`AGENTS.md`

Its purpose is to direct the agent to applicable governance and project context.

It should principally instruct the agent to:

1. read `00_Governance/01_Central/CENTRAL_GOVERNANCE.md`;
2. read `00_Governance/PROJECT_PROFILE.md`;
3. apply both sources and the standard repository conventions when working in the repository.

When creating, editing or reviewing a governed architecture diagram, an agent must also read:

- `00_Governance/01_Central/01_Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`;
- the applicable approved architecture documentation; and
- where present, `01_Architecture/Diagrams/DIAGRAM_CONVENTION_LEARNING.md`.

When creating, editing, reviewing or superseding a DDR, an agent must also read:

- `00_Governance/01_Central/01_Standards/DDR_STANDARD.md`.

When creating a new DDR, the agent should use the centrally managed implementation aid:

- `00_Governance/01_Central/02_Templates/DDR.template.md`.

The deployed central paths identify the active centrally managed artefacts.

Agents must not select between historical or alternative central copies.

`DIAGRAM_CONVENTION_LEARNING.md` in `01_Architecture/Diagrams/` contains provisional product-local observations and working defaults. It is not governance, approved architecture or a product-specific override of the central standard.

The root `AGENTS.md` must not become an additional governance rulebook or a location for project-specific operating rules.

#### 2.4 Project Profile

Every product repository contains:

`00_Governance/PROJECT_PROFILE.md`

The Project Profile defines what the product is.

It contains at minimum:

- project name;
- DDR origin code;
- purpose;
- scope;
- explicit boundaries and out-of-scope responsibilities;
- authoritative architecture artefact;
- external contracts consumed;
- relevant external dependencies or evidence sources where necessary.

The DDR origin code is the product's immutable code used when allocating DDR identifiers. It identifies the product in which a DDR originates and does not represent current DDR ownership.

The Project Profile must not repeat common governance, workflow, validation, DDR, repository or operating rules already defined centrally.

Project-specific governance overrides are not permitted as standing rules.

If a project exposes a genuine need for a different rule, that need is raised through the governance-improvement process.

#### 2.4.1 Project Profile Change Classification

Changes to `PROJECT_PROFILE.md` are classified according to their semantic effect rather than through a dedicated profile change class.

Examples:

- a substantive change to product scope, responsibility or architectural boundary normally carries `Change: Architecture`;
- a correction or descriptive update that does not alter architecture or another governed authority may carry `Change: Documentation`;
- changing the declaration that a product consumes an existing external contract does not by itself mean the provider-owned contract has changed and therefore does not automatically require `Change: Contract`;
- other change classes apply only where their underlying governed subject is actually changed.

File location or filename does not override semantic classification.

#### 2.5 Authority by Subject

Different authoritative sources answer different questions.

| Subject | Authoritative source |
|---|---|
| Governance rules and operating model | `CENTRAL_GOVERNANCE.md` |
| Product identity, scope and declared external dependencies | `PROJECT_PROFILE.md` |
| Approved product architecture | Approved `*_ARCHITECTURE.md` |
| Architecture diagram construction and shared presentation conventions | `ARCHITECTURE_DIAGRAM_STANDARD.md` |
| DDR construction, numbering, status and supersession specification | `DDR_STANDARD.md` |
| Production-evidence acquisition, freshness, retention, integrity and reuse practice | `PRODUCTION_EVIDENCE_STANDARD.md` |
| Central Governance release/distribution protocol | `GOVERNANCE_DISTRIBUTION_STANDARD.md` |
| Cross-product interface | Provider-owned authoritative contract |
| Significant durable design rationale | Applicable DDR |
| Current implemented/runtime state | Approved current production evidence |
| Operational work state | Linear |
| Repository/version history and exact repository states | Git/GitHub |

These sources do not form a simple universal priority hierarchy.

For example:

- production evidence establishes what currently runs;
- architecture establishes what is approved;
- Git establishes exact repository history;
- Linear establishes operational workflow state.

Where relevant authoritative sources appear inconsistent, the discrepancy must be surfaced and resolved through the applicable governed workflow.

Agents must not silently choose one source and reinterpret another.

Approved `*_ARCHITECTURE.md` documentation remains authoritative for product architecture, architectural meaning, boundaries and product-specific semantics.

`ARCHITECTURE_DIAGRAM_STANDARD.md` governs common diagram representation. It does not define product architecture.

For diagram work, the authority order is:

1. `CENTRAL_GOVERNANCE.md`;
2. `ARCHITECTURE_DIAGRAM_STANDARD.md`;
3. applicable approved `*_ARCHITECTURE.md` and governed contracts;
4. `DIAGRAM_CONVENTION_LEARNING.md`;
5. incidental existing presentation where no higher authority defines the matter.

`DIAGRAM_CONVENTION_LEARNING.md` must never override a higher-authority source.

A convention recorded in the learning file may be used as a local working default only where it does not conflict with:

1. `CENTRAL_GOVERNANCE.md`;
2. `ARCHITECTURE_DIAGRAM_STANDARD.md`;
3. approved product architecture;
4. applicable contracts; or
5. an explicit user instruction.

Higher-authority sources always prevail.

#### 2.5.1 State Labelling

Where an authoritative artefact contains information representing different lifecycle states, those states must be clearly distinguishable.

In particular, distinguish where applicable:

- current implemented state;
- current approved architecture;
- approved target state;
- proposed or exploratory design;
- historical state;
- unresolved or uncertain state.

Proposed or exploratory design must not be described as current implementation or current approved architecture.

#### 2.6 Governance Improvement Feedback

Agents must monitor the operation of the governance model during normal work.

Governance-improvement observations and recommendations are advisory only. They do not become governance unless explicitly accepted by the user and incorporated into the applicable authoritative central Governance artefact through its defined approval lifecycle.

The constitutional feedback loop remains:

`observe → evidence → recommend → user review → applicable central change if accepted`

Detailed observation, recommendation, review and promotion mechanics are consolidated in Section 26.1.

#### 2.7 Project AAR Register

Each product repository maintains:

`00_Governance/AAR_REGISTER.md`

The register captures governance and operating-model observations arising from real project work.

It must not become:

- a product defect backlog;
- an execution log;
- a substitute for Linear;
- a repository for ordinary task notes.

AAR entries should contain at minimum:

- date;
- source issue/task;
- observation;
- practical impact;
- recommendation;
- status;
- central follow-up reference where applicable.

Statuses are:

- `Open`
- `Promoted`
- `Rejected`
- `Superseded`

Entries are append-only except for status and follow-up/reference fields.

Recurring review and promotion mechanics for open observations are defined in Section 26.2.

#### 2.8 In-Flight User Authority

The user remains the final authority over the project governance model.

The user may explicitly authorise an in-flight override for a specific work item.

An override may:

- resolve ambiguity;
- provide task-specific direction;
- authorise an exception to a normal governance rule;
- permit current work to proceed where strict application would otherwise block it.

Where an override is given, the agent must:

1. record the override and its scope against the current work item or PR;
2. proceed according to the authority provided;
3. not treat the override as a permanent rule;
4. not reuse it automatically on later work;
5. record an AAR observation where it exposes a recurring governance gap or defect.

An in-flight override changes authority for that work item only.

Only an accepted and formally incorporated central change alters governance for future work.

This authority remains subject to genuinely non-waivable external legal, safety or platform constraints.

---

### 3. Standard Repository Model

Every product repository follows the same centrally governed repository model unless central governance itself is changed.

Repository structure favours convention over configuration.

Agents should infer expected handling of an artefact substantially from its location.

Top-level folders should use meaningful subfolders where this improves organisation. Large flat collections of unrelated files should be avoided.

Detailed standard repository paths, folder purposes, placement rules and materialisation mechanics are defined in **Appendix H — Authoritative Repository Structure and Artefact Placement**. Appendix H is consulted when detailed placement is material; ordinary work need not load the full placement catalogue where the relevant existing location is already established.

#### 3.1 Central and Product Ownership Boundary

Everything under:

`00_Governance/01_Central/**`

is centrally managed content.

Product-local work must not create, edit, rename, move or delete anything within that subtree.

The central governance repository remains the source of truth for all content deployed into that subtree.

`PROJECT_PROFILE.md` and `AAR_REGISTER.md` are product-owned artefacts and remain outside the centrally managed subtree.

Templates within `01_Central/02_Templates/` are centrally managed implementation aids. Their presence in a product repository does not make them independent governance authorities.

`ARCHITECTURE_DIAGRAM_STANDARD.md`, `DDR_STANDARD.md` and `PRODUCTION_EVIDENCE_STANDARD.md` are exact deployed copies of their centrally approved standards and must not contain product-specific amendments.

Product-specific architectural meaning belongs in the applicable approved architecture documentation. Product-specific durable design rationale belongs in the applicable product DDRs. Product/environment evidence routes belong in the applicable Project Profile or environment authority.

Routine architecture, validation output, audit evidence or product work must not accumulate in `00_Governance/01_Central/`.

Repository location does not change the substantive authority relationships defined elsewhere in this Governance book. In particular, approved `*_ARCHITECTURE.md` remains authoritative for product architecture; diagrams support but do not replace that record; provider-owned contracts remain authoritative for their interfaces; centrally governed Standards retain only their defined scope; and centrally managed templates remain non-authoritative implementation aids.

#### 3.2 Repository Organisation Principle

New recurring top-level artefact classes are raised through the AAR/governance-improvement process rather than introduced independently by individual products.

The canonical top-level structure and detailed placement rules remain authoritative through Appendix H.

#### 3.3 Secrets and Credentials

Credentials, passwords, tokens, private keys and other secret runtime values must not be committed to governed repositories or deliberately retained in validation, audit or production-evidence artefacts.

Repository artefacts should reference the applicable external secret mechanism where required.

Authorised evidence capture must exclude secrets where reasonably possible.

If an accidental capture contains secret material, it must not be committed or retained as normal governed evidence.

Create a safe replacement capture rather than editing the unsafe capture into an apparently original state.

The immutability requirement for retained evidence applies once evidence has been accepted for retention; it does not require preservation of an unsafe accidental capture.

---

## Part II — Work Management and Execution

### 4. Linear as the Workflow Authority

Linear is the authoritative source for the operational state of work.

The workflow is actor-neutral.

Appendix A is authoritative for the gates that permit movement between workflow states.

#### 4.1 Workflow Profiles

A workflow profile defines the Linear workflow that an issue must follow.

Each governed change class has a default workflow profile defined in Section 5.1.

Two workflow profiles are currently defined:

| Workflow profile | Definition | Linear workflow |
|---|---|---|
| `WF-01` | Code workflow profile. Applies to issues whose selected workflow requires controlled progression through Beta before completion. | `Backlog → Ready → In Progress → Ready for Review → Ready for Validation → Beta → Done` |
| `WF-02` | Non-Code workflow profile. Applies to issues whose selected workflow does not require a Beta stage before completion. | `Backlog → Ready → In Progress → Ready for Review → Ready for Validation → Done` |

Two workflow profiles are currently defined because genuine product runtime implementation changes require a Beta stage before completion, while non-runtime and central Governance tooling changes do not solely by virtue of being executable.

The workflow-profile model is intentionally structured so that profile definitions, change-class mappings and precedence can be changed or extended later without redesigning the underlying change-class model.

Where a governed operational work item has no applicable change class, it follows workflow profile `WF-02`.

If an applicable change class is subsequently assigned, the workflow-profile selection rules in Section 5 apply from that point.

Appendix A is authoritative for the gates applicable to each workflow profile and the transitions those gates control.

#### 4.2 Backlog

`Backlog` means the issue is known but is not yet prepared for execution.

It may still require clarification, acceptance criteria, dependency identification, design decisions, change-class identification or prioritisation.

#### 4.3 Ready

`Ready` means the issue is sufficiently prepared to start without redesigning or materially reinterpreting the task.

An issue may enter `Ready` only when **Appendix A G0** is satisfied.

`Ready` means eligible for execution.

It does not itself trigger automatic delegation.

#### 4.4 In Progress

`In Progress` means work is actively being performed.

Manual and delegated work use the same state.

#### 4.5 Ready for Review

`Ready for Review` means:

- the proposed change is complete;
- the reviewable artefact or PR is available;
- substantive execution has paused;
- human review is required.

#### 4.6 Ready for Validation

`Ready for Validation` means:

- applicable human acceptance has been obtained and remains valid;
- accepted substance is ready for applicable validation;
- no further design/content review is expected unless the accepted substance changes;
- only applicable technical, runtime, integrity or evidence validation remains.

#### 4.7 Beta

`Beta` applies where the selected workflow profile requires a Beta stage.

It means:

- review is complete;
- applicable pre-beta validation has passed;
- the PR has been squash-merged to `main`;
- the exact resulting `main` commit SHA has been identified;
- the user has authorised beta deployment;
- that SHA has been deployed to `ha-starburst`;
- deployed state has been verified;
- real-world beta operation is underway.

#### 4.8 Done

`Done` means all completion requirements applicable to the issue have been satisfied against the final implemented state.

The applicable completion gate is defined in Appendix A.

Applicable change-class-specific completion controls are defined in Appendix B.

`Done` must not be treated as an implementation-complete, merge-complete or deployment-complete shortcut.

Stable release is separate from individual issue completion.

#### 4.9 Blocked

`Blocked` is an exception state.

It is used only where work genuinely cannot proceed because of an unresolved dependency, access problem, external constraint or required user decision.

An agent must not declare work blocked merely because the first tool or evidence route failed.

#### 4.10 Changes Requested

`Changes Requested` is a rework state.

Before a PR has been merged, the same issue, branch and PR should normally remain in use.

After a code PR has already been merged for beta, a beta failure remains on the same Linear issue but corrective implementation uses a new branch and PR from the current appropriate `main` state.

Where correction changes previously accepted content or behaviour, the work returns through human review.

Where correction is purely technical and leaves accepted substance unchanged, it may return directly to validation where Appendix A permits.

#### 4.11 Workflow Integrity

Linear status must reflect the real operational state.

Comments and narrative updates do not substitute for required state transitions.

GitHub may hold detailed implementation/review discussion, but Linear remains workflow authority.

A displayed `Done` state is not sufficient evidence of valid closure where the required closure evidence is absent or contradictory.

If an agent encounters an issue already marked `Done` without evidence that applicable review, validation, acceptance criteria, post-change revalidation and required human acceptance were satisfied, the agent must surface the inconsistency rather than treating the status alone as proof of completion.

#### 4.11.1 Post-Validation State Changes

If a merge, deployment, synchronization, environment update or other state-changing action occurs after validation, any acceptance criterion or validation conclusion affected by that action must be revalidated before closure.

Revalidation is proportionate to the changed state. Unaffected evidence may be reused where Section 15.4 and Appendix A.6 permit.

A state-changing action must not be treated as administrative merely because the substantive design was already accepted.

#### 4.12 Sole Work Tracker

Linear is the sole product and governance work tracker and workflow authority.

GitHub Issues or other repository issue trackers must not be introduced as a parallel backlog, work queue or workflow record.

This applies to:

- product changes;
- central governance changes;
- governed rollout work;
- releases where a tracked release issue is required;
- audit or assurance work requiring an operational work item.

GitHub remains the version-control and review surface for branches, commits, pull requests and release/version history.

GitHub Releases and pull requests are not alternative product work trackers.

---

### 5. Change Classes

Every governed change issue identifies the type or types of change using controlled Linear labels.

Change classes determine applicable change-class-specific controls and each change class defines a default workflow profile.

The selected workflow profile determines the workflow and applicable transition gates.

Change classes do not replace workflow state.

Operational activities such as a release or formal audit that do not themselves change governed product content are not required to invent an artificial change class.

Appendix A defines workflow transition gates and workflow-profile gate applicability.

Appendix B defines change-class-specific controls.

#### 5.1 Standard Change Classes

| Change class | Definition | Default workflow profile |
|---|---|---|
| `Change: Code` | Changes executable or deployable product implementation, including runtime-controlling configuration. | `WF-01` |
| `Change: Architecture` | Changes approved structure, responsibilities, boundaries, components, interactions or architectural behaviour. | `WF-02` |
| `Change: Contract` | Creates or changes an authoritative product-provided interface/contract, including inputs, outputs, schemas, guarantees or compatibility expectations. | `WF-02` |
| `Change: Governance` | Changes rules, controls, authority, repository conventions, workflow or governance process. | `WF-02` |
| `Change: Governance Tooling` | Changes executable automation, release/deployment tooling, validation tooling or workflow implementation whose governed purpose is to operate or assure the central Governance system and which is not deployable product runtime implementation. | `WF-02` |
| `Change: DDR` | Creates, updates or supersedes a Design Decision Record. | `WF-02` |
| `Change: Documentation` | Changes durable explanatory or operational documentation not governed as architecture, contract, governance, DDR or diagram. | `WF-02` |
| `Change: Diagram` | Creates or changes a governed diagram or visual architecture artefact. | `WF-02` |

A single issue or file may require multiple classes.

There is no generic `Mixed` class.

Executable central Governance tooling is not assigned `Change: Code` solely because it is executable. Where the same issue also changes genuine deployable product runtime implementation, both `Change: Governance Tooling` and `Change: Code` apply and Section 5.2 selects `WF-01`.

#### 5.2 Multiple Change Classes

Applicable controls are cumulative.

The issue satisfies controls required by every relevant change class unless a control is explicitly incompatible or inapplicable.

**Where any change class assigned to an issue has a default workflow profile of `WF-01`, then this workflow profile takes precedence over all other default workflow profiles, with the result that the issue must follow workflow profile `WF-01`.**

#### 5.3 Assignment

Change classes should be assigned before `Ready`.

If scope changes during execution, labels must be updated before the affected gate is reached.

Classes must not be omitted to avoid controls.

#### 5.4 Change-Class Simplicity

The set remains deliberately small.

New classes require a genuinely distinct control need and arise through central governance review informed by AAR evidence.

---

### 6. Sub-Issues and Issue Decomposition

A single Linear issue may contain multiple change classes where they form one cohesive logical change.

Work is not split merely because it affects different artefact classes.

#### 6.1 When to Use Sub-Issues

Use a sub-issue where part of the work:

- has distinct acceptance criteria;
- can be executed independently;
- requires materially different sequencing/dependencies;
- requires separate ownership/delegation;
- is independently reviewable;
- will likely complete at a different time;
- would otherwise make the parent difficult to control.

#### 6.2 Parent/Sub-Issue Relationship

The parent describes the overall outcome.

Each sub-issue defines its executable scope and change classes.

Dependencies are explicit where sequencing matters.

The parent completes only when sub-issues required for its outcome have completed.

#### 6.3 Cohesion Principle

Split by independent work outcome, not file type.

Issue decomposition should reduce complexity rather than create administration.

#### 6.4 Multi-Repository Work

A single cohesive Linear work item may affect more than one repository.

The issue must not be split merely because several repositories are affected.

Where the normal Git route applies:

- each changed repository normally has its own issue branch;
- each changed repository normally has its own linked PR;
- all repository changes remain traceable to the same governing Linear issue.

An explicitly approved lightweight exception may apply where permitted by Section 12.7.

All repository-specific obligations required for the outcome must be complete before the applicable issue gate is passed.

#### 6.5 Scoped Change Principle

Work only within the approved issue scope and make the smallest change reasonably required to satisfy it.

Do not opportunistically:

- reformat;
- relayout;
- rename;
- relocate;
- refactor;
- restructure;
- or otherwise modify unrelated material.

Newly discovered work outside scope should be recorded separately unless the user explicitly expands the current issue scope.

---

### 7. Execution Routes

Governed work may be performed manually or delegated.

Invocation determines how work starts, not how it is governed afterward.

All routes converge on the same applicable workflow, gates, evidence and completion rules.

`Ready` means eligible for execution; it is not itself an execution trigger.

Work starts only through an explicit user/manual instruction, an explicitly invoked supported delegation route, or an automatic delegation rule previously enabled by explicit user decision.

#### 7.1 Manual User Execution

The user may perform work directly.

Manual work is not required to imitate agent-specific mechanics that do not contribute to a control objective.

#### 7.2 Codex Desktop

The user may explicitly instruct Codex Desktop to pick up or resume a Linear issue.

The agent should establish current issue context, confirm repository/change classes, reflect `In Progress`, perform the work and update workflow state normally.

#### 7.3 Linear `@Codex`

The user may invoke Codex through the supported Linear/Codex route.

The same downstream governance applies.

#### 7.4 Future Automatic Delegation

The model supports future automatic delegation from qualifying states such as:

- `Ready`
- `Changes Requested`

Automatic delegation is disabled initially.

It may only be enabled by explicit user decision.

It must never bypass human approval or other governance gates.

#### 7.5 Rework and Resume

Before merge, rework normally resumes the same issue, branch and PR.

After a merged beta candidate fails, the same Linear issue continues but corrective Git work uses a new branch and PR.

#### 7.6 Execution-Route Neutrality

Equivalent risk receives equivalent governance regardless of actor.

Governance distinguishes the control that must be satisfied from the actor or mechanism used to satisfy it.

---

## Part III — Durable Product Knowledge

### 8. Knowledge Retention

Durable product knowledge is captured during normal work rather than reconstructed later.

#### 8.1 Completion Check

Before completion determine whether the change:

1. altered product architecture;
2. created, changed or superseded a decision meeting the DDR threshold;
3. created or changed a provider-owned contract;
4. changed another authoritative durable artefact.

Where yes, the corresponding authoritative artefact must be updated.

This is a lightweight completion check, not a broad documentation audit.

#### 8.2 Architecture

Known architectural changes update the authoritative `*_ARCHITECTURE.md` during the same logical work.

Architecture changes must be grounded in:

- the current authoritative architecture;
- materially applicable contracts;
- production evidence where current implementation state is relevant;
- materially applicable DDRs.

Historical context should be consulted only where materially necessary to understand or justify the change.

Architecture must not be invented or altered merely for implementation, documentation or diagramming convenience.

Where production evidence and approved architecture differ, the discrepancy must be surfaced and resolved rather than silently normalised.

#### 8.3 Decisions

Decisions meeting the DDR threshold are captured during normal work.

Audit-based DDR recovery is a backstop.

#### 8.4 Contracts

Provider-owned contract changes update the provider's authoritative contract during the same logical work.

Declared consumers are assessed for compatibility.

#### 8.5 Supporting Artefacts

Supporting durable artefacts are updated only where genuinely affected.

---

### 9. Design Decision Records

DDRs preserve significant durable design decisions and their rationale.

They do not record every implementation choice.

#### 9.1 Threshold

A DDR is normally required where a decision:

- establishes or materially changes architectural direction;
- chooses among meaningful alternatives with lasting consequences;
- establishes a future constraint;
- creates an important cross-product design principle;
- deliberately accepts a material trade-off;
- supersedes an earlier durable decision;
- would otherwise be difficult to reconstruct safely later.

A DDR is not normally required for routine implementation/configuration choices, obvious corrections or purely presentational decisions.

#### 9.2 Relationship to Architecture

Architecture states what is approved now.

A DDR explains why an important decision was made.

Current architecture must be understandable without reconstructing it from historical DDRs.

#### 9.3 Location and Ownership

Each DDR is owned by one product.

`Owner` means the product currently accountable for maintaining the DDR.

The authoritative DDR is stored in the current owning product's:

`02_Decisions/`

Detailed identifier, numbering, allocation and ownership mechanics are defined in the centrally governed `DDR_STANDARD.md`.

#### 9.4 DDR Standard and Template

Detailed mandatory DDR content, statuses, numbering, allocation, ownership, immutability and supersession mechanics are defined in:

`00_Governance/01_Central/01_Standards/DDR_STANDARD.md`

The central authoritative source is:

`/Standards/Product/DDR_STANDARD.md`

When a DDR is created, edited, reviewed or superseded, the applicable agent must apply the active DDR Standard together with this section and other applicable governance controls.

For a new DDR, the centrally managed implementation aid is:

`00_Governance/01_Central/02_Templates/DDR.template.md`

The template is non-authoritative and must not override either `CENTRAL_GOVERNANCE.md` or `DDR_STANDARD.md`.

#### 9.5 Recovered Decisions

A retrospective DDR may be created where audit discovers a missing durable decision and sufficient evidence remains.

This is recovery, not the preferred normal process.

---

### 10. Contract Ownership and Compatibility

Authoritative cross-product contracts are provider-owned.

Consumers do not maintain authoritative duplicates.

#### 10.1 Provider Authority

The provider stores the authoritative contract in its `03_Contracts/` area.

#### 10.2 Consumer Declaration

Consumers identify external contracts they consume in `PROJECT_PROFILE.md`.

#### 10.3 Contract Change Assessment

Before approving a provider-owned contract change:

1. identify all declared consumers;
2. assess the change as compatible or potentially breaking for each;
3. determine whether implementation/expectation is affected;
4. identify required consumer follow-up;
5. resolve material compatibility risk required for approval.

Full consumer testing is not automatic.

Validation depth is proportionate to actual contract delta and credible risk.

A provider-owned contract is not approved in isolation from its declared consumers.

#### 10.4 Cross-Product Dependency Boundary

Cross-product dependencies must use an explicit governed interface or contract.

A consumer must not depend on another product's undocumented internal implementation as though it were a supported interface.

This includes reliance on internal:

- entities;
- files;
- data structures;
- helper conventions;
- implementation details;
- runtime behaviour not represented by the governed interface.

Where an exceptional temporary dependency on an undocumented internal is genuinely necessary, it requires an explicit task-specific user override under Section 2.8.

Such an override:

- applies only to the stated work item;
- must be recorded;
- must not establish the internal as a supported interface;
- must trigger an AAR observation where the dependency is expected to persist or recur.

---

## Part IV — Git, Review and Change Acceptance

### 11. Git Working Model and Linear Alignment

Git records version history.

Linear records operational state.

The table below shows which Git concepts normally become relevant at each Linear state and where those concepts are defined.

| Linear state | Git/GitHub activity | Relevant definition |
|---|---|---|
| `Backlog` | Normally no Git activity | — |
| `Ready` | Normally no Git activity yet | — |
| `In Progress` | Create/use issue branch; make changes; commit; push as needed | 11.2 Branch, 11.3 Commit, 11.4 Push |
| `Ready for Review` | Branch pushed; linked PR open and reviewable | 11.4 Push, 11.5 Pull Request |
| `Changes Requested` — pre-merge | Continue same branch/PR; commit and push corrections | 11.2–11.6 |
| `Changes Requested` — after failed beta | Same Linear issue; create corrective branch/PR from appropriate `main` state | 11.1, 11.2, 11.5, 11.6 |
| `Ready for Validation` | Reviewed PR represents accepted proposed change; merge has not yet occurred | 11.5 Pull Request, 11.7 Merge |
| `Beta` | Applicable PR has been squash-merged; resulting `main` SHA is deployed to `ha-starburst` | 11.1 `main`, 11.7 Merge |
| `Done` | Required issue-level Git actions complete | 11.7 Merge |
| `Blocked` | Preserve current Git state for later resumption | 11.2 Branch, 11.3 Commit, 11.5 Pull Request |

The table is a workflow guide.

Sections 11.1–11.8 define the individual Git concepts.

#### 11.1 `main`

`main` represents accepted integrated development state.

It does not mean every commit has passed beta or is a stable release.

Stable SemVer tags identify proven stable states.

#### 11.2 Branch

A branch is a separate line of work for an issue.

Normal model:

`one independently reviewable Linear work item → one issue branch`

A corrective branch may be required after a previously merged beta candidate fails.

#### 11.3 Commit

A commit records an identifiable Git state.

Multiple commits may occur during implementation/rework.

A commit alone does not publish, request review, merge or release work.

#### 11.4 Push

Push sends commits to GitHub.

Implementation may contain multiple:

`change → commit → push`

cycles.

#### 11.5 Pull Request

A pull request proposes incorporation of a branch into `main`.

It provides the principal GitHub review surface and may contain:

- diffs;
- comments;
- requested changes;
- approvals;
- automated checks;
- merge history.

Opening a PR does not mean the change has been accepted or merged.

#### 11.6 Review Changes

Before merge, requested changes normally use the applicable Appendix A rework and review gates while continuing on the existing branch and PR.

After a merged beta candidate fails, the same Linear issue continues through the applicable Appendix A rework gates using a new corrective branch/PR.

The Linear issue remains the same unless the correction has become an independently governable piece of work requiring issue decomposition under Section 6.

#### 11.7 Merge

The standard merge method is:

**Squash merge**

The commits in an issue PR are incorporated into `main` as one resulting issue-level commit.

Where the applicable workflow profile requires Beta, squash merge occurs after review and applicable pre-Beta validation and before Beta deployment.

The resulting `main` SHA becomes the beta candidate.

Where the applicable workflow profile does not require Beta, merge normally occurs after review and applicable validation, immediately before `Done`.

#### 11.8 Tag and Release

A Git tag identifies an exact commit using a durable name.

Stable product releases use SemVer tags such as:

`v1.2.0`

Central governance approval uses a governance-specific approval tag such as:

`governance-v2.0.0`

Tags resolve to exact Git commits.

Beta uses exact commit SHAs and does not require a beta tag.

---

### 12. Branch and Pull Request Rules

Default:

`one independently reviewable Linear work item → one dedicated branch → one linked PR`

#### 12.1 Dedicated Work Branches

A branch normally remains associated with the issue through implementation, review, requested changes and validation until merge.

Long-lived branches containing unrelated issues should be avoided.

#### 12.2 Pull Requests

The PR should be linked to the Linear issue.

The relationship among issue, branch, proposed change, review and completion should remain clear.

#### 12.3 Rework Before Merge

Review or validation rework before merge normally continues on the same branch and PR.

#### 12.4 Rework After Merge

If a merged beta candidate fails, corrective work remains on the same Linear issue but uses a new corrective branch and PR.

The earlier merged PR remains immutable historical evidence of the failed beta candidate.

#### 12.5 Scope

Git structure follows work decomposition rather than repository folder or file type.

#### 12.6 Actor Neutrality

Manual and automated execution use the same Git traceability standard.

#### 12.7 Lightweight Non-Code Route

A clearly presentational/editorial non-code change may bypass the normal dedicated branch/PR route only with explicit user approval for that work item.

Eligibility requires that the change:

- does not alter substantive meaning, intent, behaviour, responsibility, boundary, interface, decision or governance rule;
- does not alter an authoritative position;
- does not create downstream compatibility/dependency impact;
- cannot reasonably alter runtime behaviour or governed interpretation;
- can confidently be assessed as presentational/editorial;
- retains sufficient traceability through Git history.

Examples may include:

- spelling/grammar;
- formatting;
- whitespace;
- alignment;
- non-semantic wording polish;
- diagram positioning where relationships and labels remain unchanged.

If reasonable interpretation could change, use the normal governed route.

The agent may recommend the lightweight route but may not self-authorise it.

Appendix A.4 defines its relationship to normal gates.

#### 12.8 Exceptional Direct Changes

Other direct changes to the protected target branch are not normal governed work.

A specific in-flight user override may authorise one, but it does not create a standing alternative workflow.

#### 12.9 Post-Merge Branch Cleanup

Issue branches are temporary work branches.

After a pull request is merged, its head branch is deleted automatically under the normal governed operating model.

Post-merge branch retention is outside the normal model.

At the time this rule was established, the governed repositories were private repositories using GitHub Free and protected branches/rulesets were not available as an operational mechanism for preserving a merged branch from automatic deletion.

If a future migration, release, rollback or other governed use case genuinely requires a branch to survive merge:

1. the need must be raised as separate governed work before merge;
2. the work must define an implementable technical retention control for the repository and GitHub plan then in force;
3. Linear or PR documentation alone must not be relied upon to preserve the branch;
4. the exception must be approved before the merge that would otherwise trigger deletion.

No branch may be deleted where unresolved, unmerged, review-active, rollback-required or otherwise explicitly retained governed work remains.

Squash-merge commit identity differences are not, by themselves, evidence that substantive branch content is missing from `main`; substantive content must be assessed where cleanup safety is in doubt.

---

### 13. Code Review

Code requires human review at the applicable Appendix A human-acceptance gate before validation may proceed.

GitHub is the detailed code-review surface.

Linear remains workflow authority.

#### 13.1 Entry

A code issue enters `Ready for Review` when:

- implementation is complete;
- branch is pushed;
- linked PR exists;
- change is meaningfully reviewable;
- substantive execution has paused.

#### 13.2 Human Review

The user may examine:

- diff;
- inline comments;
- questions;
- approval;
- requested changes.

Detailed review feedback remains attached to the PR rather than duplicated into Linear.

#### 13.3 Accepted Review

Acceptance satisfies the substantive human-review requirement for the applicable Appendix A gate.

It does not mean validation, Beta or stable release has completed.

#### 13.4 Changes Requested

Required changes proceed through the applicable Appendix A rework gate.

Before merge, the same issue/branch/PR normally continue.

#### 13.5 Review Authority

Human approval is initially mandatory for code.

Automated or agent review may support but not replace it unless central governance is later changed.

---

### 14. Non-Code Review

Non-code review is proportionate to artefact and risk.

It must not inherit code-review ceremony automatically.

#### 14.1 Entry

A non-code issue enters `Ready for Review` when:

- proposed change is meaningfully reviewable;
- artefact is available;
- applicable review surface exists;
- substantive execution has paused.

#### 14.2 Text-Based Artefacts

Architecture, contracts, DDRs, governance and durable documentation normally use a linked PR where the standard Git route applies.

Review establishes whether the artefact is acceptable in substance.

#### 14.3 Diagrams and Visual Artefacts

A textual or XML diff alone is insufficient where visual result matters.

The user must be able to review the final visual artefact.

Manual user edits during review may remain within the same issue/branch/PR.

A new issue is not required merely because the user performs final visual adjustment.

After visual acceptance, exact accepted state is used for final applicable integrity/provenance validation.

Earlier hashes or renders do not remain final evidence if the artefact changes afterward.

Governed architecture diagrams must be reviewed against the active `ARCHITECTURE_DIAGRAM_STANDARD.md` when Section 22.15 makes the current standard applicable to the diagram.

The canonical conformance trigger is therefore:

- a newly created governed architecture diagram;
- a substantive change in an area governed by the standard; or
- work explicitly brought into scope for a conformance update.

A purely presentational or editorial change does not by itself require previously grandfathered content elsewhere in the diagram to be brought into current-standard conformance.

Human visual review remains required where visual meaning matters.

Compliance with the diagram standard does not replace review of the product-specific architectural meaning represented by the diagram.

#### 14.4 Presentational Versus Substantive

A change is presentational only where it changes how information is displayed, not what it means.

Presentational examples include:

- layout;
- spacing;
- alignment;
- typography;
- annotation positioning;
- spelling/grammar;
- non-semantic polish;
- diagram object placement without semantic change.

A change is substantive where it can alter reasonable interpretation, including responsibilities, boundaries, contracts, governance, decisions, diagram relationships or meaning-bearing labels.

If reasonable interpretation could change, treat the change as substantive.

#### 14.5 Review Authority

Automation may assist but does not replace required human judgement over architecture, contracts, governance, durable decisions or final visual acceptance.

---

## Part V — Validation and Completion

### 15. Validation Model

Validation provides evidence that a governed change or repository state satisfies applicable controls.

It is proportionate to:

- change class;
- risk;
- affected dependencies;
- reusable evidence;
- exact state being assessed.

The default is not to run every available validator.

Appendix A is authoritative for workflow transition gates and workflow-profile gate applicability.

Appendix B is authoritative for change-class-specific controls.

#### 15.1 Universal Integrity and Selection

Every governed change receives one lightweight universal selection/integrity assessment.

Its purpose is to:

- confirm issue/change classification is sufficient;
- identify applicable class-specific and dependency-triggered controls;
- confirm exact state being assessed is identifiable;
- consider durable-knowledge obligations;
- detect obvious repository/change-integrity problems.

It is not a universal substantive validation suite.

#### 15.2 Change-Class-Specific Validation

Substantive validation is driven by applicable change class and identified risk.

A class does not inherit unrelated validation merely because another validator exists.

#### 15.3 Dependency-Triggered Validation

Validation follows the credible affected dependency chain only as far as impact can reasonably propagate.

Traversal requires a specific affected dependency or risk.

“Related to” is not sufficient justification.

Appendix A.5 defines the dependency stop rule.

#### 15.4 Reusable Evidence

Evidence may be reused where relevant immutable state remains unchanged.

Useful identifiers include:

- Git SHA;
- file hash;
- stable release tag.

Unchanged state should not be revalidated solely to reproduce the same evidence.

Appendix A.6 defines the evidence reuse rule.

#### 15.5 Final-Acceptance Validation

Where review can alter an artefact, final validation applies to the exact user-accepted state.

This is especially important for diagrams and manually adjusted governed artefacts.

Validation of a governed architecture diagram may include conformity with the active Architecture Diagram Standard.

Validation of the standard itself and validation of a product diagram are separate controls.

Deployment of a new Architecture Diagram Standard does not by itself require revalidation of unchanged product diagrams.

#### 15.6 Validation Selection

Before substantive validation determine:

1. applicable change classes;
2. universal integrity/selection result;
3. applicable class-specific checks;
4. material dependency impact;
5. reusable valid evidence;
6. need for final-acceptance validation.

Only the resulting set is executed.

#### 15.7 Validation Evidence

Retained evidence should identify:

- what was validated;
- control/risk addressed;
- exact state;
- result;
- reuse validity where relevant.

Routine output is not retained indefinitely merely because it exists.

#### 15.8 Merge Preservation

Where applicable validation is performed before a squash merge, the resulting merge commit may rely on that evidence where the governed content is demonstrably identical to the validated and accepted content.

A change in Git commit identity alone does not require substantive revalidation.

Where useful, post-merge integrity confirmation may establish preservation by comparing the relevant accepted content, file hash or equivalent immutable representation.

Prior validation evidence does not carry forward where the merge:

- changes the governed content;
- changes its effective meaning;
- introduces additional unvalidated content;
- otherwise means the merged state is no longer equivalent to the accepted validated state.

For artefacts requiring final-state validation, including visually accepted diagrams, the merged artefact must remain the exact accepted content even though its enclosing Git commit SHA may differ.

---

### 16. Validation Failure Handling

Validation failure is assessed according to what failed and what correction is required.

Rework follows the applicable Appendix A rework gate.

Whether repeated human review is required depends on whether the accepted substance has changed, as defined by Appendix A and the applicable change-class controls in Appendix B.

#### 16.1 Validation-Tool Failure

A broken validator or tool failure must be distinguished from an artefact/product failure.

Expected negative search results, no-match outcomes and runtime/tool errors are not automatically governed-change failures.

### 17. Non-Code Completion

Non-code completion follows the applicable workflow profile and transition gates defined in Appendix A.

Applicable change-class-specific completion controls are defined in Appendix B.

Sections 17.1–17.5 describe the operating model and evidence expectations for non-code completion; they do not independently authorise workflow transitions.

#### 17.1 Merge Timing

Normal non-code PR merge occurs after human acceptance and applicable validation, immediately before `Done`.

#### 17.2 Final Accepted State

The merged state must preserve the exact final accepted governed content.

Where applicable, final integrity/provenance evidence refers to that accepted content and its resulting repository state.

Section 15.8 governs preservation of pre-merge evidence across squash merge.

#### 17.3 Presentational Changes

Presentational work uses the lightest applicable path.

The lightweight Git route remains subject to explicit user approval under Section 12.7 and Appendix A.4.

#### 17.4 No Stable Release Requirement

Non-code issue completion does not by itself require a product stable-release step.

#### 17.5 Final Closure Evidence

Before a governed issue enters `Done`, closure evidence must record enough information to establish:

- the result of each acceptance criterion against the final implemented state;
- required review status;
- applicable validation result;
- any post-change revalidation performed;
- unresolved findings status;
- required human acceptance;
- completion of required post-merge, deployment, synchronization or environment-update work.

The authoritative issue closure record is maintained in Linear.

Supporting review, validation, Git, deployment or other evidence may remain in its authoritative native location and must be linked or referenced from the Linear closure record where required to establish closure.

Human acceptance and transition authority are governed by Appendix A.

Any separately required action-specific authorisation remains mandatory.

### 18. Code Completion and Beta

Code completion follows the applicable workflow profile and transition gates defined in Appendix A.

Where the selected workflow profile requires Beta, the code issue reaches `Done` only after applicable review, validation and successful Beta operation.

Stable release is separate.

Applicable change-class-specific controls are defined in Appendix B.

#### 18.1 Entry to Beta

Entry to `Beta` occurs only when the applicable Appendix A Beta-entry gate and Appendix B code controls have been satisfied.

The resulting deployed candidate state is the state against which Beta operation is assessed.

#### 18.2 Beta Candidate Integrity

Beta result applies only to the exact deployed runtime-affecting state represented by the candidate SHA.

A later runtime-affecting change does not inherit that result.

#### 18.3 Beta Operation

Beta testing focuses on behaviour and risks introduced by the change.

Duration and depth are proportionate to risk.

#### 18.4 Successful Beta

Successful Beta satisfies the Beta-operation requirement for completion.

Transition from `Beta` to `Done` is governed by the applicable Appendix A gate.

The implementation issue is complete when that gate is satisfied, but no stable product release is automatically created.

#### 18.5 Failed Beta

A failed Beta requires rework through the applicable Appendix A rework gate.

The failed candidate remains part of Git history.

Corrective implementation uses a new branch and PR under the same Linear issue unless issue decomposition is genuinely required.

`ha-starburst` may be rolled back to a selected stable tag with explicit user authorisation.

#### 18.6 Agent-Assisted Beta Deployment

Initial beta deployment is agent-assisted rather than fully automatic.

The agent performs deployment mechanics only after explicit user authorisation.

Deployment must:

- target a specific SHA;
- verify deployed state;
- preserve rollback capability.

#### 18.7 Failed-Beta `main` Protection

When a beta candidate fails, `main` contains a known failed runtime state until that failure is corrected or otherwise explicitly resolved.

During that period:

- new runtime-affecting changes must not merge to `main` unless the user explicitly authorises the exception;
- corrective work for the failed beta may proceed through the normal corrective branch/PR route;
- non-runtime-affecting changes may proceed only where they do not interfere with correction, rollback, evidence or traceability of the failed candidate.

The failed commit remains part of Git history.

Where appropriate, a deployed environment may be rolled back independently under the applicable user-authorised rollback process.

The failed-beta restriction ends only when either:

1. a corrective candidate successfully completes Beta; or
2. the user explicitly abandons or reverts the failed change and the affected repository/runtime state has been brought to an accepted known state.

Creating a corrective branch, opening a corrective PR, or merely identifying a proposed fix does not by itself resolve the failed-beta restriction.

Normal runtime-affecting merge activity resumes only after one of the resolution conditions above is satisfied.

---

## Part VI — Stable Product Release

### 19. Stable Release

A stable release promotes an integrated product state whose runtime-affecting content has valid beta/stable coverage into an explicitly versioned stable state.

It is product-level activity separate from individual issue completion.

#### 19.1 Stable Authority

Stable promotion requires explicit user authorisation.

Successful beta does not automatically create a release.

#### 19.2 Semantic Versioning

Stable releases use:

`vMAJOR.MINOR.PATCH`

| Version component | Use when |
|---|---|
| `MAJOR` | Breaking or deliberately incompatible product or consumer-facing contract change |
| `MINOR` | Backward-compatible new capability or materially expanded behaviour |
| `PATCH` | Backward-compatible fix, correction, documentation-only release, or internal change with no new external capability |

Version significance reflects released product behaviour/state, not implementation effort.

#### 19.3 Beta and Stable Coverage

A stable release SHA must have valid runtime coverage for all runtime-affecting content included in that release.

Runtime content already contained in an earlier stable release is considered to retain established runtime coverage while that content remains unchanged.

Runtime-affecting content introduced or altered after that established coverage must obtain applicable beta coverage before stable promotion.

The release SHA may therefore be:

- an exact successfully beta-tested SHA; or
- a later descendant where changes introduced after the applicable beta/stable coverage are demonstrably non-runtime-affecting and have passed their applicable controls.

Any runtime-affecting change introduced after the applicable beta result requires a new beta candidate.

A non-runtime-affecting change does not require Home Assistant redeployment merely to reproduce coverage for unchanged runtime content.

#### 19.4 Release Cut-Off

The selected stable SHA is the release cut-off.

Later commits on `main` are not part of that release.

#### 19.5 Stable Tag and GitHub Release

Every stable release receives:

- a SemVer Git tag;
- a corresponding GitHub Release.

Beta SHAs do not require GitHub Releases or beta tags.

The GitHub Release should concisely identify:

- version/tag;
- exact SHA;
- material changes;
- deployment considerations;
- known material limitations;
- previous stable rollback target.

#### 19.6 Agent-Assisted Stable Deployment

Initial stable deployment is agent-assisted and requires explicit user authorisation.

The agent deploys the exact tagged version to user-selected environments and verifies deployed state.

The model supports deployment to:

- `ha-starburst`;
- `ha-glenrosa`.

#### 19.7 Rollback

Rollback is agent-assisted and requires explicit user authorisation.

Each environment may be rolled back independently to a selected previous stable tag.

#### 19.8 Release Integrity

A stable release must remain traceable to:

- SemVer tag;
- exact released SHA;
- applicable beta/stable coverage;
- GitHub Release;
- deployment state;
- relevant supporting evidence.

---

### 20. Release Modes

Stable releases use either **Simple Release** or **Managed Release**.

#### 20.1 Simple Release

Simple Release is the default where:

- the intended stable SHA is known;
- all runtime-affecting content has valid beta/stable coverage;
- subsequent un-beta-tested changes, if any, are demonstrably non-runtime-affecting and have passed their applicable controls;
- promotion is straightforward;
- established agent-assisted deployment is sufficient;
- no unusual sequencing exists;
- no cross-product coordination exists;
- no migration/environment preparation is required;
- no material release-specific validation is required.

A separate Linear release issue is not required.

A Simple Release is a promotion action rather than a parallel backlog item.

Its durable release record is the Git tag and GitHub Release.

#### 20.2 Managed Release

Use a Managed Release where release activity itself requires material operational coordination, including:

- multiple coordinated products/releases;
- dependency-sensitive sequencing;
- migration/environment preparation;
- special release validation;
- special rollback preparation;
- several distinct execution steps requiring lifecycle tracking;
- explicit user decision that managed control is warranted.

A dedicated Linear work item manages the release.

#### 20.3 Escalation

A Simple Release may be converted to Managed if unexpected complexity appears.

#### 20.4 Release Completion

Release completion requires:

- explicit promotion;
- correct tag;
- GitHub Release;
- intended deployment completed;
- deployed state verified;
- applicable release checks passed;
- rollback target identified.

---

## Part VII — Assurance and Governance Operations

### 21. Audit Model

Audit is a periodic assurance backstop.

It does not replace normal knowledge capture.

#### 21.1 Scope and Bounded Execution

Each audit defines explicit scope and must not silently expand.

Where the size, risk or execution method of an engagement warrants it, the audit may define bounded execution controls appropriate to the engagement.

Examples include:

- maximum batch size;
- review checkpoints;
- pause-for-user-review or approval points;
- staged population release;
- other bounded execution controls.

These controls belong to the applicable audit work instruction or engagement definition rather than becoming permanent central values.

The applicable audit work instruction or engagement definition defines the actual values.

Central governance deliberately does not prescribe a universal batch size.

Where a batch or checkpoint control is defined, the agent must follow it and must not silently continue beyond the authorised boundary.

#### 21.2 Engagement Folder

Each formal audit/AAR has its own `07_Audit/` subfolder.

#### 21.3 Review Log

The Review Log is the authoritative audit population and progress record.

It must uniquely identify every in-scope item and contain sufficient state to determine, without relying on agent memory:

- whether every item in the defined population was reviewed;
- the review outcome for each item;
- whether a finding or follow-up resulted;
- whether the applicable audit checkpoint was completed.

It contains at minimum:

- source issue/item identifier;
- product/project;
- review status;
- review result;
- finding reference where applicable;
- completion/checkpoint state.

Audit completeness is determined from the Review Log, not agent memory or scattered comments.

When creating a Review Log, the centrally managed implementation aid is:

`00_Governance/01_Central/02_Templates/AUDIT_REVIEW_LOG.template.md`

The template is non-authoritative and must not override this section or any engagement-specific governed instruction.

#### 21.4 Reviewed Versus Archive Ready

A review label means an issue was included and reviewed.

`Reviewed` means the item was examined within the defined audit scope.

It does not mean the issue is archive-ready.

`Reviewed` and `Archive Ready` are distinct concepts.

An issue may be marked `Archive Ready` only where:

- the issue is `Done`;
- there is no unresolved audit finding that requires the issue to remain operationally active;
- required follow-up has either completed or is separately governed and traceable;
- applicable durable-knowledge obligations have been satisfied.

Archival is an administrative action following `Archive Ready`.

Archiving does not:

- change the audit result;
- remove historical Linear traceability;
- alter Git history;
- replace required durable documentation.

#### 21.5 Findings

Audits use the following findings taxonomy:

- `Documentation Update`
- `DDR`
- `Investigation / Integrity`
- `Already Captured / No Finding`

The taxonomy may be refined centrally if operating evidence shows a need.

Substantive findings are resolved through normal governed Linear/Git work.

The audit itself records the finding and its disposition; it does not silently make untracked substantive fixes.

#### 21.6 Audit Completion

An audit engagement completes only when:

- defined population is fully accounted for;
- Review Log is complete;
- findings are resolved or explicitly retained/deferred;
- final engagement state is recorded;
- required labels/checkpoints are applied.

Audit completion does not trigger unrelated broad revalidation.

---

### 22. Central Governance Change, Release and Distribution Lifecycle

Approved central governance is maintained in the central Governance Git/GitHub repository.

Central governance artefacts required locally by product agents are distributed into the centrally managed product subtree:

`00_Governance/01_Central/**`

Content within that subtree remains centrally owned and must not be locally altered by product work.

Governance distribution is deployment of already-approved central content, not a new substantive governance decision and not a second approval step.

The central Governance repository owns the authoritative recipient population, deployment projection and release-control artefacts used to perform automated central-governance release and distribution.

Each release/distribution event is governed operationally through Linear.

The specialised authoritative downstream distribution protocol is defined in the central-only:

`/Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md`

That Standard applies to central Governance downstream distribution operations and the executor. It is not a product-local working authority and is not part of the product projection. Independent central-only Standard approval/release lifecycle requirements are defined by Section 22.14 rather than by product distribution.

#### Section 22 Lifecycle Map

For navigation, the existing numbered controls in this section group into the following lifecycle domains:

- **Source and projected identity** — Sections 22.1–22.2.
- **Permanent Governance change authority and approval** — Sections 22.3–22.6.
- **Post-approval release and distribution** — Sections 22.7–22.10.
- **Completion and integrity** — Sections 22.11–22.13.
- **Independent centrally governed Standard lifecycle, applicability and provenance** — Sections 22.14–22.14.3.
- **Existing diagram conformance** — Section 22.15.

This map is navigation only. It does not create, weaken, duplicate or replace any control, and the numbered subsections remain authoritative for the controls they contain.

#### 22.1 Source

The authoritative source of every centrally deployed governance artefact is its approved location in the central Governance repository.

The deployed product projection contains:

```text
00_Governance/01_Central/
├── CENTRAL_GOVERNANCE.md
├── 01_Standards/
│   ├── ARCHITECTURE_DIAGRAM_STANDARD.md
│   ├── DDR_STANDARD.md
│   └── PRODUCTION_EVIDENCE_STANDARD.md
└── 02_Templates/
    ├── PROJECT_PROFILE.template.md
    ├── DIAGRAM_CONVENTION_LEARNING.md
    ├── DDR.template.md
    └── AUDIT_REVIEW_LOG.template.md
```

#### 22.2 Projected Artefact Identity

Every approved centrally projected artefact identifies its own:

- version;
- approval status;
- approval tag;
- approval date.

Each artefact is independently versioned and uses its own tag namespace.

The approval tag resolves through Git to the exact approved commit SHA and reading the artefact through that tag must return the approved content.

An artefact therefore does not attempt to contain the SHA of the commit that contains itself.

#### 22.3 Central Governance Changes Require Linear

A permanent change to the central governance model must originate from and remain governed by a Linear work item.

A central governance change follows the workflow profile selected under Sections 4.1 and 5 and the applicable gates and controls in Appendices A and B.

Governance-book-specific approval requirements for changes to `CENTRAL_GOVERNANCE.md` are additionally defined in Appendix C.

The Linear issue carries:

`Change: Governance`

and any additional applicable change classes.

GitHub provides the detailed change and review surface.

Linear remains the workflow authority.

A permanent governance change must not be made solely through an untracked GitHub branch, pull request, direct commit or repository edit.

#### 22.4 Relationship to In-Flight User Overrides

A task-specific user override under Section 2.8 does not constitute a permanent central governance change.

Such an override may govern the stated work item without first changing `CENTRAL_GOVERNANCE.md`.

If the override identifies a rule that should apply to future work, that permanent change must subsequently follow the normal Linear-governed central governance change route.

#### 22.5 Governance Change Impact Assessment

Before approval, a central governance change must assess:

- which products are affected;
- whether existing product repositories remain compatible with the changed governance;
- whether transition action is required;
- whether staged distribution is safe;
- whether temporary mixed governance versions across products create material risk;
- rollback or restoration considerations.

The assessment must be proportionate to the change.

#### 22.6 Pre-Merge Governance Approval

Before central governance content is merged, the applicable pre-merge requirements in Appendix C must be satisfied.

Human approval applies to the substantive proposed governance content.

#### 22.7 Merge and Approval Release

After substantive approval and applicable validation, squash merge of the accepted Governance pull request to `main` is the substantive approval boundary and automatically initiates the governed post-approval release process and, where projected artefacts changed, downstream distribution.

The automatic process must preserve at minimum:

- source-event identity from the Governance pull request and exact merge commit;
- independent verification that the pull request was merged to `main` at that exact commit;
- immutable create/reuse/verification semantics for required changed projected-artefact approval tags;
- immutable create/reuse/verification semantics for required changed independently released central-only Standard approval tags under Section 22.14;
- verification of applicable release metadata and exact approved content;
- derivation and Linear recording of applicable release provenance; and
- automatic continuation into governed downstream distribution only where one or more projected artefacts changed.

Multiple independently versioned artefacts changed by one pull request may legitimately have different approval tags resolving to the same merge commit.

Where no projected artefact changed, downstream product distribution is not required and must not be performed solely to produce `no_change` rollout results.

The deterministic post-approval release process does not require a second substantive governance approval.

#### 22.8 Distribution Is Not Re-Approval

Copying exact already-approved central governance artefacts into their defined locations within `00_Governance/01_Central/**` is governance deployment, not a new substantive governance decision.

Distribution does not require repeated substantive review merely because a deployed product copy changes.

Distribution requires:

- Git traceability;
- correct approved source;
- correct target repository and path;
- exact content/integrity verification;
- applicable version/tag traceability;
- rollout-state recording.

Detailed automated-distribution protocol is defined in the active Governance Distribution Standard.

#### 22.9 Staged Distribution and Partial Failure

Each product continues under the exact approved central artefact versions currently deployed there until later approved versions are successfully installed.

A rollout remains incomplete until every targeted product has either:

- received and integrity-verified the intended approved central content; or
- been explicitly deferred or excluded.

A failed rollout must not be represented as complete.

Temporary mixed versions are permitted only as an explicit traceable rollout state.

If a distribution step fails:

- record the affected product and failure;
- stop further rollout where continuing could create material inconsistency or risk;
- retain or restore the affected product's previous approved central content where required.

#### 22.10 Governance Rollout Tracking

Under the normal automated route, the Linear issue declared in the source Governance pull request remains the operational authority for the complete post-approval release event and any applicable downstream distribution.

That issue governs:

- the approved Governance change;
- the source Governance pull request and exact merge commit;
- independently released central-only Standard approval tags/provenance changed by the source event, where applicable;
- the complete projected artefact-to-approval-tag release set, where projected artefacts changed;
- downstream distribution to the governed product population, where projected artefacts changed;
- per-product rollout results, where distribution occurs; and
- completion of the automatic release/rollout.

A separate Linear rollout issue is not required for the normal automatic route.

Where a deferred, staged, exceptional or otherwise independently governable follow-up requires work beyond the automatic release event, a separate Linear issue may be created for that follow-up.

Such a follow-up issue:

- tracks deployment or remediation of already-approved governance;
- does not reopen substantive approval of the governance content;
- does not require `Change: Governance` solely because it distributes unchanged approved artefacts; and
- must remain traceable to the original approved Governance release event.

#### 22.11 Governance Content-Change Completion Boundary

Under the normal automated route, the governing central-governance issue reaches `Done` only when:

1. the accepted governance content has been merged;
2. every required changed independently released central-only Standard approval tag has been created or validly reused and verified under Section 22.14;
3. where projected artefacts changed, every required changed projected-artefact approval tag has been created or validly reused and verified;
4. where projected artefacts changed, the complete projected release set has been derived and recorded against the governing Linear issue;
5. where projected artefacts changed, automatic downstream distribution has been executed for the governed product population; and
6. where distribution occurs, every targeted product has reached an acceptable terminal rollout state under the active Governance Distribution Standard.

The acceptable terminal rollout states are:

- `merged`;
- `no_change`;
- explicitly `deferred`; or
- explicitly `excluded`.

A blocked, failed or still-open required release/provenance/deployment step keeps the governing issue incomplete.

Creation of approved governance artefact versions and product deployment remain distinct lifecycle concepts, but under the normal automated route all applicable release/provenance and distribution steps form one continuous governed event before the governing issue reaches `Done`.

#### 22.12 Permanent Governance Change and Distribution

Permanent governance changes follow the applicable workflow profile, Appendix A transition gates, Appendix B change-class controls and, for changes to `CENTRAL_GOVERNANCE.md`, Appendix C approval requirements.

Following human acceptance, applicable validation and merge to `main`, the normal governed route automatically performs required central-only Standard approval-tag creation/verification under Section 22.14, projected-artefact approval-tag creation/verification where applicable, and downstream distribution only where projected artefacts changed.

A separate rollout issue is required only where subsequent deployment or remediation has become an independently governable piece of work under Section 22.10.

Automatic post-merge release/distribution must not bypass or replace substantive human approval of the Governance change itself.

#### 22.13 Drift

A locally altered, misplaced, mismatched, incomplete or untraceable artefact within `00_Governance/01_Central/**` is a governance-integrity issue.

Restore the applicable approved central artefact rather than preserve local divergence.

Product-local work must not resolve such drift by editing centrally managed content.

#### 22.14 Centrally Governed Standard Lifecycle

A centrally governed Standard may be changed without changing or releasing a new version of `CENTRAL_GOVERNANCE.md` only where its applicable lifecycle provides independent approval/release provenance and the change does not require alteration of the rule book itself.

Changes to a centrally governed Standard follow the applicable workflow profile, Appendix A transition gates and Appendix B change-class controls.

The issue must identify the Standard being changed and use the applicable change classes.

A change to a centrally governed Standard must include `Change: Governance`; `Change: Documentation` may also apply where appropriate, and other applicable change classes may also be used.

Product-applicable Standards are projected unchanged to every product to which they apply. Their presence in the product projection does not make distribution a new substantive approval.

Central-only Standards are maintained beneath:

`/Standards/Central/`

They are not part of `GOVERNANCE_PROJECTION.yaml` and are not deployed to product repositories while they remain central-only.

##### 22.14.1 Directory-Based Standard Discovery

For centrally governed Standards, repository structure is the normal machine-readable discovery and applicability mechanism:

- a Standard beneath `/Standards/Product/` is product-applicable;
- a Standard beneath `/Standards/Central/` is central-only.

The release mechanism must discover Standards from those governed directories rather than require a second registry that repeats Standard paths and applicability.

Each Standard remains authoritative for its own release metadata, including its version, approval status, approval tag and approval date. The executor must validate that metadata and preserve the Standard's established approval-tag namespace across releases.

A deliberately governed authoritative source-path migration between folders changes applicability only where the Governance change explicitly says so. A relocation within the same applicability category must not silently change Standard identity or approval-tag namespace. Historical approval tags remain immutable and continue to prove the historical path/content they originally approved; they are not moved or reinterpreted when the current authoritative path changes.

`GOVERNANCE_PROJECTION.yaml` remains the operational source-to-destination population for artefacts deployed to products. It does not define whether a Standard exists or whether a central-only Standard participates in the independent release lifecycle.

Root-level files beneath `/Standards/` are not recognised as current governed Standards. Historical root paths remain available through Git history and historical approval tags for provenance; they are not live discovery or applicability exceptions.

##### 22.14.2 Independent Standard Release

An independently released centrally governed Standard identifies its own:

- version;
- approved status;
- approval tag; and
- approval date.

The Standard's approval-tag namespace is part of its durable release identity and must remain stable across ordinary version changes and governed source-path relocations unless an explicit Governance change deliberately changes that identity.

For each changed independently released Standard, the post-approval release mechanism must:

1. bind to the source Governance pull request and exact merge commit;
2. verify the Standard was changed in that source event;
3. read the exact accepted Standard bytes from that merge commit at its discovered authoritative source path;
4. validate declared release metadata and established tag namespace;
5. create or validly reuse the immutable approval tag at the exact merge commit;
6. verify the tag resolves to that commit and contains the exact accepted Standard bytes at the discovered source path;
7. record the release/provenance against the governing Linear issue;
8. remain idempotent and bound to the original source event on rerun; and
9. prevent issue completion while required release/provenance evidence is incomplete or contradictory.

Approval of a new independently released Standard version does not change the version of `CENTRAL_GOVERNANCE.md` unless the rule book itself also changes.

For an independently released central-only Standard, completion of the approval/tag/provenance lifecycle does not trigger product distribution. Product rollout occurs only if the same source event also changes one or more projected artefacts.

##### 22.14.3 Historical Transitional Provenance

The independent central-only Standard lifecycle established in Governance 6.1.0 is now the active lifecycle for central-only Standards.

`GOVERNANCE_DISTRIBUTION_STANDARD.md` v1.0.0 remains historical evidence of the earlier Governance-coupled transitional lifecycle. Its approved bytes are those contained in the Governance 6.0.0 merge commit identified by `governance-v6.0.0`. No independent v1.0.0 Standard tag exists or is implied, and that historical provenance must not be rewritten or reinterpreted.

Current Standard tag namespaces include:

- Architecture Diagram Standard: `diagram-standard-vX.Y.Z`
- DDR Standard: `ddr-standard-vX.Y.Z`
- Production Evidence Standard: `production-evidence-standard-vX.Y.Z`
- Governance Distribution Standard: `governance-distribution-standard-vX.Y.Z`

For a product-applicable Standard, deployment validation is limited to:

- correct approved source version;
- correct target path;
- exact content/integrity;
- successful distribution to the intended products; and
- traceable rollout state.

For a central-only independently released Standard, validation is limited to its required release/provenance controls and any substantive checks applicable to the Standard change itself; product deployment validation does not apply.

#### 22.15 Existing Diagram Conformance

Approval or deployment of a new Architecture Diagram Standard does not automatically require existing governed diagrams to be modified.

The active standard applies when a diagram is:

- newly created;
- substantively changed in an area governed by the standard; or
- explicitly brought into scope for a conformance update.

A standard change must not create an automatic repository-wide diagram remediation obligation unless the approved standard change explicitly requires migration because continued use of the previous representation would create a material governance or architectural risk.

---

### 23. Validation Tooling Lifecycle

Validation tooling has a defined purpose, authority and lifecycle.

Existence of a script does not make it mandatory.

#### 23.1 Authority

It must be possible to determine:

- risk/control addressed;
- triggering classes/dependencies;
- whether validator is authoritative;
- evidence produced.

#### 23.2 New Validators

Add new tooling only for a defined control need.

Define:

- risk;
- trigger;
- inputs;
- pass/fail;
- overlap with existing tooling.

#### 23.3 Changed Validators

Changes to validation tooling are assessed separately from the product state they validate.

Tool changes do not automatically trigger broad product revalidation.

Executable validation/release/deployment/workflow tooling whose governed purpose is to operate or assure the central Governance system uses `Change: Governance Tooling` rather than `Change: Code` solely because it is executable. It requires the Appendix B Governance Tooling controls and does not require Home Assistant Beta unless the same issue also contains genuine deployable product runtime implementation.

#### 23.4 Superseded Validators

Superseded/transitional validators are retired, removed or clearly marked non-authoritative.

Conflicting overlapping validators require authority resolution rather than automatic execution of both.

#### 23.5 Runtime Assumptions

Environment assumptions such as OS, PowerShell version, locale, date parsing, file layout and dependency versions should be explicit where relevant.

Regression checks tied to those assumptions run when those assumptions or tooling change, not automatically after unrelated changes.

---

### 24. Production Evidence Authority

Where current implemented/runtime state is material to governed work, sufficiently reliable and sufficiently current production evidence must be obtained through an approved evidence route.

Detailed production-evidence acquisition, freshness, retained-evidence handling, provenance, integrity and reuse practice is governed by the active product-applicable:

`00_Governance/01_Central/01_Standards/PRODUCTION_EVIDENCE_STANDARD.md`

The central authoritative source is:

`/Standards/Product/PRODUCTION_EVIDENCE_STANDARD.md`

The applicable Project Profile or other explicit environment authority identifies the actual product/environment production and evidence route. Central Governance and the Production Evidence Standard do not hard-code environment-specific connector or endpoint identities.

When production evidence is material, agents apply this section, the active Production Evidence Standard and the applicable Project Profile/environment authority together.

#### 24.1 Evidence Availability

Before declaring required production evidence unavailable or work blocked, use the approved route and other applicable approved evidence capabilities in accordance with the Production Evidence Standard.

A failed first route does not by itself establish that required evidence is unavailable or that work is blocked.

#### 24.2 Freshness Requirement

Where freshness affects a governed decision, sufficiently current evidence is required.

Detailed assessment of live versus retained evidence, contextual freshness, provenance and limitations is governed by the Production Evidence Standard.

#### 24.3 Production Versus Architecture

Production evidence establishes what is implemented or currently observed within its evidenced scope.

Approved architecture establishes what is approved.

A discrepancy is surfaced rather than silently resolved or normalised.

#### 24.4 Production Mutation Boundary

Production evidence access is read-only by default.

Availability of a write-capable tool does not authorise mutation.

For ordinary implementation work, a live-state mutation, service call, reload, restart or configuration change requires:

- the mutation to fall within the governing Linear issue scope;
- applicable governance gates to have passed;
- required explicit user authorisation.

For beta or stable deployment, authority may instead arise directly from the applicable beta/release rule together with the required explicit user deployment authorisation.

This permits a Simple Release without inventing a separate Linear release issue.

The Production Evidence Standard does not create or broaden mutation authority.

Broader technical permissions do not create broader governance authority.

---

### 25. Agent Execution Efficiency

Agents use the minimum context, evidence and dependency scope needed to complete work safely.

#### 25.1 Working Set

Once relevant governance, profile, architecture, contracts, issue context, repository structure, tool routes and evidence are established, they form the current working set.

Unchanged artefacts should not be repeatedly reread unless:

- they may have changed;
- a new phase requires fresh verification;
- context is genuinely insufficient;
- a gate requires latest-state verification.

#### 25.2 Bounded Dependency Traversal

Follow dependencies only as far as necessary for objective, acceptance criteria, change classes, identified risk or applicable gates.

Stop when further traversal cannot reasonably affect the decision or evidence.

#### 25.3 Tool Discovery

Use established tool routes where already known.

Do not repeatedly rediscover the same connector, MCP route, schema, repository or evidence source without reason.

#### 25.4 Historical Context

Use Git, Linear and audit history where materially helpful.

Do not automatically traverse extensive history where current authoritative state is sufficient.

#### 25.5 Expected Negative Outcomes

Distinguish:

- expected no-match;
- genuine execution error;
- validation failure;
- unavailable capability.

No result is not automatically an error.

#### 25.6 Existing Evidence

Reuse valid established evidence, including evidence tied to unchanged immutable state.

Refresh where freshness/state genuinely matters.

#### 25.7 Execution Logging

Use platform-native execution history, Git, Linear and retained validation/audit evidence where sufficient.

Do not create a detailed parallel agent self-log by default.

#### 25.8 Efficiency Does Not Bypass Control

Efficiency never bypasses genuinely applicable:

- human review;
- validation;
- fresh production evidence;
- knowledge retention;
- contract compatibility;
- beta;
- other required gates.

---

### 26. Monitoring and Continuous Improvement

Governance 2.0 maintains a monitoring register for operating-model hypotheses, risks and improvement questions that require evidence from real use before becoming governance.

Monitoring items are not controls and must not be treated as mandatory requirements.

The current monitoring population is recorded in the central Governance repository at:

`/MONITORING_REGISTER.md`

The register records operational monitoring state only. It is not a source of Governance rules and is not part of the centrally managed product projection.

Applicable monitoring evidence-source and disposition rules are defined in Appendix F.

A monitoring item only alters governance if it is formally promoted through the governance-improvement process and approved centrally.

#### 26.1 Governance Improvement Review and Promotion

If an agent identifies that central governance is:

- ambiguous;
- incomplete;
- internally inconsistent;
- unnecessarily burdensome;
- causing repeated execution inefficiency;
- failing to cover a recurring risk;
- encouraging workarounds;
- retaining a stale or duplicative control,

the agent should record the observation and provide a concise recommendation.

The recommendation should identify:

- the rule, omission or operating-model issue;
- the practical effect encountered;
- available evidence or examples;
- the proposed central change;
- known risks or trade-offs.

The recommendation is advisory only.

It does not become governance unless explicitly accepted by the user and incorporated into the applicable authoritative central governance artefact through its defined approval lifecycle.

This may be `CENTRAL_GOVERNANCE.md` or a separately governed central standard where that standard is the authoritative artefact for the subject.

The feedback loop is:

`observe → evidence → recommend → user review → applicable central change if accepted`

#### 26.2 Project AAR Review and Promotion

Open observations in product `00_Governance/AAR_REGISTER.md` files are periodically reviewed for possible central promotion.

Review of an AAR observation does not change the register's authority or make the observation Governance. Promotion occurs only where the observation is accepted through the governance-improvement process and incorporated into the applicable authoritative central Governance artefact through its normal approval lifecycle.

The AAR register remains product-owned operational learning state and must retain the purpose, boundaries, required fields, statuses and append-only rules defined in Section 2.7.

#### 26.3 Diagram Convention Learning and Review

Agents may add or refine `DIAGRAM_CONVENTION_LEARNING.md` incidentally during normal governed work only where that work involves creation, editing or review of a governed architecture diagram.

This restriction governs incidental learning capture. It does not prevent periodic review, disposition or maintenance of existing learning entries under this section.

An entry should be recorded only where a convention is:

- recurring;
- clearly deliberate; or
- explicitly reinforced during the work.

Agents must not create arbitrary new conventions merely for diagramming convenience.

A single accidental or isolated presentation detail should not normally be recorded.

Entries should remain lightweight.

Each entry should record, at minimum:

- the observed convention; and
- sufficient provenance to understand where it was learned, normally the originating Linear issue or equivalent work reference.

Example:

```markdown
## Gateway sizing

- Observed convention: ASTV routing gateways use 50 × 50 diamonds.
- First observed: ASTV-78
```

Additions or refinements made solely to `DIAGRAM_CONVENTION_LEARNING.md` as incidental learning:

- travel with the branch, PR or other normal change surface of the diagram work that produced the observation;
- do not require a separate Linear issue;
- do not add a change class;
- do not introduce an additional review or validation gate;
- do not prevent the originating work item from completing; and
- do not constitute approval of the convention as governance or architecture.

Periodic disposition or maintenance may update or remove learning entries without requiring concurrent creation, editing or review of a governed architecture diagram. Such changes travel with the governance, assurance or other governed work surface through which the periodic review is being performed.

Previously recorded learning may be reused as a provisional local working default where it does not conflict with a higher authority.

Use of a learned convention does not make that convention approved.

Rejection or removal of a learned convention does not retrospectively make earlier diagrams governance failures merely because they used that convention while it remained provisional.

Product `DIAGRAM_CONVENTION_LEARNING.md` files must be reviewed periodically and proportionately.

No fixed review cadence is required.

A review may occur through governance review, assurance activity, accumulation of meaningful learning, or another suitable checkpoint.

The review may update `DIAGRAM_CONVENTION_LEARNING.md` directly to record the resulting disposition of existing entries. This maintenance does not require concurrent diagram editing and is governed by the work surface through which the review is performed.

Each learned convention may be:

- **Promoted** — incorporated into the applicable centrally governed standard through its normal approval lifecycle;
- **Retained locally** — remains useful product-local learning;
- **Rejected** — removed because it is undesirable, accidental or unsupported; or
- **Superseded** — replaced by a newer local convention or central rule.

Promotion must be a deliberate human decision.

Similar conventions appearing independently across multiple products are strong candidates for centralisation, but similarity alone does not automatically promote them.

Periodic review of learning files is intended to improve central standards over time without turning incidental agent learning into a separate governance workflow.

---

## Appendices

### Appendix A — Authoritative Workflow Gate Matrix

This appendix is the **single authoritative source for workflow transition gates and workflow-profile gate applicability**.

The workflow profile applicable to an issue is determined under Sections 4.1 and 5.

The applicable change-class-specific controls for each gate or workflow point are defined in **Appendix B — Authoritative Change-Class Control Matrix**.

`Change: Governance Tooling` uses `WF-02` unless the same issue also carries a `WF-01` class such as genuine product `Change: Code`, in which case Section 5.2 precedence applies.

The actor performing the work does not change the applicable workflow profile or gate.

#### A.1 Preparation and Review Gates

| Gate | Transition / point | `WF-01` | `WF-02` | Universal requirement |
|---|---|---:|---:|---|
| **G0 — Ready Gate** | `Backlog → Ready` | Yes | Yes | Objective, acceptance criteria, repository, applicable change classes and material dependencies sufficiently defined; no unresolved prerequisite decision |
| **G1 — Start Gate** | `Ready → In Progress` | Yes | Yes | An authorised execution trigger has occurred; execution route selected; normal Git route established where applicable |
| **G2 — Review-Readiness Gate** | `In Progress → Ready for Review` | Yes | Yes | Proposed change complete and reviewable; applicable PR/review surface available; substantive execution paused |
| **G3 — Human Acceptance Gate** | Human acceptance while in `Ready for Review` | Yes | Yes | Required human review completed and accepted |
| **G4 — Validation Entry Gate** | `Ready for Review → Ready for Validation` | Yes | Yes | Applicable human acceptance has been obtained and remains valid; accepted substance is ready for applicable validation |

Human acceptance obtained at **G3** remains valid through validation and completion while the accepted substance remains unchanged.

Fresh human acceptance is required where:

- the previously accepted substance changes; or
- a separate action-specific authorisation is expressly required by Governance.

Action-specific authorisation, including beta deployment or stable release/deployment authorisation where applicable, does not constitute a second acceptance of unchanged substantive content.

#### A.2 Validation and Completion Gates

| Gate / point | Transition / point | `WF-01` | `WF-02` | Universal requirement |
|---|---|---:|---:|---|
| **Validation activity** | During `Ready for Validation` | Yes | Yes | Applicable validation is performed against the accepted substance and current relevant state; valid reusable evidence is considered; affected requirements are revalidated following relevant state-changing actions |
| **G5 — Beta Entry Gate** | `Ready for Validation → Beta` | Yes | No | Applicable validation passed and all requirements for entry to Beta are satisfied |
| **G6 — Beta Completion Gate** | `Beta → Done` | Yes | No | Completion obligations satisfied against the final implemented and beta-validated state |
| **G7 — Completion Gate** | `Ready for Validation → Done` | No | Yes | Applicable validation passed and completion obligations satisfied against the final implemented state |

#### A.3 Rework and Exception Gates

| Gate | Transition | Universal requirement |
|---|---|---|
| **G8 — Rework Gate** | Review/validation/Beta → `Changes Requested` | Required correction identified and recorded |
| **G9 — Technical Correction Return** | `Changes Requested → Ready for Validation` without repeated review | Permitted only where accepted substance has not changed |
| **G10 — Blocker Exit Gate** | `Blocked → prior active state` | Genuine blocker resolved or required user guidance/override supplied and recorded; resume the preserved work state through the applicable execution/Git route |

#### A.4 Lightweight Non-Code Exception

A clearly presentational/editorial non-code change may use the lightweight Git route only where:

1. it meets the eligibility criteria in Section 12.7; and
2. the user explicitly approves that route for the specific work item.

The exception may simplify Git/PR mechanics.

It does not:

- authorise semantic change;
- remove applicable classification;
- bypass required human judgement;
- convert a substantive change into a presentational one.

#### A.5 Dependency Stop Rule

Any gate that triggers dependency assessment follows this rule:

> Validate only the credible affected dependency chain, and stop when downstream impact is no longer reasonably possible.

Relationship alone does not justify additional validation.

#### A.6 Evidence Reuse Rule

Where evidence already proves an applicable requirement against the exact unchanged immutable state, it may be reused unless freshness itself is material to the control.

Section 15.8 additionally governs preservation of pre-merge validation evidence where squash merge changes Git commit identity without changing governed content.

---

### Appendix B — Authoritative Change-Class Control Matrix

This appendix is the **single authoritative source for change-class-specific controls**.

Where an issue has multiple change classes, applicable controls are cumulative unless explicitly incompatible or inapplicable.

The workflow profile determines which workflow gates apply. The assigned change classes determine the additional controls that must be satisfied at those gates or workflow points.

#### B.1 Preparation and Review Controls

| Gate | Code | Architecture | Contract | Governance | Governance Tooling | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|---|
| **G0** | Product runtime code scope/objective identifiable | Architectural concern/boundary identifiable | Provider/consumer relationship identifiable | Governance scope identifiable | Central Governance tooling purpose/control objective and non-product-runtime boundary identifiable | DDR need identifiable where already known | Durable-document scope identifiable | Diagram/visual scope identifiable |
| **G1** | — | — | — | — | — | — | — | — |
| **G2** | Linked PR pushed; implementation ready for human review | Authoritative architecture change reviewable | Contract delta and declared-consumer impact identifiable | Governance change reviewable; Appendix C preparation applies only where `CENTRAL_GOVERNANCE.md` is being changed; separately governed standards follow Section 22.14 | Linked PR pushed; tooling implementation and affected Governance control/release behaviour reviewable | DDR change reviewable | Durable documentation reviewable | Final or near-final visual artefact available for human visual review |
| **G3** | Human code approval | Human acceptance of architectural substance | Human acceptance plus proportionate consumer compatibility assessment | Human acceptance of governance change | Human technical acceptance of tooling behaviour and fit with the governing control objective | Human acceptance of durable decision record | Human acceptance of the final intended documentation state | Human visual acceptance of final intended state; Architecture Diagram Standard conformity reviewed where applicable |
| **G4** | Applicable tests/technical checks identified | Applicable architecture consistency and authority checks identified | Compatibility validation requirements identified | Governance structure/integrity checks identified | Applicable unit/integration/fixture and release/provenance checks identified | Identifier, ownership and supersession checks identified | Applicable integrity/document checks identified | Applicable integrity/provenance and standard-conformity checks identified |

#### B.2 Validation and Completion Controls

| Gate / point | Code | Architecture | Contract | Governance | Governance Tooling | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|---|
| **Validation activity** | Applicable product tests/technical checks pass; candidate suitable for merge/Beta | Applicable architecture consistency and authority checks pass | Compatibility risk resolved; consumer validation only where justified | Governance structure/integrity checks pass; Appendix C requirements apply only where `CENTRAL_GOVERNANCE.md` is being changed; separately governed standards satisfy Section 22.14 | Applicable unit/integration/fixture checks pass; governing control objective, failure behaviour, release/provenance integrity and rerun behaviour validated where relevant; Home Assistant Beta is not required solely for Governance Tooling | Identifier, ownership and supersession consistency pass | Only applicable integrity/document checks | Exact final accepted bytes/content used for integrity/provenance checks; Architecture Diagram Standard conformity confirmed where applicable |
| **G5** | PR squash-merged to `main`; resulting SHA identified; user authorises beta deployment; exact SHA deployed to `ha-starburst`; deployed state verified | If part of same issue, architecture obligations already satisfied before Beta | If part of same issue, compatibility obligations already satisfied before Beta | If part of same issue, governance obligations already satisfied before Beta | Applies only where the same issue also selects WF-01 through another class; Governance Tooling obligations already satisfied before Beta | If part of same issue, DDR obligations already satisfied before Beta | If part of same issue, durable-document obligations already satisfied where required | If part of same issue, final accepted diagram obligations already satisfied |
| **G6** | Beta succeeds against exact deployed candidate state; result remains traceable | — | — | — | — | — | — | — |
| **G7** | — | Accepted architecture state merged | Accepted contract state merged | Accepted governance state merged; Appendix C post-merge requirements apply only to `CENTRAL_GOVERNANCE.md` changes; separately governed standards complete under Section 22.14; distribution follows Section 22 where within scope | Accepted tooling implementation merged; required technical checks pass; any affected post-merge release/provenance state is validated; no Home Assistant Beta is required unless another applicable class selected WF-01 | DDR state merged | Accepted durable documentation merged | Exact visually accepted content merged |

#### B.3 Rework and Exception Controls

| Gate | Code | Architecture | Contract | Governance | Governance Tooling | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|---|
| **G8** | Pre-merge correction normally continues same branch/PR. Failed Beta correction uses same Linear issue but new corrective branch/PR | Substantive correction returns through human review | Contract meaning/compatibility correction returns through human review | Governance-substance correction returns through human review | Tooling behaviour/control-semantics correction returns through human review | Decision-substance correction returns through human review | Substantive correction returns through human review where required | Semantic/visual-meaning correction returns through human visual review |
| **G9** | Technical-only correction may bypass repeated review only where product code behaviour remains unchanged | Metadata/provenance-only correction | Metadata/provenance-only correction | Technical packaging/approval-metadata correction where governance substance is unchanged | Technical-only correction may bypass repeated review only where accepted tooling behaviour and governing control semantics remain unchanged | Metadata/provenance-only correction where decision is unchanged | Non-substantive technical correction | Integrity/provenance regeneration against unchanged accepted content |
| **G10** | — | — | — | — | — | — | — | — |

---

### Appendix C — Governance Change Approval Checklist

This appendix is mandatory whenever `CENTRAL_GOVERNANCE.md` is changed.

For the `Change: Governance` class, Appendix C requirements apply only where `CENTRAL_GOVERNANCE.md` itself is being changed.

A change confined to a separately governed standard follows the centrally governed standard lifecycle in Section 22.14 and does not, by itself, trigger Appendix C or a new `CENTRAL_GOVERNANCE.md` release.

#### C.1 Governance Semantic Versioning

Governance versions use:

`vMAJOR.MINOR.PATCH`

Classify the change by its effect rather than by the file or section changed.

| Version component | Governance change |
|---|---|
| `PATCH` | Backward-compatible correction or clarification that does not create a new obligation or materially alter authority |
| `MINOR` | Backward-compatible new rule, control or capability, or material expansion of an existing one |
| `MAJOR` | Incompatible rule change, removal or material weakening of an existing protection, changed authority boundary, or change requiring coordinated migration |

Urgency does not determine the version increment.

#### C.2 Linear and GitHub Preconditions

Before a permanent central governance change may be approved:

- [ ] a governing Linear issue exists;
- [ ] the issue carries `Change: Governance`;
- [ ] any additional applicable change classes are present;
- [ ] the issue has satisfied the applicable `Ready` and review gates;
- [ ] the change has been made through the central governance repository;
- [ ] the normal dedicated branch and linked pull-request route has been used unless a specific authorised exception applies;
- [ ] substantive human review has been completed;
- [ ] Linear accurately reflects the current workflow state.

A GitHub pull request without a governing Linear work item is not sufficient authority for a permanent central governance change.

#### C.3 Governance Impact Assessment

Before governance content may be merged:

- [ ] affected products have been identified;
- [ ] compatibility with the changed governance has been assessed;
- [ ] transition implications have been assessed;
- [ ] staged-distribution safety has been considered;
- [ ] temporary mixed-version risk has been considered;
- [ ] rollback/restoration implications have been considered.

#### C.4 Pre-Merge Approval Requirements

Before governance content may be merged:

- [ ] change followed applicable governance workflow;
- [ ] change classes are correct;
- [ ] substantive human governance review is complete;
- [ ] governance SemVer classification is correct;
- [ ] intended version is correct;
- [ ] intended approval tag is defined;
- [ ] intended approval date is defined;
- [ ] applicable Appendix A pre-merge gates have passed.

#### C.5 Post-Merge Approval-Release Requirements

After merge and before the governance version is available for distribution:

- [ ] exact accepted governance content has been merged;
- [ ] resulting commit has been identified;
- [ ] approval tag has been created against that exact commit;
- [ ] tag resolves to the expected commit;
- [ ] governance version/tag/date metadata is correct;
- [ ] distributable `CENTRAL_GOVERNANCE.md` is the exact approved artefact.

Product distribution performs integrity validation only and does not repeat substantive governance approval.

---

### Appendix D — Historical Provenance Pointer — DDR Standard Extraction (Non-Operative)

The detailed DDR specification formerly contained in this appendix is now governed by the centrally governed:

`Standards/Product/DDR_STANDARD.md`

Its scope and authority are defined by Sections 2.2, 9.4 and 22.14.

This appendix defines no independent DDR requirements.

---

### Appendix E — Historical Provenance Pointer — Audit Controls Consolidation (Non-Operative)

The audit control requirements formerly contained in this appendix are consolidated into Section 21 — Audit Model.

This appendix defines no independent audit requirements.

---

### Appendix F — Monitoring Register

Monitoring items are hypotheses or operating-model questions, not mandatory controls.

#### F.1 Operational Register

The current monitoring population and item state are maintained in the central Governance repository at:

`/MONITORING_REGISTER.md`

The register is operational state only. It does not create or amend Governance rules, and routine maintenance of the monitored population does not by itself change `CENTRAL_GOVERNANCE.md`.

The register is not part of the centrally managed product projection. Ordinary product agents do not need to load it merely to apply Governance.

Where register content appears to conflict with this governance book, this governance book prevails and the conflict must be surfaced.

#### F.2 Evidence Sources

Prefer evidence already produced through normal operation:

- Linear history;
- Git/GitHub;
- native agent telemetry;
- validation evidence;
- audit findings;
- release records;
- AAR registers;
- user intervention.

A separate heavyweight telemetry system must not be introduced without evidence of need.

#### F.3 Disposition

Monitoring items may be:

- `Retained`
- `Closed — No Change`
- `Promoted`
- `Superseded`

Only a `Promoted` item that then follows normal central governance review and approval becomes a governance rule.

---

### Appendix G — Historical Provenance Pointer — Governance Distribution Standard Extraction (Non-Operative)

The specialised central Governance release/distribution protocol formerly contained in this appendix is now governed by the central-only:

`Standards/Central/GOVERNANCE_DISTRIBUTION_STANDARD.md`

Its scope, applicability and authority are defined by Sections 2.2, 22 and 22.14.

This appendix defines no independent Governance distribution requirements.

---

### Appendix H — Authoritative Repository Structure and Artefact Placement

This appendix is the authoritative detailed repository-reference surface for the standard product-repository model governed by Section 3.

It defines canonical paths, folder purposes, placement rules and materialisation mechanics. Section 3 remains authoritative for the constitutional repository model, central-versus-product ownership boundary, convention-over-configuration principle, new recurring top-level artefact-class control, and secrets/credentials boundary.

#### H.1 Canonical Top-Level Structure

Top-level folders use:

`##_Name`

The baseline is:

```text
<Product>/
│
├── AGENTS.md
├── 00_Governance/
├── 01_Architecture/
├── 02_Decisions/
├── 03_Contracts/
├── 04_Source/
├── 05_Tests/
├── 06_Validation/
├── 07_Audit/
└── 08_Deployment/
```

A standard structural location need not physically exist in Git until it contains required content.

Empty standard folders must not be materialised solely through placeholder files such as `.gitkeep` or dummy `README.md` files unless a specific operational requirement requires the physical directory to exist.

#### H.2 `00_Governance/`

Contains centrally deployed governance artefacts and product-owned governance/context artefacts.

The standard structure is:

```text
00_Governance/
├── 01_Central/
│   ├── CENTRAL_GOVERNANCE.md
│   ├── 01_Standards/
│   │   ├── ARCHITECTURE_DIAGRAM_STANDARD.md
│   │   ├── DDR_STANDARD.md
│   │   └── PRODUCTION_EVIDENCE_STANDARD.md
│   └── 02_Templates/
│       ├── PROJECT_PROFILE.template.md
│       ├── DIAGRAM_CONVENTION_LEARNING.md
│       ├── DDR.template.md
│       └── AUDIT_REVIEW_LOG.template.md
├── PROJECT_PROFILE.md
└── AAR_REGISTER.md
```

The ownership and mutation boundary for `00_Governance/01_Central/**` is defined in Section 3.1 and applies to this structure.

#### H.3 `01_Architecture/`

Contains authoritative and supporting architecture artefacts.

The authoritative architecture document uses:

`*_ARCHITECTURE.md`

For example:

```text
01_Architecture/
├── <PRODUCT>_ARCHITECTURE.md
└── Diagrams/
    ├── <governed diagram files>
    └── DIAGRAM_CONVENTION_LEARNING.md
```

Architecture diagrams support the authoritative architecture record but do not replace it.

Product-local recurring diagram presentation conventions may be captured in `DIAGRAM_CONVENTION_LEARNING.md`.

`DIAGRAM_CONVENTION_LEARNING.md` is the standard location for product-local diagram convention learning.

It must not be used to restate central standards, architecture, contracts or governance.

The learning file contains provisional product-local observations and working defaults only. Incidental capture, reuse, maintenance, review and disposition mechanics are defined in Section 26.3.

#### H.4 `02_Decisions/`

Contains Design Decision Records.

Routine issue notes, temporary design discussion and implementation history do not belong here.

#### H.5 `03_Contracts/`

Contains authoritative interfaces/contracts provided by this product.

Consumers reference the provider-owned contract from their `PROJECT_PROFILE.md`; they do not maintain authoritative duplicates.

#### H.6 `04_Source/`

Contains executable or deployable product implementation.

Source remains clearly separated from tests, validation tooling, governance, architecture, audit and deployment tooling.

#### H.7 `05_Tests/`

Contains tests of product behaviour.

Examples include:

- unit tests;
- integration tests;
- behavioural tests;
- fixtures;
- test helpers;
- implementation test scripts.

Purpose:

> Determine whether the product behaves as intended.

#### H.8 `06_Validation/`

Contains validation tooling and retained validation evidence concerning governed repository/change integrity.

Where useful:

```text
06_Validation/
├── Tools/
└── Evidence/
```

Purpose:

> Determine whether the governed change or repository state satisfies applicable controls.

Validation must not become a duplicate testing framework.

#### H.9 `07_Audit/`

Reserved for formal audit and review engagements.

Each engagement has its own subfolder.

Routine PR history, normal Linear issue notes and temporary development output do not belong here.

#### H.10 `08_Deployment/`

Contains deployment and rollback mechanics where required.

Examples include:

- install/update helpers;
- beta deployment helpers;
- stable deployment helpers;
- rollback tooling;
- deployment manifests;
- environment mappings.

This folder must not contain duplicate authoritative source.
