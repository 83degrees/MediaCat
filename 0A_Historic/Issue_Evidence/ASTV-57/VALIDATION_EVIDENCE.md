# ASTV-57 Validation Evidence

## Scope and pickup gate

ASTV-57 was retrieved in `Ready` in the MediaCat project and moved to
`In Progress` before implementation. Its prerequisite issues were confirmed
complete:

- `ASTV-24` — schema and field semantics;
- `ASTV-31` — normalized item lookup;
- `ASTV-55` — schema-v3 loader and immutable model; and
- `ASTV-56` — completed 17-item schema-v3 catalogue.

The implementation remained local and non-live. It did not change the loader,
resolver, service registration, stored catalogue, integration manifest, another
runtime module, a shared contract, production evidence, or Home Assistant state.

## Rollback evidence and hashes

| Artifact | SHA-256 |
| --- | --- |
| Pre-change `custom_components/curated_media/media_source.py` | `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd` |
| `evidence/astv-57/rollback/media_source.py` | `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd` |
| Validated post-change `custom_components/curated_media/media_source.py` | `dfd66c3ce3f879fa3de284f9199df6dc03b25345ce0c5033f465563fcda51c3b` |

The source and preserved copy were both 9,636 bytes before editing. Restoration
steps are recorded in `evidence/astv-57/ROLLBACK_INSTRUCTIONS.md`.

## Changed files

- `custom_components/curated_media/media_source.py`
- `tests/test_media_source.py`
- `evidence/astv-57/rollback/media_source.py`
- `evidence/astv-57/ROLLBACK_INSTRUCTIONS.md`
- `evidence/astv-57/VALIDATION_EVIDENCE.md`
- `CURRENT_STATE.md`
- `01_Architecture/MEDIACAT_ARCHITECTURE.md`

The workspace has an initialized but uncommitted repository in which the existing
project baseline is untracked. This list is therefore based on the exact task
operations and file/hash checks, not a Git diff against a committed baseline.
Pytest also refreshed ignored `.pytest_cache` and `__pycache__` data; those are
generated local test caches, not authored artifacts.

## Implemented behaviour

- Catalogue model dispatch keeps the original schema-v2 browse, search, item,
  artwork, identifier, direct-stream, and MIME-fallback path intact.
- Schema v3 reads only `execution_methods.ha_mplayer.source` and never selects an
  ASTV method, endpoint, preference, profile, or fallback.
- Root and category order, `category_label`, `catalogue_label`, description/tags
  search, and `artwork.local` presentation are preserved from stored data.
- The completed `radio` category retains 17 stored members and exposes its 14
  playable members in their authored relative order. `smooth_radio`, `lbc_radio`,
  and `news_briefing` remain stored but are absent and directly unresolvable.
- Direct URL sources return the exact stored URL and MIME type.
- Home Assistant Media Source URIs are passed once to the standard resolver with
  `target_media_player` unchanged. The exact final `PlayMedia` result is returned.
- Curated Media self-reference and delegated unresolved `media-source://` output
  stop explicitly. Delegated owner failures surface without fallback or retry.
- Missing direct URL/MIME, unusable delegated URI, unsupported source type,
  missing item/category, and unsupported identifiers stop explicitly at the
  Media Source boundary.

## Focused validation

Command:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest tests\test_media_source.py -q
```

Result on 2026-08-24: `15 passed, 7 warnings in 3.22s`.

The focused suite covers:

- schema-v2 root/category/item browse, authored order, identifiers, local artwork,
  title/description/tag search, exact stream resolution, MIME fallback, and
  existing identifier failures;
- schema-v3 root/category browse, the exact 14-item playable order, assistant-only
  filtering and direct failures, labels, local artwork, partial case-folded
  search, blank search, and item-search rejection;
- exact direct URL and MIME results;
- one delegated resolution call, unchanged target player, and exact result;
- surfaced delegated failure with no retry;
- self-reference and unresolved delegated-output stops; and
- missing, unsupported, and unusable sources with no other-method fallback.

## Complete MediaCat validation

Command:

```powershell
& '.\.venv\Scripts\python.exe' -m pytest
```

Final result on 2026-08-24: `49 passed, 7 warnings in 4.62s`.

The warnings are dependency deprecations from the test-only Home Assistant stack;
no test failed. The suite includes all catalogue migration, schema-v2 baseline,
schema-v3 model, normalized lookup, and Media Source tests.

## Test-environment limitation

The documented test-only environment is Windows 11, Python 3.12.13, Home
Assistant 2024.12.5, pytest 9.1.1, pluggy 1.6.0, and anyio 4.6.2.post1. The copied
production adapter uses newer Media Browser search and `can_search` result fields
which Home Assistant 2024.12.5 does not provide. The focused test module supplies
only those browse/search result containers while retaining the installed
`MediaSourceItem`, `PlayMedia`, exceptions, and standard resolver call signature.

These are non-live interface-behaviour tests. They do not prove compatibility
with the unidentified production Home Assistant version, runtime activation, or
successful live playback.

## Production and deployment boundary

Read-only final hash checks still found:

- production-evidence `custom_components/curated_media/media_source.py`:
  `39c55307ecf7f88ab3efe99d7f85619cb6e89ff6956eabab16250dd7ee8754dd`; and
- production-evidence `curated_media/catalogue.yaml`:
  `5fd55cd35b89b8d1958954173b49c94e3429130aff9766a767b4a223d28f02a8`.

No production file, service, integration configuration, loaded catalogue, reload,
runtime state, or live Home Assistant action was changed or invoked. `ASTV-65`
still owns coherent deployment of the schema-v3 loader, normalized lookup, Media
Source implementation, and catalogue plus immediate live proof and deployed
rollback.
