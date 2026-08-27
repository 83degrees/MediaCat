# ASTV-56 per-item migration matrix

## Scope and interpretation

This matrix records the one-off, non-live migration into target catalogue
`curated_media`. It is evidence for `ASTV-56`, not a reusable conversion rule.
The target item identity is always the combination of `catalogue_id:
curated_media` and the item ID shown below. ASTV intent keys remain separate
ASTV identities even when their text matches a MediaCat item ID.

For each schema-v2 row, `title` is carried to both `catalogue_label` and
`type_metadata.station_name`; `type`, `description`, ordered `tags`, and both
artwork references are carried unchanged unless an exception is stated. The
direct URL and MIME value move into the `ha_mplayer` source. Legacy top-level
`providers`, `source.type`, and `source.format` are omitted.

| Position | Source system and record | Target item | Metadata disposition | Execution method / source type | Explicit exception or decision |
| ---: | --- | --- | --- | --- | --- |
| 1 | Curated Media schema v2 / `bbc_radio_1` | `curated_media` / `bbc_radio_1` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 2 | Curated Media schema v2 / `bbc_radio_1xtra` | `curated_media` / `bbc_radio_1xtra` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 3 | Curated Media schema v2 / `bbc_radio_2`; ASTV / `bbc_radio_2` is a reference-only record | `curated_media` / `bbc_radio_2` | Existing identity and metadata carried; no duplicate appended | `ha_mplayer` / `url` | The matching ASTV key does not create another MediaCat item or an alias |
| 4 | Curated Media schema v2 / `bbc_radio_3` | `curated_media` / `bbc_radio_3` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 5 | Curated Media schema v2 / `bbc_radio_4`; correction decision `ASTV-28` | `curated_media` / `bbc_radio_4` | Existing metadata carried; local artwork retained; external artwork corrected | `ha_mplayer` / `url` | External artwork is `https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/BBC_Radio_4_2022.svg/960px-BBC_Radio_4_2022.svg.png` |
| 6 | Curated Media schema v2 / `bbc_radio_4_extra` | `curated_media` / `bbc_radio_4_extra` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 7 | Curated Media schema v2 / `bbc_radio_5_live` | `curated_media` / `bbc_radio_5_live` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 8 | Curated Media schema v2 / `bbc_radio_5_sports_extra` | `curated_media` / `bbc_radio_5_sports_extra` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 9 | Curated Media schema v2 / `bbc_radio_6_music` | `curated_media` / `bbc_radio_6_music` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 10 | Curated Media schema v2 / `bbc_world_service` | `curated_media` / `bbc_world_service` | Existing identity and metadata carried | `ha_mplayer` / `url` | None |
| 11 | Curated Media schema v2 / `bbc_radio_scotland` | `curated_media` / `bbc_radio_scotland` | Existing identity and metadata carried | `ha_mplayer` / `url` | Adds the approved one-off `mime_type: audio/aac`; this is not an inference rule |
| 12 | ASTV intent catalogue / `classic_fm` | `curated_media` / `classic_fm` | `data.title` becomes both labels; `data.icon_url` becomes `artwork.local`; no description or tags invented | `ha_mplayer` / `ha_media_source` | Opaque Radio Browser URI and `content_type` carried exactly; legacy ASTV envelope omitted |
| 13 | ASTV intent catalogue / `lbc_news` | `curated_media` / `lbc_news` | `data.title` becomes both labels; `data.icon_url` becomes `artwork.local`; no description or tags invented | `ha_mplayer` / `ha_media_source` | Opaque Radio Browser URI and `content_type` carried exactly; legacy ASTV envelope omitted |
| 14 | ASTV intent catalogue / `gold_radio` | `curated_media` / `gold_radio` | `data.title` becomes both labels; `data.icon_url` becomes `artwork.local`; no description or tags invented | `ha_mplayer` / `ha_media_source` | Opaque Radio Browser URI and `content_type` carried exactly; legacy ASTV envelope omitted |
| 15 | ASTV intent catalogue / `smooth_radio`; source-shape decision `ASTV-54` | `curated_media` / `smooth_radio` | Approved label and station name added; artwork, description, and tags remain absent | `g_home_device` / `assistant_command` | Provider becomes `google_assistant`; command is item-specific and `append_target` remains `true` |
| 16 | ASTV intent catalogue / `lbc_radio`; correction decisions `ASTV-34` and `ASTV-54` | `curated_media` / `lbc_radio` | Approved label and station name added; artwork, description, and tags remain absent | `g_home_device` / `assistant_command` | Command is `play LBC Radio on Global Player`; `Kitchen Speaker` is removed and `append_target` is `true` |
| 17 | ASTV intent catalogue / `news_briefing`; source-shape decision `ASTV-54` | `curated_media` / `news_briefing` | Approved temporary label and station name are `My News Briefing`; artwork, description, and tags remain absent | `g_home_device` / `assistant_command` | Provisional `radio` classification; `ASTV-66` owns later semantic refinement |

## Ordered membership result

The schema-v2 order occupies positions 1–11 unchanged. The six ASTV-derived
items occupy positions 12–17 in the exact order approved by `ASTV-56`. Every
target item occurs once in `categories.radio.items`; `bbc_radio_2` retains
position 3.

## Activation boundary and downstream handoff

The matrix describes the inactive repository artifact only. It does not alter
the schema-v2 catalogue or any ASTV intent record. `ASTV-57` still owns
schema-v3 Home Assistant Media Source support, `ASTV-64` still owns method-neutral
ASTV data preparation, and `ASTV-65` owns coordinated deployment, cutover, live
proof, and any rollback invocation.
