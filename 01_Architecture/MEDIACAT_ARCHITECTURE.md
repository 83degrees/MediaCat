# MediaCat Architecture

## Status

This is the authoritative current-state MediaCat architecture. The normalized
schema-v3 architecture became current through `ASTV-65` proof on
2026-08-24, and the permanent standalone AdvMedia gateway became a second direct
lookup consumer through `ASTV-67` on 2026-08-25.

Fresh read-only Home Assistant verification was performed through the Home
Assistant MCP between `2026-08-25T15:04:29.407605+01:00` and
`2026-08-25T15:12:23.884728+01:00`. It confirmed the current registered actions,
schema-v3 activation boundary, Media Source behavior, direct lookup consumers,
consumer definitions and recent completed traces. No Home Assistant action or
service was invoked, and no reload, restart, configuration change, catalogue
change, playback request or other production mutation occurred.

During transition, the precise cross-product interfaces remain current
operational authorities in the shared Governance 1.2 copies under
`Home_Assistant/contracts/`. Their approved Governance 2.0 target provider
locations are:

- `MediaCat/03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md`;
- `ASTV/03_Contracts/ASTV_EXECUTION_DISPATCH_INTERFACE.md`;
- `AdvMedia/03_Contracts/ASTV_ADVMEDIA_INTERFACE.md`; and
- `AdvMedia/03_Contracts/ADVMEDIA_MEDIACAT_GATEWAY_INTERFACE.md`.

The target provider locations do not activate themselves before the T7/T8
coordinated cutover.

Sections labelled **historical pre-cutover** describe the schema-v2 topology
captured for `ASTV-25` / `ASTV-26`. They are not current production behavior.

The authoritative current-production visual companion is
[MEDIACAT_ARCHITECTURE.drawio](Diagrams/MEDIACAT_ARCHITECTURE.drawio). It shows the
MediaCat product boundary and deployed Curated Media implementation at one
logical level, with ASTV and AdvMedia only at their MediaCat-facing caller
boundaries. This document remains the authoritative prose narrative, and the
contracts listed above remain authoritative for precise interfaces.

---

## Product Boundary

**MediaCat** owns media identity, catalogue structure, metadata, membership,
available execution methods and the route-specific source facts returned to its
consumers.

**Curated Media** is the deployed Home Assistant catalogue integration under the
`curated_media` domain. It is one catalogue within MediaCat, not a synonym for
the MediaCat product. There is no separate deployed `mediacat` Home Assistant
domain.

MediaCat is separate from:

- **ASTV**, which owns intent orchestration, area/domain preference,
  execution-method selection, endpoint selection and fallback policy; and
- **AdvMedia**, which processes a caller-selected Home Assistant media method
  into endpoint/profile-specific playback data.

The deployed MediaCat runtime is therefore the Curated Media integration and its
loaded catalogue. Product ownership is broader than the current deployment and
does not authorize uncontracted data movement or a new runtime.

---

## Current Production Evidence

### Fresh live read-only verification

Home Assistant Core `2026.8.3` was running during the verification window. The
following live objects were inspected without invoking a Home Assistant action
or service:

| Live object | Verified current evidence |
| --- | --- |
| Registered `curated_media` actions | Exactly `resolve_item(item_id)` and `resolve_media_record(catalogue_id, item_id)` were registered with response support. The normalized action description identifies the loaded schema-v3 catalogue and returned-record version 1. |
| Loaded schema boundary | Maintained integration source registers `resolve_media_record` only when the loaded model is `CatalogueV3`; its live registration therefore proves that schema-v3 loading and setup succeeded. |
| Media Source root | `media-source://curated_media` returned the `Curated Media` app root with one expandable/searchable `Radio` category. |
| Media Source category | `category/radio` returned exactly 14 playable items in stored order. |
| Media Source search | A live `BBC` search returned the expected 11 playable BBC items. |
| Media Source resolution | Read-only resolution of direct-URL `bbc_radio_2` and delegated `classic_fm` returned final non-recursive URLs with `audio/aac`. No playback was requested. |
| ASTV direct lookup consumer | `script.astv_intent_engine_media`, hash `883e77ec37747186`, calls `resolve_media_record` before ASTV method and endpoint selection. Its latest retained completed trace returned normalized Classic FM record version 1 and selected `ha_mplayer`. |
| AdvMedia gateway direct consumer | `script.advmedia_prepare_playback`, hash `9f431a2d1adc80f9`, calls `resolve_media_record` once and the AdvMedia core once. Its latest completed trace returned the contracted three-field result. |
| ASTV-to-AdvMedia path | The live adapter hash was `f3cd9fa7b196ccce`; the core hash was `cd467d7ae50b0fce`. Their latest paired completed traces passed the complete record and selected method without a second lookup. |
| ASTV assistant path | The latest retained completed `script.astv_g_home_device_engine` trace consumed a normalized `assistant_command` source and executed wholly within ASTV, outside AdvMedia. |

