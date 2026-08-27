# ASTV-65 Rollback Window Closure — 2026-08-25

## Closure authority

Graham explicitly instructed Codex to override the ASTV-65 minimum 24-hour
operational-retention requirement, close the rollback window immediately, and
move ASTV-65 to `Done`. The durable Linear work instruction records this
ASTV-65-only exception.

- Frozen cutover proof: `2026-08-24T20:09:37.490Z`
- Final read-only checkpoint: approximately `2026-08-25T09:17Z`
- Elapsed time at checkpoint: 13.12 hours
- Exception recorded in Linear: `2026-08-25T09:18:52.360Z`

This exception changes no production architecture, contract, governance
release, interface, or general rollback rule.

## Final read-only checkpoint

- Home Assistant Core 2026.8.3 reported healthy and supported.
- Home Assistant configuration validation returned `valid` with no errors.
- No active Repairs issues were present.
- The latest ASTV UID Gateway, Media Intent Engine, and AdvMedia core traces
  were `stopped` / `finished`. The latest normal household run finished at
  `2026-08-25T04:16:37.509154Z`.
- All retained Google Home Device traces were `stopped` / `finished`.
- No AdvMedia log matches were present.
- Post-cutover Curated Media matches contained the standard custom-integration
  warning. The missing-item exception was the intentional boundary test.
- ASTV error matches were pre-cutover test failures from 2026-08-24 15:43–15:49,
  before the successful cutover proof.
- Current general system errors were unrelated to ASTV-65: HomeKit/Plex feature
  reporting, Chromecast reconnection, an automation-blueprint entity, Hue
  scenes, a mobile battery sensor, and Lovelace migration.

## Retained evidence

The protected backup `9b2dbd73`, deployment bundle, rollback bundle, manifests,
and validation records are retained as read-only historical evidence. They are
no longer maintained as an operational rollback commitment for ASTV-65. No
rollback artifact was deleted or modified as part of closure.
