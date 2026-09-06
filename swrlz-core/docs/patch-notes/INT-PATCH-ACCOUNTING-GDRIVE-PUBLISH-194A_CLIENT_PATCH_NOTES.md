# CLIENT R97 / VC223 — INT-PATCH-ACCOUNTING-GDRIVE-PUBLISH-194A

- Candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R97`
- Version: `2.1.27`
- Version name: `2.1.27-patch-accounting-gdrive-r97`
- Source SHA-256: `17b97f121da1cede54eb13c9881cd9742d7fa09a9a76d4488c4e09b12f7a7b2c`
- Parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R96`
- Parent SHA-256: `21fe0a77a561fd2181d97595369076c708a2e9f77d9215a170c17de2afc8a9d5`
- SERVER compatibility reference: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R133`; component advancement is independent.

R97 is an accounting/publication repair successor to R96. The R96 runtime changes are preserved. This checkpoint fixes the package-internal authority surfaces that caused Patch Note Accounting to reject R96 and aligns Google Drive publication with the existing Forge contract: `/SWRLZ Forge/CLIENT/latest.json` plus immutable `/CLIENT/releases/<candidate>/` source+metadata.

## Main changes
- Updates `CHANGELOG.md`, `ReleaseNotes.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` to the exact R97/VC223/checkpoint identity.
- Advances Android source identity only; no CLIENT runtime behavior is intentionally changed.
- Publishes CLIENT independently from SERVER; no lockstep revision assumption is introduced.
- Preserves R96 artifact-generation envelope normalization and R95 Google reauth routing repair.

## Evidence boundary
Source/accounting/package and Drive-contract publication only. Fresh GitHub Android/Kotlin compile, APK/sign/install and device acceptance remain required.
