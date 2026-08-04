# SWRLZ Server Patch Notes

This repository-level log records server, routing, build, deployment, and continuity changes that affect SWRLZ server candidates or their delivery pipeline.

## 2026-08-04 — APK Router checkout-timeout repair

**Status:** Implemented on branch; merge-triggered SERVER R7 validation queued  
**Branch:** `fix/apk-router-checkout-timeout-20260804`  
**Workflow:** `.github/workflows/swrlz-apk-router.yml`  
**Incident run:** `30919011515`  
**Validation request:** `INT-CI-065-SERVER-R7-CHECKOUT-REPAIR`

### Root cause

The `Validate source resolver` job had a five-minute job timeout. Its default `actions/checkout@v4` fetch attempted to retrieve the current repository snapshot and was canceled before checkout completed. Resolver tests, route preparation, Android build, signing, provenance generation, and artifact upload therefore never ran.

The repository is approximately 1.6 GB, so a shallow history depth alone does not prevent the current snapshot's large blobs from dominating checkout time.

### Changes

- Increased the resolver-test and route-preparation job timeouts from 5 to 20 minutes.
- Replaced broad checkout operations with authenticated Git partial clones using `--filter=blob:none` and cone-mode sparse checkout.
- Limited resolver tests to `swrlz-core/tools/ci`.
- Limited route preparation to `swrlz-core/tools/ci` and `swrlz-core/requests` while retaining two commits for changed-path resolution.
- Limited each Android build matrix lane to its selected CLIENT or SERVER source directory plus CI tools, requests, and release records.
- Removed the build job's full-history `fetch-depth: 0` behavior.
- Preserved existing source resolution, checksum verification, Gradle build, optional signing, provenance, artifact upload, and release-commit behavior.
- Refreshed the existing enabled SERVER R7 request ID so merging the repair PR triggers validation through the patched workflow without modifying the source candidate.

### Validation plan

Merging PR #4 changes `swrlz-core/requests/000_CURRENT.request`, which is already an APK Router push trigger. The resulting run must complete:

1. Resolver unit tests.
2. SERVER route resolution.
3. Source and checksum verification for `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R7.transport.json`.
4. Gradle debug APK production.
5. Provenance recording and artifact upload.

### Truth boundary

This patch addresses the confirmed checkout cancellation. It does not yet prove that the selected Android source compiles or that an APK artifact uploads successfully. Validation remains pending until the merge-triggered workflow run completes.

### Rollback

Revert the workflow and validation-request commits associated with this patch. No Android source candidate, APK, model, credential, or release artifact is modified by the CI checkout repair itself.
