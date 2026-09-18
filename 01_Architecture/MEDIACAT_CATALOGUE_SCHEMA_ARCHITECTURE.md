# MediaCat Catalogue Schema Architecture

## 1. Status and Authority

### 1.1 Document State

- Candidate state: proposed under `ASTV-52` pending governed human review.
- Intended accepted state: authoritative current-approved stored-catalogue
  architecture for `catalogue_schema_version: 3`.
- Implementation state: detailed enforcement is an approved target only. The
  current implemented loader enforces schema-version dispatch and the minimum
  root shape but does not yet enforce all rules in this document.

### 1.2 Authority Boundary

This document owns the stored MediaCat catalogue schema, authoring semantics,
and preventative-validation policy for schema version 3. A maintainer must be
able to author, review, and modify a catalogue from this document without
inspecting Python source.

The provider-owned
[`MEDIACAT_ITEM_LOOKUP_INTERFACE.md`](../03_Contracts/MEDIACAT_ITEM_LOOKUP_INTERFACE.md)
remains the sole authority for the consumer-facing lookup request and normalized
returned record. The general runtime architecture remains in
[`MEDIACAT_ARCHITECTURE.md`](MEDIACAT_ARCHITECTURE.md). This document does not
transfer ASTV method or endpoint selection, AdvMedia processing, or external
provider ownership to MediaCat.

## 2. Design and Evidence Basis

The policy was assessed against:

- the schema-v3 field inventory and normalized-record design accepted in
  `ASTV-24`;
- the `assistant_command` design accepted in `ASTV-54`;
- the direct-URL, Radio Browser, Google Home, and Media Source proof completed
  by `ASTV-65`;
- the current maintained catalogue at
  `04_Source/config/mediacat/catalogue.yaml`;
- the current MediaCat runtime architecture and lookup contract; and
- the material policy choices approved by Graham in `ASTV-52` on 2026-09-18.

The maintained catalogue's 17 current records conform to the policy defined
here. The representative seven-type fixture contains fields that were
deliberately accepted by the earlier permissive model but are not part of this
closed schema; it must be aligned by separately authorized implementation work
before it can serve as a strict-validation fixture.

## 3. Complete Catalogue Skeleton

The stored YAML is traversed in the order shown below. Bracketed names describe
dynamic mapping keys; they are not literal field names.

```yaml
catalogue_id: <catalogue_id>
catalogue_schema_version: 3
items:
  <item_id>:
    catalogue_label: <label>
    type: <media_type>
    description: <description>
    tags:
      - <tag>
    artwork:
      local: /local/<path>
      external: https://<host>/<path>
    content_rating: <rating>
    type_metadata:
      <type-specific fields>: <values>
    execution_methods:
      <execution_method>:
        source:
          source_type: <source_type>
          <source-specific fields>: <values>
categories:
  <category_id>:
    category_label: <label>
    items:
      - <item_id>
```

Optional fields shown in this skeleton are omitted when they do not apply. The
following sections define each structural level, beginning at the root and
ending at category records.

## 4. Root Catalogue Object

### 4.1 Root Shape

```yaml
catalogue_id: curated_media
catalogue_schema_version: 3
items:
  example_station: {}
categories: {}
```

The root has exactly four fields:

| Field | Presence | Type and rule |
| --- | --- | --- |
| `catalogue_id` | Required | Identifier string. The maintained catalogue value is `curated_media`. |
| `catalogue_schema_version` | Required | Integer exactly `3`. It is not the integration version or returned-record version. |
| `items` | Required | Non-empty ordered mapping of item ID to item record. |
| `categories` | Required | Ordered mapping of category ID to category record; it may be empty. |

The empty item object above illustrates root shape only; it is not a valid
complete item. Section 5 defines the required item fields.

### 4.2 Catalogue-Scoped Identity

Item identity is catalogue-scoped: the canonical identity is the pair
`(catalogue_id, item_id)`. The item ID exists only as the `items` mapping key and
must not be duplicated inside the stored item.

### 4.3 Root Ordering

The `items` and `categories` mappings are authored ordered data. Validation and
loading must preserve their YAML mapping order. Root category order defines
category browse order.

## 5. `items` Mapping and Item Objects

### 5.1 `items` Mapping

