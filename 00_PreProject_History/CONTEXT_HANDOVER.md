# MediaCat – Pre-Project Context Handover

## Purpose

This document preserves the important context, decisions, current-state understanding, and unresolved architectural questions that existed before MediaCat was established as a dedicated project.

It is historical context only.

It does not override:

1. current production evidence;
2. current interface contracts;
3. approved architecture documentation;
4. applicable `AGENTS.md` governance.

Where this document conflicts with current production evidence, production evidence is authoritative.

---

## Product Identity

The product is named **MediaCat**.

MediaCat is a separate product from:

- ASTV;
- AdvMedia.

**Curated Media** is one catalogue within MediaCat.

Curated Media must not be treated as the name of the MediaCat product itself.

The MediaCat product may ultimately support multiple catalogues.

---

## Original Development Context

The functionality that is now being separated into MediaCat originally developed as part of broader Home Assistant media work.

The early implementation was associated with a catalogue/integration referred to as `curated_media`.

That implementation evolved from earlier custom-radio work and became capable of holding structured media records including:

- media item identifiers;
- titles;
- media types;
- playable source information;
- artwork;
- descriptions;
- tags;
- categories.

The current production implementation and its exact schema must be verified from production evidence before architectural or implementation decisions are made.

---

## Reason for Creating a Separate MediaCat Project

MediaCat is being separated from AdvMedia because its responsibilities have developed into a distinct product boundary.

MediaCat is expected to own information about:

- media identity;
- catalogue membership;
- metadata;
- available ways of obtaining or delivering a media item.

This is distinct from:

- ASTV orchestration and endpoint-selection policy;
- AdvMedia media execution.

MediaCat may eventually support multiple catalogues, of which Curated Media is one.

---

## Emerging Media Route Model

A key design requirement identified before project creation is that one logical media item may have multiple delivery routes.

For example, a request for BBC Two could potentially be satisfied through:

- a television tuner;
- BBC iPlayer;
- another future delivery mechanism.

Therefore MediaCat should distinguish between:

- the logical media item;
- the available routes through which that item can be delivered.

A route may contain provider- or mechanism-specific information required for downstream execution.

The exact route schema has not yet been designed or approved.

---

## ASTV Responsibilities

The current architectural understanding is that ASTV is the household intent and orchestration layer.

ASTV already contains logic relating to:

- intent;
- area resolution;
- playback/output domain;
- endpoint preference;
- fallback / pecking-order behaviour.

For a given area and domain, ASTV has been designed so that one device or method can take precedence, with fallback to other configured choices when the preferred option is unavailable.

This preference and fallback policy is considered an ASTV responsibility.

---

## AdvMedia Responsibilities

AdvMedia is the downstream media execution system.

Production evidence indicates that ASTV has already selected the target endpoint by the time AdvMedia is called.

The current ASTV-to-AdvMedia handoff includes information such as:

- media item identifier;
- media catalogue;
- media player;
- optional media profile.

Therefore endpoint resolution must not be assumed to be an AdvMedia responsibility.

The exact current production flow must continue to be verified against production evidence and the current ASTV–AdvMedia interface contract.

---

## Current Catalogue Resolution Behaviour

The current design assumes that AdvMedia is responsible for interrogating the existing catalogue and obtaining the media record required for playback.

This is the current-state architectural assumption and should not be changed without explicit design and implementation work.

---

## Design Issue Discovered During Pre-Project Discussion

A significant architectural issue was identified during discussion of multiple delivery routes.

If ASTV is responsible for selecting the preferred endpoint/method before AdvMedia is called, ASTV may need to know which delivery routes are actually available for the requested media item.

For example:

- ASTV may prefer a TV tuner for `playback.video`;
- a secondary preference may be an application-based route;
- MediaCat may know that a particular media item is available through both routes.

ASTV cannot correctly apply its preference/fallback policy if route availability is known only after the AdvMedia handoff.

This exposes a possible future change to the MediaCat interaction model.

---

## Agreed Future Design Direction

The following has been agreed as a **design direction for investigation**, not as an authorised production change.

A future architecture may work as follows:

1. ASTV identifies the requested logical media item.
2. ASTV queries MediaCat for the available routes for that item.
3. MediaCat returns route-selection information.
4. ASTV compares those available routes against its existing area/domain preference and fallback order.
5. ASTV selects the preferred viable route and endpoint.
6. ASTV passes a reference to the selected route, together with the selected endpoint and media request, to AdvMedia.
7. AdvMedia retrieves the execution-specific details for that selected route from MediaCat.
8. AdvMedia performs playback.

Under this model:

- MediaCat advertises available routes;
- ASTV makes the household policy/orchestration decision;
- AdvMedia performs the selected execution.

