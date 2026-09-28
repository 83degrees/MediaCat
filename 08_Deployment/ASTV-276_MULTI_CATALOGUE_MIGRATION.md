# ASTV-276 Multi-Catalogue Migration and Beta Validation

## Scope

This runbook migrates one Home Assistant instance from the maintained single
catalogue file to MediaCat's directory-backed multi-catalogue registry. It does
not deploy MediaCat Manager or modify the read-only `ha-assets` mirror.

## State distinction

- Pre-migration production path: `/config/mediacat/catalogue.yaml`.
- Candidate/approved target path: `/config/mediacat/catalogues/*.yaml`.
- Logical Curated Media identity remains `catalogue_id: curated_media`.
- Production activation is not established by this document; retained Beta
  evidence must identify the exact deployed candidate and observed runtime.

## Preconditions

1. The exact accepted ASTV-276 candidate is integrated into persistent `beta`.
2. Beta deployment is explicitly authorized under the issue workflow.
3. The existing catalogue and integration directory are backed up outside the
   paths being replaced.
4. `/config/mediacat/catalogues/` is created.
5. The existing catalogue is copied unchanged to a YAML filename in the new
   directory. The filename may be `curated-media.yaml`; identity remains the
   in-file `catalogue_id`.
6. No duplicate copy of `catalogue_id: curated_media` remains in the discovery
   directory.

## Deployment and preflight

1. Deploy the accepted `custom_components/mediacat/` candidate.
2. Place the maintained Curated Media document under
   `/config/mediacat/catalogues/` and remove the obsolete single-file path only
   after backup confirmation.
3. Run Home Assistant configuration validation.
4. Restart Home Assistant for the integration-code deployment.
5. Confirm the `mediacat` integration initializes and registers exactly:
   `resolve_media_record`, `get_admin_capabilities`, `validate_catalogue`, and
   `reload_catalogue`.
6. Call `mediacat.get_admin_capabilities` and confirm schema version 4,
   `active_catalogue_ids` containing `curated_media`, and both validation and
   transactional reload support.

## Beta acceptance checks

1. Resolve representative `curated_media` items through
   `mediacat.resolve_media_record` and compare their normalized returned-record
   content with the pre-migration baseline.
2. Browse, search and play representative Curated Media entries through the
   `mediacat` Media Source.
3. Validate a known-good YAML document and a deliberately invalid in-memory
   document; confirm neither validation call changes active catalogue state.
4. Add a second valid test catalogue whose filename differs from its in-file
   ID, reload, and confirm lookup and catalogue-scoped Media Browser paths.
5. Introduce a duplicate-ID or invalid candidate, call reload, and confirm the
   response reports failure while lookups against the previously active
   registry still succeed unchanged.
6. Restore the intended Beta directory contents, reload successfully and
   confirm the final active catalogue IDs.

Retained evidence must record the exact candidate SHA, deployed integration
identity, relevant file hashes, action responses/results, configuration-check
result and the final active registry state. Do not retain secrets or mutable
Home Assistant snapshots in this repository.

## Rollback

1. Stop further catalogue edits.
2. Restore the backed-up pre-ASTV-276 integration directory and
   `/config/mediacat/catalogue.yaml`.
3. Remove the candidate-only catalogue directory from the active configuration
   only after confirming the backed-up file is restored.
4. Run Home Assistant configuration validation and restart.
5. Confirm the historical single catalogue loads and representative
   `curated_media` lookup and Media Source behavior are restored.
6. Record rollback candidate identity and resulting production state against
   ASTV-276.