```yaml
items:
  example_station:
    catalogue_label: Example Station
    type: radio
    type_metadata:
      station_name: Example Station
    execution_methods:
      ha_mplayer:
        source:
          source_type: url
          url: https://streams.example.test/live.aac
          mime_type: audio/aac
```

`items` is a required, non-empty ordered mapping. Every mapping key is an item
ID satisfying the identifier rule in section 7.2. Every value is an item object
defined in section 5.2. Duplicate item keys are invalid.

### 5.2 Item Object

```yaml
catalogue_label: Example Station — London
type: radio
description: Independent live radio
tags:
  - radio
  - london
artwork:
  local: /local/mediacat/example-station.png
  external: https://images.example.test/example-station.png
content_rating: general
type_metadata:
  station_name: Example Station
execution_methods:
  ha_mplayer:
    source:
      source_type: url
      url: https://streams.example.test/live.aac
      mime_type: audio/aac
```

Each `items.<item_id>` value contains only these fields:

| Field | Presence | Type and meaning |
| --- | --- | --- |
| `catalogue_label` | Required | Non-blank MediaCat browse, search, administration, and disambiguation label. It is not player metadata. |
| `type` | Required | One of the seven supported media types in section 5.4. |
| `description` | Optional | Non-blank player-independent description. |
| `tags` | Optional | Non-empty ordered list of unique, non-blank free-text strings. No controlled vocabulary is imposed. |
| `artwork` | Optional | Artwork object defined in section 5.3. |
| `content_rating` | Optional | Non-blank free-text classification. No rating-system vocabulary is imposed. |
| `type_metadata` | Required | Type-selected object defined in section 5.4. |
| `execution_methods` | Required | Non-empty mapping defined in section 5.5. |

Required fields must be present and valid. Optional fields are omitted rather
than stored as null, blank, or empty placeholders.

### 5.3 `artwork` Object

```yaml
artwork:
  local: /local/mediacat/example-station.png
  external: https://images.example.test/example-station.png
```

`artwork` contains only `local` and `external`. Each child is optional, but at
least one must be present when `artwork` exists.

| Field | Presence | Rule |
| --- | --- | --- |
| `local` | Optional | Non-blank `/local/...` Home Assistant reference. |
| `external` | Optional | Absolute HTTP(S) URL with a host. |

A local-only object is valid:

```yaml
artwork:
  local: /local/mediacat/example-station.png
```

An external-only object is also valid:

```yaml
artwork:
  external: https://images.example.test/example-station.png
```

Missing artwork is valid. MediaCat does not synthesize a placeholder or copy
one artwork field into the other. Stored order does not express preference.
Known consumers retain their governed behavior: the Media Source projection
uses `local`, while the current Google Cast mapping prefers `external` and then
uses `local`. Those consumer behaviors do not make artwork required here.

### 5.4 `type_metadata` Object

```yaml
type: music_track
type_metadata:
  track_title: Example Track
  artist: Example Artist
  album_title: Example Album
  disc_number: 1
  track_number: 2
  release_date: "2026-09-18"
```

`type_metadata` contains only the fields listed for the selected `type`. The
semantic title or name field is required; every other listed field is optional.
A required semantic title is never derived from `catalogue_label`.

| `type` | Required semantic field | Optional fields |
| --- | --- | --- |
| `radio` | `station_name` | None |
| `music_track` | `track_title` | `artist`, `album_artist`, `album_title`, `composer`, `disc_number`, `track_number`, `release_date` |
| `podcast_episode` | `episode_title` | `podcast_title`, `creator`, `publisher`, `publication_date`, `episode_number` |
| `live_tv` | `channel_name` | None |
| `tv_episode` | `episode_title` | `series_title`, `season_number`, `episode_number`, `first_broadcast_date` |
| `movie` | `movie_title` | `secondary_title`, `studio`, `release_date` |
| `photo` | `image_title` | `creator`, `creation_datetime`, `location`, `latitude`, `longitude`, `width_pixels`, `height_pixels` |

Exact valid shapes for each type are illustrated below. Optional lines may be
omitted, but no unlisted field may be added.

