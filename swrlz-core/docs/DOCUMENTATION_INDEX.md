# Documentation Index

## Current authority and migration

- `CURRENT_AUTHORITY.md` — current promoted repository/source authority, later candidate lineage, hashes, and evidence boundary
- `reference/source-of-truth.md` — authority hierarchy
- `reference/documentation-manifest.md` — package accounting, source-authority evidence, ZIP-only build eligibility, chunk-transport policy, and documentation synchronization history
- `architecture/repository-migration-foundation.md` — selected repository layout

## Component patch notes

- `client/PATCH_NOTES.md` — maintained CLIENT candidate/update ledger; every accepted CLIENT implementation checkpoint must be represented here before documentation is complete
- `server/PATCH_NOTES.md` — maintained SERVER candidate/update ledger; every accepted SERVER implementation checkpoint must be represented here before documentation is complete

Patch notes are lineage/navigation evidence and do not outrank canonical source ZIP/SHA, accepted contracts/manifests, or stronger build/device/promotion evidence. Shared checkpoints that change both apps update both ledgers.

## Architecture

- `architecture/system-overview.md`
- `architecture/client-architecture.md`
- `architecture/client-theme-chrome-runtime-v1.md` — declarative CLIENT chrome, progress, startup, performance, and accessibility boundaries
- `architecture/repository-migration-foundation.md`
- `architecture/conversational-artifact-forge-and-file-organization-v1.md` — Forge transport/lifecycle, Chat package discovery, Local Artifact Resolver, safe file organization, multi-folder Keep Organized, and 039F/039N build-input boundaries
- `architecture/SWRLZ_ARCHIVE_LINEAGE_AND_FILE_ORGANIZATION_EXTENSION_V1.md` — archive inspection, extracted-tree lineage detection, package clustering, divergence handling, cleanup planning, and archive-safety extension for INT-FILE-039M
- `architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` — canonical distributed CLIENT/SERVER/SWRLIE architecture, LOCAL/LAN/ONLINE modes, SERVER network/Forge authority direction, model independence, model lifecycle, node hosting, telemetry, and implementation-status boundaries
- `architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` — R1-R5 SWRLIE runtime evolution, SWRLZ Skills placement, behavioral baseline/model tiers, grounding, personality-control direction, efficiency/density, hardware tiers, and future Simulation Forge/media specialists
- `architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md` — canonical SWRLZ primary identity, LLM-as-replaceable-reasoning-engine, Swurlzara-as-profile-lens, intrinsic Truth Firewall, self-reflection semantics, and model/profile swap invariants
- `architecture/SWRLZ_RUNTIME_AND_LIVE_PACK_UPDATE_ARCHITECTURE_V1.md` — companion architecture for stable runtime products, SERVER-owned live-pack discovery, SWRLIE base-plus-modules evolution, incremental/content-addressed fetch, hot activation generations, rollback, and separate signed APK runtime updates

## Contracts

- `contracts/SWRLZ_UPDATE_AND_PACK_MANIFEST_CONTRACT_V1.md` — common manifest, product/activation classes, compatibility, object identity, lineage, signing, update planning, state machine, rollback, source adapters, and CLIENT/SERVER authority boundaries for runtime and live-pack updates

## Runtime and implementation analysis

- `client/CLIENT_IMPLEMENTATION_ANALYSIS.md`
- `server/SERVER_IMPLEMENTATION_ANALYSIS.md`
- `missions/action-resolution.md`

## Reference

- `reference/evidence-classification.md`
- `reference/feature-registry.md`
- `reference/module-map.md`
- `reference/status-matrix.md`
- `reference/documentation-manifest.md`

## WordMesh

- `wordmesh/WORDMESH_IMPLEMENTATION_GAP_ANALYSIS.md`

## Releases

- `releases/compatibility-matrix.md`
- `releases/CLIENT_CFv2.1.9_PACKAGE_PAIR_REPAIR.md`
- `releases/CLIENT_CFv2.1.8_THEME_CHROME_RUNTIME_REPAIR.md`

## Checkpoints and engineering evidence

- `checkpoints/INT-CI-DOC-060A_ROUTER_INTEGRITY_AND_PATCH_NOTES_SYNC.md` — 2026-07-31 repair record for Source Package Integrity nested-transport evidence misrouting, APK Router lane-root/BOTH hardening, current candidate/documentation synchronization, and the mandatory per-component patch-note rule; branch-only until explicit merge approval
- `checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md` — docs-only synchronization of CLIENT CFv2.1.22 R1, SERVER CFv2.1.9 R6/VC64 lineage, corrected SWRLZ/LLM/Swurlzara identity semantics, intrinsic Truth Firewall, Behavioral-EQ v2 direction, operator-reported Q4_K_M/Q8_0 benchmark state, feedback-ledger/plugin direction, and conversation-first Chat requirements; no promotion or implementation authority change
- `checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md` — docs-only synchronization of SERVER CFv2.1.9 SWRLIE candidate R1-R5 source lineage, exact SHAs/Forge commits, feature progression, and evidence boundaries; no authority promotion
- `checkpoints/INT-DOC-UPD-040C-040D_UPDATE_ARCHITECTURE_SYNC.md` — docs-only integration record for game-like SWRLZ live packs, modular SWRLIE delivery, SERVER-owned update discovery, and separate runtime/APK update supervision; 040C/040D remain planned implementation checkpoints
- `checkpoints/INT-DOC-AI-040A_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_SYNC.md` — docs-only integration record for the distributed intelligence architecture; no source/build/promotion authority change
- `checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` — implemented repository CI support for verified chunk reconstruction and ZIP-only build eligibility; no source promotion
- `checkpoints/INT-FORGE-039F-039N_DOCUMENTATION_IMPACT_SET.md` — maintained-document impact classification for the CI application
- `checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md` — documentation synchronization for Precheck/Promotion Gate, Forge 039K/039L, and FILES 039M; does not change source authority
- `checkpoints/INT-THEME-035D_CLIENT_PACKAGE_PAIR_REPAIR.md`
- `checkpoints/INT-THEME-035C_CLIENT_THEME_CHROME_RUNTIME_REPAIR.md`
- `engineering/Engineering_Log.md`
- `evidence/INT-THEME-035C_PROGRESS_GEOMETRY_PREVIEW.jpg` — static geometry evidence, not Android runtime evidence
- `handoffs/INT-THEME-035D_SOURCE_HANDOFF.md`
- `evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md`
- `handoffs/INT-THEME-035C_SOURCE_HANDOFF.md`

## Recent candidate / approved-scope synchronization

- CLIENT CFv2.1.26 R1 / VC124 / `INT-FORGE-054A-R2`: shared Forge conveyor parity, configurable SAF lanes, build ledger, artifact/log download policy, Chat/Settings catch-up while preserving CLIENT-only Missions/legacy Dev Mode; source SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`
- SERVER CFv2.1.24 R1 / VC82 / `INT-FORGE-054A-R2`: shared Forge conveyor/lineage foundation while preserving SERVER-specific runtime/inference authority; source SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`
- Latest repository transports from Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`: CLIENT CFv2.1.27 R1 SHA `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`; SERVER CFv2.1.25 R1-1 SHA `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`; transport identity only unless stronger evidence is linked
- `INT-FILE-059A`: approved shared CLIENT/SERVER Forge File Lab + Archive Cartographer scope, but approval is not implementation/package evidence

## Historical rebuild records

- `rebuild-v2/`
- `handoffs/`
