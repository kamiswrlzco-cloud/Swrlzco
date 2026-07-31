# INT-CI-061A — Router, Source Integrity, Documentation and Patch-Note Synchronization

**Date:** 2026-07-31  
**Repository:** `kamiswrlzco-cloud/Swrlzco`  
**Branch:** `main`  
**Scope:** GitHub CI routing + documentation/patch-note accounting.  
**Does not authorize or claim:** workflow dispatch, APK build success, candidate promotion, release, deployment, or installation.

## Triggering evidence

GitHub Actions run evidence for commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` showed `SWRLZ Source Package Integrity` failing with:

`Missing ZIP: swrlz-core/sources/client/.transport/CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1/evidence/CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1.zip`

The source-integrity workflow converted a **nested chunk-transport evidence sidecar** into an invented sibling ZIP path. That nested evidence file belongs to the lane-root `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1.transport.json` identity.

A separate APK Router screenshot showed `Validate source resolver` waiting for a GitHub-hosted `ubuntu-latest` runner to come online. That state is runner provisioning/queue evidence, not proof of a resolver-code failure.

## CI corrections

### Source Package Integrity

`.github/workflows/source-package-integrity.yml` now:

- watches the source tree but maps changed paths to **canonical lane-root source identities**;
- maps `.transport/<bundle>/...` chunks/evidence to `<bundle>.transport.json`;
- never fabricates a nested evidence ZIP;
- resolves direct or chunked sources through the canonical source resolver;
- reconstructs/validates chunk transports before package-pair verification;
- deduplicates multiple changed members belonging to one transport;
- fails closed when a changed transport member has no lane-root transport identity.

Shared mapping logic lives in `swrlz-core/tools/ci/resolve_changed_source_identities.py` with regression coverage in `test_resolve_changed_source_identities.py`.

### APK Router

`.github/workflows/swrlz-apk-router.yml` now:

- runs both resolver regression suites;
- supports manual `CLIENT`, `SERVER`, or `BOTH` routing;
- allows explicit lane-root `.zip` or `.transport.json` identity for single-component manual dispatch;
- rejects one explicit source identity for a `BOTH` dispatch;
- rejects concurrent release-commit mode for `BOTH` while leaving ordinary build artifacts available;
- treats lane-root checksum/manifest sidecars as source-lane build signals;
- restricts push route classification to lane-root source/evidence signals instead of any arbitrary nested path;
- preserves existing request-file routing, build, signing, provenance, artifact and optional release-commit behavior.

No workflow was manually dispatched by this checkpoint.

## Current candidate accounting

Current repository transport from Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`:

- CLIENT CFv2.1.27 R1 / VC125 / SHA `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` / INT-AI-060A;
- SERVER CFv2.1.25 R1 / VC83 / SHA `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` / INT-AI-060A, transported under the repository filename `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1.transport.json`.

INT-FILE-059A previously packaged different source bytes using the same external component version/revision values:

- CLIENT CFv2.1.27 R1 / SHA `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`;
- SERVER CFv2.1.25 R1 / SHA `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`.

This is documented as an external identity collision. No source is silently overwritten or promoted. The next source candidate must advance version and/or revision.

## Documentation synchronization

Added/updated current-lineage surfaces:

- `docs/CURRENT_AUTHORITY.md` — promoted authority unchanged; current candidate pointer added;
- `docs/reference/CURRENT_CANDIDATE_LINEAGE.md` — current transport + 059A/060A collision accounting;
- `docs/patch-notes/CLIENT_PATCH_NOTES.md` — current CLIENT candidate timeline;
- `docs/patch-notes/SERVER_PATCH_NOTES.md` — current SERVER candidate timeline;
- `docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory per-update patch-note/lineage contract.

## Patch-note rule now locked

Every future CLIENT/SERVER source candidate must update, in the same bounded checkpoint, all patch-history surfaces present in the package: `ReleaseNotes.md`, `CHANGELOG.md`, `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, repository component patch notes, and current candidate accounting when transport changes.

Patch notes remain index/navigation evidence. Source ZIPs, exact checksums, manifests, accepted contracts and checkpoint evidence remain higher authority.

## Truth / evidence boundary

- CI source routing fixes are repository changes only until a later workflow run proves runtime CI behavior.
- GitHub hosted-runner availability is external infrastructure state and is not claimed fixed by YAML changes.
- No APK was built by this checkpoint.
- No source candidate was promoted.
- No release, deployment, or installation occurred.
