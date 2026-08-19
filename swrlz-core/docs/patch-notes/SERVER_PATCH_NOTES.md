# SERVER Patch Notes — Current Candidate Pointer

## SERVER R133 / VC256 — INT-PATCH-ACCOUNTING-GDRIVE-PUBLISH-194A

- Candidate: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R133`
- Version: `2.1.27`
- Version name: `2.1.27-patch-accounting-gdrive-r133`
- Source SHA-256: `0c850daf4370b5e26d2a2a94b011faca8921a92b2e74f84d4c8177a3eefd25d8`
- Parent: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R132`
- Parent SHA-256: `bec7b0606525a3394290942586937884037a63e05b15ebfcfe41a8a953efdc4f`
- Component advancement: `INDEPENDENT_COMPONENT_ADVANCEMENT`

R133 is the current prepared SERVER repository candidate. It preserves R132 runtime behavior and repairs package/repository patch-accounting plus canonical Google Drive publication. It does not claim Android compile, APK/sign/install, device acceptance, promotion, release, or deployment.

Full checkpoint notes: `INT-PATCH-ACCOUNTING-GDRIVE-PUBLISH-194A_SERVER_PATCH_NOTES.md`.

## Historical preservation

The prior cumulative SERVER patch-note body remains preserved in Git history at blob `65a0c19bdd09c2b159618509037ccee702998b70` and in package-internal checkpoint/lineage records. This file is now the explicit current-candidate accounting pointer so SERVER can advance independently from CLIENT without stale paired-version semantics.
