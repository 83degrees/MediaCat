# ASTV-65 Pre-Cutover Readiness Evidence

## Status

Readiness result: **go-live checkpoint reached; production activation not yet
authorized**.

ASTV-65 was retrieved in `Ready` and moved to `In Progress`. All fifteen Linear
blocking relations are `Done`; ASTV-35 and the separately required ASTV-69 are
also `Done`. ASTV-69 records explicit user acceptance of the inactive governance
1.1.1 candidate. Active governance remains 1.1.0.

## Local and isolated validation

- MediaCat: `49 passed`, with seven dependency deprecation warnings.
- AdvMedia: `69 passed`.
- `precutover_proof.py`: passed for all seven records with exactly seven
  normalized lookups, seven ASTV method selections, four intercepted AdvMedia
  handoffs, three intercepted Google Assistant commands, and zero external
  actions.
- Media Browser projection: 17 stored radio members, 14 playable members in
  stored relative order, and `smooth_radio`, `lbc_radio`, and `news_briefing`
  excluded as assistant-command-only items.
- Target AdvMedia package: exactly eight scripts; the ASTV direct-core path has
  no MediaCat lookup, while the v1 compatibility path has exactly one normalized
  lookup and one shared-core call per branch.
- Stored-catalogue consumer audit: the prepared ASTV and AdvMedia consumers have
  no `catalogue_schema_version`, category, catalogue-item-map, or other stored
  internal dependency. They use the normalized lookup and returned
  `execution_methods` only.

## Artifact and rollback proof

`bundle-manifest.json` records nine deployment files and nine rollback files.
`verify_bundles.py` rechecked all 18 files and proved every bundle byte is equal
to its recorded governed source.

Key prepared artifact hashes:

| Artifact | SHA-256 |
| --- | --- |
| Schema-v3 Curated Media catalogue | `067b2948bba11cbd418f90dc94f39b80f7f530091c3f388bc3e4313de03510c7` |
| Seven-record ASTV replacement plus unchanged routine | `a9c3bb87a933847d25e1f06f73b3780ae4e1338d10e5441742c51ff7075ed703` |
| Eight-script AdvMedia package | `f46b97b239c0d139a7568baa00b3b6f9f41c6ef3c8b3a8ec239b65ba7e0eac15` |
| Schema-v2 Curated Media catalogue rollback | `5fd55cd35b89b8d1958954173b49c94e3429130aff9766a767b4a223d28f02a8` |
| Complete legacy ASTV catalogue rollback | `8b99b82a4d2e5c47f787a1393b844486086f726c12b4cefc9eb48b71181ecbd2` |

The complete six-script live AdvMedia configuration was captured under
`rollback/advmedia-live/`. The two new target script IDs were absent, providing
an exact removal boundary for rollback.

## Live drift and health evidence

All accepted ASTV hashes matched:

| Script | Live and accepted hash |
| --- | --- |
| `script.astv_intent_engine_media` | `883e77ec37747186` |
| `script.astv_select_intent_engine` | `bda1d825cd330779` |
| `script.astv_select_execution_engine` | `9d2eedaeba1f5b86` |
| `script.astv_ha_mplayer_engine` | `7f2e5588e9a9cedb` |
| `script.astv_adapter_advmedia` | `fe00d0cea795cc06` |
| `script.astv_g_home_device_engine` | `a51304a3b2c88287` |
| `script.astv_provider_g_assist` | `052ce3c242fe4e93` |

The six current AdvMedia definitions were present at hashes captured in
`live-script-inventory.json`. The new core and translator were absent. Live
service discovery exposed only `curated_media.resolve_item`; normalized
`curated_media.resolve_media_record` was not active. All seven live intent
lookups returned only `params.output` plus legacy `params.sources`, with no
`catalogue_id` or `item_id`. This proves the active production set remains
coherently legacy rather than mixed.

Home Assistant Core is `2026.8.3`; the pre-restart configuration check is valid.
No current AdvMedia or Curated Media structured system-log entries were returned.
One aggregated ASTV error group ended at 2026-08-24T14:49:14Z and corresponds to
the failed ASTV-63 attempt already recorded before restoration and corrected
installation; the current seven script hashes all match the corrected accepted
baselines.

## Governance candidate and restoration proof

- Active governance VERSION: `1.1.0`.
- ASTV-69 inactive candidate: `1.1.1`, accepted and `Done`.
- Current two-contract registry validation: passed.
- Isolated target three-contract validation: passed.
- Governance CR validation: passed.
- Complete 41-file restoration `-WhatIf`: passed with active files untouched.

No contract or architecture status is promoted before successful immediate live
proof.

## Full backup

Home Assistant backup `Before_ASTV-65_MediaCat_v3_Cutover` completed and was
relisted successfully:

- backup ID: `e3398ae8`;
- size: 185,579,520 bytes;
- Home Assistant version: 2026.8.3;
- Home Assistant configuration included;
- recorder database excluded; and
- local Supervisor backup agent: `hassio.local`.

## Remaining evidence limits

- The historical `Production_ReadOnly/starburst` snapshot still lacks a capture
  manifest and cannot establish its own freshness. Fresh live script hashes,
  intent-record lookups, service discovery, system health, configuration check,
  and backup evidence supplement it for this cutover.
- Local MediaCat tests use Home Assistant 2024.12.5 on Python 3.12, not the live
  Core 2026.8.3 / Python 3.14.6 runtime. Live compatibility is therefore proved
  only by the controlled post-restart health gate and immediate checks.
- Audible playback and the Home Assistant Media Browser UI smoke test require
  user observation during the cutover session.

## Go-live boundary

Do not pause media requests, copy either config bundle, install AdvMedia, reload,
restart, or run the seven normal-entry media checks until the user explicitly
approves this production cutover session.

After approval, the user performs only the complete `deployment/config/` merge
into `/config` and confirms the nine named overwrites completed without error.
Codex then installs the eight AdvMedia scripts, validates configuration, restarts
once, runs the paused health and compatibility gates, resumes requests, and
coordinates the seven audible checks plus the Media Browser smoke test.

Any activation or immediate-proof failure triggers complete atomic rollback; no
production debugging or partial repair is attempted during the cutover window.
