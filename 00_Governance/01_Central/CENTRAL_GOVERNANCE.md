# CENTRAL_GOVERNANCE.md

**Governance version:** 3.1.1
**Status:** Approved
**Approval tag:** `governance-v3.1.1`
**Approval date:** 2026-09-03

**Authority of appendices:**  
All appendices form an integral part of this governance book and carry the same authority as the main body unless an appendix explicitly states otherwise. Agents must apply applicable appendix requirements together with the relevant body sections and must not treat appendices as optional or supplementary guidance.

---

# Contents

## Part I — Governance Foundations

1. Objective  
2. Governance Model  
3. Standard Repository Structure  

## Part II — Work Management and Execution

4. Linear as the Workflow Authority  
5. Change Classes  
6. Sub-Issues and Issue Decomposition  
7. Execution Routes  

## Part III — Git, Review and Change Acceptance

8. Git Working Model and Linear Alignment  
9. Branch and Pull Request Rules  
10. Code Review  
11. Non-Code Review  

## Part IV — Validation and Completion

12. Validation Model  
13. Validation Failure Handling  
14. Non-Code Completion  
15. Code Completion and Beta  

## Part V — Release and Durable Product Knowledge

16. Stable Release  
17. Release Modes  
18. Knowledge Retention  
19. Design Decision Records  
20. Contract Ownership and Compatibility  

## Part VI — Assurance and Governance Operations

21. Audit Model  
22. Governance Deployment  
23. Validation Tooling Lifecycle  
24. Production Evidence and Tool Routes  
25. Agent Execution Efficiency  
26. Monitoring and Continuous Improvement  

## Appendices

- Appendix A — Authoritative Workflow Gate Matrix
- Appendix B — Authoritative Change-Class Control Matrix
- Appendix C — Governance Change Approval Checklist
- Appendix D — DDR Standard
- Appendix E — Audit Reference
- Appendix F — Monitoring Register
- Appendix G — Central Governance Distribution Control Model

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

---

### 2. Governance Model

#### 2.1 One Central Governance Book

There is one authoritative central governance book:

`CENTRAL_GOVERNANCE.md`

The central governance repository owns and approves this artefact.

Once approved, the exact approved file is deployed unchanged into each product repository as part of the centrally managed governance projection defined in Section 3.1.

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
- `/DDR_REGISTRY.md`
- `/Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`
- `/Templates/PROJECT_PROFILE.template.md`
- `/Templates/DIAGRAM_CONVENTION_LEARNING.md`

`DDR_REGISTRY.md` is a central-only governance artefact and is not deployed into product repositories.

Central governance artefacts required locally by product agents are deployed through the centrally managed governance projection defined in Section 3.1.

The repository's `main` branch represents the accepted integrated governance state.

The central governance repository is not required to use the standard product-repository folder structure.

GitHub hosts the repository and may technically enforce branch, pull-request and merge controls.

`CENTRAL_GOVERNANCE.md` remains authoritative for what those controls mean and when they apply.

GitHub configuration does not replace or independently redefine central governance.

#### Centrally Governed Standards

Governance may define centrally governed standards for subjects that require consistent rules across products but are expected to evolve independently of `CENTRAL_GOVERNANCE.md`.

A centrally governed standard:

- is authoritative within its defined scope;
- is maintained in the central Governance repository;
- has one fixed authoritative filename and path;
- may be versioned, approved and deployed independently of `CENTRAL_GOVERNANCE.md`;
- must not contradict `CENTRAL_GOVERNANCE.md`; and
- must be distributed unchanged to every product to which it applies.

The first centrally governed standard is:

`ARCHITECTURE_DIAGRAM_STANDARD.md`

Its authoritative central-repository path is:

`/Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`

Its deployed product path is:

`00_Governance/01_Central/01_Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`

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
- purpose;
- scope;
- explicit boundaries and out-of-scope responsibilities;
- authoritative architecture artefact;
- external contracts consumed;
- relevant external dependencies or evidence sources where necessary.

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

Open observations are periodically reviewed for possible central promotion.

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

### 3. Standard Repository Structure

Every product repository follows the same standard top-level structure unless central governance itself is changed.

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

Top-level folders should use meaningful subfolders where this improves organisation.

Large flat collections of unrelated files should be avoided.

A standard structural location need not physically exist in Git until it contains required content.

Empty standard folders must not be materialised solely through placeholder files such as `.gitkeep` or dummy `README.md` files unless a specific operational requirement requires the physical directory to exist.

#### 3.1 `00_Governance/`

Contains centrally deployed governance artefacts and product-owned governance/context artefacts.

The standard structure is:

```text
00_Governance/
├── 01_Central/
│   ├── CENTRAL_GOVERNANCE.md
│   ├── 01_Standards/
│   │   └── ARCHITECTURE_DIAGRAM_STANDARD.md
│   └── 02_Templates/
│       ├── PROJECT_PROFILE.template.md
│       └── DIAGRAM_CONVENTION_LEARNING.md
├── PROJECT_PROFILE.md
└── AAR_REGISTER.md
```

Everything under:

`00_Governance/01_Central/**`

is centrally managed content.

Product-local work must not create, edit, rename, move or delete anything within that subtree.

The central governance repository remains the source of truth for all content deployed into that subtree.

`PROJECT_PROFILE.md` and `AAR_REGISTER.md` are product-owned artefacts and remain outside the centrally managed subtree.

`DDR_REGISTRY.md` remains central-only and is not deployed into product repositories.

Templates within `01_Central/02_Templates/` are centrally managed implementation aids. Their presence in a product repository does not make them independent governance authorities.

`ARCHITECTURE_DIAGRAM_STANDARD.md` is an exact deployed copy of the centrally approved standard and must not contain product-specific amendments.

Product-specific architectural meaning belongs in the applicable approved architecture documentation.

Routine architecture, validation output, audit evidence or product work must not accumulate in `00_Governance/01_Central/`.

#### 3.2 `01_Architecture/`

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

#### Diagram Convention Learning

Agents may add or refine `DIAGRAM_CONVENTION_LEARNING.md` incidentally during normal governed work only where that work involves creation, editing or review of a governed architecture diagram.

This restriction governs incidental learning capture. It does not prevent periodic review, disposition or maintenance of existing learning entries under Section 26.1.

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

Periodic disposition or maintenance under Section 26.1 may update or remove learning entries without requiring concurrent creation, editing or review of a governed architecture diagram. Such changes travel with the governance, assurance or other governed work surface through which the periodic review is being performed.

Previously recorded learning may be reused as a provisional local working default where it does not conflict with a higher authority.

Use of a learned convention does not make that convention approved.

Rejection or removal of a learned convention does not retrospectively make earlier diagrams governance failures merely because they used that convention while it remained provisional.

#### 3.3 `02_Decisions/`

Contains Design Decision Records.

Routine issue notes, temporary design discussion and implementation history do not belong here.

#### 3.4 `03_Contracts/`

Contains authoritative interfaces/contracts provided by this product.

