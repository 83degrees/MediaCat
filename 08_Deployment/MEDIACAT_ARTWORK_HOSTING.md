# MediaCat public artwork hosting

## Purpose

This document defines the operational procedure for publishing MediaCat artwork
that must be reachable by Internet-based consumers such as Google Cast.

The durable hosting decision is recorded in
`02_Decisions/DDR-03-003.md`. The authoritative catalogue vocabulary remains
in `01_Architecture/MEDIACAT_CATALOGUE_SCHEMA_ARCHITECTURE.md`.

## Hosting model

Public artwork is stored in a Cloudflare R2 Standard bucket.

For production use, expose the bucket through a custom HTTPS domain owned by the
operator. Cloudflare's `r2.dev` endpoint is limited to setup and verification.

Home Assistant is not made public solely to serve artwork.

## Object-key convention

Use stable lowercase paths grouped by media type:

```text
radio/<item-id>.png
tv/<item-id>.png
movie/<item-id>.png
podcast/<item-id>.png
music/<item-id>.png
photo/<item-id>.png
```

Examples:

```text
radio/classic-fm.png
tv/bbc-iplayer.png
```

Prefer PNG for catalogue logos/artwork unless the source and consuming clients
are known to support another format reliably.

## Initial R2 setup

1. Create an R2 Standard bucket dedicated to MediaCat artwork.
2. Enable public access for setup/testing.
3. Upload one representative image using the governed object-key convention.
4. Confirm the object is retrievable over unauthenticated HTTPS.
5. For production use, connect a custom domain to the bucket and use that
   hostname for catalogue URLs.
6. Do not expose `ha-shorefoot` or another Home Assistant instance to provide
   the public image URL.

## Adding artwork

1. Choose the MediaCat `item_id`.
2. Create an object key under the appropriate media-type folder.
3. Upload the image to R2.
4. Verify the public URL in an unauthenticated browser/session.
5. Add or update the catalogue item's `artwork.external` with the complete
   HTTPS URL.
6. Retain `artwork.local` if Home Assistant-local presentation still benefits
   from the local copy.
7. Run the normal MediaCat catalogue validation and governed change workflow.

Example:

```yaml
artwork:
  local: /local/radio-logos/Classic-FM.png
  external: https://<public-artwork-host>/radio/classic-fm.png
```

## Replacing artwork

Where the logical artwork identity is unchanged, replace the R2 object at the
existing key so the catalogue URL remains stable.

Use a new object key only when the logical asset identity changes or when a
deliberately versioned URL is required. If a new key is used, update
`artwork.external` through the normal governed catalogue change.

## Verification

For a new or replaced public asset:

1. Fetch the HTTPS URL without authentication.
2. Confirm the response is an image and not an HTML error/redirect page.
3. Resolve the MediaCat record and confirm `artwork.external` contains the
   expected URL.
4. From the Shorefoot environment, start representative Google Cast playback.
5. Confirm the Cast display retrieves and renders the artwork.
6. Record the successful runtime verification against the governing Linear
   issue before completion.