```yaml
# radio
type: radio
type_metadata:
  station_name: Example Station

# music_track
type: music_track
type_metadata:
  track_title: Example Track
  artist: Example Artist
  album_artist: Example Album Artist
  album_title: Example Album
  composer: Example Composer
  disc_number: 1
  track_number: 2
  release_date: "2026-09-18"

# podcast_episode
type: podcast_episode
type_metadata:
  episode_title: Example Episode
  podcast_title: Example Podcast
  creator: Example Creator
  publisher: Example Publisher
  publication_date: "2026-09-18"
  episode_number: 3

# live_tv
type: live_tv
type_metadata:
  channel_name: Example Channel

# tv_episode
type: tv_episode
type_metadata:
  episode_title: Example Episode
  series_title: Example Series
  season_number: 1
  episode_number: 4
  first_broadcast_date: "2026-09-18"

# movie
type: movie
type_metadata:
  movie_title: Example Movie
  secondary_title: An Example Subtitle
  studio: Example Studio
  release_date: "2026-09-18"

# photo
type: photo
type_metadata:
  image_title: Example Photograph
  creator: Example Photographer
  creation_datetime: "2026-09-18T12:00:00Z"
  location: London
  latitude: 51.5072
  longitude: -0.1276
  width_pixels: 1920
  height_pixels: 1080
```

The title/name fields and all other textual metadata are non-blank strings.
Additional relationships and value rules are:

| Fields | Rule |
| --- | --- |
| `release_date`, `publication_date`, `first_broadcast_date` | Valid quoted `YYYY-MM-DD` calendar date. |
| `creation_datetime` | Valid quoted RFC 3339 datetime with timezone. |
| `disc_number`, `track_number`, `episode_number`, `season_number` | Integer greater than zero. |
| `latitude`, `longitude` | Both present or both absent; finite numbers within their geographic ranges. |
| `width_pixels`, `height_pixels` | Both present or both absent; integers greater than zero. |

The temporary current `news_briefing` classification remains `type: radio` with
`station_name: My News Briefing` until `ASTV-66` authorizes a replacement type.
This compatibility record does not broaden the media-type vocabulary.

### 5.5 `execution_methods` Mapping

```yaml
execution_methods:
  ha_mplayer:
    source:
      source_type: url
      url: https://streams.example.test/live.aac
      mime_type: audio/aac
  g_home_device:
    source:
      source_type: assistant_command
      provider: google_assistant
      command: Play Example Station
      append_target: true
```

`execution_methods` is a required, non-empty mapping. Each key is a current
contracted ASTV execution-method name and each value is the entry defined in
section 5.5.1.

| Execution method | Permitted `source_type` |
| --- | --- |
| `ha_mplayer` | `url`, `ha_media_source` |
| `g_home_device` | `assistant_command` |

An item may expose either current method or both when it has a valid source for
each. Mapping order does not define priority or fallback. ASTV owns method
preference and selection; MediaCat returns all authored methods. Adding another
method name or changing a method/source pairing requires separately approved
cross-product design and compatibility assessment.

#### 5.5.1 Execution-Method Entry

```yaml
ha_mplayer:
  source:
    source_type: url
    url: https://streams.example.test/live.aac
    mime_type: audio/aac
```

Every `execution_methods.<method>` value contains exactly one required field,
`source`. It may not contain configuration, priority, fallback, endpoint, or
other fields. The `source` object is selected by `source_type` as described in
section 5.5.2.

#### 5.5.2 `source` Object

```yaml
source:
  source_type: url
  url: https://streams.example.test/live.aac
  mime_type: audio/aac
```

Every `execution_methods.<method>.source` is a mapping selected by required
`source_type`. It contains only the fields in the applicable row.

| `source_type` | Required fields | Optional fields |
| --- | --- | --- |
| `url` | `source_type`, `url`, `mime_type` | `provider` |
| `ha_media_source` | `source_type`, `provider`, `uri`, `media_type` | None |
| `assistant_command` | `source_type`, `provider`, `command`, `append_target` | None |

The source type must be permitted for its parent method by section 5.5.

##### 5.5.2.1 `url` Source

```yaml
source:
  source_type: url
  url: https://streams.example.test/live.aac
  mime_type: audio/aac
  provider: example_streams
```

| Field | Presence | Rule |
| --- | --- | --- |
| `source_type` | Required | Exactly `url`. |
| `url` | Required | Absolute HTTP(S) URL with a non-empty host. |
| `mime_type` | Required | Non-blank `type/subtype` value. |
| `provider` | Optional | Provider identifier. |

MediaCat does not connect to the URL, test stream availability, infer a MIME
type, or retry another source during catalogue loading or lookup.

##### 5.5.2.2 `ha_media_source` Source