Consumers reference the provider-owned contract from their `PROJECT_PROFILE.md`; they do not maintain authoritative duplicates.

#### 3.5 `04_Source/`

Contains executable or deployable product implementation.

Source remains clearly separated from tests, validation tooling, governance, architecture, audit and deployment tooling.

#### 3.6 `05_Tests/`

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

#### 3.7 `06_Validation/`

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

#### 3.8 `07_Audit/`

Reserved for formal audit and review engagements.

Each engagement has its own subfolder.

Routine PR history, normal Linear issue notes and temporary development output do not belong here.

#### 3.9 `08_Deployment/`

Contains deployment and rollback mechanics where required.

Examples include:

- install/update helpers;
- beta deployment helpers;
- stable deployment helpers;
- rollback tooling;
- deployment manifests;
- environment mappings.

This folder must not contain duplicate authoritative source.

#### 3.10 Repository Organisation Principle

Repository structure favours convention over configuration.

Agents should infer expected handling of an artefact substantially from its location.

New recurring top-level artefact classes are raised through the AAR/governance-improvement process rather than introduced independently by individual products.

#### 3.11 Secrets and Credentials

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

Two workflow profiles are currently defined because code changes require a Beta stage before completion, while non-code changes do not.

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

Revalidation is proportionate to the changed state. Unaffected evidence may be reused where Section 12.4 and Appendix A.6 permit.

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
| `Change: Code` | Changes executable or deployable implementation, including runtime-controlling configuration. | `WF-01` |
| `Change: Architecture` | Changes approved structure, responsibilities, boundaries, components, interactions or architectural behaviour. | `WF-02` |
| `Change: Contract` | Creates or changes an authoritative product-provided interface/contract, including inputs, outputs, schemas, guarantees or compatibility expectations. | `WF-02` |
| `Change: Governance` | Changes rules, controls, authority, repository conventions, workflow or governance process. | `WF-02` |
| `Change: DDR` | Creates, updates or supersedes a Design Decision Record. | `WF-02` |
| `Change: Documentation` | Changes durable explanatory or operational documentation not governed as architecture, contract, governance, DDR or diagram. | `WF-02` |
| `Change: Diagram` | Creates or changes a governed diagram or visual architecture artefact. | `WF-02` |

A single issue or file may require multiple classes.

There is no generic `Mixed` class.

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

An explicitly approved lightweight exception may apply where permitted by Section 9.7.

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

## Part III — Git, Review and Change Acceptance

### 8. Git Working Model and Linear Alignment

Git records version history.

Linear records operational state.

The table below shows which Git concepts normally become relevant at each Linear state and where those concepts are defined.

| Linear state | Git/GitHub activity | Relevant definition |
|---|---|---|
| `Backlog` | Normally no Git activity | — |
| `Ready` | Normally no Git activity yet | — |
| `In Progress` | Create/use issue branch; make changes; commit; push as needed | 8.2 Branch, 8.3 Commit, 8.4 Push |
| `Ready for Review` | Branch pushed; linked PR open and reviewable | 8.4 Push, 8.5 Pull Request |
| `Changes Requested` — pre-merge | Continue same branch/PR; commit and push corrections | 8.2–8.6 |
| `Changes Requested` — after failed beta | Same Linear issue; create corrective branch/PR from appropriate `main` state | 8.1, 8.2, 8.5, 8.6 |
| `Ready for Validation` | Reviewed PR represents accepted proposed change; merge has not yet occurred | 8.5 Pull Request, 8.7 Merge |
| `Beta` | Applicable PR has been squash-merged; resulting `main` SHA is deployed to `ha-starburst` | 8.1 `main`, 8.7 Merge |
| `Done` | Required issue-level Git actions complete | 8.7 Merge |
| `Blocked` | Preserve current Git state for later resumption | 8.2 Branch, 8.3 Commit, 8.5 Pull Request |

The table is a workflow guide.

Sections 8.1–8.8 define the individual Git concepts.

#### 8.1 `main`

`main` represents accepted integrated development state.

It does not mean every commit has passed beta or is a stable release.

Stable SemVer tags identify proven stable states.

#### 8.2 Branch

A branch is a separate line of work for an issue.

Normal model:

`one independently reviewable Linear work item → one issue branch`

A corrective branch may be required after a previously merged beta candidate fails.

#### 8.3 Commit

A commit records an identifiable Git state.

Multiple commits may occur during implementation/rework.

A commit alone does not publish, request review, merge or release work.

#### 8.4 Push

Push sends commits to GitHub.

Implementation may contain multiple:

`change → commit → push`

cycles.

#### 8.5 Pull Request

A pull request proposes incorporation of a branch into `main`.

It provides the principal GitHub review surface and may contain:

- diffs;
- comments;
- requested changes;
- approvals;
- automated checks;
- merge history.

Opening a PR does not mean the change has been accepted or merged.

#### 8.6 Review Changes

Before merge, requested changes normally use the applicable Appendix A rework and review gates while continuing on the existing branch and PR.

After a merged beta candidate fails, the same Linear issue continues through the applicable Appendix A rework gates using a new corrective branch/PR.

The Linear issue remains the same unless the correction has become an independently governable piece of work requiring issue decomposition under Section 6.

#### 8.7 Merge

The standard merge method is:

**Squash merge**

The commits in an issue PR are incorporated into `main` as one resulting issue-level commit.

Where the applicable workflow profile requires Beta, squash merge occurs after review and applicable pre-Beta validation and before Beta deployment.

The resulting `main` SHA becomes the beta candidate.

Where the applicable workflow profile does not require Beta, merge normally occurs after review and applicable validation, immediately before `Done`.

#### 8.8 Tag and Release

A Git tag identifies an exact commit using a durable name.

Stable product releases use SemVer tags such as:

`v1.2.0`

Central governance approval uses a governance-specific approval tag such as:

`governance-v2.0.0`

Tags resolve to exact Git commits.

Beta uses exact commit SHAs and does not require a beta tag.

---

### 9. Branch and Pull Request Rules

Default:

`one independently reviewable Linear work item → one dedicated branch → one linked PR`

#### 9.1 Dedicated Work Branches

A branch normally remains associated with the issue through implementation, review, requested changes and validation until merge.

Long-lived branches containing unrelated issues should be avoided.

#### 9.2 Pull Requests

The PR should be linked to the Linear issue.

The relationship among issue, branch, proposed change, review and completion should remain clear.

#### 9.3 Rework Before Merge

Review or validation rework before merge normally continues on the same branch and PR.

#### 9.4 Rework After Merge

If a merged beta candidate fails, corrective work remains on the same Linear issue but uses a new corrective branch and PR.

The earlier merged PR remains immutable historical evidence of the failed beta candidate.

#### 9.5 Scope

Git structure follows work decomposition rather than repository folder or file type.

#### 9.6 Actor Neutrality

Manual and automated execution use the same Git traceability standard.

#### 9.7 Lightweight Non-Code Route

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

#### 9.8 Exceptional Direct Changes

