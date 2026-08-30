# Architecture Diagram Standard v1.0

## Status and purpose

This is the approved Governance 2.0 target representation standard for shared
architecture-diagram construction and presentation. It is not product
architecture authority and does not make Governance 2.0 operational.

The approved product `*_ARCHITECTURE.md` defines semantic architecture. A
diagram represents that authority and must not introduce architecture,
ownership, interfaces, behaviour, or returns of its own.

## General principles

- Preserve existing diagrams through the smallest authorized change where
  possible. Do not opportunistically move, resize, rename, delete, restyle,
  reroute, compact, crop, centre, symmetrize, or clean up unrelated objects.
- Represent actual approved relationships only. Do not add components or flows
  for visual convenience.
- Keep external systems distinguishable. Do not depict foreign internals as
  though the local product owns them.
- Prefer layout clarity and readable local grouping over symmetry.
- Architecture determines the canvas and layout; the canvas must not constrain
  or invent architecture.
- Minimise crossings, unnecessary bends, long loops, diagonals, and decorative
  routing. Preserve deliberate whitespace where it improves comprehension.
- Use exact governed product, component, service, field, and interface names.

Product-local colours, gateway sizes, phase bands, fonts, and other established
local conventions are outside this central standard. Preserve them where they
exist, but do not promote them to shared rules.

## Boundaries and ownership

Show product boundaries, ownership, calls, meaningful returns, external
systems, and data sources clearly when they are relevant to the represented
architecture. A consumer may show its governed relationship with a provider,
but must not expand the provider into unowned internal detail.

Use the authoritative provider-owned contract name for a cross-product
interface. A diagram label or convenient local term must not create a parallel
contract authority.

## Gateways

Use a diamond only for a genuine control-flow gateway:

- **Exclusive split:** one incoming flow and mutually exclusive outgoing
  branches. Label each outcome on its outgoing connector.
- **Exclusive merge:** multiple mutually exclusive inputs converge into one
  output. A merge is convergence only; do not depict a function, script,
  transformer, or consolidator as a merge diamond.
- **Parallel or synchronisation gateway:** use only for genuine parallel work or
  synchronisation and mark the gateway with `+`.

Do not use a gateway merely because a caller invokes several functions. Gateway
placement may be offset when that makes routing clearer.

## Calls, returns, and connectors

- One invocation is represented by one solid directional call connector.
- Never draw one connector per variable.
- A meaningful return is a separate dashed directional connector.
- Never combine call and return into a double-headed connector.
- Do not invent a return that the governed architecture or contract does not
  define.
- Keep call and return routes visually distinct.
- Prefer straight or simple orthogonal routes and clear 90-degree turns.

Sequence alone does not prove that sibling functions call one another. Connect
the components that actually communicate.

## Variables and connector labels

- Each represented variable has its own bordered connector-native label.
- Multiple variables use multiple separate labels on the same connector.
- Never use one combined payload label.
- Never use a detached label shape as a substitute for a connector-native
  label.
- Preserve exact governed names. A caller capture name may legitimately differ
  from the returned field name and must not be normalized for visual
  consistency.
- Decision outcomes use native labels on their outgoing connectors and remain
  close enough to the gateway to preserve their association.

Labels must remain readable, visually associated with the correct connector,
and clear of components and unrelated connectors.

## Editing control and supporting outputs

Only one editor may write or save a `.drawio` file at a time. Before editing,
confirm that no other editor will save concurrently and reread the latest saved
file. Preserve established manual layout and styles except where the approved
change requires an adjustment.

PNG and PDF exports are supporting outputs only unless separately governed.
They do not replace the editable diagram or the approved architecture Markdown.

## Review checks

Architecture correctness and diagram-standard conformity are separate checks.
A diagram change is ready for validation only when reviewers can confirm:

1. every represented component, boundary, relationship, call, return, variable,
   and outcome matches the approved architecture and applicable contract;
2. no foreign internals, ownership, interface, variable, or return was invented;
3. gateway semantics and call/return connector conventions are correct;
4. every represented variable has a separate bordered connector-native label;
5. existing product-local conventions and unrelated layout were preserved;
6. routing is readable without unnecessary crossings, bends, or decorative
   loops; and
7. the editable source was saved by a single active editor and any supporting
   exports are clearly non-authoritative.
