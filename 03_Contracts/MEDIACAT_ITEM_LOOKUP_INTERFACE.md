# MediaCat Item Lookup Interface Contract

## Contract Record

| Property | Value |
| --- | --- |
| Owner | MediaCat |
| Current producer | Home Assistant action `mediacat.resolve_media_record` |
| Consumers | ASTV; AdvMedia standalone gateway `script.advmedia_prepare_playback`; AdvMedia core as a downstream consumer of the complete normalized record supplied by ASTV or the standalone gateway |
| Contract version | `2.1.0` candidate under `ASTV-52` |
| Returned-record version | `1` |
| Status | Current producer and returned-record v1; proposed backward-compatible presence clarification under `ASTV-52` |
| Source path | `03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md` |

Under Governance 2.0, this provider-owned document is the single authoritative
definition of the MediaCat item-lookup inputs and normalized returned-record
v1. Other contracts must reference this document rather than copy or redefine
the record schema. The former shared Governance 1.2 copy under
`Home_Assistant/contracts/` is retired and non-authoritative.

External contract references resolve to these operational provider-owned
locations:

- `AdvMedia/03_Contracts/ADVMEDIA_MEDIACAT_GATEWAY_INTERFACE.md`;
- `AdvMedia/03_Contracts/ASTV_ADVMEDIA_INTERFACE.md`; and
- `ASTV/03_Contracts/ASTV_EXECUTION_DISPATCH_INTERFACE.md`.

