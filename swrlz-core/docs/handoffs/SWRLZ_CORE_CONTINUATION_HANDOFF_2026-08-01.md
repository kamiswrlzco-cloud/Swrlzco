# SWRLZ-Core Continuation Handoff — 2026-08-01

Status: **Current-thread migration handoff**  
Repository: `kamiswrlzco-cloud/Swrlzco`  
Operating rule: **integrate; do not overwrite**

## Start here in the next chat

Use this handoff together with the three companion documents in the migration pack:

1. `SWRLZ_INTEGRITY_WORKFLOW_COMPATIBILITY_ISSUE_AND_FIX_2026-08-01.docx`
2. `SWRLZ_CORE_THREE_DEEP_ANALYSES_AND_PHASE_INTEGRATION_HISTORY_2026-08-01.docx`
3. `SWRLZ_UPDATE_RESPONSE_FORMAT_AND_APPROVAL_BOUNDARY_STANDARD_2026-08-01.docx`

Treat canonical source ZIPs, SHA-256 receipts, manifests, implementation files, accepted contracts, and GitHub evidence as authority. The repository is the long-term source of truth. Do not infer promotion or acceptance from source packaging alone.

## Non-negotiable project behavior

- Work one bounded checkpoint at a time.
- Separate facts, requirements, assumptions, recommendations, and evidence.
- Do not modify source, build, trigger workflows, install, promote, release, or deploy without explicit authorization.
- Preserve offline-first behavior, identity, trust, Truth Firewall, lineage, local-versus-remote distinctions, and protocol-version discipline.
- Shared capabilities that both CLIENT and SERVER support are synchronized dual updates unless a correction intentionally retains one component byte-exact.
- Before every stop, state the waiting approval, what it authorizes, what it does not authorize, the expected result, and the exact approval phrase.

## Authority and identity matrix

### Historical accepted anchors

| Component | Accepted anchor | versionCode | SHA-256 | Status |
|---|---|---:|---|---|
| CLIENT | CFv2.1.26 R1 | 124 | `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` | Accepted lineage anchor |
| SERVER | CFv2.1.24 R1 | 82 | `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` | Accepted lineage anchor |

### Current delivered source candidates

| Component | Candidate | versionCode | Source SHA-256 | Metadata SHA-256 | Build/acceptance status |
|---|---|---:|---|---|---|
| CLIENT | CFv2.1.26 R6 | 129 | `09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136` | `39021fb0efc77de30369417655326f695d276029873a78c3d3d3326982733eb6` | Source/static delivery; Android compile not yet established |
| SERVER | CFv2.1.26 R9 | 92 | `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f` | `a43e469ff292009deea70cf1f77b9134136b88bd5e77b7c679f8d9af4542f94f` | Source/static delivery; Android compile not yet established |

### Relevant repository upload commits

- CLIENT R6 source + metadata: `cfcdd4c306c5c0051309307cc5b867bb638a8a7e`
- SERVER R9 verified upload: `380c2e5fd898e377972670b5ed797c34dc63e782`

## Completed checkpoint sequence

### INT-FORGE-064A — metadata-bundle contract and resolver bootstrap

Established canonical source + metadata + evidence packaging, strict metadata ZIP verification, chunked transport schema 2, direct and chunked resolver parity, and temporary complete legacy sidecar compatibility.

### INT-FIX-064A-CLIENT-R3

Corrected CLIENT Forge imports. CLIENT R3 source SHA-256: `fd6a65ba7043be4870d222835b9c61b95dbf493b42b03253db813b36ac4cbda8`.

### INT-FORGE-064B-CLIENT-R4

Added project-root discovery, automatic CLIENT/SERVER/BOTH classification, one-action verify/stage/upload, conflict blocking, durable transaction reconciliation, and workflow-success precedence. CLIENT R4 was user-reported as building successfully; device acceptance was not promoted.

### INT-FORGE-064C-DUAL-SYNC

Ported the shared Forge automation to SERVER while retaining CLIENT R4 byte-exact. Codified the shared-capability dual-update rule.

### INT-FORGE-064D-DUAL-DOWNLOADS-PIPELINE

Separated the Downloads inbox from the Project root, added metadata ZIP recognition without extraction, bounded legacy extractor-folder recovery, exact source/build descriptions, durable build identity, safe artifact unpacking, and actual APK placement under `Download/<projectName>/apk/`.