```yaml
source:
  source_type: ha_media_source
  provider: radio_browser
  uri: media-source://radio_browser/example-station
  media_type: station
```

| Field | Presence | Rule |
| --- | --- | --- |
| `source_type` | Required | Exactly `ha_media_source`. |
| `provider` | Required | Provider identifier. |
| `uri` | Required | Absolute `media-source://` URI with non-empty authority and resource path; authority equals `provider`. |
| `media_type` | Required | Non-blank Home Assistant media-content-type string. |

The URI remains opaque after these structural checks. MediaCat does not
dereference it during catalogue loading or normalized lookup. Runtime provider
failure remains at the Home Assistant Media Source execution boundary.

##### 5.5.2.3 `assistant_command` Source

```yaml
source:
  source_type: assistant_command
  provider: google_assistant
  command: Play Example Station
  append_target: true
```

| Field | Presence | Rule |
| --- | --- | --- |
| `source_type` | Required | Exactly `assistant_command`. |
| `provider` | Required | Provider identifier. |
| `command` | Required | Non-blank item-specific command string. |
| `append_target` | Required | YAML boolean. |

MediaCat does not append an endpoint, construct a final assistant command, or
execute it. Those remain ASTV responsibilities.

## 6. `categories` Mapping and Category Objects

### 6.1 `categories` Mapping

```yaml
categories:
  featured:
    category_label: Featured
    items:
      - example_station
```

`categories` is a required ordered mapping and may be empty. Each mapping key
is a category ID satisfying the identifier rule in section 7.2. Every value is
a category object defined in section 6.2. Duplicate category keys are invalid.

The category model is flat. Categories have no parent, child, priority, or
separate order field. Root mapping order defines category browse order.

### 6.2 Category Object

```yaml
featured:
  category_label: Featured
  items:
    - example_station
    - another_station
```

Each `categories.<category_id>` value contains exactly:

| Field | Presence | Rule |
| --- | --- | --- |
| `category_label` | Required | Non-blank catalogue and Media Browser label. |
| `items` | Required | Non-empty ordered list of unique item IDs. Every reference must exist in root `items`. |

The `items` list defines membership display order. An item may appear in
multiple categories or in none. Absence from all categories does not prevent
catalogue-scoped lookup. Category membership also does not guarantee Media
Source visibility: that projection applies its separately documented playable-
item rules.

## 7. Cross-Cutting Authoring and Validation Rules

### 7.1 Closed Vocabulary

1. Schema v3 is a closed authoring vocabulary. Every field must be defined by
   this document at its exact structural location.
2. There are no arbitrary additive-field extension points in schema v3.
   Unknown root, item, metadata, category, execution-method, or source fields
   are validation errors. Dynamic mapping keys explicitly defined in this
   document are not unknown fields.
3. A new stored field or extension point requires an approved schema-
   architecture change. If it can appear in a normalized returned record, the
   lookup contract and consumer compatibility must also be assessed.
4. Stored-data closed-vocabulary rules are separate from returned-record
   compatibility. Consumers of returned-record version 1 continue to ignore
   unknown additive returned fields as defined by the lookup contract.

### 7.2 Identifiers and Mapping Keys

`catalogue_id`, item IDs, category IDs, execution-method keys, and provider
identifiers are strings matching:

```text
^[a-z0-9][a-z0-9_-]*$
```

They are case-sensitive. YAML mapping keys must be unique; duplicate keys are a
validation error rather than last-value-wins input.

The maintained Curated Media catalogue uses `catalogue_id: curated_media`.
Future catalogues may use another conforming identifier only through separately
authorized adapter and catalogue work.

### 7.3 Missing, Empty, and Null Values

| Situation | Rule |
| --- | --- |
| Missing required field | Invalid. |
| Missing optional field | Valid; omission means no value is supplied. |
| Explicit YAML `null` | Invalid for every modelled field. |
| Blank or whitespace-only string | Invalid. Values are not silently trimmed or rewritten. |
| Empty optional mapping or list | Invalid; omit the optional field instead. |
| Empty required mapping or list | Invalid except that the root `categories` mapping may be empty. |
| YAML boolean where an integer or number is required | Invalid. |

No schema field has a generated default.

### 7.4 Common Value Formats

- Ordinary text fields are non-blank strings.
- Date fields are quoted strings containing a valid calendar date in
  `YYYY-MM-DD` form.
