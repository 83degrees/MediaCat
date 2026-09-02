# ASTV-56 migration and validation evidence

## Work instruction and boundary

- Linear issue: `ASTV-56`
- Pickup status: moved from `Ready` to `In Progress` on 2026-08-24
- Workspace: MediaCat repository only
- Artifact status: prepared and tested; inactive and not deployed
- Production boundary: no production file, ASTV intent record, active catalogue,
  integration configuration, reload, restart, action, or playback was changed or
  invoked

All declared blockers (`ASTV-28`, `ASTV-31`, `ASTV-32`, `ASTV-34`, `ASTV-35`,
`ASTV-54`, and `ASTV-55`) were in `Done` at pickup. The source-controlled
schema-v3 loader and normalized lookup from `ASTV-55` and `ASTV-31` were present
and used by the focused tests.

## Source capture

The two migration input files were inspected and hashed read-only at
2026-08-24T15:19:51Z, before the first repository edit.

| Authoritative input | File size | Captured file modification time (UTC) | SHA-256 |
| --- | ---: | --- | --- |
| `Production_ReadOnly/starburst/curated_media/catalogue.yaml` | 8,356 bytes | 2026-08-03T15:56:38Z | `5fd55cd35b89b8d1958954173b49c94e3429130aff9766a767b4a223d28f02a8` |
| `Production_ReadOnly/starburst/assistive/astv_intent_catalogue.yaml` | 2,309 bytes | 2026-08-11T19:23:52Z | `8b99b82a4d2e5c47f787a1393b844486086f726c12b4cefc9eb48b71181ecbd2` |

The v2 hash matches the MediaCat evidence index, and the ASTV intent-catalogue
hash also matches that index. The source content matches the values described by
the approved instruction: 11 ordered schema-v2 items, seven ASTV media records,
and one unrelated ASTV routine record. No unexpected media record or changed
value was found.

Approved non-mechanical decisions were taken from `ASTV-28` (Radio 4 artwork),
`ASTV-32` (omit legacy top-level `providers` and preserve a complete rollback
unit), `ASTV-34` (endpoint-independent LBC command), and `ASTV-54`
(`assistant_command` source shape).

### Evidence limitations

The read-only snapshot has no capture manifest, capture timestamp, Home Assistant
version, `configuration.yaml`, `.storage`, runtime logs, or action traces. Its
freshness and current live activation are therefore not proved. File modification
times are inventory facts, not provenance. No live read-only query supplemented
the snapshot. The migration is consequently proved only against the governed
static baseline already used to prepare `ASTV-56`.

## Target artifact

| Artifact | File size | SHA-256 |
| --- | ---: | --- |
| `curated_media/catalogue.yaml` | 11,243 bytes | `067b2948bba11cbd418f90dc94f39b80f7f530091c3f388bc3e4313de03510c7` |

The target has exactly the four approved root fields, 17 distinct items, and one
`radio` category containing all items once in the agreed order. The per-item
source and target decisions are recorded in `MIGRATION_MATRIX.md`.

## Rollback package hashes

Package root: `evidence/astv-56/rollback/schema-v2/`

| Package-relative file | File size | SHA-256 |
| --- | ---: | --- |
| `configuration-fragment.yaml` | 99 bytes | `28d6153b618273efeede4941f7d5ea5317c6336b45a9109c4723e85a653f60c6` |
| `curated_media/catalogue.yaml` | 8,356 bytes | `5fd55cd35b89b8d1958954173b49c94e3429130aff9766a767b4a223d28f02a8` |
| `custom_components/curated_media/__init__.py` | 2,808 bytes | `a616d8b31da495b266e015efc8af68610cc9213ee373f27a3a653d63bb643c9e` |
| `custom_components/curated_media/catalogue.py` | 12,333 bytes | `6eb7ef511483310afea4f9aa53a3546e72a419bd818654cf062dc5eedee5675b` |
| `custom_components/curated_media/const.py` | 371 bytes | `3e98b96dbf37f330ae1faf58f3f39b22aaab51e3f054033be0aff9cfe5e1c278` |
| `custom_components/curated_media/manifest.json` | 192 bytes | `a9523e1ee385e6ebac055d82d9b169a92fb9a9b273323f6867f808eb9beca566` |
| `custom_components/curated_media/media_source.py` | 9,636 bytes | `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd` |
| `custom_components/curated_media/resolver.py` | 901 bytes | `667d2a8fc00e10d292ff235b0bed23f590bb5a9da56086022aef38c20113f0ac` |
| `custom_components/curated_media/services.yaml` | 410 bytes | `461c093b6bbd82acbffcf5f82bb1cd9462ef9ee0c138891d59850c93cba7e2f4` |

The catalogue and seven integration-file hashes match the read-only source
files. The prepared configuration fragment is new, inactive rollback material;
the source snapshot did not contain the full activation configuration.

## Test and rehearsal results

Environment:

- Windows 11
- Python 3.12.13
- Home Assistant 2024.12.5 (test-only)
- pytest 9.1.1

Command:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest -q
```

Result:

```text
..................................                                       [100%]
34 passed in 2.13s
```

The focused migration proof establishes that:

- the complete v3 catalogue loads through the `ASTV-55` loader;
- the root, 17 distinct item IDs, and authored category order are exact;
- every schema-v2 identity, description, ordered tag list, artwork value, URL,
  and MIME value is retained except for the two approved item-specific changes;
- the six ASTV-derived items match the approved values exactly;
- Radio 4 uses the corrected external artwork and Radio Scotland uses
  `mime_type: audio/aac`;
- LBC contains no endpoint name and uses `append_target: true`;
- top-level `providers`, v2 `source.type`, and v2 `source.format` are absent;
- representative `url`, `ha_media_source`, and `assistant_command` items return
  complete normalized records through the `ASTV-31` resolver;
- normalized v3 records omit top-level `providers` while retaining legitimate
  execution-source providers;
- the isolated rollback package loads through its preserved schema-v2
  implementation and resolves `bbc_radio_1` with the original
  `providers.radio_music.service: bbc_radio_one` value.

This is loader, lookup, data, and rollback-rehearsal proof only. It is not Home
Assistant Media Browser compatibility, playback, production runtime, activation,
or live-freshness evidence.

## Remaining non-live boundary and handoff

The v3 artifact and rollback package are ready for `ASTV-65`. `ASTV-57` remains
responsible for schema-v3 Home Assistant Media Source behaviour, and `ASTV-64`
remains responsible for preparing ASTV media intent records for the coordinated
cutover. `ASTV-65` owns deployment, activation, immediate live proof, rollback
invocation if required, and eventual promotion of the target to current
production architecture.
