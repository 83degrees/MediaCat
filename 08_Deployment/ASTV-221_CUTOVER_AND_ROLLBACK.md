# ASTV-221 MediaCat Namespace Cutover and Rollback

## Authority and boundary

This procedure describes the approved phased route. It does not itself
authorize a Home Assistant deployment, restart, configuration mutation,
consumer deployment, or legacy removal. Perform each state-changing phase only
at the applicable WF-01 gate with explicit user authority and record the exact
candidate and environment state in Linear.

The logical catalogue identifier remains `curated_media` throughout. Do not
replace request `catalogue_id` values with `mediacat`.

## Phase 1 — preflight and rollback capture

1. Identify the exact accepted MediaCat candidate commit on persistent `beta`.
2. Confirm `custom_components/mediacat/` and `mediacat/catalogue.yaml` in the
   candidate are the intended deployment sources.
3. Verify the deployed legacy component, catalogue, Home Assistant version,
   active configuration/include route, registered legacy actions, and legacy
   Media Source root.
4. Capture an attributable backup or restorable copy of the mutable production
   state needed to restore the legacy component, catalogue, and configuration.
5. Record hashes or another sufficient identity for deployed source and
   catalogue files before change.
6. Run Home Assistant configuration/preflight validation required by the
   environment. Stop on failure.

## Phase 2 — parallel MediaCat deployment

1. Add the accepted candidate's `custom_components/mediacat/` at
   `/config/custom_components/mediacat/` without changing or removing
   `/config/custom_components/curated_media/`.
2. Add the accepted candidate's `mediacat/catalogue.yaml` at
   `/config/mediacat/catalogue.yaml` without changing or removing the legacy
   catalogue path.
3. Confirm both catalogue files have the intended equivalent content and both
   retain `catalogue_id: curated_media`.
4. Apply only the minimum configuration/restart or reload required for Home
   Assistant to discover both integrations.
5. Verify startup/configuration logs contain no registration conflict, import
   failure, catalogue-load failure, or Media Source collision.

## Phase 2 validation

Record results against the exact deployed candidate:

- `curated_media.resolve_item` and `mediacat.resolve_item` are registered;
- `curated_media.resolve_media_record` and
  `mediacat.resolve_media_record` are registered with response support;
- `media-source://curated_media` and `media-source://mediacat` are available;
- domain data is independent under `hass.data["curated_media"]` and
  `hass.data["mediacat"]`;
- representative raw lookup responses are equivalent;
- representative normalized URL, delegated Media Source, and
  assistant-command records are equivalent;
- browse roots, category/item ordering, search results, playable subset, direct
  resolution, delegated resolution, and self-reference rejection are
  equivalent apart from the expected domain/name change; and
- existing ASTV and AdvMedia consumers remain operational on the legacy action.

Any difference in request/response fields or record values is a failed parity
gate. Do not begin consumer migration.

## Phase 3 — independent consumer migration

AdvMedia migrates under `ASTV-223` and ASTV migrates under `ASTV-224`. For each
product independently:

1. change only the action domain to `mediacat.resolve_media_record` and make any
   separately authorized architecture/contract/test updates;
2. keep `catalogue_id: curated_media` unchanged;
3. run the product's complete applicable tests and configuration validation;
4. deploy while both provider domains remain available;
5. run product-specific and end-to-end behaviour validation; and
6. record that rollback is the action-domain change back to
   `curated_media.resolve_media_record`.

A failure in one consumer must not force rollback of a successfully validated
other consumer. Restore only the affected consumer unless provider parity or
Home Assistant stability is implicated.

## Phase 4 — legacy retirement readiness

Before legacy removal:

1. retrieve completion and runtime-validation evidence for ASTV-223 and
   ASTV-224;
2. search all active product repositories and deployed Home Assistant
   configuration for `curated_media.*`,
   `custom_components/curated_media`, `/config/curated_media`, and
   `media-source://curated_media`;
3. classify every remaining match as active or historical and resolve every
   active dependency;
4. verify current `mediacat` startup, actions, catalogue lookup, Media Source,
   ASTV, AdvMedia, and end-to-end behaviour;
5. confirm the rollback capture is still usable; and
6. obtain the separately required authority for legacy removal.

Do not treat `catalogue_id: curated_media`, historical evidence, or retained
rollback records as active legacy runtime dependencies solely because the text
matches.

## Phase 5 — legacy removal

Only after the retirement-readiness gate passes:

1. remove the active legacy integration/configuration entry and
   `/config/custom_components/curated_media/`;
2. remove `/config/curated_media/` only after confirming nothing active reads
   it;
3. restart or reload Home Assistant as required;
4. verify `mediacat` loads, both actions remain registered under `mediacat`,
   Media Source operations succeed, and no legacy action/Media Source remains;
5. rerun ASTV, AdvMedia, and end-to-end validation; and
6. record exact final state, results, post-change actions, limitations, and
   rollback disposition in the ASTV-221 closure evidence.

## Rollback

### Before legacy removal

Return only the affected consumer action reference to
`curated_media.resolve_media_record`. If the new provider destabilizes Home
Assistant, disable/remove the new `mediacat` configuration/component and
catalogue using the recorded pre-change state; leave the legacy provider and
consumers intact.

### After legacy removal

Restore the recorded legacy component, catalogue directory, and configuration
state; restart/reload; verify legacy action and Media Source registration; then
return affected consumers to `curated_media.resolve_media_record`. Revalidate
the restored paths and record the resulting environment identity. Do not infer
successful rollback from file restoration alone.