- Datetime fields are quoted RFC 3339 strings with an explicit `Z` or numeric
  UTC offset.
- Counts, sequence numbers, widths, and heights are integers greater than zero.
- Latitude and longitude are finite numbers; latitude is between `-90` and
  `90`, and longitude is between `-180` and `180`.
- Direct and external-artwork URLs are absolute `http` or `https` URLs with a
  non-empty host. Query strings are permitted and no network request is made
  during validation.
- A Home Assistant local artwork reference begins with `/local/` and contains a
  non-empty path after that prefix.
- A MIME type is a non-blank `type/subtype` value. MediaCat does not maintain a
  codec or format allowlist.

### 7.5 Defaults and Fallback

- There are no stored or returned default values.
- A semantic title or name never falls back to `catalogue_label`.
- Missing optional metadata remains omitted; MediaCat does not emit `null` or
  an empty placeholder.
- Missing artwork is permitted and produces no placeholder.
- MediaCat lookup does not choose, reorder, or retry execution methods.
- A source failure does not cause MediaCat or AdvMedia to select another source
  or method. Runtime fallback policy remains ASTV-owned.
- Lookup of an unknown catalogue or item fails explicitly and returns no
  partial or alternative record.

## 8. Validation Ownership and Failure Behavior

| Boundary | Owner and responsibility | Failure behavior |
| --- | --- | --- |
| YAML decoding and duplicate-key detection | MediaCat catalogue loading | Reject the complete candidate catalogue with a path-specific error. |
| Stored schema structure, vocabulary, requiredness, values, references, and ordering retention | MediaCat catalogue loading | Reject the complete candidate catalogue; retain no partial loaded state. |
| Catalogue and item lookup identity | MediaCat normalized lookup | Fail explicitly for the requested reference and return no record. |
| Returned-record presence and compatibility | MediaCat lookup contract and producer | Do not emit a successful partial record. Contract implementation gaps require separately authorized MediaCat work. |
| Method preference and selection | ASTV | Stop according to the ASTV contract when no configured method matches; MediaCat does not substitute. |
| Selected source translation and profile processing | AdvMedia for `ha_mplayer` | Fail at the AdvMedia boundary; do not choose another method/source. |
| Assistant command construction and execution | ASTV for `g_home_device` | Fail at the ASTV execution boundary; MediaCat does not execute or retry. |
| External URL, Media Source provider, assistant, endpoint, or player availability | Respective runtime owner | Execution-time failure; preventative catalogue validation does not claim liveness. |

Validation errors should identify the catalogue path and violated rule, for
example:

```text
items.example_photo.type_metadata.longitude is required when latitude is present
```

The validator must report enough location context to correct authored data. An
implementation may aggregate independent errors or stop after the first, but it
must not silently discard, coerce, default, or partially activate invalid data.
The complete catalogue is accepted or rejected atomically.

## 9. Relationship to Returned Record Version 1

For a successful lookup of a schema-v3 stored item, MediaCat copies the complete
defined item record into a new flat response and adds:

- `returned_record_version: 1`;
- root `catalogue_id`; and
- `item_id` from the selected `items` mapping key.

It does not return `catalogue_schema_version`, `categories`, the root `items`
mapping, or lookup/selection context. The lookup contract, not this document,
defines the resulting consumer promises.

Stored `catalogue_schema_version` and consumer-facing
`returned_record_version` have independent compatibility lifecycles. A stored
schema change does not automatically change the returned-record version; a
returned-record breaking change requires its own contract versioning and
coordinated consumer work.

Because schema v3 has no stored additive extension point, arbitrary unknown
stored fields must never reach lookup. Separately, a future producer or
returned-record version may add a contract-compatible returned field through
governed work, and version-1 consumers remain required to ignore unknown
additive returned fields.

## 10. Representative Invalid Examples

Each fragment is invalid at catalogue-load time.

### 10.1 Unknown Field

```yaml
items:
  example_station:
    catalogue_lable: Example Station
```

`catalogue_lable` is not a defined field. The loader must report the unknown
field; it must not treat it as an additive extension or silently lose the label.

### 10.2 Explicit Null and Empty Optional Collection

```yaml
description: null
tags: []
```

Optional unknown values are omitted. Explicit null and an empty optional list
are both invalid.

### 10.3 Missing Semantic Title

