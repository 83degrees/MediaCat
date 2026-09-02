# ASTV-65 Prepared Cutover Evidence

This directory is the inactive, pre-cutover evidence and recovery package for
ASTV-65. Nothing under it is an active Home Assistant configuration include.

## Config-root bundles

- `deployment/config/` contains the nine files to merge into Home Assistant
  `/config` only after explicit production go-live approval.
- `rollback/config/` contains the complete compatible nine-file schema-v2 and
  legacy-ASTV restoration set.
- `bundle-manifest.json` records every source, `/config` target, size, and
  SHA-256.
- `verify_bundles.py` proves both bundles are byte-equal to their governed
  sources.

Both config roots contain these exact targets:

- `custom_components/curated_media/__init__.py`
- `custom_components/curated_media/catalogue.py`
- `custom_components/curated_media/const.py`
- `custom_components/curated_media/manifest.json`
- `custom_components/curated_media/media_source.py`
- `custom_components/curated_media/resolver.py`
- `custom_components/curated_media/services.yaml`
- `curated_media/catalogue.yaml`
- `assistive/astv_intent_catalogue.yaml`

## AdvMedia rollback

`rollback/advmedia-live/` contains the exact six live script definitions and
configuration hashes captured before cutover. The new
`script.advmedia_process_media_record` and
`script.advmedia_translate_media_source` IDs were absent and are recorded as
such in `live-script-inventory.json`.

AdvMedia deployment and restoration are performed through Home Assistant's
script configuration interface, not by copying files into `/config`.

## Emergency backup

The verified full Home Assistant backup is
`Before_ASTV-65_MediaCat_v3_Cutover`, backup ID `e3398ae8`. It includes Home
Assistant configuration and excludes the recorder database. It is the
last-resort recovery path only if Core does not return and the targeted rollback
cannot be coordinated through the normal interfaces.

## Atomic rollback

Any immediate cutover failure restores the complete `rollback/config/` set and
all six captured AdvMedia definitions as one compatible unit. The two newly
introduced AdvMedia scripts are removed if they were installed. Do not retain a
schema-v3 catalogue, a partial seven-record ASTV replacement, or a mixed
AdvMedia package.

## Cutover attempt

The 2026-08-24 activation attempt failed the paused compatibility health gate
and was atomically rolled back before normal ASTV media requests resumed. See
`CUTOVER_ATTEMPT_2026-08-24.md` for the failure and restoration evidence.
