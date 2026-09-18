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

## 3. Root Catalogue Object

### 3.1 Root Shape

```yaml
catalogue_id: curated_media
catalogue_schema_version: 3
items: {...}
categories: {...}
```

The root has exactly four fields. `{...}` defers a nested mapping to the section
that owns it; `[...]` similarly summarizes a list. Optional example fields are
marked with `# optional`.

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `catalogue_id` | Required | String | — | Catalogue identifier. The maintained catalogue value is `curated_media`; the identifier rules in section 6.2 apply. |
| `catalogue_schema_version` | Required | Integer | `3` | Stored catalogue schema version. It is not the integration version or returned-record version. |
| `items` | Required | Object | — | Non-empty ordered mapping of item ID to item object, defined in section 4. |
| `categories` | Required | Object | — | Ordered mapping of category ID to category object, defined in section 5; it may be empty. |

### 3.2 Catalogue-Scoped Identity

Item identity is catalogue-scoped: the canonical identity is the pair
`(catalogue_id, item_id)`. The item ID exists only as the `items` mapping key and
must not be duplicated inside the stored item.

### 3.3 Root Ordering

The `items` and `categories` mappings are authored ordered data. Validation and
loading must preserve their YAML mapping order. Root category order defines
category browse order.

## 4. `items` Collection

```yaml
items:
  <item_id>: {...}
```

`items` is a required, non-empty ordered mapping. `<item_id>` represents the
string mapping key; its indented value is the item object. Every item ID
satisfies the identifier rule in section 6.2. Duplicate item keys are
invalid. Item mapping order is authored data and must be preserved. The item ID
exists only as the mapping key and is not repeated inside its object.

### 4.1 `<item_id>`

```yaml
<item_id>:
  catalogue_label: Example Station — London
  type: radio
  description: Independent live radio  # optional
  tags: [...]                           # optional
  artwork: {...}                        # optional
  content_rating: general              # optional
  type_metadata: {...}
  execution_methods: {...}
```

Each item object contains only these fields:

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `catalogue_label` | Required | String | — | Non-blank MediaCat browse, search, administration, and disambiguation label. It is not player metadata. |
| `type` | Required | String | `radio`, `music_track`, `podcast_episode`, `live_tv`, `tv_episode`, `movie`, `photo` | Selects the exact `type_metadata` vocabulary in section 4.3. |
| `description` | Optional | String | — | Non-blank player-independent description. |
| `tags` | Optional | List of strings | — | Non-empty ordered list of unique, non-blank free-text tags. No controlled vocabulary is imposed. |
| `artwork` | Optional | Object | — | Artwork references defined in section 4.2. |
| `content_rating` | Optional | String | — | Non-blank free-text classification. No rating-system vocabulary is imposed. |
| `type_metadata` | Required | Object | — | Type-selected metadata object defined in section 4.3. |
| `execution_methods` | Required | Object | — | Non-empty mapping of available execution methods defined in section 4.4. |

Required fields must be present and valid. Optional fields are omitted rather
than stored as null, blank, or empty placeholders.

### 4.2 `<item_id>.artwork`

```yaml
artwork:
  local: /local/mediacat/example-station.png                 # optional
  external: https://images.example.test/example-station.png  # optional
```

`artwork` contains only `local` and `external`. Each child is optional, but at
least one must be present when `artwork` exists.

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `local` | Optional | String | — | Non-blank `/local/...` Home Assistant reference. |
| `external` | Optional | String | — | Absolute HTTP(S) URL with a non-empty host. |

A local-only object is valid:

```yaml
artwork:
  local: /local/mediacat/example-station.png  # optional
```

An external-only object is also valid:

```yaml
artwork:
  external: https://images.example.test/example-station.png  # optional
```

Missing artwork is valid. MediaCat does not synthesize a placeholder or copy
one artwork field into the other. Stored order does not express preference.
Known consumers retain their governed behavior: the Media Source projection
uses `local`, while the current Google Cast mapping prefers `external` and then
uses `local`. Those consumer behaviors do not make artwork required here.

### 4.3 `<item_id>.type_metadata`

`type_metadata` contains exactly the fields defined by the selected item
`type`. Each supported type has a required semantic title or name, which is
never derived from `catalogue_label`. Optional fields are omitted when unknown
or inapplicable; no unlisted field may be added.

