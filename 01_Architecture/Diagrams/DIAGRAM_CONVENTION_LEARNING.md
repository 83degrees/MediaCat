# MediaCat Diagram Convention Learning

## Status

This file records MediaCat-local visual conventions observed in the current
governed diagram. It does not define architecture and does not amend the central
Architecture Diagram Standard.

## Established MediaCat-local conventions

- The diagram separates verified caller boundaries, the MediaCat product
  boundary, the deployed Curated Media runtime boundary, and external sources.
- The deployed runtime is divided into catalogue load and storage, normalized
  lookup, and Home Assistant Media Source regions.
- Yellow cylinder shapes are used for the catalogue source and immutable loaded
  catalogue snapshot.
- Green is used for the normalized lookup action and the ASTV lookup-caller
  boundary; orange is used for the standalone AdvMedia caller boundary.
- Purple is used for the Home Assistant Media Browser and Media Source flow.
- Neutral grey is used for direct source facts and the external Radio Browser
  Media Source provider.
- Applicable boxes show both friendly descriptions and technical action,
  function, path, or identity names.
- External-owned ASTV, AdvMedia, Home Assistant, and Radio Browser elements are
  shown only at the MediaCat-facing boundary and are not expanded into unowned
  internals.
- Current-production scope and evidence limitations are stated directly on the
  diagram; historical and future topology is excluded.

Shared connector, variable-label, gateway, boundary, editing, and review rules
remain defined only by
`00_Governance/01_Central/01_Standards/ARCHITECTURE_DIAGRAM_STANDARD.md`.
