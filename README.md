# MediaCat

MediaCat is a Home Assistant custom integration that provides governed media
catalogue lookup, Media Source browsing, and catalogue administration services.

## Installation

Add `83degrees/MediaCat` to HACS as a custom integration repository, install
MediaCat, and restart Home Assistant when prompted. The integration source is
published from `custom_components/mediacat/`; catalogue data and optional
package configuration are separate deployable units and are not installed by
HACS.

Governed Beta installations use the immutable tag supplied in the applicable
operator handoff. Stable installations use the normal HACS release flow.

## Configuration and operation

MediaCat currently loads its catalogue registry from
`/config/mediacat/catalogues/`. Supported services and exact interface promises
are documented in the provider-owned contracts under `03_Contracts/`.

Deployment authority, validation, rollback, and evidence requirements are
documented under `08_Deployment/`.
