# INT-CI-064H — Source Package Integrity Compatibility Incident and Repair Plan

Date: 2026-08-01  
Repository: `kamiswrlzco-cloud/Swrlzco`  
Workflow run: `30716759640`  
Status: **OPEN — CI-only repair not yet applied**

## Executive summary

The Source Package Integrity workflow failed after Forge successfully uploaded the CLIENT R6 source ZIP and its metadata ZIP. The failure does **not** indicate source corruption, manifest corruption, or a CLIENT runtime defect. The workflow stopped before package verification because the repository resolver's public Python API and the changed-source identity mapper drifted out of compatibility with the integrity workflow.

Two defects must be corrected together:

1. The integrity workflow imports `resolve_source`, while the current resolver exposes `resolve`.
2. The changed-source mapper treats `<SOURCE_STEM>_METADATA.zip` as an independent Android source identity instead of mapping it to the matching source ZIP or transport manifest.

No new CLIENT or SERVER candidate is required for this repair.

## Evidence

Forge upload commit:

- Commit: `cfcdd4c306c5c0051309307cc5b867bb638a8a7e`
- Files committed:
  - `swrlz-core/sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R6.zip`
  - `swrlz-core/sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R6_METADATA.zip`

The workflow identity-resolution step emitted both files as separate identities, including the metadata ZIP. The verification step then failed with:

```text
ImportError: cannot import name 'resolve_source' from 'resolve_swrlz_source'
```

The failure occurred before source hashing, metadata-bundle verification, manifest verification, or Android compilation.

## Root cause 1 — resolver API compatibility regression

The current resolver's internal entry point is:

```python
resolve(...)
```

The integrity workflow still imports:

```python
from resolve_swrlz_source import resolve_source
```

The stable compatibility surface was removed when the resolver was replaced for schema-2 transport support. Existing workflow consumers were not migrated at the same time.

### Required repair

Restore a compatibility wrapper that delegates to the current implementation without changing resolver behavior:

```python
def resolve_source(repo_root, component, explicit_source=None, work_dir=None):
    return resolve(repo_root, component, explicit_source or "", work_dir)
```

The wrapper must remain covered by a regression test so future internal refactors do not break workflow callers.

## Root cause 2 — metadata ZIP misclassified as a source identity

The changed-source mapper currently handles every lane-root `.zip` as a source identity. Under the canonical package contract, `_METADATA.zip` is evidence for one source package and must never be built independently.

### Required mapping behavior

```text
CLIENT_<identity>_METADATA.zip
→ CLIENT_<identity>.zip
```

or, when the canonical identity is chunked:

```text
CLIENT_<identity>_METADATA.zip
→ CLIENT_<identity>.transport.json
```

The mapper must:

- recognize `_METADATA.zip` before generic `.zip` handling;
- resolve exactly one matching direct ZIP or transport manifest;
- deduplicate source and metadata changes into one identity;
- fail closed when both direct and transport identities exist;
- fail closed when neither identity exists;
- preserve legacy loose checksum/manifest mapping.

## Required regression coverage

1. `resolve_source` compatibility import and delegation.
2. Direct source ZIP plus metadata ZIP maps to one identity.
3. Metadata ZIP maps to a direct source ZIP.
4. Metadata ZIP maps to a chunked transport identity.
5. Direct and chunked ambiguity fails closed.
6. Orphan metadata ZIP fails closed.
7. CLIENT R6 source plus metadata verifies successfully.
8. Existing loose sidecar and nested transport mapping tests remain green.

## What the repair authorizes

The bounded repair is CI-only. It changes resolver compatibility, changed-source identity mapping, and their focused tests. It does not require reissuing CLIENT R6 or SERVER R9.

## What the repair does not authorize

- CLIENT or SERVER source changes.
- New candidate revisions.
- Android or APK builds beyond the workflow automatically triggered by the approved CI-only change.
- Installation, device acceptance, promotion, release, or deployment.

## Expected result

The integrity workflow imports the resolver successfully, maps CLIENT R6 and its metadata ZIP to one canonical source identity, verifies the source and metadata contract, and stops treating metadata bundles as independent Android source packages.

## Exact approval phrase

```text
APPROVE INT-CI-064H-INTEGRITY-COMPAT — RESTORE THE RESOLVE_SOURCE COMPATIBILITY API IN THE GITHUB SOURCE RESOLVER, UPDATE CHANGED-SOURCE IDENTITY MAPPING SO METADATA ZIPS MAP TO THEIR EXACT DIRECT OR CHUNKED SOURCE IDENTITY INSTEAD OF BECOMING INDEPENDENT SOURCES, ADD DEDUPLICATION, ORPHAN/AMBIGUITY FAIL-CLOSED BEHAVIOR, AND FOCUSED REGRESSION TESTS, APPLY THE CI-ONLY REPAIR TO GITHUB, AND ALLOW THE AUTOMATIC SOURCE PACKAGE INTEGRITY WORKFLOW TRIGGERED BY THOSE CHANGES; NO CLIENT OR SERVER SOURCE CHANGE, NEW CANDIDATE, ANDROID BUILD, APK INSTALL, DEVICE ACCEPTANCE, PROMOTION, RELEASE, OR DEPLOYMENT.
```

## Evidence basis

- `workflow_30716759640_SWRLZ_Source_Package_Integrity_logs.zip`
- Forge commit `cfcdd4c306c5c0051309307cc5b867bb638a8a7e`
- `swrlz-core/tools/ci/resolve_swrlz_source.py`
- `swrlz-core/tools/ci/resolve_changed_source_identities.py`
- `SWRLZ_SOURCE_METADATA_BUNDLE_CONTRACT_V1.md`