Other direct changes to the protected target branch are not normal governed work.

A specific in-flight user override may authorise one, but it does not create a standing alternative workflow.

#### 9.9 Post-Merge Branch Cleanup

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

### 10. Code Review

Code requires human review at the applicable Appendix A human-acceptance gate before validation may proceed.

GitHub is the detailed code-review surface.

Linear remains workflow authority.

#### 10.1 Entry

A code issue enters `Ready for Review` when:

- implementation is complete;
- branch is pushed;
- linked PR exists;
- change is meaningfully reviewable;
- substantive execution has paused.

#### 10.2 Human Review

The user may examine:

- diff;
- inline comments;
- questions;
- approval;
- requested changes.

Detailed review feedback remains attached to the PR rather than duplicated into Linear.

#### 10.3 Accepted Review

Acceptance satisfies the substantive human-review requirement for the applicable Appendix A gate.

It does not mean validation, Beta or stable release has completed.

#### 10.4 Changes Requested

Required changes proceed through the applicable Appendix A rework gate.

Before merge, the same issue/branch/PR normally continue.

#### 10.5 Review Authority

Human approval is initially mandatory for code.

Automated or agent review may support but not replace it unless central governance is later changed.

---

### 11. Non-Code Review

Non-code review is proportionate to artefact and risk.

It must not inherit code-review ceremony automatically.

#### 11.1 Entry

A non-code issue enters `Ready for Review` when:

- proposed change is meaningfully reviewable;
- artefact is available;
- applicable review surface exists;
- substantive execution has paused.

#### 11.2 Text-Based Artefacts

Architecture, contracts, DDRs, governance and durable documentation normally use a linked PR where the standard Git route applies.

Review establishes whether the artefact is acceptable in substance.

#### 11.3 Diagrams and Visual Artefacts

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

#### 11.4 Presentational Versus Substantive

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

#### 11.5 Review Authority

Automation may assist but does not replace required human judgement over architecture, contracts, governance, durable decisions or final visual acceptance.

---

## Part IV — Validation and Completion

### 12. Validation Model

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

#### 12.1 Universal Integrity and Selection

Every governed change receives one lightweight universal selection/integrity assessment.

Its purpose is to:

- confirm issue/change classification is sufficient;
- identify applicable class-specific and dependency-triggered controls;
- confirm exact state being assessed is identifiable;
- consider durable-knowledge obligations;
- detect obvious repository/change-integrity problems.

It is not a universal substantive validation suite.

#### 12.2 Change-Class-Specific Validation

Substantive validation is driven by applicable change class and identified risk.

A class does not inherit unrelated validation merely because another validator exists.

#### 12.3 Dependency-Triggered Validation

Validation follows the credible affected dependency chain only as far as impact can reasonably propagate.

Traversal requires a specific affected dependency or risk.

“Related to” is not sufficient justification.

Appendix A.5 defines the dependency stop rule.

#### 12.4 Reusable Evidence

Evidence may be reused where relevant immutable state remains unchanged.

Useful identifiers include:

- Git SHA;
- file hash;
- stable release tag.

Unchanged state should not be revalidated solely to reproduce the same evidence.

Appendix A.6 defines the evidence reuse rule.

#### 12.5 Final-Acceptance Validation

Where review can alter an artefact, final validation applies to the exact user-accepted state.

This is especially important for diagrams and manually adjusted governed artefacts.

Validation of a governed architecture diagram may include conformity with the active Architecture Diagram Standard.

Validation of the standard itself and validation of a product diagram are separate controls.

Deployment of a new Architecture Diagram Standard does not by itself require revalidation of unchanged product diagrams.

#### 12.6 Validation Selection

Before substantive validation determine:

1. applicable change classes;
2. universal integrity/selection result;
3. applicable class-specific checks;
4. material dependency impact;
5. reusable valid evidence;
6. need for final-acceptance validation.

Only the resulting set is executed.

#### 12.7 Validation Evidence

Retained evidence should identify:

- what was validated;
- control/risk addressed;
- exact state;
- result;
- reuse validity where relevant.

Routine output is not retained indefinitely merely because it exists.

#### 12.8 Merge Preservation

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

### 13. Validation Failure Handling

Validation failure is assessed according to what failed and what correction is required.

Rework follows the applicable Appendix A rework gate.

Whether repeated human review is required depends on whether the accepted substance has changed, as defined by Appendix A and the applicable change-class controls in Appendix B.

#### 13.1 Validation-Tool Failure

A broken validator or tool failure must be distinguished from an artefact/product failure.

Expected negative search results, no-match outcomes and runtime/tool errors are not automatically governed-change failures.

### 14. Non-Code Completion

Non-code completion follows the applicable workflow profile and transition gates defined in Appendix A.

Applicable change-class-specific completion controls are defined in Appendix B.

Sections 14.1–14.5 describe the operating model and evidence expectations for non-code completion; they do not independently authorise workflow transitions.

#### 14.1 Merge Timing

Normal non-code PR merge occurs after human acceptance and applicable validation, immediately before `Done`.

#### 14.2 Final Accepted State

The merged state must preserve the exact final accepted governed content.

Where applicable, final integrity/provenance evidence refers to that accepted content and its resulting repository state.

Section 12.8 governs preservation of pre-merge evidence across squash merge.

#### 14.3 Presentational Changes

Presentational work uses the lightest applicable path.

The lightweight Git route remains subject to explicit user approval under Section 9.7 and Appendix A.4.

#### 14.4 No Stable Release Requirement

Non-code issue completion does not by itself require a product stable-release step.

#### 14.5 Final Closure Evidence

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

### 15. Code Completion and Beta

Code completion follows the applicable workflow profile and transition gates defined in Appendix A.

Where the selected workflow profile requires Beta, the code issue reaches `Done` only after applicable review, validation and successful Beta operation.

Stable release is separate.

Applicable change-class-specific controls are defined in Appendix B.

#### 15.1 Entry to Beta

Entry to `Beta` occurs only when the applicable Appendix A Beta-entry gate and Appendix B code controls have been satisfied.

The resulting deployed candidate state is the state against which Beta operation is assessed.

#### 15.2 Beta Candidate Integrity

Beta result applies only to the exact deployed runtime-affecting state represented by the candidate SHA.

A later runtime-affecting change does not inherit that result.

#### 15.3 Beta Operation

Beta testing focuses on behaviour and risks introduced by the change.

Duration and depth are proportionate to risk.

#### 15.4 Successful Beta

Successful Beta satisfies the Beta-operation requirement for completion.

Transition from `Beta` to `Done` is governed by the applicable Appendix A gate.

The implementation issue is complete when that gate is satisfied, but no stable product release is automatically created.

#### 15.5 Failed Beta

A failed Beta requires rework through the applicable Appendix A rework gate.

The failed candidate remains part of Git history.

Corrective implementation uses a new branch and PR under the same Linear issue unless issue decomposition is genuinely required.

`ha-starburst` may be rolled back to a selected stable tag with explicit user authorisation.