The live configuration search found the two direct normalized lookup consumers
listed above and no `resolve_item` consumer. The search was explicitly partial:
three YAML-defined scripts and three YAML-defined automations were not exposed by
the per-object configuration API. It therefore corroborates the contracted
consumer set but does not prove the absence of every possible external caller.

### Maintained source and deployment evidence

The maintained integration and catalogue bytes match the `ASTV-65` deployment
bundle manifest:

| Artifact | SHA-256 |
| --- | --- |
| `custom_components/curated_media/__init__.py` | `bb70761491f4824636fc98adaf546823f841ba8a9fa32ea9558ad096a0c0dc0d` |
| `custom_components/curated_media/catalogue.py` | `139dd9bd6dc73798146a0c82d1c009cb0e3ae3cb4b03136940a9f2bcd0540e98` |
| `custom_components/curated_media/media_source.py` | `dfd66c3ce3f879fa3de284f9199df6dc03b25345ce0c5033f465563fcda51c3b` |
| `custom_components/curated_media/resolver.py` | `f01a6c2071d8fe1d0c8788237ab624625de20c88077351e211b689d13e99c12c` |
| `custom_components/curated_media/services.yaml` | `ca9a219975f6ad0da047c85796817714c9f693dbac269381f26843f8f1fe0fe9` |
| `curated_media/catalogue.yaml` | `067b2948bba11cbd418f90dc94f39b80f7f530091c3f388bc3e4313de03510c7` |

The deployment bundle and successful cutover evidence are under
`../evidence/astv-65/`. The historical `Production_ReadOnly/starburst` snapshot
remains read-only evidence for the pre-cutover schema-v2 baseline only.

---

## Current Curated Media Deployment

### Setup and storage

The custom integration uses the Home Assistant domain `curated_media`. During
`async_setup`, it reads:

`<Home Assistant config>/curated_media/catalogue.yaml`

The catalogue is loaded off the event loop, validated, recursively frozen and
stored at `hass.data["curated_media"]["catalogue"]`. A load or validation failure
logs an error, causes setup to return `False` and prevents action registration.

The maintained and `ASTV-65`-deployed stored root declares
`catalogue_id: curated_media` and `catalogue_schema_version: 3`. That catalogue
contains 17 items and one ordered `radio` category. Fourteen records have a
usable `ha_mplayer` source and are exposed through Media Source; `smooth_radio`,
`lbc_radio` and `news_briefing` are assistant-command-only and are omitted from
Media Source. Fresh live browse results confirmed the
one-category/14-playable projection.

Stored catalogue schema version 3 and consumer-facing returned-record version 1
have independent compatibility lifecycles. The lookup contract, not stored YAML,
is the source of truth for consumer fields and presence promises.

### Current exposed interfaces

#### Normalized item lookup

`curated_media.resolve_media_record` is the current cross-product lookup
boundary. It is registered only for a loaded schema-v3 catalogue, accepts exact
`catalogue_id` and `item_id` inputs, and returns one complete unwrapped normalized
record with:

- `returned_record_version: 1`;
- the requested catalogue-scoped identity; and
- every stored execution method for the item.

The producer does not choose a method, endpoint, fallback or media-player
profile. Exact success, failure and compatibility behavior is defined only by
the MediaCat item-lookup contract.

#### Retained legacy raw lookup

`curated_media.resolve_item` remains registered as a separate compatibility
action. It accepts only `item_id` and returns a response-safe copy of the stored
item mapping without adding catalogue identity or returned-record version. It is
not the normalized cross-product boundary.

The maintained loader and Media Source adapter retain schema-v2 branches for
rollback compatibility, and the live ASTV Media Intent Engine definition retains
a legacy `request.params.sources` branch for requests without a MediaCat
reference. Current migrated media requests take the normalized branch. None of
these retained compatibility paths reclassifies `resolve_item` or schema v2 as
the current MediaCat architecture.

