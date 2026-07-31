# SWRLZ Documentation

This tree is the maintained engineering-documentation seed for the official
`kamiswrlzco-cloud/Swrlzco` repository.

Start with:

1. [`CURRENT_AUTHORITY.md`](CURRENT_AUTHORITY.md) — promoted CLIENT/SERVER source authority, later candidate lineage, and evidence boundary
2. [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md) — maintained documentation map and recent synchronization state
3. [`reference/CURRENT_STATUS_2026-07-31.md`](reference/CURRENT_STATUS_2026-07-31.md) — current overlay for Forge/CI/File-Lab/patch-note state newer than rebuild-derived status tables
4. [`client/PATCH_NOTES.md`](client/PATCH_NOTES.md) and [`server/PATCH_NOTES.md`](server/PATCH_NOTES.md) — mandatory per-component update/lineage ledgers; patch notes do not outrank canonical source/evidence authority
5. [`reference/source-of-truth.md`](reference/source-of-truth.md) — authority hierarchy and evidence classes
6. [`checkpoints/INT-CI-DOC-060A_ROUTER_INTEGRITY_AND_PATCH_NOTES_SYNC.md`](checkpoints/INT-CI-DOC-060A_ROUTER_INTEGRITY_AND_PATCH_NOTES_SYNC.md) — 2026-07-31 Source Package Integrity repair, APK Router lane-root/BOTH hardening, and patch-note synchronization policy
7. [`architecture/conversational-artifact-forge-and-file-organization-v1.md`](architecture/conversational-artifact-forge-and-file-organization-v1.md) — Forge transport/lifecycle, Chat artifact discovery, and safe file-organization architecture
8. [`checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md`](checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md) — repository CI implementation of verified chunk reconstruction and ZIP-only build eligibility
9. [`checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md`](checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md) — Precheck/Promotion Gate plus approved Forge/File Organizer requirements
10. [`architecture/repository-migration-foundation.md`](architecture/repository-migration-foundation.md) — repository layout foundation

## 2026-07-31 synchronization boundary

Maintained documentation now records the `INT-FORGE-054A-R2` CLIENT/SERVER Forge-conveyor lineage, the latest repository transport identities from Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`, and the approved-but-not-yet-implementation-evidenced `INT-FILE-059A` File Lab / Archive Cartographer scope.

The current `INT-CI-DOC-060A` workflow/documentation repair is staged on `checkpoint/int-ci-doc-060a-router-docs`. Until an explicit merge/promotion step, branch changes are not main-branch implementation evidence and no workflow rerun, APK build, release, deployment, or installation is implied.

Historical checkpoint and release evidence remains indexed in [`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).
Documentation Rebuild v2 source reports are preserved under `rebuild-v2/` as historical
evidence. Raw `.reference` source-tree duplicates and extracted Office internals from the
original documentation ZIP are intentionally not imported into the active repository.