The central contract registry described the former legacy namespace as version
`1.0.0`. ASTV-69 prepared its activation for the coordinated
[ASTV-65](https://linear.app/83degrees/issue/ASTV-65/prove-and-coordinate-mediacat-v3-cross-product-cutover)
cutover. ASTV-77 later revalidated the registry entry at
`2026-08-25T10:40:23.614Z` for the current standalone AdvMedia gateway consumer
without changing any lookup field or semantic meaning.

ASTV-67 made the AdvMedia standalone gateway a direct lookup consumer after
deployment, proof, and legacy-wrapper retirement on 2026-08-25.
Its separate request/result boundary is defined by
`ADVMEDIA_MEDIACAT_GATEWAY_INTERFACE.md`;
this contract continues to own the lookup request and complete normalized
returned record.

## Production and Migration Verification

Fresh read-only Home Assistant verification between
`2026-08-25T15:04:29.407605+01:00` and
`2026-08-25T15:12:23.884728+01:00` confirmed:

- exactly two registered `curated_media` actions:
  `resolve_item(item_id)` and
  `resolve_media_record(catalogue_id, item_id)`;
- the normalized action's live description identifies the loaded schema-v3
  catalogue and returned-record version 1, while the retained raw action is
  explicitly separate;
- maintained producer source registers `resolve_media_record` only for a loaded
  `CatalogueV3`, so live registration proves successful schema-v3 setup;
- `script.astv_intent_engine_media`, configuration hash
  `883e77ec37747186`, is the current ASTV direct lookup consumer;
- `script.advmedia_prepare_playback`, configuration hash
  `9f431a2d1adc80f9`, is the current AdvMedia direct lookup consumer; and
- retained completed traces show each consumer receiving an unwrapped
  returned-record-v1 mapping, with the standalone gateway calling the lookup
  once and passing the complete record to the AdvMedia core once.

The live configuration search found those two direct normalized consumers and no
`resolve_item` consumer. That search was partial because three YAML-defined
scripts and three YAML-defined automations were not exposed by Home Assistant's
per-object configuration API, so it does not prove the absence of every possible
external caller.

No lookup action or other Home Assistant service was invoked during this
verification. The Home Assistant MCP does not expose arbitrary live
`hass.data` objects or deployed filesystem bytes; current producer output was
therefore checked through retained completed live traces, registered action
definitions, maintained source and this contract. No field, requiredness,
semantic or compatibility rule changed as a result of the verification.

That verification is the pre-namespace-migration baseline. On 2026-09-15,
ASTV-221 deployed and registered `mediacat` in parallel. ASTV-223 and ASTV-224
then migrated the AdvMedia and ASTV consumers respectively; Home Assistant
configuration checks and representative end-to-end playback passed after each
deployment. Their repository validation preserved the exact lookup request,
response, failure, and returned-record-version semantics defined here.

ASTV-225 records that the temporary `curated_media` producer was subsequently
removed from production, Home Assistant validation passed, both `mediacat`
actions remained registered, the legacy actions were absent, and representative
ASTV and AdvMedia playback passed. `mediacat.resolve_media_record` is therefore
the sole current implemented producer. This repository candidate aligns the
provider-owned contract with that proven production-first retirement.
Historical evidence and rollback material retain the former namespace without
granting it current contract status.

## Purpose and Scope

The current lookup retrieves one known logical media item using its
catalogue-scoped identity. MediaCat returns one complete, flat, player-independent
record containing every execution method available for that item.

The sole current producer is the Home Assistant action
`mediacat.resolve_media_record`.

`mediacat.resolve_item` is a separate raw-item lookup and is not the normalized
cross-product interface defined by this contract.

This contract does not define search or discovery by title, type, tags, provider,
or other metadata. It does not expose the stored catalogue schema, categories,
loader internals, or profile-specific playback data.

## Ownership

MediaCat owns:

- media identity and catalogue-scoped lookup;
- the normalized record structure and compatibility version;
- catalogue metadata and item membership;
- the execution methods and route-specific source facts available for an item;
- returning all available execution methods without selecting one; and
- explicit lookup failure when the requested item cannot be resolved.

ASTV owns:

- the requested intent and target area;
- execution-method preference and selection;
- endpoint selection;
- runtime fallback policy; and
- passing the complete returned record and its selected method through the
  applicable execution path.

AdvMedia consumes only this normalized returned-record contract. It must not
depend on MediaCat's stored catalogue schema, category structure, loader, parser,
or other undocumented internals.

## Required and Optional

Within this contract, **required** means that the producer promises to supply the
field on the applicable successful interface path and a consumer may rely on it.
**Optional** means that the interface permits omission.

These presence rules are cross-product promises. On success, required fields are
present and non-null. Optional fields are either present with their applicable
value or omitted; the producer does not represent an absent optional value as
`null` or an empty placeholder.

These promises do not define stored catalogue authoring, value-level validation,
defaults, or preventative validation. Those subjects are owned by
[`MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md`](../01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md).

## Lookup Request

The current lookup has exactly these required inputs:

| Field | Presence | Meaning |
| --- | --- | --- |
| `catalogue_id` | Required | Identifies the catalogue that owns or supplies the requested item. |
| `item_id` | Required | Identifies the item within `catalogue_id`. |

The lookup resolves one known item. MediaCat does not infer an alternative
catalogue or item and does not perform execution-method selection.

## Successful Response

Success returns one unwrapped mapping with `returned_record_version: 1`. The
record contains every available entry in `execution_methods`; it does not contain
an ASTV-selected method.

### Required top-level producer promises

| Field | Meaning |
| --- | --- |
| `returned_record_version` | Integer structural version of the normalized consumer-facing record. The initial value is `1`; it is not an item revision or stored-catalogue version. |
| `catalogue_id` | Catalogue identity supplied in the request and owning the returned item. |
| `item_id` | Item identity supplied in the request and resolved within `catalogue_id`. |
| `catalogue_label` | MediaCat-owned human-readable label for browsing, searching, administration, and disambiguation. It is not automatically player metadata. |
| `type` | Player-independent media classification. The initial vocabulary is `radio`, `music_track`, `podcast_episode`, `live_tv`, `tv_episode`, `movie`, and `photo`. |
| `type_metadata` | Non-empty mapping of semantic fields selected by `type`. It contains the required semantic title/name for the selected type and any applicable optional fields listed below. |
| `execution_methods` | Mapping of every execution method available for the item, keyed by the contracted ASTV execution-method name. MediaCat reports availability; ASTV selects a method. |

### Optional top-level fields

| Field | Meaning |
| --- | --- |
| `description` | General player-independent description of the item. |
| `tags` | List of free-text catalogue discovery and search terms. |
| `artwork` | Player-independent artwork mapping. When present, it contains at least one of `local` or `external`; either child may be omitted. Missing artwork is represented by omission of `artwork`, not by `null` or an empty mapping. |
| `content_rating` | Free-text audience or content classification. |

When present, `artwork.local` is a Home Assistant-local artwork reference and
`artwork.external` is an internet-reachable artwork URL. The returned record does
not decide which reference a particular player can use.

### Type-metadata vocabulary

The initial `type_metadata` field vocabulary and producer presence promises are:

| `type` | Required fields | Optional fields |
| --- | --- | --- |
| `radio` | `station_name` | None |
| `music_track` | `track_title` | `artist`, `album_artist`, `album_title`, `composer`, `disc_number`, `track_number`, `release_date` |
| `podcast_episode` | `episode_title` | `podcast_title`, `creator`, `publisher`, `publication_date`, `episode_number` |
| `live_tv` | `channel_name` | None |
| `tv_episode` | `episode_title` | `series_title`, `season_number`, `episode_number`, `first_broadcast_date` |
| `movie` | `movie_title` | `secondary_title`, `studio`, `release_date` |
| `photo` | `image_title` | `creator`, `creation_datetime`, `location`, `latitude`, `longitude`, `width_pixels`, `height_pixels` |

These fields express media semantics, not player-specific names. The required
semantic title/name is not replaced by or derived from `catalogue_label`.
Optional type-metadata fields are omitted when absent and are not returned as
`null` or empty placeholders. Detailed stored-value formats and validation are
owned by the schema architecture.

### Execution-method structure

Each `execution_methods.<execution_method>` entry contains exactly one `source`.
The mapping key is the contracted ASTV execution-method name and is not duplicated
inside the entry. MediaCat returns every available method and does not attach ASTV
preference, fallback order, or endpoint data.

`execution_methods` contains at least one entry on every successful record.

The initial source vocabulary and presence promises are:

| `source_type` | Required producer promises | Optional fields |
| --- | --- | --- |
| `url` | `source_type`, `url`, `mime_type` | `provider` |
| `ha_media_source` | `source_type`, `provider`, `uri`, `media_type` | None |
| `assistant_command` | `source_type`, `provider`, `command`, `append_target` | None |

Source field meanings are:

| Field | Meaning |
| --- | --- |
| `source_type` | Selects the applicable source structure. |
| `url` | Directly playable media URL. |
| `mime_type` | Media representation required by the execution layer for a URL source. |
| `provider` | Technical system supplying or resolving the source. For `url` it may be omitted; for `ha_media_source` it identifies the Media Source provider; for `assistant_command` it identifies the assistant family. |
| `uri` | Opaque Home Assistant `media-source://` reference. MediaCat does not dereference it during lookup. |
| `media_type` | Home Assistant media content type used with an `ha_media_source` URI. |
| `command` | Item-specific assistant command text. |
| `append_target` | Boolean telling ASTV whether to append its independently selected endpoint phrase to the assistant command. |

Provider identity does not select the ASTV execution method. Assistant identity is
carried by `provider`, not by creating a provider-specific source type.

### Canonical shape

```yaml
returned_record_version: 1
catalogue_id: <owning catalogue>
item_id: <resolved item ID>
catalogue_label: <MediaCat browse/admin label>
type: <radio|music_track|podcast_episode|live_tv|tv_episode|movie|photo>
description: <optional player-independent description>
tags:
  - <optional free-text tag>
artwork:
  local: <optional Home Assistant-local artwork reference>
  external: <optional internet-reachable artwork URL>
content_rating: <optional free-text classification>
type_metadata:
  <fields selected by type>
execution_methods:
  <contracted_execution_method>:
    source:
      source_type: <url|ha_media_source|assistant_command>
      <fields selected by source_type>
```

For stored Curated Media items, MediaCat copies the complete selected item mapping
into this flat record and adds `returned_record_version`, `catalogue_id`, and
`item_id`. It does not return `catalogue_schema_version`, `categories`, the full
`items` mapping, lookup context, ASTV selection context, or player-specific
translations. Future catalogue adapters must produce this normalized contract or
introduce an explicitly versioned extension.

## Consumer Rules

ASTV may inspect `execution_methods` to select a method according to ASTV-owned
preference and endpoint policy. The selected method name remains ASTV context and
is not added to the MediaCat record.

On ASTV's direct-core path, AdvMedia receives the complete record from ASTV
together with `selected_execution_method`. On the separately contracted
standalone path, the AdvMedia gateway obtains the same complete record directly
from this lookup and passes it unchanged to the same core. The core reads
exactly:

`media_record.execution_methods[selected_execution_method].source`

The AdvMedia core does not select another method, perform a MediaCat lookup,
inspect stored catalogue structure, or reinterpret category and loader data.
The exact ASTV-to-AdvMedia handoff is defined in
`ASTV_ADVMEDIA_INTERFACE.md`.

The standalone gateway's one-lookup/one-core behavior is defined in
`ADVMEDIA_MEDIACAT_GATEWAY_INTERFACE.md`.

The separate ASTV-owned media and Google Home paths are defined in
`ASTV_EXECUTION_DISPATCH_INTERFACE.md`.

## Failure Contract

If MediaCat cannot resolve the requested `catalogue_id` or `item_id`:

- MediaCat stops the lookup with an explicit error identifying the requested
  reference;
- MediaCat returns no partial or empty normalized record;
- ASTV stops the media request before method and endpoint selection;
- ASTV does not automatically try another catalogue, item, or legacy media data;
  and
- this contract does not introduce a detailed error-code vocabulary or broader
  validation framework.

This is execution-boundary behaviour, not preventative catalogue data-entry
validation.

## Compatibility Policy

### Completed namespace migration

Changing the producer action from the historical
`curated_media.resolve_media_record` to
`mediacat.resolve_media_record` is a breaking endpoint-name change and is the
reason for contract version `2.0.0`. It does not change request fields,
response fields, their meanings, failure behaviour, or
`returned_record_version: 1`.

During the completed migration both action domains accepted the same exact
request and promised the same response and failure behaviour. Consumers changed
only the Home Assistant action domain and continue to send logical
`catalogue_id: curated_media`; they must not substitute `mediacat` for the
catalogue identifier. Removal of the temporary legacy action completed the
endpoint migration and did not change the returned-record version.

### Returned-record compatibility

The `2.1.0` candidate under `ASTV-52` strengthens producer guarantees for
already modelled returned-record-v1 fields: the applicable semantic title/name
is required, optional absence is omission rather than `null`, artwork is
non-empty when present, and at least one execution method is returned. It does
not add, remove, rename, move, or reinterpret a returned field, and it does not
change the returned-record version. Current catalogue records already satisfy
these guarantees; detailed preventative enforcement remains separate
MediaCat implementation work.

Consumers of returned-record version `1` must ignore unknown additive fields.
Adding such a field without changing existing meaning is compatible.

This additive compatibility rule applies to the consumer-facing returned record
only. It does not permit arbitrary unknown fields in a stored schema-v3
catalogue; stored vocabulary and extension policy are owned by the schema
architecture.

Removing, renaming, moving, changing the type of, changing the presence promise
of, or reinterpreting a returned field is breaking. A breaking change requires a
new `returned_record_version`, coordinated producer and consumer work, updated
contracts, and cutover evidence.

Stored `catalogue_schema_version` evolves independently and is not exposed through
this interface. Consumers must not use stored catalogue structure as a substitute
for this contract.

## Implementation and Cutover History

This contract did not authorize runtime or catalogue-data change by itself.
Separate work instructions owned implementation and proof:

- [ASTV-31](https://linear.app/83degrees/issue/ASTV-31/implement-mediacat-normalized-item-lookup-and-returned-record-v1) — MediaCat lookup and returned-record v1 producer.
- [ASTV-55](https://linear.app/83degrees/issue/ASTV-55/implement-curated-media-catalogue-schema-v3-loader-and-model) and [ASTV-56](https://linear.app/83degrees/issue/ASTV-56/migrate-current-media-data-into-curated-media-schema-v3) — stored Curated Media schema and data migration.
- [ASTV-57](https://linear.app/83degrees/issue/ASTV-57/update-curated-media-home-assistant-media-source-for-schema-v3) — MediaCat Media Source compatibility.
- [ASTV-60](https://linear.app/83degrees/issue/ASTV-60/update-astv-media-intent-engine-for-mediacat-lookup-and-method-selection) — ASTV lookup and method selection consumer.
- [ASTV-58](https://linear.app/83degrees/issue/ASTV-58/implement-advmedia-processing-core-for-mediacat-returned-records) and [ASTV-27](https://linear.app/83degrees/issue/ASTV-27/implement-advmedia-source-translation-for-mediacat-returned-records) — AdvMedia normalized-record processing.
- [ASTV-61](https://linear.app/83degrees/issue/ASTV-61/implement-astv-execution-dispatch-media-context-changes), [ASTV-62](https://linear.app/83degrees/issue/ASTV-62/update-astv-ha-media-player-path-for-normalized-mediacat-handoff), and [ASTV-63](https://linear.app/83degrees/issue/ASTV-63/update-astv-google-home-media-path-for-mediacat-execution-data) — ASTV dispatch and execution consumers.
- [ASTV-65](https://linear.app/83degrees/issue/ASTV-65/prove-and-coordinate-mediacat-v3-cross-product-cutover) — coordinated cross-product proof and cutover.
- [ASTV-67](https://linear.app/83degrees/issue/ASTV-67/implement-standalone-advmedia-mediacat-gateway-and-clean-up-legacy) — implemented and proved the current standalone AdvMedia gateway and retired its legacy lookup wrapper.
- [ASTV-69](https://linear.app/83degrees/issue/ASTV-69/governance-cr-activate-mediacat-contracts-in-the-central-registry-at) — prepared registry, manifest, index, and governance-validation activation for cutover.
- [ASTV-221](https://linear.app/83degrees/issue/ASTV-221/rename-curated-media-integration-and-domain-to-mediacat-mediacat) — introduced and validated the `mediacat` namespace in parallel.
- [ASTV-223](https://linear.app/83degrees/issue/ASTV-223/migrate-advmedia-mediacat-lookup-from-curated-media-to-mediacat) and [ASTV-224](https://linear.app/83degrees/issue/ASTV-224/migrate-astv-mediacat-references-from-curated-media-to-mediacat) — migrated and validated the active consumers.
- [ASTV-225](https://linear.app/83degrees/issue/ASTV-225/retire-legacy-curated-media-compatibility-surface) — recorded the production-first legacy-producer retirement and aligned repository source and governed knowledge with the resulting single-domain state.

## Design Provenance

This contract records the approved decisions from
[ASTV-24](https://linear.app/83degrees/issue/ASTV-24/define-curated-media-types-field-completeness-and-schema-structure),
[ASTV-23](https://linear.app/83degrees/issue/ASTV-23/design-mediacat-returned-record-mapping-into-google-cast-metadata), and
[ASTV-54](https://linear.app/83degrees/issue/ASTV-54/define-mediacat-assistant-command-source-for-g-home-device).
`ASTV-52` adds the consumer-facing presence promises above while leaving stored
authoring and preventative validation with the schema architecture. It does not
authorize runtime validation implementation.