#### 4.3.1 `radio`

```yaml
type_metadata:
  station_name: Example Station
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `station_name` | Required | String | — | Non-blank player-facing station name. |

The temporary current `news_briefing` classification remains `type: radio` with
`station_name: My News Briefing` until `ASTV-66` authorizes a replacement type.
This compatibility record does not broaden the media-type vocabulary.

#### 4.3.2 `music_track`

```yaml
type_metadata:
  track_title: Example Track
  artist: Example Artist              # optional
  album_artist: Example Album Artist  # optional
  album_title: Example Album          # optional
  composer: Example Composer          # optional
  disc_number: 1                      # optional
  track_number: 2                     # optional
  release_date: "2026-09-18"          # optional
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `track_title` | Required | String | — | Non-blank player-facing track title. |
| `artist` | Optional | String | — | Non-blank performing artist. |
| `album_artist` | Optional | String | — | Non-blank album-level artist. |
| `album_title` | Optional | String | — | Non-blank album title. |
| `composer` | Optional | String | — | Non-blank composer name. |
| `disc_number` | Optional | Integer | — | Disc sequence number greater than zero. |
| `track_number` | Optional | Integer | — | Track sequence number greater than zero. |
| `release_date` | Optional | String | — | Quoted valid calendar date in `YYYY-MM-DD` form. |

#### 4.3.3 `podcast_episode`

```yaml
type_metadata:
  episode_title: Example Episode
  podcast_title: Example Podcast  # optional
  creator: Example Creator        # optional
  publisher: Example Publisher    # optional
  publication_date: "2026-09-18"  # optional
  episode_number: 3               # optional
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `episode_title` | Required | String | — | Non-blank player-facing episode title. |
| `podcast_title` | Optional | String | — | Non-blank podcast or show title. |
| `creator` | Optional | String | — | Non-blank episode or podcast creator. |
| `publisher` | Optional | String | — | Non-blank publisher name. |
| `publication_date` | Optional | String | — | Quoted valid calendar date in `YYYY-MM-DD` form. |
| `episode_number` | Optional | Integer | — | Episode sequence number greater than zero. |

#### 4.3.4 `live_tv`

```yaml
type_metadata:
  channel_name: Example Channel
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `channel_name` | Required | String | — | Non-blank player-facing channel name. |

#### 4.3.5 `tv_episode`

```yaml
type_metadata:
  episode_title: Example Episode
  series_title: Example Series        # optional
  season_number: 1                    # optional
  episode_number: 4                   # optional
  first_broadcast_date: "2026-09-18"  # optional
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `episode_title` | Required | String | — | Non-blank player-facing episode title. |
| `series_title` | Optional | String | — | Non-blank series title. |
| `season_number` | Optional | Integer | — | Season sequence number greater than zero. |
| `episode_number` | Optional | Integer | — | Episode sequence number greater than zero. |
| `first_broadcast_date` | Optional | String | — | Quoted valid calendar date in `YYYY-MM-DD` form. |

#### 4.3.6 `movie`

```yaml
type_metadata:
  movie_title: Example Movie
  secondary_title: An Example Subtitle  # optional
  studio: Example Studio                # optional
  release_date: "2026-09-18"            # optional
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `movie_title` | Required | String | — | Non-blank player-facing movie title. |
| `secondary_title` | Optional | String | — | Non-blank secondary title or subtitle. |
| `studio` | Optional | String | — | Non-blank studio name. |
| `release_date` | Optional | String | — | Quoted valid calendar date in `YYYY-MM-DD` form. |

#### 4.3.7 `photo`

```yaml
type_metadata:
  image_title: Example Photograph
  creator: Example Photographer              # optional
  creation_datetime: "2026-09-18T12:00:00Z"  # optional
  location: London                           # optional
  latitude: 51.5072                          # optional; pair with longitude
  longitude: -0.1276                         # optional; pair with latitude
  width_pixels: 1920                         # optional; pair with height_pixels
  height_pixels: 1080                        # optional; pair with width_pixels
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `image_title` | Required | String | — | Non-blank player-facing image title. |
| `creator` | Optional | String | — | Non-blank image creator or photographer. |
| `creation_datetime` | Optional | String | — | Quoted RFC 3339 datetime with an explicit `Z` or numeric UTC offset. |
| `location` | Optional | String | — | Non-blank human-readable location. |
| `latitude` | Optional | Number | — | Finite value from `-90` to `90`; present if and only if `longitude` is present. |
| `longitude` | Optional | Number | — | Finite value from `-180` to `180`; present if and only if `latitude` is present. |
| `width_pixels` | Optional | Integer | — | Pixel width greater than zero; present if and only if `height_pixels` is present. |
| `height_pixels` | Optional | Integer | — | Pixel height greater than zero; present if and only if `width_pixels` is present. |

### 4.4 `<item_id>.execution_methods`

```yaml
execution_methods:
  ha_mplayer:
    source: {...}
  g_home_device:
    source: {...}
