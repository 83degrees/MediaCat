# MediaCat Administration Interface Contract

## Contract record

| Property | Value |
| --- | --- |
| Owner | MediaCat |
| Producer | Home Assistant actions in the `mediacat` domain |
| Consumer | MediaCat Manager; human/operational callers using the same supported actions |
| Contract version | `1.0.0` |
| Status | Current multi-catalogue capability, validation and transactional reload interface |
| Source issue | `ASTV-276` |

This provider-owned contract is the sole supported boundary for a local
catalogue-management client to discover MediaCat capabilities, validate a
candidate document and activate on-disk catalogue changes. MediaCat owns schema
meaning and runtime activation. MediaCat Manager owns editing, filesystem
writes, atomic file replacement, backups/history and user workflow.

## Common rules

- All actions are response-only Home Assistant actions.
- `admin_interface_version` versions this administration contract independently
  from stored `catalogue_schema_version` and lookup `returned_record_version`.
- Validation and reload return structured outcomes. An invalid candidate is an
  expected negative result, not a partial success.
- The interface accepts no filesystem path from a caller. The catalogue
  directory is fixed by MediaCat, and validation accepts document content.
- None of these actions writes, renames or deletes a catalogue file.
- No action accepts or returns secrets or repository credentials.

## `mediacat.get_admin_capabilities`

### Request

The request has no fields.

### Response

```yaml
admin_interface_version: 1
current_catalogue_schema_version: 4
supported_catalogue_schema_versions: [4]
catalogue_directory: mediacat/catalogues
catalogue_file_extensions: [.yaml, .yml]
active_catalogue_ids: [curated_media]
validation_supported: true
transactional_reload_supported: true
```

`catalogue_directory` is relative to the Home Assistant configuration root.
`active_catalogue_ids` reflects the current immutable in-memory registry, not an
unvalidated directory scan. List order is deterministic discovery order.

## `mediacat.validate_catalogue`

### Request

| Field | Presence | Type | Meaning |
| --- | --- | --- | --- |
| `catalogue_yaml` | Required | String | One complete UTF-8 catalogue YAML document. |

Validation applies the same duplicate-key, schema-version, closed-vocabulary,
value, pairing and reference checks used by runtime loading. It does not write
the document, inspect any caller-supplied path, change active runtime state or
test external resource liveness.

### Successful validation response

```yaml
valid: true
catalogue_id: <validated in-file identity>
catalogue_schema_version: 4
item_count: <integer>
category_count: <integer>
errors: []
```

### Rejected validation response

```yaml
valid: false
errors:
  - code: invalid_catalogue
    message: <path/rule-specific diagnostic>
```

No catalogue summary fields are promised on rejection. The initial interface
may stop at the first error; consumers must not assume aggregation.

## `mediacat.reload_catalogue`

The singular action name represents one transactional reload operation over the
complete configured catalogue registry.

### Request

The request has no fields.

### Successful reload response

```yaml
reloaded: true
active_catalogue_ids: [<catalogue_id>, ...]
catalogue_count: <integer>
errors: []
```

MediaCat discovers all `.yaml` and `.yml` files under
`/config/mediacat/catalogues/`, validates every document, rejects duplicate
in-file `catalogue_id` values, constructs a complete immutable candidate and
then performs one active-registry replacement. Normal lookup and Media Source
requests therefore observe either the prior registry or the complete new
registry, never a partially reloaded mixture.

### Rejected reload response

```yaml
reloaded: false
active_catalogue_ids: [<still-active catalogue_id>, ...]
errors:
  - code: reload_failed
    message: <path/rule-specific diagnostic>
```

Any discovery, read, YAML, schema or duplicate-identity failure retains the
previous active registry unchanged. Reload does not roll back an external
filesystem write; MediaCat Manager owns file snapshots and restoration.

Concurrent reload requests are serialized within one Home Assistant runtime.

## Storage and identity

- Each discovered YAML file contains exactly one catalogue document.
- The document's `catalogue_id` is authoritative.
- A filename need not equal `catalogue_id` and may change without changing
  catalogue identity.
- Duplicate catalogue IDs across files invalidate the complete registry
  candidate.
- The directory may contain non-YAML files; MediaCat ignores them.
- At least one supported YAML catalogue is required for successful setup or
  reload.

## Compatibility policy

Additive response fields are backward compatible; consumers must ignore fields
they do not understand. Removing, renaming, moving or reinterpreting a promised
field, changing its type or presence, accepting a caller-selected filesystem
path, or weakening failed-reload state preservation is breaking and requires a
new `admin_interface_version` with coordinated consumer work.

Adding a stored schema version to the supported list is not by itself an admin
interface break. The stored schema's own governed architecture and migration
rules still apply.