The rationale for excluding the legacy schema-v2 top-level `providers` mapping
from schema v3 while preserving a complete schema-v2 rollback package is
recorded in [DDR-001](../02_Decisions/DDR-001.md).

#### Home Assistant Media Source

The `curated_media` Media Source is a separate Home Assistant browse/search/play
surface over the same loaded catalogue. In schema v3 it:

- preserves stored category and item order;
- exposes only `radio` records with a usable
  `execution_methods.ha_mplayer.source`;
- searches catalogue label, description and tags;
- returns direct `url` sources unchanged with their MIME type; and
- delegates `ha_media_source` URIs once to their owning Media Source domain,
  rejecting Curated Media self-reference or a delegated result that remains a
  Media Source URI.

It does not fall back to another execution method when a record is unplayable.
Assistant-command-only records are intentionally absent from browse and search.

---

## Current Normalized Cross-Product Flow

### ASTV media path

1. A migrated ASTV media intent supplies `catalogue_id` and `item_id`.
2. `script.astv_intent_engine_media` calls
   `curated_media.resolve_media_record` once and receives the complete record.
3. ASTV intersects its area/domain preference with the keys in
   `media_record.execution_methods`, chooses one method and selects that method's
   endpoint.
4. `script.astv_select_intent_engine` passes the complete record, selected method
   and endpoint once to `script.astv_select_execution_engine`.
5. For `ha_mplayer`, ASTV passes the complete record and selected context through
   `script.astv_ha_mplayer_engine` and `script.astv_adapter_advmedia` to
   `script.advmedia_process_media_record`. AdvMedia reads only the selected
   source, resolves or accepts the media profile and returns playback data. ASTV
   performs the final `media_player.play_media` call.
6. For `g_home_device`, ASTV reads the selected `assistant_command` source,
   combines it with its selected endpoint as directed by `append_target`, and
   invokes the assistant SDK. This path does not call AdvMedia and has no
   media-player profile.

The complete MediaCat record remains unchanged through the ASTV dispatch path;
the selected method is separate ASTV-owned context.

### Standalone AdvMedia gateway path

`script.advmedia_prepare_playback` is the permanent standalone AdvMedia gateway
for callers that already hold a catalogue reference, selected method and
endpoint. It:

1. passes `catalogue_id` and `item_id` unchanged to
   `curated_media.resolve_media_record` exactly once;
2. passes the complete returned record and caller-selected context to
   `script.advmedia_process_media_record` exactly once; and
3. returns the complete AdvMedia three-field result unchanged.

The retired `script.advmedia_find_media_record` wrapper and former
`media_catalogue` / `media_item_id` compatibility shape are historical. The
gateway has no catalogue allow-list and performs no selection, fallback, retry
or final playback action.

### Current preference and fallback semantics

ASTV owns method preference, method selection, endpoint selection and fallback
policy. The current selection step chooses the first configured preference that
is present in the returned record's execution-method keys. It does not test live
endpoint, provider or stream availability during selection and does not
automatically retry a later method after failure. Current behavior is ordered
configured-method matching, not runtime availability-aware failover.

---

## Current Boundary Ownership

### MediaCat / Curated Media

- owns catalogue-scoped identity, metadata, membership and ordered categories;
- owns available execution methods and their source facts;
- loads and holds the immutable catalogue;
- returns the complete normalized record without selection context;
- exposes the playable subset through Home Assistant Media Source; and
- owns explicit lookup failure for an unknown catalogue or item.

### ASTV

- owns intent and target-area resolution;
- owns method preference/selection, endpoint selection and fallback policy;
- carries the complete MediaCat record with the separately selected method;
- owns the assistant-command execution path; and
- performs the final Home Assistant playback action on the `ha_mplayer` path.

### AdvMedia

- consumes a complete normalized record plus caller-selected method and endpoint;
- translates the selected Home Assistant source;
- resolves or accepts the media-player profile;
- builds profile-specific playback data; and
- neither performs a second lookup on the ASTV direct-core path nor performs the
  final playback action.

The standalone gateway is additionally a direct MediaCat lookup consumer under
its own contract. That does not transfer method, endpoint, fallback or profile
ownership to MediaCat or AdvMedia.