```

`execution_methods` is a required, non-empty mapping. Each key is a current
contracted ASTV execution-method name. Each
`execution_methods.<method>` value contains exactly one required field,
`source`. It may not contain configuration, priority, fallback, endpoint, or
other fields.

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `source` | Required | Object | — | Method-specific source object selected by `source_type` and defined in section 4.4.1. |

| Execution method | Permitted `source_type` |
| --- | --- |
| `ha_mplayer` | `url`, `ha_media_source` |
| `g_home_device` | `assistant_command` |

An item may expose either current method or both when it has a valid source for
each. Mapping order does not define priority or fallback. ASTV owns method
preference and selection; MediaCat returns all authored methods. Adding another
method name or changing a method/source pairing requires separately approved
cross-product design and compatibility assessment.

#### 4.4.1 `source` Variants

```yaml
source:
  source_type: url
  url: https://streams.example.test/live.aac
  mime_type: audio/aac
  provider: example_streams  # optional
```

Every `execution_methods.<method>.source` is a mapping selected by required
`source_type`. It contains only the fields in the applicable row.

| `source_type` | Required fields | Optional fields |
| --- | --- | --- |
| `url` | `source_type`, `url`, `mime_type` | `provider` |
| `ha_media_source` | `source_type`, `provider`, `uri`, `media_type` | None |
| `assistant_command` | `source_type`, `provider`, `command`, `append_target` | None |

The source type must be permitted for its parent method by section 4.4.

##### 4.4.1.1 `url`

```yaml
source:
  source_type: url
  url: https://streams.example.test/live.aac
  mime_type: audio/aac
  provider: example_streams  # optional
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `source_type` | Required | String | `url` | Selects the direct-URL source shape. |
| `url` | Required | String | — | Absolute HTTP(S) URL with a non-empty host. |
| `mime_type` | Required | String | — | Non-blank `type/subtype` value. |
| `provider` | Optional | String | — | Provider identifier. |

MediaCat does not connect to the URL, test stream availability, infer a MIME
type, or retry another source during catalogue loading or lookup.

##### 4.4.1.2 `ha_media_source`

```yaml
source:
  source_type: ha_media_source
  provider: radio_browser
  uri: media-source://radio_browser/example-station
  media_type: station
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `source_type` | Required | String | `ha_media_source` | Selects the Home Assistant Media Source shape. |
| `provider` | Required | String | — | Provider identifier. |
| `uri` | Required | String | — | Absolute `media-source://` URI with non-empty authority and resource path; authority equals `provider`. |
| `media_type` | Required | String | — | Non-blank Home Assistant media-content-type value. |

The URI remains opaque after these structural checks. MediaCat does not
dereference it during catalogue loading or normalized lookup. Runtime provider
failure remains at the Home Assistant Media Source execution boundary.

##### 4.4.1.3 `assistant_command`

```yaml
source:
  source_type: assistant_command
  provider: google_assistant
  command: Play Example Station
  append_target: true
```

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `source_type` | Required | String | `assistant_command` | Selects the assistant-command source shape. |
| `provider` | Required | String | — | Provider identifier. |
| `command` | Required | String | — | Non-blank item-specific command. |
| `append_target` | Required | Boolean | `true`, `false` | Whether ASTV appends its selected target to the authored command. |

MediaCat does not append an endpoint, construct a final assistant command, or
execute it. Those remain ASTV responsibilities.

## 5. `categories` Collection

```yaml
categories:
  <category_id>: {...}
```

`categories` is a required ordered mapping and may be empty. Each mapping key
is a category ID satisfying the identifier rule in section 6.2. Duplicate
category keys are invalid. Root mapping order defines category browse order.
Each mapping value is a category object.

