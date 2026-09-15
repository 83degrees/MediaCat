# ASTV-225 Legacy Namespace Retirement and Rollback

## Authority and intended final state

This procedure defines the controlled Beta deployment and rollback route for
ASTV-225. It does not itself authorize a Home Assistant configuration change,
file removal, restart, or deployment. Perform live actions only after the
reviewed candidate is accepted, integrated into persistent `beta`, and the user
has authorized that exact Beta deployment.

The intended final state loads only:

- `/config/custom_components/mediacat/`;
- `/config/mediacat/catalogue.yaml`;
- the `mediacat` Home Assistant configuration entry; and
- the `mediacat.resolve_item` and `mediacat.resolve_media_record` actions.

Logical `catalogue_id: curated_media` and `returned_record_version: 1` remain
unchanged. Historical and rollback evidence is retained without loading the
legacy runtime.

## Pre-removal gate and rollback capture

Before deleting any live legacy path:

1. Record the exact accepted MediaCat `beta` commit and the deployed ASTV and
   AdvMedia candidate identities.
2. Confirm current AdvMedia and ASTV definitions call
   `mediacat.resolve_media_record` and representative playback still succeeds.
3. Search active Home Assistant configuration, packages, scripts, automations,
   dashboards, and external deployment sources for `curated_media.*`,
   `media-source://curated_media`, `/config/custom_components/curated_media`,
   and `/config/curated_media`.
4. Classify each match. Stop if any active dependency remains; do not classify
   logical `catalogue_id: curated_media` or historical evidence as a runtime
   dependency.
5. Capture a restorable copy of the complete live legacy component directory,
   catalogue directory, and configuration entry from the last accepted
   pre-retirement state. Record file hashes, configuration identity, Home
   Assistant version, capture time, and storage location.
6. Verify the rollback copy contains the compatible component, catalogue, and
   activation configuration together. A catalogue-only copy is insufficient.
7. Run the environment's Home Assistant configuration check and stop on
   failure.

## Beta removal and validation

1. Deploy the accepted candidate's `/config/custom_components/mediacat/` and
   `/config/mediacat/catalogue.yaml` without changing catalogue contents.
2. Remove the live `curated_media:` configuration entry if present.
3. Remove `/config/custom_components/curated_media/`.
4. Remove `/config/curated_media/` only after the active-reference scan proves
   that nothing still reads that path.
5. Run Home Assistant configuration validation. Stop and roll back on failure.
6. Restart or reload Home Assistant using the minimum environment-supported
   action required for component discovery.
7. Confirm `mediacat.resolve_item` and `mediacat.resolve_media_record` are
   registered, and confirm no `curated_media.*` action or
   `media-source://curated_media` root remains.
8. Validate representative normalized lookups for URL, delegated Media Source,
   and assistant-command records. Confirm `catalogue_id: curated_media` and
   `returned_record_version: 1` in the returned records.
9. Validate MediaCat browse, search, direct resolution, delegated resolution,
   and recursion rejection under `media-source://mediacat`.
10. Run representative AdvMedia standalone and ASTV end-to-end playback.
11. Record exact deployed state, every validation result, any post-validation
    state change and targeted revalidation, evidence limitations, and rollback
    disposition in ASTV-225.

## Rollback triggers

Roll back if any of the following occurs after legacy removal:

- Home Assistant configuration validation or startup fails;
- either required `mediacat` action is absent or fails;
- MediaCat catalogue loading or Media Source behaviour fails;
- AdvMedia or ASTV playback fails because the MediaCat provider is unavailable;
- an active dependency on the retired namespace is discovered; or
- the final deployed state cannot be identified or validated sufficiently.

## Rollback procedure

1. Stop further validation and record the failure and current environment
   identity.
2. Restore the captured legacy component to
   `/config/custom_components/curated_media/`.
3. Restore the captured legacy catalogue directory to
   `/config/curated_media/` and restore the captured `curated_media:`
   configuration entry if it existed.
4. Run Home Assistant configuration validation, then restart or reload as
   required.
5. Confirm legacy action and Media Source registration and execute a
   representative legacy normalized lookup.
6. If the failure prevents `mediacat.resolve_media_record` from serving active
   consumers, revert the affected AdvMedia and/or ASTV action-domain reference
   to `curated_media.resolve_media_record` using their last accepted
   pre-retirement states. Do not change logical `catalogue_id: curated_media`.
7. Revalidate the restored MediaCat, AdvMedia, and ASTV paths and record the
   resulting exact environment state. File restoration alone is not proof of a
   successful rollback.

Do not delete the rollback capture until ASTV-225 Beta validation, human
acceptance, promotion-equivalence checks, and closure obligations are complete.