#### 15.6 Agent-Assisted Beta Deployment

Initial beta deployment is agent-assisted rather than fully automatic.

The agent performs deployment mechanics only after explicit user authorisation.

Deployment must:

- target a specific SHA;
- verify deployed state;
- preserve rollback capability.

#### 15.7 Failed-Beta `main` Protection

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

## Part V — Release and Durable Product Knowledge

### 16. Stable Release

A stable release promotes an integrated product state whose runtime-affecting content has valid beta/stable coverage into an explicitly versioned stable state.

It is product-level activity separate from individual issue completion.

#### 16.1 Stable Authority

Stable promotion requires explicit user authorisation.

Successful beta does not automatically create a release.

#### 16.2 Semantic Versioning

Stable releases use:

`vMAJOR.MINOR.PATCH`

| Version component | Use when |
|---|---|
| `MAJOR` | Breaking or deliberately incompatible product or consumer-facing contract change |
| `MINOR` | Backward-compatible new capability or materially expanded behaviour |
| `PATCH` | Backward-compatible fix, correction, documentation-only release, or internal change with no new external capability |

Version significance reflects released product behaviour/state, not implementation effort.

#### 16.3 Beta and Stable Coverage

A stable release SHA must have valid runtime coverage for all runtime-affecting content included in that release.

Runtime content already contained in an earlier stable release is considered to retain established runtime coverage while that content remains unchanged.

Runtime-affecting content introduced or altered after that established coverage must obtain applicable beta coverage before stable promotion.

The release SHA may therefore be:

- an exact successfully beta-tested SHA; or
- a later descendant where changes introduced after the applicable beta/stable coverage are demonstrably non-runtime-affecting and have passed their applicable controls.

Any runtime-affecting change introduced after the applicable beta result requires a new beta candidate.

A non-runtime-affecting change does not require Home Assistant redeployment merely to reproduce coverage for unchanged runtime content.

#### 16.4 Release Cut-Off

The selected stable SHA is the release cut-off.

Later commits on `main` are not part of that release.

#### 16.5 Stable Tag and GitHub Release

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

#### 16.6 Agent-Assisted Stable Deployment

Initial stable deployment is agent-assisted and requires explicit user authorisation.

The agent deploys the exact tagged version to user-selected environments and verifies deployed state.

The model supports deployment to:

- `ha-starburst`;
- `ha-glenrosa`.

#### 16.7 Rollback

Rollback is agent-assisted and requires explicit user authorisation.

Each environment may be rolled back independently to a selected previous stable tag.

#### 16.8 Release Integrity

A stable release must remain traceable to:

- SemVer tag;
- exact released SHA;
- applicable beta/stable coverage;
- GitHub Release;
- deployment state;
- relevant supporting evidence.

---

### 17. Release Modes

Stable releases use either **Simple Release** or **Managed Release**.

#### 17.1 Simple Release

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

#### 17.2 Managed Release

Use a Managed Release where release activity itself requires material operational coordination, including:

- multiple coordinated products/releases;
- dependency-sensitive sequencing;
- migration/environment preparation;
- special release validation;
- special rollback preparation;
- several distinct execution steps requiring lifecycle tracking;
- explicit user decision that managed control is warranted.

A dedicated Linear work item manages the release.

#### 17.3 Escalation

A Simple Release may be converted to Managed if unexpected complexity appears.

#### 17.4 Release Completion

Release completion requires:

- explicit promotion;
- correct tag;
- GitHub Release;
- intended deployment completed;
- deployed state verified;
- applicable release checks passed;
- rollback target identified.

---

### 18. Knowledge Retention

Durable product knowledge is captured during normal work rather than reconstructed later.

#### 18.1 Completion Check

Before completion determine whether the change:

1. altered product architecture;
2. created, changed or superseded a decision meeting the DDR threshold;
3. created or changed a provider-owned contract;
4. changed another authoritative durable artefact.

Where yes, the corresponding authoritative artefact must be updated.

This is a lightweight completion check, not a broad documentation audit.

#### 18.2 Architecture

Known architectural changes update the authoritative `*_ARCHITECTURE.md` during the same logical work.

Architecture changes must be grounded in:

- the current authoritative architecture;
- materially applicable contracts;
- production evidence where current implementation state is relevant;
- materially applicable DDRs.

Historical context should be consulted only where materially necessary to understand or justify the change.

Architecture must not be invented or altered merely for implementation, documentation or diagramming convenience.

Where production evidence and approved architecture differ, the discrepancy must be surfaced and resolved rather than silently normalised.

#### 18.3 Decisions

Decisions meeting the DDR threshold are captured during normal work.

Audit-based DDR recovery is a backstop.

#### 18.4 Contracts

Provider-owned contract changes update the provider's authoritative contract during the same logical work.

Declared consumers are assessed for compatibility.

#### 18.5 Supporting Artefacts

Supporting durable artefacts are updated only where genuinely affected.

---

### 19. Design Decision Records

DDRs preserve significant durable design decisions and their rationale.

They do not record every implementation choice.

#### 19.1 Threshold

A DDR is normally required where a decision:

- establishes or materially changes architectural direction;
- chooses among meaningful alternatives with lasting consequences;
- establishes a future constraint;
- creates an important cross-product design principle;
- deliberately accepts a material trade-off;
- supersedes an earlier durable decision;
- would otherwise be difficult to reconstruct safely later.

A DDR is not normally required for routine implementation/configuration choices, obvious corrections or purely presentational decisions.

#### 19.2 Relationship to Architecture

Architecture states what is approved now.

A DDR explains why an important decision was made.

Current architecture must be understandable without reconstructing it from historical DDRs.

#### 19.3 Location and Numbering

Product DDRs are stored in:

`02_Decisions/`

Identifiers use one global sequence:

`DDR-###`

The allocation authority is the central:

`/DDR_REGISTRY.md`

held in the central governance repository.

Allocation and concurrent-update rules are defined in Appendix D.

#### 19.4 DDR Standard

Mandatory DDR content, statuses, registry fields, numbering and supersession mechanics are defined in Appendix D.

#### 19.5 Recovered Decisions

A retrospective DDR may be created where audit discovers a missing durable decision and sufficient evidence remains.

This is recovery, not the preferred normal process.

---

### 20. Contract Ownership and Compatibility

Authoritative cross-product contracts are provider-owned.

Consumers do not maintain authoritative duplicates.

#### 20.1 Provider Authority

The provider stores the authoritative contract in its `03_Contracts/` area.

#### 20.2 Consumer Declaration

Consumers identify external contracts they consume in `PROJECT_PROFILE.md`.

#### 20.3 Contract Change Assessment

Before approving a provider-owned contract change:

1. identify all declared consumers;
2. assess the change as compatible or potentially breaking for each;
3. determine whether implementation/expectation is affected;
4. identify required consumer follow-up;
5. resolve material compatibility risk required for approval.

Full consumer testing is not automatic.

Validation depth is proportionate to actual contract delta and credible risk.

