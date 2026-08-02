# INT-DOC-065A — CLIENT/SERVER Patch-Note Catch-up and Every-Update Enforcement

**Date:** 2026-08-01  
**Repository:** `kamiswrlzco-cloud/Swrlzco`  
**Branch:** `main`  
**Scope:** repository documentation, candidate accounting and prospective patch-note CI audit.  
**Does not authorize or claim:** source feature changes, APK build, installation, trust elevation, promotion, release or deployment.

## Trigger

Repository patch notes and current candidate pointers were still frozen at the earlier INT-AI-060A line while Forge had advanced the active lineage to:

- CLIENT CFv2.1.26 R8 / VC131 / SHA `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` / commit `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b`;
- SERVER CFv2.1.26 R13 / VC96 / SHA `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` / commit `474e1336ee65c8088ea8c6ca8a7ce5b329a540f5`.

The existing patch-note contract required same-checkpoint synchronization, but no independent CI audit enforced it.

## Documentation synchronized

- `docs/patch-notes/CLIENT_PATCH_NOTES.md` now records R6 → R7 → R8 and keeps divergent 2.1.27 lineage separate by SHA.
- `docs/patch-notes/SERVER_PATCH_NOTES.md` now records R9 → R10 → R11 → R12 → R13 and the R12 Tunnel Settings ANR evidence.
- `docs/reference/CURRENT_CANDIDATE_LINEAGE.md` now points to CLIENT R8 and SERVER R13 and separates build, install, device-defect and promotion evidence.
- `docs/CURRENT_AUTHORITY.md` retains promoted CLIENT CFv2.1.9 and SERVER CFv2.1.0 while updating only the candidate pointer.
- `README.md` now points to the current accounting surfaces and workflow.
- `docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` now defines documentation-complete, explicit current debt and CI enforcement.

## Package-internal debt discovered

The source ZIPs are immutable evidence and were not rewritten.

- CLIENT R8 has a current `CHANGELOG.md`, but `ReleaseNotes.md` opens at R1 and lineage JSON identifies R4/VC127.
- SERVER R13 has a current `CHANGELOG.md`, but `ReleaseNotes.md` opens at R3 and lineage JSON identifies R5/VC88.

Those exact source SHAs are grandfathered as `DEBT_RECORDED`, not declared correct. The next candidate for each component must update all three internal surfaces.

## Prospective enforcement

Added:

- `tools/ci/verify_patch_note_accounting.py`;
- `tools/ci/test_verify_patch_note_accounting.py`;
- `.github/workflows/patch-note-accounting.yml`.

The workflow audits source and documentation updates independently from Source Package Integrity and APK Router. Missing/stale patch notes fail the documentation workflow without relabeling the source package or Android build as corrupt.

The workflow does not auto-edit or auto-commit documents. This preserves reviewable source/document lineage and prevents an automated job from inventing implementation notes.

## Evidence and status boundaries

- CLIENT R8 / SERVER R11 successful builds are owner-reported; no run ID is invented.
- SERVER R12 Tunnel Settings ANR is owner-reported on-device defect evidence; it is not device acceptance.
- SERVER R13 repository source transport is established; this checkpoint does not claim an R13 Android build or runtime result.
- Promoted authority is unchanged.
- No source package, APK, release or deployment was created by this documentation checkpoint.

## Locked rule

Every future CLIENT/SERVER update must state one of:

- `PATCH_ACCOUNTING=PASS`;
- `PATCH_ACCOUNTING=DEBT_RECORDED` only for the two exact grandfathered SHAs;
- `PATCH_ACCOUNTING=FAIL` and the checkpoint remains documentation-incomplete.
