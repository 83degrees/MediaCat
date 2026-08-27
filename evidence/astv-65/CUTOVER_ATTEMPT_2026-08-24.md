# ASTV-65 Cutover Attempt — 2026-08-24

## Outcome

The coordinated activation was rolled back during the paused post-restart
health gate. No normal ASTV media requests were released and none of the seven
normal-entry-point live checks ran.

The blocking check was the required legacy AdvMedia compatibility failure for
assistant-command-only `smooth_radio`. At `2026-08-24T18:19:01Z`,
`script.advmedia_prepare_playback` completed successfully but returned empty
`media_player` and playback fields. It did not fail explicitly because fixed
`ha_mplayer` was unavailable, so ASTV-65's acceptance criterion was not met.
No production debugging or patching was attempted.

## Atomic rollback

- The user confirmed the complete `rollback/config/` bundle was merged into
  Home Assistant `/config`.
- All six captured AdvMedia definitions were restored with optimistic hashes.
- `script.advmedia_process_media_record` and
  `script.advmedia_translate_media_source` were removed.
- Home Assistant configuration validation returned `valid` before restart.
- The rollback restart completed; the fresh recorder run began at
  `2026-08-24T18:22:47.737761Z`. The restart request itself returned HTTP 504
  after its client wait, but subsequent live health evidence proves Core
  restarted and returned normally.

## Post-rollback verification

- Home Assistant Core `2026.8.3` is healthy and configuration validation is
  still `valid`.
- Curated Media exposes only legacy `curated_media.resolve_item`; the schema-v3
  `curated_media.resolve_media_record` service is absent.
- All seven ASTV records resolve through the side-effect-free intent lookup and
  again contain `params.sources`; none contains `catalogue_id` or `item_id`.
- The six AdvMedia script hashes exactly match the pre-cutover capture:
  - `advmedia_prepare_playback`: `792fec2e08d41ded`
  - `advmedia_find_media_record`: `328847f70ddb6b0e`
  - `advmedia_resolve_player_mediaprofile`: `74c54bdc7f341ce0`
  - `advmedia_mediaprofile_handler`: `2494f48b1867ba36`
  - `advmedia_mediaprofile_generic`: `6c148bf41844b7b9`
  - `advmedia_mediaprofile_googlecast`: `2c490c894dd2a466`
- All six restored AdvMedia scripts were idle; the two cutover-only script IDs
  were absent.
- A legacy `bbc_radio_2` catalogue lookup returned the schema-v2 item and the
  unchanged AdvMedia entry returned a complete generic playback payload.
- Structured system-log searches for `curated_media`, `advmedia`, and `astv`
  returned no relevant startup entries.

Normal media requests may resume in the restored legacy state. Contracts,
architecture narratives, governance `1.1.1`, and the central release record
were not promoted.