A provider-owned contract is not approved in isolation from its declared consumers.

#### 20.4 Cross-Product Dependency Boundary

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

## Part VI — Assurance and Governance Operations

### 21. Audit Model

Audit is a periodic assurance backstop.

It does not replace normal knowledge capture.

#### 21.1 Scope

Each audit defines explicit scope and must not silently expand.

Where the size, risk or execution method of an engagement warrants it, the audit may define:

- batch sizes;
- review checkpoints;
- pause-for-approval points;
- other bounded execution controls.

These controls belong to the applicable audit work instruction or engagement definition rather than becoming permanent central values.

#### 21.2 Engagement Folder

Each formal audit/AAR has its own `07_Audit/` subfolder.

#### 21.3 Review Log

The Review Log is the authoritative audit population and progress record.

It must:

- uniquely identify every in-scope item;
- record sufficient review state to determine the outcome for each item;
- provide sufficient information to establish, without relying on agent memory, whether the complete defined population was reviewed.

Audit completeness is determined from the Review Log, not agent memory or scattered comments.

Required Review Log fields are defined in Appendix E.

#### 21.4 Reviewed Versus Archive Ready

A review label means an issue was included and reviewed.

It does not mean the issue is archive-ready.

`Reviewed` and `Archive Ready` are distinct concepts.

Archive readiness is determined under Appendix E.

#### 21.5 Findings

Audits use the findings taxonomy in Appendix E.

Substantive governed fixes proceed through normal Linear/Git workflow rather than invisibly inside the audit.

#### 21.6 Audit Completion

An audit completes when:

- defined population is reviewed;
- Review Log is complete;
- findings are resolved or explicitly deferred;
- final audit state is recorded;
- required engagement labels/checkpoints are applied.

Detailed audit reference requirements are defined in Appendix E.

---

### 22. Governance Deployment

Approved central governance is maintained in the central Governance Git/GitHub repository.

Central governance artefacts required locally by product agents are distributed into the centrally managed product subtree:

`00_Governance/01_Central/**`

Content within that subtree remains centrally owned and must not be locally altered by product work.

Governance distribution is deployment of already-approved central content, not a new substantive governance decision and not a second approval step.

The central Governance repository owns the authoritative recipient population, deployment projection and distribution-control artefacts used to perform automated central-governance distribution.

Each distribution event is governed operationally through Linear.

The detailed control model for automated distribution, including recipient selection, projection semantics, version provenance, pre-flight validation, downstream PR handling, idempotency, rollout-state handling and completion rules, is defined in **Appendix G — Central Governance Distribution Control Model**.

#### 22.1 Source

The authoritative source of every centrally deployed governance artefact is its approved location in the central Governance repository.

The deployed product projection contains:

```text
00_Governance/01_Central/
├── CENTRAL_GOVERNANCE.md
├── 01_Standards/
│   └── ARCHITECTURE_DIAGRAM_STANDARD.md
└── 02_Templates/
    ├── PROJECT_PROFILE.template.md
    └── DIAGRAM_CONVENTION_LEARNING.md
```

The authoritative global DDR allocation registry remains:

`/DDR_REGISTRY.md`

in the central Governance repository and is not part of the deployed product projection.

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

After substantive approval and applicable validation, squash merge of the accepted Governance pull request to `main` is the substantive approval boundary and automatically initiates the governed post-approval release and distribution process.

The automatic process must:

1. take the source Governance pull-request number and exact merge commit from the merged pull-request event;
2. independently verify that the pull request was merged to `main` and that its recorded merge commit matches the triggering event;
3. identify every projected artefact changed by the merged pull request;
4. create each changed artefact's declared approval tag against that exact merge commit where the tag does not already exist;
5. verify and reuse an existing declared tag only where it already resolves to that exact merge commit;
6. fail without moving or overwriting any declared tag that resolves elsewhere;
7. verify each changed artefact's tag, version, approval metadata and content;
8. derive the complete release set from all projected artefacts at that merge commit under Appendix G;
9. continue automatically into governed downstream distribution.

Multiple independently versioned artefacts changed by one pull request may legitimately have different approval tags resolving to the same merge commit.

The deterministic post-approval release and distribution process does not require a second substantive governance approval.

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

Detailed automated-distribution controls are defined in Appendix G.

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

Under the normal automated route, the Linear issue declared in the source Governance pull request remains the operational authority for the complete post-approval release and distribution event.

That issue governs:

- the approved Governance change;
- the source Governance pull request and exact merge commit;
- the complete projected artefact-to-approval-tag release set;
- downstream distribution to the governed product population;
- per-product rollout results; and
- completion of the automatic rollout.

A separate Linear rollout issue is not required for the normal automatic distribution path.

Where a deferred, staged, exceptional or otherwise independently governable follow-up requires work beyond the automatic release event, a separate Linear issue may be created for that follow-up.

Such a follow-up issue:

- tracks deployment or remediation of already-approved governance;
- does not reopen substantive approval of the governance content;
- does not require `Change: Governance` solely because it distributes unchanged approved artefacts; and
- must remain traceable to the original approved Governance release event.

#### 22.11 Governance Content-Change Completion Boundary

Under the normal automated route, the governing central-governance issue reaches `Done` only when:

1. the accepted governance content has been merged;
2. every required changed-artefact approval tag has been created or validly reused and verified;
3. the complete release set has been derived and recorded against the governing Linear issue;
4. automatic downstream distribution has been executed for the governed product population; and
5. every targeted product has reached an acceptable terminal rollout state under Appendix G.

The acceptable terminal states are:

- `merged`;
- `no_change`;
- explicitly `deferred`; or
- explicitly `excluded`.

A blocked, failed or still-open deployment keeps the governing issue incomplete.

Creation of an approved governance version and deployment of that version remain distinct lifecycle concepts, but under the normal automated route they form one continuous governed release event before the governing issue reaches `Done`.

#### 22.12 Permanent Governance Change and Distribution

Permanent governance changes follow the applicable workflow profile, Appendix A transition gates, Appendix B change-class controls and, for changes to `CENTRAL_GOVERNANCE.md`, Appendix C approval requirements.

Following human acceptance, applicable validation and merge to `main`, the normal governed route automatically performs approval-tag creation or verification, complete release-set derivation and downstream distribution under Appendix G.

A separate rollout issue is required only where subsequent deployment or remediation has become an independently governable piece of work under Section 22.10.

Automatic post-merge distribution must not bypass or replace substantive human approval of the Governance change itself.

#### 22.13 Drift

A locally altered, misplaced, mismatched, incomplete or untraceable artefact within `00_Governance/01_Central/**` is a governance-integrity issue.

Restore the applicable approved central artefact rather than preserve local divergence.

Product-local work must not resolve such drift by editing centrally managed content.

#### 22.14 Centrally Governed Standard Lifecycle

A centrally governed standard may be changed without changing or releasing a new version of `CENTRAL_GOVERNANCE.md`, provided the change does not require alteration of the rule book itself.

