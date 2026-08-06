# SERVER Patch Notes

**Scope:** SERVER / §wyrver source-candidate lineage, repository transport history, and prepared direct successors.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply Android compilation, installation, device acceptance, promotion, release, or deployment unless separate evidence is named.

## Current prepared repository candidate — 2026-08-05

### CFv2.1.27 R10 — INT-FORGE-082A

- canonical candidate: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R10`
- display role: §wyrver / SERVER
- versionCode: `133`
- version: `2.1.27`
- revision: `R10`
- checkpoint: `INT-FORGE-082A`
- source SHA-256: `4c4358fc4995986c05e29f78621f8cb949eda77ee58a938d8a80f1189e18f770`
- metadata bundle SHA-256: `4a31abefc4d43fc9c9164d2d130d3c9706a05fcfd823c2c5c868b32c808cfbdf`
- direct parent: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R9.zip`
- repository identity when transported: `sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R10.zip` or its canonical transport descriptor
- evidence workflow: `31069235859`
- build state: source-only successor; no Android build success claimed
- promotion: not promoted

Changes:

- adds duplicate-aware Forge upload/build orchestration;
- permits an exact repository duplicate to skip source re-upload while still dispatching an explicit APK Router build;
- preserves independent CLIENT and SERVER handling during mixed uploads so one duplicate does not block the other lane;
- binds build monitoring to the expected component, candidate stem, and artifact identity;
- removes fallback behavior that could associate a CLIENT watch with an unrelated SERVER result;
- preserves §wyrver SERVER authority, `server-root`, local/remote distinctions, approval gates, Truth Firewall, lineage, offline-first behavior, compatibility identifiers, and protocol discipline.

## Immediate lineage

### CFv2.1.27 R9 — INT-FORGE-081A

- direct parent of R10;
- integrated Dragon Master Workshop, Invitation Invocation, §wyrlish, §wyrlix/§wyrver naming, Theme Zero, theme anchors, presence, voice roadmap, Forge Chronicle, and roadmap documentation;
- repaired malformed doubled Kotlin braces in `ForgeConveyorStateStore.kt`;
- source-only evidence; no Android build success claimed.

### CFv2.1.27 R7 — INT-FORGE-079A

- introduced the adaptive Forge Project Conveyor, need-based file-analysis orchestration, Council contracts, persistent conveyor state, threshold-review foundation, and Architecture Genome scaffolding;
- source-only evidence; no Android build success claimed.

## Preserved earlier verified SERVER lineage

The earlier repository candidate remains historical evidence and is not rewritten:

- `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2`
- versionCode `130`
- checkpoint `INT-FIX-075A`
- source SHA-256 `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`
- exact-SHA Android debug build success in workflow `30965115165`; device/runtime acceptance pending; not promoted.

The failed R1 parent, R35-R45 catch-up, R30-R34 control/UI history, and earlier SERVER milestones remain preserved in Git history and package-internal lineage. This reconciliation advances the non-promoted candidate accounting pointer only; it does not erase prior evidence or change promoted authority.

## Patch-accounting evidence

Patch Note Accounting run `31068508343` displayed as failure because current package and repository accounting surfaces did not yet identify the latest SERVER candidate/checkpoint/SHA consistently. This repository reconciliation addresses the repository-side omissions only. Package-internal accounting remains bound to the exact uploaded source archive and is not rewritten here.

## Mandatory accounting rule

Every later SERVER candidate must update package-internal `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file, `../reference/CURRENT_CANDIDATE_LINEAGE.md`, and the non-promoted candidate pointer in `../CURRENT_AUTHORITY.md`. Patch Note Accounting remains separate from source integrity, Android builds, device acceptance, promotion, release, and deployment.
