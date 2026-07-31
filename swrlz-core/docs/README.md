# SWRLZ Documentation

This tree is the maintained engineering-documentation root for the official
`kamiswrlzco-cloud/Swrlzco` repository.

Start with:

1. [`CURRENT_AUTHORITY.md`](CURRENT_AUTHORITY.md) — promoted CLIENT/SERVER authority plus current-candidate pointer and evidence boundary
2. [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md) — maintained documentation map through the current 2026-07-31 CI/candidate synchronization
3. [`reference/CURRENT_CANDIDATE_LINEAGE.md`](reference/CURRENT_CANDIDATE_LINEAGE.md) — current CLIENT/SERVER candidate transport, Forge/File-Lab/Truth-Core progression, and identity-collision accounting
4. [`patch-notes/CLIENT_PATCH_NOTES.md`](patch-notes/CLIENT_PATCH_NOTES.md) and [`patch-notes/SERVER_PATCH_NOTES.md`](patch-notes/SERVER_PATCH_NOTES.md) — maintained per-component candidate/update ledgers
5. [`contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`](contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md) — active contract requiring every future source update to synchronize package and repository patch-history surfaces
6. [`checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md`](checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md) — Source Package Integrity nested-transport fix, APK Router lane-root/BOTH hardening, and documentation/patch-note synchronization
7. [`reference/status-matrix.md`](reference/status-matrix.md) — current status matrix updated through Forge File Lab, Truth Core, and CI router lineage
8. [`reference/module-map.md`](reference/module-map.md) — module map updated through current candidates and CI router synchronization
9. [`reference/source-of-truth.md`](reference/source-of-truth.md) — authority hierarchy and evidence classes
10. [`architecture/conversational-artifact-forge-and-file-organization-v1.md`](architecture/conversational-artifact-forge-and-file-organization-v1.md) — Forge transport/lifecycle, Chat artifact discovery, and file-organization architecture

## 2026-07-31 synchronization boundary

Current documentation separates three recent source identities explicitly:

- shared Forge parent: CLIENT CFv2.1.26 R1 / SERVER CFv2.1.24 R1 under `INT-FORGE-054A-R2`;
- File Lab / Archive Cartographer packages: CLIENT CFv2.1.27 R1 / SERVER CFv2.1.25 R1 under `INT-FILE-059A`;
- current repository transport: CLIENT CFv2.1.27 R1 / SERVER CFv2.1.25 R1 under `INT-AI-060A` at Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`.

059A and 060A reused the same external component version/revision values for different source bytes. The collision is preserved by SHA-256, versionName, checkpoint and provenance; it must not be silently conflated. The next source candidate must advance version and/or revision.

`INT-CI-061A` fixes the Source Package Integrity nested transport-evidence routing defect and hardens APK Router source-lane/BOTH behavior. The checkpoint changed repository CI/documentation only and does not claim a workflow rerun, APK build, promotion, release, deployment, or installation.

Historical checkpoint and release evidence remains indexed in [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).
Documentation Rebuild v2 source reports are preserved under `rebuild-v2/` as historical evidence. Raw `.reference` source-tree duplicates and extracted Office internals from the original documentation ZIP are intentionally not imported into active authority.