Changes to the Architecture Diagram Standard follow the applicable workflow profile, Appendix A transition gates and Appendix B change-class controls.

The issue must identify the standard being changed and use the applicable change classes.

A change to the Architecture Diagram Standard must include `Change: Governance`; `Change: Documentation` may also apply where appropriate, and other applicable change classes may also be used.

The standard retains its own independent version, approval tag and approval lifecycle.

Standard tags use:

`diagram-standard-vX.Y.Z`

Approval of a new diagram-standard version does not change the version of `CENTRAL_GOVERNANCE.md`.

An approved standard may be distributed independently of a `CENTRAL_GOVERNANCE.md` release and is deployed unchanged to:

`00_Governance/01_Central/01_Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`

Distribution is deployment of an already-approved standard, not reapproval of that standard.

Deployment validation is limited to:

- correct approved source version;
- correct target path;
- exact content/integrity;
- successful distribution to the intended products; and
- traceable rollout state.

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

#### 23.4 Superseded Validators

Superseded/transitional validators are retired, removed or clearly marked non-authoritative.

Conflicting overlapping validators require authority resolution rather than automatic execution of both.

#### 23.5 Runtime Assumptions

Environment assumptions such as OS, PowerShell version, locale, date parsing, file layout and dependency versions should be explicit where relevant.

Regression checks tied to those assumptions run when those assumptions or tooling change, not automatically after unrelated changes.

---

### 24. Production Evidence and Tool Routes

Where current production evidence is required, agents use the approved evidence route before declaring evidence unavailable or work blocked.

#### 24.1 Evidence Route

For Home Assistant:

1. designated HA MCP connection for the relevant environment;
2. approved read-only snapshot/retained evidence where direct access is unavailable or inappropriate;
3. another explicitly approved project evidence source.

#### 24.2 Capability Check

Before declaring a capability unavailable, check:

- available tools;
- deferred/connected tools;
- Project Profile;
- central governance;
- known environment-specific route.

The first failed attempt is not sufficient to declare a blocker.

#### 24.3 Freshness

Live evidence represents current state.

Snapshots represent their recorded capture time.

Where freshness affects a decision, sufficiently current evidence is required.

#### 24.4 Production Versus Architecture

Production evidence shows what is implemented.

Architecture shows what is approved.

A discrepancy is surfaced rather than silently resolved.

#### 24.5 Retained Production Evidence

Retained production snapshots or captures are immutable read-only evidence.

Do not:

- edit them;
- rename or restructure their contents to make them easier to use;
- regenerate them in place;
- retrospectively correct them;
- use them as a working directory;
- treat a later interpretation as though it formed part of the original capture.

Before relying on retained evidence, consider its recorded:

- source;
- capture time;
- scope;
- inclusions and exclusions;
- completeness;
- integrity information;
- known limitations.

If a capture is deficient, record the limitation or create a new authorised capture.

Do not retrospectively alter the original evidence to remove the deficiency.

#### 24.6 Scope and Reuse

Gather only evidence needed for current scope and risk.

Reuse sufficiently current evidence already established for the same work item where valid.

#### 24.7 Production Mutation Boundary

Production evidence access is read-only by default.

Availability of a write-capable tool does not authorise mutation.

For ordinary implementation work, a live-state mutation, service call, reload, restart or configuration change requires:

- the mutation to fall within the governing Linear issue scope;
- applicable governance gates to have passed;
- required explicit user authorisation.

For beta or stable deployment, authority may instead arise directly from the applicable beta/release rule together with the required explicit user deployment authorisation.

This permits a Simple Release without inventing a separate Linear release issue.

Where practical, local, static or otherwise non-mutating validation should precede controlled runtime mutation.

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

Their detailed contents, evidence sources and dispositions are defined in Appendix F.

A monitoring item only alters governance if it is formally promoted through the governance-improvement process and approved centrally.

#### 26.1 Diagram Convention Review

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

1. it meets the eligibility criteria in Section 9.7; and
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

Section 12.8 additionally governs preservation of pre-merge validation evidence where squash merge changes Git commit identity without changing governed content.

---

### Appendix B — Authoritative Change-Class Control Matrix

This appendix is the **single authoritative source for change-class-specific controls**.

Where an issue has multiple change classes, applicable controls are cumulative unless explicitly incompatible or inapplicable.

The workflow profile determines which workflow gates apply. The assigned change classes determine the additional controls that must be satisfied at those gates or workflow points.

#### B.1 Preparation and Review Controls

| Gate | Code | Architecture | Contract | Governance | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|
| **G0** | Code scope/runtime objective identifiable | Architectural concern/boundary identifiable | Provider/consumer relationship identifiable | Governance scope identifiable | DDR need identifiable where already known | Durable-document scope identifiable | Diagram/visual scope identifiable |
| **G1** | — | — | — | — | — | — | — |
| **G2** | Linked PR pushed; implementation ready for human review | Authoritative architecture change reviewable | Contract delta and declared-consumer impact identifiable | Governance change reviewable; Appendix C preparation applies only where `CENTRAL_GOVERNANCE.md` is being changed; separately governed standards follow Section 22.14 | DDR and registry change reviewable | Durable documentation reviewable | Final or near-final visual artefact available for human visual review |
| **G3** | Human code approval | Human acceptance of architectural substance | Human acceptance plus proportionate consumer compatibility assessment | Human acceptance of governance change | Human acceptance of durable decision record | Human acceptance of the final intended documentation state | Human visual acceptance of final intended state; Architecture Diagram Standard conformity reviewed where applicable |
| **G4** | Applicable tests/technical checks identified | Applicable architecture consistency and authority checks identified | Compatibility validation requirements identified | Governance structure/integrity checks identified | Identifier, registry and supersession checks identified | Applicable integrity/document checks identified | Applicable integrity/provenance and standard-conformity checks identified |

#### B.2 Validation and Completion Controls

| Gate / point | Code | Architecture | Contract | Governance | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|
| **Validation activity** | Applicable tests/technical checks pass; candidate suitable for merge/Beta | Applicable architecture consistency and authority checks pass | Compatibility risk resolved; consumer validation only where justified | Governance structure/integrity checks pass; Appendix C requirements apply only where `CENTRAL_GOVERNANCE.md` is being changed; separately governed standards satisfy Section 22.14 | Identifier, registry and supersession consistency pass | Only applicable integrity/document checks | Exact final accepted bytes/content used for integrity/provenance checks; Architecture Diagram Standard conformity confirmed where applicable |
| **G5** | PR squash-merged to `main`; resulting SHA identified; user authorises beta deployment; exact SHA deployed to `ha-starburst`; deployed state verified | If part of same issue, architecture obligations already satisfied before Beta | If part of same issue, compatibility obligations already satisfied before Beta | If part of same issue, governance obligations already satisfied before Beta | If part of same issue, DDR obligations already satisfied before Beta | If part of same issue, durable-document obligations already satisfied where required | If part of same issue, final accepted diagram obligations already satisfied |
| **G6** | Beta succeeds against exact deployed candidate state; result remains traceable | — | — | — | — | — | — |
| **G7** | — | Accepted architecture state merged | Accepted contract state merged | Accepted governance state merged; Appendix C post-merge requirements apply only to `CENTRAL_GOVERNANCE.md` changes; separately governed standards complete under Section 22.14; distribution follows Section 22 where within scope | DDR and registry state merged | Accepted durable documentation merged | Exact visually accepted content merged |

