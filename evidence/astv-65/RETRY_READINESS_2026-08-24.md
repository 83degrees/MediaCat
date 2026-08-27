# ASTV-65 Retry Readiness — 2026-08-24

## Outcome

The production and product readiness checks pass, but a refreshed governance
rollback baseline is required before a new go-live decision. No cutover was
started, no media-request pause was requested, and production remains on the
complete schema-v2/legacy state restored after the first attempt.

Governance CR `ASTV-74` records the blocker. It must prepare and obtain user
acceptance for a refreshed inactive candidate before ASTV-65 resumes.

## Corrected AdvMedia target

- `ASTV-73` is user-accepted and `Done`.
- Corrected eight-script package SHA-256:
  `d63352918fb0095d136010f40efe5fee230feaf2586835a8118e293ddaeeba679`.
- ASTV-73 pre-correction rollback package SHA-256:
  `f46b97b239c0d139a7568baa00b3b6f9f41c6ef3c8b3a8ec239b65ba7e0eac15`.
- The full AdvMedia suite passed: `102 passed, 5 warnings` on the pinned real
  Home Assistant Core 2026.8.3 test engine.
- The first local invocation encountered only an inaccessible stale global
  pytest temp directory. The complete suite passed after rerunning with a fresh
  isolated temp root; no source or test assertion changed.

## Refreshed local proof

- MediaCat full suite: `49 passed, 7 warnings`.
- Seven-record isolated proof: passed with seven lookups, seven method
  selections, four intercepted AdvMedia handoffs, three intercepted assistant
  commands, and zero external actions.
- Media Browser projection: exactly 14 playable records in stored order; the
  three assistant-command-only records remain excluded.
- All 18 files in the deployment and rollback config-root bundles remain
  byte-equal to their governed sources.

## Refreshed live baseline

Captured from live Home Assistant at approximately
`2026-08-24T19:29:16Z` through `2026-08-24T19:30:36Z`:

- Home Assistant configuration check: `valid`.
- Curated Media exposes only legacy `curated_media.resolve_item`.
- All seven ASTV records resolve with legacy `params.sources`; none exposes
  target `catalogue_id` or `item_id`.
- All affected ASTV and AdvMedia scripts are idle.
- Accepted ASTV hashes still match:
  - `astv_intent_engine_media`: `883e77ec37747186`
  - `astv_select_intent_engine`: `bda1d825cd330779`
  - `astv_select_execution_engine`: `9d2eedaeba1f5b86`
  - `astv_ha_mplayer_engine`: `7f2e5588e9a9cedb`
  - `astv_adapter_advmedia`: `fe00d0cea795cc06`
  - `astv_g_home_device_engine`: `a51304a3b2c88287`
  - `astv_provider_g_assist`: `052ce3c242fe4e93`
- The six active AdvMedia hashes still match the captured rollback set:
  - `advmedia_prepare_playback`: `792fec2e08d41ded`
  - `advmedia_find_media_record`: `328847f70ddb6b0e`
  - `advmedia_resolve_player_mediaprofile`: `74c54bdc7f341ce0`
  - `advmedia_mediaprofile_handler`: `2494f48b1867ba36`
  - `advmedia_mediaprofile_generic`: `6c148bf41844b7b9`
  - `advmedia_mediaprofile_googlecast`: `2c490c894dd2a466`
- No new relevant structured system-log entries were present. Raw-log matches
  were the normal custom-integration warning, the deliberately generated
  first-attempt missing-item error, and older pre-cutover ASTV test errors.

## Refreshed full backup

- Name: `Before_ASTV-65_MediaCat_v3_Cutover_Retry_20260824`
- Backup ID: `9b2dbd73`
- Size: 185,548,800 bytes
- Home Assistant included: yes
- Recorder database included: no
- Home Assistant version: 2026.8.3
- Verification: present in the live backup list and protected.

## Governance blocker

Active governance remains `1.1.0` with the two-contract registry. The accepted
ASTV-69 inactive candidate registry and generated instruction hashes are still
unchanged, and the old rollback dry run still selects 41 targets.

However, ASTV-73 legitimately updated `AdvMedia/CURRENT_STATE.md` and
`AdvMedia/01_Architecture/ADVMEDIA_ARCHITECTURE.md` after ASTV-69's immutable
41-file rollback baseline was captured. The governed release validator now
fails active-release preservation because that baseline does not represent the
actual current pre-cutover product-document state. Applying it during rollback
could erase accepted ASTV-73 documentation.

`ASTV-74` is the linked patch-level Governance CR to create a new immutable
baseline and semantically identical inactive candidate. Until it is validated,
accepted, and `Done`, ASTV-65 must not request or begin another go-live.

## Blocker resolution

Graham accepted ASTV-74 and moved it to `Done` at
`2026-08-24T19:48:05.892Z`. The refreshed inactive governance `1.1.2`
candidate retains the accepted three-contract registry target byte-for-byte and
uses `00_Governance/baselines/2026-08-24-astv-74-activation/manifest.json` as
its current 41-file rollback source.

ASTV-65 reran the CR validator, active two-contract release validation,
isolated three-contract target validation, and 41-target restoration `-WhatIf`.
All four commands passed. Active governance remains `1.1.0`; the `1.1.2`
candidate is accepted but inactive. The governance blocker is resolved and the
new production go/no-go checkpoint may be presented.
