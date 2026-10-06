# MediaCat HACS Deployment Runbook

## Scope and authority

This runbook applies the governed route:

`haos_integration -> hacs -> HOME_ASSISTANT_INTEGRATION_DEPLOYMENT_STANDARD.md`

The authoritative integration source is `custom_components/mediacat/**` and its
stable version is the `version` in `manifest.json`. This runbook does not
authorise Beta deployment, stable promotion, production deployment, or rollback.
Once explicit stable-promotion authority exists, stable tag and GitHub Release
creation follow automatically as part of the approved HACS mechanism.

## Beta preparation and handoff

After the accepted issue PR is integrated into persistent `beta`, record its
full candidate SHA and derive the immutable lightweight tag
`vX.Y.Z-beta.<short-sha>` from the manifest version. Confirm the tag is unused,
create it at the exact candidate SHA, verify the tagged tree contains valid
root `hacs.json`, push it without creating a GitHub prerelease, and independently
verify the remote tag resolves to the recorded SHA. Tag creation and push require
the applicable Beta/deployment authority.

The operator handoff records the immutable Beta tag, full SHA, tag-to-SHA and
HACS metadata validation, prior installed version, target `starburst` instance,
and the instance-specific HACS update entity. The supported action is:

```yaml
action: update.install
target:
  entity_id: update.mediacat_update
data:
  version: "<immutable-beta-tag>"
```

Verify the actual update entity on `starburst`; do not infer it from this
example. Target the immutable tag, never `main`, `beta`, or a raw SHA. After the
update, perform the required restart or reload, confirm the expected tag is
installed, confirm MediaCat loads without errors, and perform a basic catalogue
lookup or Media Source browse check.

## Stable release

After successful Beta, unchanged promotion to `main`, required equivalence
evidence, and explicit stable-promotion authority, dispatch
`.github/workflows/hacs-release.yml` with the selected stable SHA, accepted Beta
tag, and the promotion-equivalence evidence reference when the integrated SHA
differs. The workflow invokes the authoritative machinery at
`04_Implementation/haos/packaging/hacs/hacs_release.py`. It validates repository
metadata and identity, fails on contradictory tags or missing evidence, and
creates the immutable `vX.Y.Z` tag and GitHub Release. It does not deploy to
Home Assistant or provide stable-promotion authority.

## Failure and rollback

On install, identity, load, restart, or functional-check failure, stop
progression and preserve non-secret diagnostics. Restore the exact version that
was installed immediately before the attempt using HACS and applicable rollback
authority, then repeat restart/load and functional checks. Moving branches are
not rollback identities.

Record the target instance, prior version, requested tag/version, exact Git SHA,
update entity, install result, restart/reload result, load result, functional
check, promotion equivalence, stable release identity, and any rollback result
in the governing issue or linked authoritative evidence.
