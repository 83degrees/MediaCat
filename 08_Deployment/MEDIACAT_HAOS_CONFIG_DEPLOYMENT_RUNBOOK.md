# MediaCat Home Assistant Configuration Deployment Runbook

## Purpose and authority

This runbook applies the approved route:

`haos_config -> operator_selected -> HOME_ASSISTANT_CONFIG_DEPLOYMENT_STANDARD.md`

It covers only MediaCat's three Home Assistant package files on `starburst`.
It does not authorise deployment and does not apply to the HACS integration or
managed catalogue data. The governing Linear issue, Central Governance, the
Deployment Architecture Standard, and the Home Assistant Configuration
Deployment Standard remain authoritative.

## Deterministic path map

| Governed source path | Deterministic `starburst` target path |
| --- | --- |
| `04_Implementation/haos/source/config/packages/mediacat/mediacat_automations.yaml` | `/config/packages/mediacat/mediacat_automations.yaml` |
| `04_Implementation/haos/source/config/packages/mediacat/mediacat_helpers.yaml` | `/config/packages/mediacat/mediacat_helpers.yaml` |
| `04_Implementation/haos/source/config/packages/mediacat/mediacat_scripts.yaml` | `/config/packages/mediacat/mediacat_scripts.yaml` |

Only the accepted files explicitly authorised for a deployment are transferred.
The operator may select SMB, a file editor, SCP/SFTP, direct upload, or another
available transport; the transport is not an authority source or product
dependency.

## Controlled deployment

Before transfer, record the deployment authority, authorised operator, exact
accepted commit SHA, selected source and target paths, `starburst` environment,
transport, Home Assistant configuration-check route, and rollback route. Record
source hashes where practical. Capture every immediate prior target file and
its path, time, identity, and separate rollback location before overwriting it.
Stop unless the complete affected state can be restored or the user grants the
specific governed exception allowed by the Standard.

Transfer the accepted bytes without editing, reformatting, line-ending or
encoding conversion, merge resolution, or generation. Prefer target-side hashes
or byte comparison after transfer. Otherwise record the strongest available
read-back, size, manifest, and inspection evidence and state the provenance
limitation honestly.

Run the Home Assistant-supported configuration check on `starburst` after the
transfer. Record the route, time, result, warnings, and evidence binding the
result to the deployed state. Reload or restart only after the check succeeds
and the action is authorised. A successful transfer or YAML parse does not
replace the Home Assistant configuration check.

Fail closed when authority, candidate, target, prior state, transferred bytes,
configuration validation, or required evidence is missing, ambiguous, failed,
or contradictory. To roll back, restore every affected target from the recorded
prior state, verify the restored bytes, repeat the Home Assistant configuration
check, and record the final target status.

## Deployment evidence record

```text
Governing issue and deployment authority:
Authorised operator and time:
Accepted commit SHA:
Selected source paths and source hashes:
Target instance/environment: starburst
Exact target paths:
Transport actually used:
Immediate prior-state identities and rollback locations:
Target-byte verification and remaining limitation:
Home Assistant configuration-check route, time, and result:
Reload/restart authority and result, if applicable:
Overall outcome:
Rollback and revalidation result, if invoked:
Unresolved conditions:
```
