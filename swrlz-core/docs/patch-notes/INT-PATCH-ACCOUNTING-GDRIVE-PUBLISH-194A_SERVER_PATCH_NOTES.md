# SERVER R133 / VC256 — INT-PATCH-ACCOUNTING-GDRIVE-PUBLISH-194A

- Candidate: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R133`
- Version: `2.1.27`
- Version name: `2.1.27-patch-accounting-gdrive-r133`
- Source SHA-256: `0c850daf4370b5e26d2a2a94b011faca8921a92b2e74f84d4c8177a3eefd25d8`
- Parent: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R132`
- Parent SHA-256: `bec7b0606525a3394290942586937884037a63e05b15ebfcfe41a8a953efdc4f`
- CLIENT compatibility reference: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R97`; component advancement is independent.

R133 is an accounting/publication repair successor to R132. The R132 long-form LALM/VFS runtime is preserved. This checkpoint fixes the package-internal authority surfaces that caused Patch Note Accounting to reject R132 and aligns Google Drive publication with the existing Forge contract: `/SWRLZ Forge/SERVER/latest.json` plus immutable `/SERVER/releases/<candidate>/` source+metadata.

## Main changes
- Updates `CHANGELOG.md`, `ReleaseNotes.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` to the exact R133/VC256/checkpoint identity.
- Advances Android source identity only; no SERVER runtime behavior is intentionally changed.
- Publishes SERVER independently from CLIENT; no lockstep revision assumption is introduced.
- Preserves R132 segmented long-form generation, R131 LALM namespace/log routing, R130 native `.§wyrlzx` runtime/Studio and Google reauth repair.

## Evidence boundary
Source/accounting/package and Drive-contract publication only. Fresh GitHub Android/Kotlin compile, APK/sign/install and device acceptance remain required.