#### B.3 Rework and Exception Controls

| Gate | Code | Architecture | Contract | Governance | DDR | Documentation | Diagram |
|---|---|---|---|---|---|---|---|
| **G8** | Pre-merge correction normally continues same branch/PR. Failed Beta correction uses same Linear issue but new corrective branch/PR | Substantive correction returns through human review | Contract meaning/compatibility correction returns through human review | Governance-substance correction returns through human review | Decision-substance correction returns through human review | Substantive correction returns through human review where required | Semantic/visual-meaning correction returns through human visual review |
| **G9** | Technical-only correction may bypass repeated review only where code behaviour remains unchanged | Metadata/provenance-only correction | Metadata/provenance-only correction | Technical packaging/approval-metadata correction where governance substance is unchanged | Registry/metadata-only correction where decision is unchanged | Non-substantive technical correction | Integrity/provenance regeneration against unchanged accepted content |
| **G10** | — | — | — | — | — | — | — |

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

### Appendix D — DDR Standard

#### D.1 Purpose

A DDR records a significant durable design decision and why it was made.

It is not a task log or general implementation journal.

#### D.2 Global Numbering

DDRs use:

`DDR-###`

The authoritative global allocation register is:

`/DDR_REGISTRY.md`

in the central governance repository.

The registry contains at minimum:

| DDR | Product | Title | Status |
|---|---|---|---|

#### D.3 Allocation

When a new DDR is required:

1. read the latest authoritative registry state;
2. determine the next available global number;
3. update the registry as part of the governed work;
4. create the DDR in the owning product's `02_Decisions/` folder;
5. ensure registry and DDR remain consistent through review and merge.

If concurrent work causes an allocation conflict:

1. refresh the latest registry state;
2. reallocate the losing/conflicting DDR to the next valid number;
3. update affected references before merge.

A separate reservation spreadsheet or reservation ceremony is not required.

Git conflict/merge control provides the normal concurrency safeguard.

#### D.4 Required DDR Content

Each DDR contains at minimum:

- identifier and title;
- status;
- decision;
- context;
- material alternatives considered where relevant;
- rationale;
- consequences/trade-offs;
- source Linear issue;
- superseded DDR where applicable.

#### D.5 Status

Allowed DDR statuses are:

- `Proposed` — decision is undergoing governed development/review;
- `Accepted` — governing work has completed and the decision record is authoritative historical evidence;
- `Superseded` — a later accepted DDR replaces the durable decision.

When a replacement DDR becomes accepted, the superseded DDR and central registry must be updated accordingly.

#### D.6 Supersession

When superseded:

- the old DDR remains preserved;
- the old DDR is marked `Superseded`;
- the new DDR identifies what it supersedes.

Historical decisions are not deleted merely because they are no longer current.

#### D.7 Approved DDR Immutability

Once accepted, a DDR must not be substantively rewritten.

A changed durable decision requires a new DDR that supersedes the earlier record.

Only traceable non-substantive corrections that leave the decision, rationale, alternatives and consequences unchanged may be made to an accepted DDR.

#### D.8 Architecture Relationship

Architecture must describe the current approved design without requiring agents to reconstruct it from DDR history.

DDRs preserve significant rationale, not the complete current architecture.

---

### Appendix E — Audit Reference

#### E.1 Review Log

The Review Log is the authoritative audit population/progress record.

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

#### E.2 Findings Taxonomy

Use:

- `Documentation Update`
- `DDR`
- `Investigation / Integrity`
- `Already Captured / No Finding`

The taxonomy may be refined centrally if operating evidence shows a need.

#### E.3 Reviewed Versus Archive Ready

`Reviewed` means the item was examined within the defined audit scope.

It does not mean the issue is archive-ready.

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

#### E.4 Audit Batch and Checkpoint Controls

An audit may define bounded execution controls appropriate to the engagement.

Examples include:

- maximum batch size;
- pause-for-user-review points;
- approval checkpoints;
- staged population release.

The applicable audit work instruction defines the actual values.

Central governance deliberately does not prescribe a universal batch size.

Where a batch/checkpoint control is defined, the agent must follow it and must not silently continue beyond the authorised boundary.

#### E.5 Findings Resolution

Substantive findings are resolved through normal governed Linear/Git work.

The audit itself records the finding and its disposition; it does not silently make untracked substantive fixes.

#### E.6 Audit Completion

An engagement completes only when:

- defined population is fully accounted for;
- Review Log is complete;
- findings are resolved or explicitly retained/deferred;
- final engagement state is recorded;
- required labels/checkpoints are applied.

Audit completion does not trigger unrelated broad revalidation.

---

### Appendix F — Monitoring Register

Monitoring items are hypotheses or operating-model questions, not mandatory controls.

#### F.1 Initial Monitoring Areas

Monitor:

- repeated context/Linear/tool reads;
- dependency traversal;
- context/token growth;
- user intervention;
- validation breadth;
- validation evidence reuse;
- stale or overlapping validators;
- multi-class issue cohesion;
- change-class clarity;
- DDR threshold/ceremony;
- audit effectiveness;
- provider-contract discoverability;
- branch/PR overhead for non-code;
- lightweight-route usage;
- beta/release/rollback reliability;
- Simple versus Managed Release selection;
- governance distribution/drift;
- AAR register usefulness.

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

### Appendix G — Central Governance Distribution Control Model

#### G.1 Purpose and Authority

This appendix defines the authoritative operational control model for automated distribution of approved central governance artefacts from the central Governance repository into governed product repositories.

It governs deployment mechanics only.

`CENTRAL_GOVERNANCE.md` remains the higher authority for governance meaning, ownership boundaries, approval requirements and lifecycle rules.

The deployment-control artefacts and executor must implement this appendix and must not redefine it.

#### G.2 Deployment-Control Artefacts

Automated distribution is controlled by:

`push_deploy/GOVERNED_PRODUCTS.yaml`

and:

`push_deploy/GOVERNANCE_PROJECTION.yaml`

These are authoritative operational artefacts within their defined scope.

They are maintained in the central Governance repository.

They are not deployed into product repositories.

They do not independently create substantive governance rules.

#### G.3 Governed Product Registry

`GOVERNED_PRODUCTS.yaml` defines the known product population for automated central-governance distribution.

Each product entry contains:

- `name`
- `repository`
- `central_governance`

Semantics are:

- present with `central_governance: true` — normal automated distribution target;
- present with `central_governance: false` — known product intentionally excluded from normal automated distribution;
- absent — not part of the governed product register for automated distribution.

The registry records recipient intent only.

