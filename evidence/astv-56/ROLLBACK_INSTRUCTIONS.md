# ASTV-56 schema-v2 rollback instructions

## Package and status

The complete inactive rollback unit is stored at:

`evidence/astv-56/rollback/schema-v2/`

It contains the byte-for-byte captured schema-v2 catalogue, the seven captured
schema-v2-compatible Curated Media integration definitions, and an inactive root
configuration fragment. It does not depend on reconstructing files from Git
history.

The production snapshot did not contain `configuration.yaml`, `.storage`, a
capture manifest, runtime logs, or activation traces. Consequently, the package
cannot preserve an unevidenced full production configuration. The included
`configuration-fragment.yaml` is a prepared restoration fragment, not a claim
about the missing captured file.

## Exact restoration targets

Treat `<config>` below as the Home Assistant configuration directory selected
and verified by the cutover operator.

| Package path | Restoration target |
| --- | --- |
| `custom_components/curated_media/__init__.py` | `<config>/custom_components/curated_media/__init__.py` |
| `custom_components/curated_media/catalogue.py` | `<config>/custom_components/curated_media/catalogue.py` |
| `custom_components/curated_media/const.py` | `<config>/custom_components/curated_media/const.py` |
| `custom_components/curated_media/manifest.json` | `<config>/custom_components/curated_media/manifest.json` |
| `custom_components/curated_media/media_source.py` | `<config>/custom_components/curated_media/media_source.py` |
| `custom_components/curated_media/resolver.py` | `<config>/custom_components/curated_media/resolver.py` |
| `custom_components/curated_media/services.yaml` | `<config>/custom_components/curated_media/services.yaml` |
| `curated_media/catalogue.yaml` | `<config>/curated_media/catalogue.yaml` |
| `configuration-fragment.yaml` | Merge the `curated_media:` root entry into `<config>/configuration.yaml` if the verified target configuration does not already activate the integration |

## Restoration procedure

These steps are instructions for the separately authorised `ASTV-65` cutover or
rollback operator. They were not run against production by `ASTV-56`.

1. Stop Home Assistant before replacing the integration package or catalogue.
2. Confirm the selected `<config>` directory and preserve the failed cutover
   files separately for diagnosis.
3. Copy the rollback integration directory and catalogue to the exact targets
   above as one compatible unit. Do not copy `providers` into a schema-v3 item
   and do not mix schema-v2 data with the schema-v3 implementation state.
4. Verify every copied file against the SHA-256 table in
   `VALIDATION_EVIDENCE.md`.
5. Confirm that the root Home Assistant configuration contains the
   `curated_media:` integration entry, using the packaged fragment only if the
   verified target configuration needs it.
6. Perform a full Home Assistant restart. A YAML-only reload is insufficient for
   replacement of custom-integration Python files.
7. Confirm that Curated Media setup succeeds, then invoke
   `curated_media.resolve_item` for `item_id: bbc_radio_1` and verify that the
   returned complete record contains
   `providers.radio_music.service: bbc_radio_one`.
8. Re-run the relevant pre-cutover consumer checks. If restoration fails, stop;
   do not create a hybrid v2/v3 compatibility patch.

## Non-live rehearsal result

The repository test `test_preserved_v2_package_loads_with_its_compatible_implementation`
starts an isolated Python subprocess rooted in the rollback package, loads the
preserved catalogue with the preserved schema-v2 implementation, resolves
`bbc_radio_1`, and confirms its original top-level provider value. The same test
suite loads the schema-v3 target with the v3-capable implementation and confirms
that normalized records omit top-level `providers` while legitimate execution
source providers remain present.

No active catalogue, live integration, or production configuration was replaced
or reloaded during the rehearsal.

## Retention

Keep this package inactive and available through coordinated cutover and user
review. Only explicit user closure of the rollback window retires it as an
operational rollback option. After closure, retain it as read-only historical
evidence.
