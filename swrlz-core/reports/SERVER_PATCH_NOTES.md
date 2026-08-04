# SWRLZ Server Patch Notes

This repository-level log records server, routing, build, deployment, and continuity changes that affect SWRLZ server candidates or their delivery pipeline.

## 2026-08-04 — APK Router checkout-timeout repair

**Status:** Implemented on branch; workflow validation pending  
**Branch:** `fix/apk-router-checkout-timeout-20260804`  
**Workflow:** `.github/workflows/swrlz-apk-router.yml`  
**Incident run:** `30919011515`

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

### Truth boundary

This patch addresses the confirmed checkout cancellation. It does not yet prove that the selected Android source compiles or that an APK artifact uploads successfully. Those outcomes require a workflow run using the patched branch or the merged workflow.

### Rollback

Revert the workflow commit associated with this patch. No source candidate, APK, model, key, or release artifact is modified by the CI checkout repair itself.