### INT-CI-064E — resolver bootstrap shield and SERVER R7

Applied repository resolver support for schema-2 transport and metadata bundles, quarantined unsupported historical transports, and retained fail-closed behavior for current or explicit unsupported transports. SERVER R7 workflow reached the Android compiler.

### INT-FIX-064F — SERVER R8 namespace repair

Corrected two package declarations from `sh.swurlz.nodehost.forge` to `sh.swrlz.nodehost.forge` in `ForgeAutomatedBuildRunner.kt` and `ForgeBuildMonitor.kt`. Added package-path regression verification.

### INT-FORGE-064G — synchronized storage/performance repair

Delivered CLIENT R6 and SERVER R9 with:

- public Downloads as the default inbox after explicit Android authorization;
- optional custom SAF inbox override;
- nonblocking project-root setup;
- single-flight scanning;
- one-pass Downloads classification;
- unchanged-file scan hash caching;
- full uncached pre-upload revalidation;
- preserved metadata-bundle and legacy-sidecar compatibility.

## Current open blocker — INT-CI-064H

Workflow `30716759640` failed in Source Package Integrity before package verification.

### Confirmed causes

1. The workflow imports `resolve_source`, but the current resolver exposes `resolve`.
2. The changed-source mapper emits `_METADATA.zip` as a second source identity.

### Important interpretation

- CLIENT R6 was uploaded successfully.
- The failure is CI compatibility, not demonstrated source corruption.
- No new CLIENT or SERVER candidate is needed.
- The repair must be CI-only and should not churn source identities.

### Exact next approval phrase

```text
APPROVE INT-CI-064H-INTEGRITY-COMPAT — RESTORE THE RESOLVE_SOURCE COMPATIBILITY API IN THE GITHUB SOURCE RESOLVER, UPDATE CHANGED-SOURCE IDENTITY MAPPING SO METADATA ZIPS MAP TO THEIR EXACT DIRECT OR CHUNKED SOURCE IDENTITY INSTEAD OF BECOMING INDEPENDENT SOURCES, ADD DEDUPLICATION, ORPHAN/AMBIGUITY FAIL-CLOSED BEHAVIOR, AND FOCUSED REGRESSION TESTS, APPLY THE CI-ONLY REPAIR TO GITHUB, AND ALLOW THE AUTOMATIC SOURCE PACKAGE INTEGRITY WORKFLOW TRIGGERED BY THOSE CHANGES; NO CLIENT OR SERVER SOURCE CHANGE, NEW CANDIDATE, ANDROID BUILD, APK INSTALL, DEVICE ACCEPTANCE, PROMOTION, RELEASE, OR DEPLOYMENT.
```

## Recommended first action in the next thread

1. Read the current repository versions of:
   - `swrlz-core/tools/ci/resolve_swrlz_source.py`
   - `swrlz-core/tools/ci/resolve_changed_source_identities.py`
   - their focused tests;
   - the Source Package Integrity workflow.
2. Confirm the failed workflow evidence still matches run `30716759640`.
3. Do not modify CLIENT R6 or SERVER R9.
4. Wait for or recognize the exact `INT-CI-064H-INTEGRITY-COMPAT` approval.
5. Apply the CI-only compatibility repair and allow only the automatic integrity workflow caused by those authorized changes.
6. Inspect that workflow before considering Android build or promotion steps.

## Packaging expectations

- Dual component source update: five packs.
- Single component source update: source, metadata, evidence.
- CI-only or documentation-only work: no artificial source candidate revision.
- Downloads and hashes appear first in delivery responses.

## Evidence boundaries

Known facts:

- CLIENT R6 and SERVER R9 source packages were created and statically verified.
- CLIENT R6 source and metadata were committed to GitHub.
- SERVER R9 was committed to GitHub.
- The Source Package Integrity workflow failed on resolver API compatibility before package verification.

Not established:

- Android compile success for CLIENT R6.
- Android compile success for SERVER R9.
- Installation or device acceptance for either current candidate.
- Promotion, release, or deployment.

## Thread migration instruction

The new thread should continue from this handoff, not reconstruct architecture from memory. Integrate newer repository evidence when it is stronger, but do not silently erase historical failures, candidate lineage, or pending boundaries.