---

## Historical Pre-Cutover Baseline

The `ASTV-25` / `ASTV-26` read-only snapshot captured the superseded schema-v2
deployment. It contained one version-2 Curated Media catalogue with 11 BBC radio
items, one direct stream source per item and one `radio` category. Only the raw
`curated_media.resolve_item` action was available.

In that historical flow ASTV selected method and endpoint from media data stored
in the ASTV intent record. The ASTV AdvMedia adapter called the old standalone
AdvMedia preparation path, `script.advmedia_find_media_record` called
`resolve_item`, AdvMedia built a playback payload from the raw stored item, and
ASTV performed the final playback action. Six of seven historical media intents
bypassed AdvMedia and held provider-specific facts directly in ASTV.

The historical snapshot had no capture manifest or reliable capture timestamp
and omitted configuration inclusion, `.storage`, logs and traces. It proves the
captured files but not their former runtime activation. `ASTV-65` later supplied
the live cutover proof that made schema v3 current.

### Retired historical Mermaid source

The former embedded Mermaid visual showed the retired pre-cutover
`resolve_item` / AdvMedia lookup-wrapper topology. It was removed from the active
narrative under `ASTV-80` so it cannot drift beside the authoritative current
Draw.io map. Its exact source remains preserved in Git history at the T1
baseline `c1d5f5c7a895456b1f81f7a48d3ca2c8a65c407d`, path
`01_Architecture/Archive/MEDIACAT_ARCHITECTURE_pre_ASTV-80_2026-08-25.md`, Git
blob `17f5faedc2ff36ac6f035d32a80b82e20dc1e00f`, and recorded SHA-256
`3ec2bd5bb3ab29dd6d7d48df6bbc665fdd8d4252b0f7c2552f3b6143313c3d20`.

Historical schema-v2 field tables, provider-placement questions and compatibility
risks remain available in the `ASTV-26` Linear record and the immutable
pre-cutover evidence. They are not duplicated as current architecture here.

---

## Contract Alignment

The MediaCat-owned item-lookup contract agrees with the current producer, live
registered input schema, current normalized traces and architecture above. The
three external consumer-owned contracts were reviewed for consistency:

- the ASTV execution-dispatch contract owns current lookup-before-selection,
  complete-record transport and the ASTV assistant path;
- the ASTV-AdvMedia contract owns the direct-core handoff, profile processing and
  ASTV's final playback ownership; and
- the AdvMedia-MediaCat gateway contract owns the separate one-lookup/one-core
  standalone path.

No field, requiredness, semantic, version, registry or ownership change is made
by this architecture audit.

---

## Evidence Limits

1. The Home Assistant MCP exposes registered actions, Media Source WebSocket
   reads, stored script definitions/hashes and traces, but not arbitrary live
   `hass.data` objects or deployed filesystem bytes. Schema-v3 activation is
   proved by the conditional normalized-action registration; the exact deployed
   file hashes remain tied to the `ASTV-65` deployment evidence rather than a
   fresh filesystem read.
2. No fresh normalized lookup action was invoked under `ASTV-84`. Returned-record
   behavior was checked against retained completed live traces, current action
   definitions, maintained source and the authoritative contract.
3. The live configuration-body search was partial because six YAML-defined
   objects were not exposed by Home Assistant's per-object configuration API.
   Known current consumers were verified directly, but absence of every possible
   external consumer is not proven.
4. Retained traces are finite historical runtime evidence, not continuous
   monitoring. The fresh Media Source reads verified current browse, search and
   non-playing resolution behavior during the recorded window.
5. The Governance 2.0 target migration removes the generated MediaCat
   Governance 1.2 loaders and deploys the approved central rulebook and minimal
   product loader. Governance 1.2 remains operational until coordinated cutover.

---

## Current-State Conclusion

Current production uses the normalized schema-v3 design. Curated Media produces
the complete returned-record-v1 mapping, ASTV selects method and endpoint,
AdvMedia processes only the selected Home Assistant method, and ASTV owns the
assistant path and final execution actions. The standalone AdvMedia gateway is a
second direct lookup consumer with its own contract.

`curated_media.resolve_item` and schema-v2 loader/Media Source support are
retained compatibility or historical material. The retired Mermaid source is
preserved only in the T1 Git history and the `ASTV-80` record. None of these is
the current normalized cross-product boundary.
