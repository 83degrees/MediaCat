# ASTV-65 Successful Cutover — 2026-08-24

## Outcome

The coordinated MediaCat schema-v3 cutover succeeded on the corrected retry.
Immediate proof was frozen at `2026-08-24T20:09:37.490Z`. Home Assistant Core
2026.8.3 restarted healthy, the schema-v3 Curated Media services registered, and
the corrected eight-script AdvMedia package was active.

The first attempt remains recorded in `CUTOVER_ATTEMPT_2026-08-24.md`. It was
rolled back atomically after the paused health gate exposed the nested-response
failure later corrected by `ASTV-73`. The retry began from the fully restored
legacy baseline described in `RETRY_READINESS_2026-08-24.md`.

## Protected recovery evidence

- Protected retry backup: `Before_ASTV-65_MediaCat_v3_Cutover_Retry_20260824`
- Backup ID: `9b2dbd73`
- Home Assistant version: `2026.8.3`
- Deployment and rollback inventory: `bundle-manifest.json`
- Manifest SHA-256: `fc2ef6a50659d2b250a0fc905f3f14d390b2768264fe42934acc915539e9c199`
- Complete ASTV legacy-catalogue rollback SHA-256:
  `8b99b82a4d2e5c47f787a1393b844486086f726c12b4cefc9eb48b71181ecbd2`

The coordinated rollback remains operational and must be retained for at least
24 hours after the proof timestamp.

## Paused post-restart health gate

Raw and normalized MediaCat lookups passed for direct URL, Radio Browser, and
assistant-command records. Direct calls to `script.advmedia_prepare_playback`
passed for direct URL and Radio Browser records and returned the exact contracted
three-field successful result.

The assistant-only Smooth Radio compatibility call returned `{}`. Its public and
core traces aborted explicitly, with no partial payload or fallback. Relevant
Home Assistant logs were clean.

The active AdvMedia script hashes were:

| Script role | Installed hash |
| --- | --- |
| prepare playback | `04ea248ad7159f15` |
| find media record | `241eb3c2323cd684` |
| process media record | `cd467d7ae50b0fce` |
| translate media source | `714e40332f931b1d` |
| resolve player profile | `74c54bdc7f341ce0` |
| profile handler | `33819adea4ca718c` |
| generic processor | `9623ac4a30914ee0` |
| Google Cast processor | `d66def4f17fe44b1` |

## Sequential UID proof

After the health gate, media requests resumed. Each request passed through
`script.astv_uid_gateway`, performed exactly one normalized lookup and one ASTV
method selection, and reached exactly one terminal action. Traces and relevant
logs were clean. The user confirmed audible playback for every row.

| Request | UID | Audible confirmation |
| --- | --- | --- |
| Classic FM | `7AB06354E000` | yes |
| LBC News | `689C36C82A81` | yes |
| Gold Radio | `EA9236C82A81` | yes |
| BBC Radio 2 | `DEADBEEF` | yes |
| Smooth Radio | `DEADSMOOTH` | yes |
| LBC Radio | `DEADLBC` | yes |
| News Briefing | `DEADNEWSBRIEF` | yes |

## Media Browser proof

The backend root exposed Curated Media then Radio. Radio contained exactly 14
playable items in stored order and excluded `smooth_radio`, `lbc_radio`, and
`news_briefing`. BBC search returned the expected 11 items. All 14 playable
records resolved to final non-recursive URLs and MIME types. Relevant logs were
clean. The user completed the separate visible Media Browser smoke test and
confirmed the UI.

## Status promotion and limitations

The three contracts were promoted by status only; no field, requiredness,
ownership, routing, or semantic change was made. The product architecture and
current-state narratives now classify the normalized flow as current and the
superseded schema-v2 flow as historical. Governance release 1.1.2 activation and
its final validation are recorded in
`00_Governance/reports/ASTV-74_GOVERNANCE_1.1.2_ACTIVATION_VALIDATION.md`.

The audible and UI confirmations are human-observed evidence. This proof is a
scoped immediate validation, not a continuous monitor or a complete production
capture. `ASTV_Architecture.drawio` retains the pre-cutover media topology as a
historical visual; separately authorized visual work is needed to update its
manual layout.

The ordinary active-mode governance validator assumes the central release and
generated instruction release are identical. The accepted 1.1.2 candidate
intentionally retains instruction release 1.1.0 bytes, so the applicable
candidate-aware and independent hash checks were used and the validator repair
was recorded separately as Governance CR `ASTV-75`.
