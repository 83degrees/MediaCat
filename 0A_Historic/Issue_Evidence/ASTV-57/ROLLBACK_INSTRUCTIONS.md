# ASTV-57 Local Rollback

## Preserved source

- Workspace source before ASTV-57:
  `custom_components/curated_media/media_source.py`
- Preserved copy:
  `evidence/astv-57/rollback/media_source.py`
- SHA-256 for both pre-change files:
  `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd`

The preserved file is 9,636 bytes and was copied before the implementation source
was edited. Its hash was rechecked after final validation.

## Restoration procedure

This rollback is local to the MediaCat source workspace. It does not deploy,
reload, or alter Home Assistant.

1. Copy `evidence/astv-57/rollback/media_source.py` over
   `custom_components/curated_media/media_source.py`.
2. Recalculate SHA-256 for the restored workspace file and confirm it is exactly
   `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd`.
3. Run the pre-ASTV-57 non-live suite with:

   ```powershell
   & '.\.venv\Scripts\python.exe' -m pytest `
     tests\test_catalogue_migration.py `
     tests\test_catalogue_v2_baseline.py `
     tests\test_catalogue_v3.py `
     tests\test_media_record_lookup.py
   ```

   The ASTV-57 Media Source tests intentionally describe the new behaviour and
   are not expected to pass against the restored pre-change adapter.
4. Retain this evidence and record why rollback was needed before any later
   reimplementation.

`ASTV-65` separately owns rollback of the future coherent deployed Curated Media
package. This local procedure must not be used to change production files.