```yaml
catalogue_label: Example Movie
type: movie
type_metadata: {}
```

`movie_title` is required. `catalogue_label` is not a fallback.

### 10.4 Invalid Method/Source Pairing

```yaml
execution_methods:
  ha_mplayer:
    source:
      source_type: assistant_command
      provider: google_assistant
      command: Play Example Station
      append_target: true
```

`ha_mplayer` permits only `url` or `ha_media_source`; MediaCat must reject the
record rather than allow a downstream dispatch failure.

### 10.5 Invalid Media Source Identity

```yaml
source_type: ha_media_source
provider: radio_browser
uri: media-source://another_provider/example-station
media_type: station
```

The URI authority does not match `provider`.

### 10.6 Unpaired Coordinates

```yaml
type: photo
type_metadata:
  image_title: Example Photograph
  latitude: 51.5072
```

`longitude` is required whenever `latitude` is present.

### 10.7 Invalid Category Membership

```yaml
categories:
  featured:
    category_label: Featured
    items:
      - missing_item
      - missing_item
```

The reference is unknown and duplicated. Both violate the category rules.

## 11. Complete Worked Catalogue

This assembled example covers ordered category membership, optional item data,
all three source types, and an item with multiple execution methods.

```yaml
catalogue_id: curated_media
catalogue_schema_version: 3
items:
  station_alpha:
    catalogue_label: Station Alpha — London
    type: radio
    description: Independent live radio
    tags:
      - radio
      - london
    artwork:
      local: /local/mediacat/station-alpha.png
      external: https://images.example.test/station-alpha.png
    content_rating: general
    type_metadata:
      station_name: Station Alpha
    execution_methods:
      ha_mplayer:
        source:
          source_type: url
          url: https://streams.example.test/station-alpha.m3u8
          mime_type: application/vnd.apple.mpegurl
          provider: example_streams
      g_home_device:
        source:
          source_type: assistant_command
          provider: google_assistant
          command: Play Station Alpha
          append_target: true
  station_beta:
    catalogue_label: Station Beta
    type: radio
    artwork:
      local: /local/mediacat/station-beta.png
    type_metadata:
      station_name: Station Beta
    execution_methods:
      ha_mplayer:
        source:
          source_type: ha_media_source
          provider: radio_browser
          uri: media-source://radio_browser/example-station
          media_type: station
categories:
  featured:
    category_label: Featured
    items:
      - station_beta
      - station_alpha
  radio:
    category_label: Radio
    items:
      - station_alpha
      - station_beta
```

## 12. Compatibility and Schema Evolution

- The maintained 17-item Curated Media catalogue already uses only the defined
  schema vocabulary and requires no data migration for this policy.
- The current schema-v3 loader is intentionally more permissive than this
  approved target. It preserves unknown fields and performs only minimum root
  checks. That is an implementation gap, not permission to author such fields.
- The current broad fixture contains deliberate additive root, item, source,
  and category fields used to prove earlier preservation behavior. Strict
  validation implementation must replace or relocate those cases and add
  rejection coverage.
- Enforcing this document in production is out of scope for `ASTV-52` and
  requires separately authorized `Change: Code` work, tests, Beta deployment,
  and validation.
- The normalized response remains returned-record version 1. Required semantic
  titles and non-null presence strengthen the producer guarantee without
  changing the response shape used by current consumers.
- Returned-record consumers retain additive compatibility and must ignore
  unknown additive returned fields. This rule does not make unknown stored
  fields valid.
- A new stored field, media type, source type, execution method, or defined
  extension point requires an approved change to this architecture. Any impact
  on the returned record must be assessed independently against its contract.

## 13. Required Follow-Up Implementation

`ASTV-52` changes governed architecture and the lookup contract only.
`ASTV-235` is the separately authorized MediaCat implementation issue and is
required to:

1. implement closed-vocabulary schema-v3 validation, duplicate-key detection,
   path-specific errors, and all structural/value constraints in MediaCat;
2. replace permissive additive-field tests with strict rejection and complete
   valid/invalid fixture coverage;
3. prove current catalogue conformance and schema-v2 compatibility;
4. validate Home Assistant setup failure and atomic non-activation for invalid
   schema-v3 catalogues; and
5. deploy and prove the accepted implementation through the code workflow and
   Beta gates.

No runtime, catalogue data, Home Assistant deployment, or consumer
implementation is changed by `ASTV-52`.