---

## Important Constraint

The above future design must **not** be implemented merely because it is documented here.

The current production architecture remains authoritative.

The immediate creation of the MediaCat project must be separated from any restructuring of the ASTV–AdvMedia runtime flow.

The intended approach is:

1. establish MediaCat as a dedicated governed project;
2. capture and validate the current production state;
3. design the MediaCat data model;
4. identify appropriate interfaces;
5. test the proposed architecture against real use cases;
6. create formal contracts;
7. only then consider controlled migration.

No big-bang refactor is intended.

---

## Existing ASTV Media Knowledge

A significant amount of media-specific information is currently baked into the existing ASTV intent catalogue.

This may include information that could ultimately belong in MediaCat.

The existing ASTV catalogue should therefore be treated as an important source of:

- production evidence;
- MediaCat requirements;
- migration requirements.

Information must not simply be moved out of ASTV.

Each relevant field should eventually be classified according to whether it belongs to:

- ASTV;
- MediaCat;
- AdvMedia;
- temporary compatibility/migration behaviour.

---

## Emerging Ownership Principles

The following principles were agreed during the pre-project discussion.

### ASTV

ASTV should own information and behaviour answering questions such as:

- What does the user want?
- In which area?
- What output/playback domain applies?
- Which endpoint or method has priority in that area?
- What is the fallback order?
- Which viable route/endpoint should be selected?

### MediaCat

MediaCat should own information answering questions such as:

- What is this media item?
- Which catalogue contains it?
- What metadata describes it?
- Through which routes can it be obtained?
- What route-specific data exists?

### AdvMedia

AdvMedia should own behaviour answering questions such as:

- How do I execute this already-selected media request?
- How should the selected route be translated into actions for this endpoint/profile?
- What execution-specific information is needed to perform playback?

These principles are architectural guidance and do not authorise immediate refactoring of current production.

---

## Proposed MediaCat Consumer Interfaces

The discussion suggested that MediaCat may ultimately expose two distinct types of interaction.

### Route Discovery

Used by ASTV to determine which routes are available for a logical media item.

This interface should expose only the information needed for route selection and should avoid unnecessarily coupling ASTV to MediaCat’s internal execution schema.

### Route Execution Data

Used by AdvMedia after ASTV has selected a route.

This interface would return the detailed provider/mechanism-specific information required to execute the selected route.

The exact interfaces, payloads, names, and return structures remain unresolved.

---

## Unresolved Questions

The following questions remain intentionally open:

- What is the canonical MediaCat media-item schema?
- What is the route schema?
- How are route identifiers represented?
- What constitutes a catalogue?
- Can an item belong to more than one catalogue?
- Which media aliases belong in ASTV versus MediaCat?
- What MediaCat information does ASTV need for route selection?
- What MediaCat information does AdvMedia need for route execution?
- Should ASTV and AdvMedia use separate MediaCat functions/interfaces?
- How should route availability be determined?
- How should unavailable routes be represented?
- How should the existing ASTV intent catalogue be migrated over time?
- How should the existing `curated_media` integration evolve?
- Should its Home Assistant integration/domain name eventually change?
- What compatibility period is needed?
- What cross-project contracts will ultimately be required?

These should be resolved through governed MediaCat architecture and design work rather than assumed during implementation.

---

## Project Operating Model

MediaCat should use the same working model already established for ASTV.

### ChatGPT

Primary role:

- architecture;
- design discussion;
- requirements;
- governance;
- work definition;
- review.

### Linear

Primary role:

- backlog;
- authorised work;
- workflow status;
- implementation/test tracking.

### Codex

Primary role:

- builder;
- tester;
- repository implementation work.

### Local Repository

Primary role:

- durable project context;
- architecture;
- governance;
- design records;
- implementation artefacts.

### Production Evidence

Shared read-only production evidence remains outside the MediaCat repository under the wider Home Assistant project structure.

---

## Governance Intent

MediaCat should inherit the same governance philosophy used for ASTV:

- production evidence before assumptions;
- explicit source-of-truth hierarchy;
- shared contracts at product boundaries;
- read-only production snapshots;
- controlled implementation through Linear;
- Codex as builder/tester;
- ChatGPT as design/governance workspace;
- no silent cross-project refactoring;
- no confusing proposed architecture with implemented architecture.

---

## Initial Project Goal

The initial MediaCat project goal is **not** to restructure production.

The initial goal is to:

1. establish the project and governance;
2. capture pre-project context;
3. establish current production evidence;
4. document the current MediaCat-related implementation;
5. identify the existing interfaces and dependencies;
6. establish an authoritative current-state architecture;
7. then begin deliberate target-state design.