### 5.1 `<category_id>`

```yaml
<category_id>:
  category_label: Featured
  items: [...]
```

Each category object contains exactly:

| Field | Presence | Data type | Options | Definition |
| --- | --- | --- | --- | --- |
| `category_label` | Required | String | — | Non-blank catalogue and Media Browser label. |
| `items` | Required | List of strings | — | Non-empty ordered list of unique item IDs; every reference must exist in root `items`. |

The category item list is authored within the category object. For example:

```yaml
<category_id>:
  items:
    - example_station
    - another_station
```

The category model is flat. Categories have no parent, child, priority, or
separate order field. The `items` list defines membership display order. An
item may appear in multiple categories or in none. Absence from all categories
does not prevent catalogue-scoped lookup. Category membership also does not
guarantee Media Source visibility: that projection applies its separately
documented playable-item rules.

## 6. Cross-Cutting Authoring and Validation Rules

### 6.1 Closed Vocabulary

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

### 6.2 Identifiers and Mapping Keys

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

### 6.3 Missing, Empty, and Null Values

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

### 6.4 Common Value Formats

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

### 6.5 Defaults and Fallback

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

## 7. Validation Ownership and Failure Behavior

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

## 8. Relationship to Returned Record Version 1

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

## 9. Representative Invalid Examples

Each fragment is invalid at catalogue-load time.

### 9.1 Unknown Field

```yaml
items:
  example_station:
    catalogue_lable: Example Station
```

`catalogue_lable` is not a defined field. The loader must report the unknown
field; it must not treat it as an additive extension or silently lose the label.

### 9.2 Explicit Null and Empty Optional Collection

```yaml
items:
  <item_id>:
    description: null  # optional field, but explicit null is invalid
    tags: []           # optional field, but an empty list is invalid
```

Optional unknown values are omitted. Explicit null and an empty optional list
are both invalid.

### 9.3 Missing Semantic Title

```yaml
items:
  <item_id>:
    catalogue_label: Example Movie
    type: movie
    type_metadata: {}
```

`movie_title` is required. `catalogue_label` is not a fallback.

### 9.4 Invalid Method/Source Pairing

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

### 9.5 Invalid Media Source Identity

```yaml
source:
  source_type: ha_media_source
  provider: radio_browser
  uri: media-source://another_provider/example-station
  media_type: station
```

The URI authority does not match `provider`.

### 9.6 Unpaired Coordinates

```yaml
items:
  <item_id>:
    type: photo
    type_metadata:
      image_title: Example Photograph
      latitude: 51.5072  # optional; invalid without longitude
```

`longitude` is required whenever `latitude` is present.

### 9.7 Invalid Category Membership

```yaml
categories:
  featured:
    category_label: Featured
    items:
      - missing_item
      - missing_item
```

The reference is unknown and duplicated. Both violate the category rules.

## 10. Assembled Catalogue Examples

### 10.1 Minimal Valid Catalogue

```yaml
catalogue_id: curated_media
catalogue_schema_version: 3
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
categories: {}
```

### 10.2 Complete Worked Catalogue

This assembled example covers ordered category membership, optional item data,
all three source types, and an item with multiple execution methods.

```yaml
catalogue_id: curated_media
catalogue_schema_version: 3
items:
  station_alpha:
    catalogue_label: Station Alpha — London
    type: radio
    description: Independent live radio  # optional
    tags:                                 # optional
      - radio
      - london
    artwork:                              # optional
      local: /local/mediacat/station-alpha.png                 # optional
      external: https://images.example.test/station-alpha.png  # optional
    content_rating: general              # optional
    type_metadata:
      station_name: Station Alpha
    execution_methods:
      ha_mplayer:
        source:
          source_type: url
          url: https://streams.example.test/station-alpha.m3u8
          mime_type: application/vnd.apple.mpegurl
          provider: example_streams  # optional
      g_home_device:
        source:
          source_type: assistant_command
          provider: google_assistant
          command: Play Station Alpha
          append_target: true
  station_beta:
    catalogue_label: Station Beta
    type: radio
    artwork:  # optional
      local: /local/mediacat/station-beta.png  # optional
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

## 11. Compatibility and Schema Evolution

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

## 12. Required Follow-Up Implementation

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
