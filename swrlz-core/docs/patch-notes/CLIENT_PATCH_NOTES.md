# CLIENT Patch Notes — Current Candidate Pointer

## CLIENT R97 / VC223 — INT-PATCH-ACCOUNTING-GDRIVE-PUBLISH-194A

- Candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R97`
- Version: `2.1.27`
- Version name: `2.1.27-patch-accounting-gdrive-r97`
- Source SHA-256: `17b97f121da1cede54eb13c9881cd9742d7fa09a9a76d4488c4e09b12f7a7b2c`
- Parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R96`
- Parent SHA-256: `21fe0a77a561fd2181d97595369076c708a2e9f77d9215a170c17de2afc8a9d5`
- Component advancement: `INDEPENDENT_COMPONENT_ADVANCEMENT`

R97 is the current prepared CLIENT repository candidate. It preserves R96 runtime behavior and repairs package/repository patch-accounting plus canonical Google Drive publication. It does not claim Android compile, APK/sign/install, device acceptance, promotion, release, or deployment.

Full checkpoint notes: `INT-PATCH-ACCOUNTING-GDRIVE-PUBLISH-194A_CLIENT_PATCH_NOTES.md`.

## Historical preservation

The prior cumulative CLIENT patch-note body remains preserved in Git history at blob `8764ab54845042ba58159c17ef35b65769ddcda6` and in package-internal checkpoint/lineage records. This file is now the explicit current-candidate accounting pointer so CLIENT can advance independently from SERVER without stale paired-version semantics.