Transient rollout state, deployment success/failure state and product-local governance content must not be recorded in the registry.

#### G.4 Governance Projection Manifest

`GOVERNANCE_PROJECTION.yaml` defines the centrally managed product projection.

Each entry contains:

- `source`
- `destination`

`source` identifies the authoritative central-repository artefact.

`destination` identifies the exact product-repository path.

Release selection must not be stored in the projection manifest.

The projection manifest defines the complete desired state of:

`00_Governance/01_Central/**`

for automated deployment.

#### G.5 Replacement Boundary

The deployment executor may add, replace or remove content within that subtree as necessary to make the product copy exactly equal to the defined projection.

It must not create, edit, move or delete content outside `00_Governance/01_Central/**`.

Content comparison, not version metadata alone, determines whether deployment is required.

#### G.6 Artefact Version Provenance

Each projected artefact declares its own version, approved status, approval tag and approval date within the artefact.

A single rollout may therefore contain centrally managed artefacts approved at different independent versions.

The underlying Git tag provides exact immutable source provenance.

A deployment event is identified by its source Governance pull request, merge commit and complete resolved artefact-to-tag release set rather than by any single artefact version.

The release process reads every projected artefact at the source pull request's merge commit and derives the complete current release set from the approval tag declared by each artefact.

The pull-request diff identifies which projected artefacts changed and therefore require approval tags at the merge commit. It must not be used to reconstruct the versions of unchanged projected artefacts.

#### G.7 Deployment-Event Authority

Every automated central-governance release and distribution event originates from a Governance pull request merged to `main`.

The immutable release event is identified by:

- the source Governance pull-request number; and
- that pull request's exact merge commit.

The event is operationally governed by the one Linear issue declared in the source Governance pull-request body as:

`Linear issue: <TEAM-KEY>-<NUMBER>`

The team key must not be hard-coded.

Exactly one syntactically valid identifier must be present in that field. The executor must validate through Linear that the issue exists and belongs to the Governance project.

Missing, malformed, ambiguous or invalid issue metadata must fail pre-flight.

The source pull request and merge commit establish the immutable Git release-event identity.

The Linear issue is the operational authority and rollout record for that event and governs the rollout as a whole rather than any individual projected artefact.

#### G.8 Global Pre-Flight

Before modifying any product repository, the deployment executor must validate the complete intended rollout.

Pre-flight must establish at minimum that:

- the source Governance pull request is merged and its merge commit is available;
- exactly one valid `Linear issue:` field identifies an existing issue in the Governance project;
- `GOVERNED_PRODUCTS.yaml` is valid;
- `GOVERNANCE_PROJECTION.yaml` is valid;
- every projected source exists at the source pull request's merge commit and declares valid independent release metadata;
- every declared approval tag exists in Git and contains the exact projected source artefact read at the merge commit;
- each changed projected artefact's approval tag resolves to the source pull request's merge commit;
- every destination is beneath `00_Governance/01_Central/**`;
- every selected target repository exists and is accessible.

If any global pre-flight check fails, the rollout must abort before any targeted product repository is modified.

#### G.9 Product Deployment Behaviour

For each registered product with `central_governance: true`, the executor compares the complete desired projection against the product repository's current default branch.

If the managed subtree already exactly matches the projection, the result is:

`no_change`

and no deployment PR is required.

Where deployment is required, the deployment branch is:

`governance/<governing_linear_issue>`

The branch is based on the product's current default branch.

Existing unrelated product feature branches must not be modified.

The resulting managed subtree must exactly match the projection.

#### G.10 Idempotency and Concurrency

The first run for a source Governance pull request derives and records the complete release set from that pull request's merge commit.

A rerun must recompute the release set from the same source pull request and merge commit and require it to match the recorded release set exactly.

A mismatch must fail without replacing the recorded release set.

An already-created approval tag may be reused only where it resolves to the expected commit and contains the expected artefact content. A tag that resolves elsewhere must never be moved or overwritten.

Re-running the same release event must reuse or update the existing deployment branch and pull request rather than creating duplicates.

Products already completed under the same release set must not be redeployed unnecessarily. Outstanding products resume using that same release set.

At most one open central-governance deployment PR may exist in a product repository under the normal automated route.

If a governance deployment PR for a different governing Linear issue is already open, the new deployment is blocked for that product.

The existing deployment PR must not be overwritten, combined with or repurposed for the new rollout.

#### G.11 Downstream Pull Request

Where deployment is required, the executor creates or updates a downstream PR identified by the governing Linear deployment issue.

The PR records at minimum:

- the governing Linear deployment issue;
- the source Governance repository;
- the source Governance pull request;
- the managed target subtree;
- each projected artefact;
- the corresponding approval tag.

The downstream PR is a deployment record for already-approved content, not a new substantive governance approval surface.

#### G.12 Validation and Automatic Merge

Before automatic merge, validation must prove that:

- no path outside `00_Governance/01_Central/**` is modified;
- the resulting managed subtree exactly matches the declared projection;
- projected source and approval-tag identities remain valid for the recorded release set;
- no unrelated product content is included.

A valid deployment PR may then be merged automatically.

If validation fails, the PR must not auto-merge.

A failed or unresolved merge is not a successful rollout state.

#### G.13 Rollout Results and Linear Completion

The deployment executor records one workflow-generated release-set comment on the governing Linear issue containing:

- the source Governance pull request;
- the exact source merge commit as the release-event identity; and
- the complete projected artefact-to-approval-tag release set.

Per-artefact commit SHAs are not required in Linear.

The executor also records a concise per-product result against the governing Linear issue.

Normal result states include:

- `no_change`
- `pr_created`
- `pr_updated`
- `merged`
- `blocked_existing_deployment`
- `failed`
- explicitly `deferred`
- explicitly `excluded`

The governing deployment issue may move automatically to `Done` only when every targeted product has reached an acceptable terminal state:

- `merged`
- `no_change`
- explicitly `deferred`
- explicitly `excluded`

Any blocked, failed or still-open deployment keeps the rollout incomplete.

#### G.14 Automatic Post-Approval Trigger

The normal authorised central-governance release and distribution route is the merged Governance pull-request event.

A Governance pull request merged to `main` automatically invokes the central release-and-distribution workflow.

A pull request closed without merge must not initiate release or distribution.

The workflow receives the source Governance pull-request number and exact merge commit directly from the GitHub merged-pull-request event.

Before release or downstream mutation, the executor must independently verify that:

- the source pull request was merged;
- its base branch was `main`;
- the merge commit recorded by GitHub matches the merge commit supplied by the triggering event; and
- exactly one valid `Linear issue:` field identifies an existing issue in the Governance project.

Merge following the applicable human-acceptance and validation gates is the substantive governance approval boundary.

The deterministic post-merge release and distribution process does not require a second manual deployment authorisation.

Manual selection of the source pull request or projected artefact approval tags is not part of the normal route.

A rerun must remain bound to the original source pull request, exact merge commit and complete recorded release set.
