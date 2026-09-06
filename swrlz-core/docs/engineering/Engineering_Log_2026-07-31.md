# SWRLZ Engineering Log — 2026-07-31 Extension

This file extends the older `Engineering_Log.md` without rewriting historical entries. Promoted authority remains in `../CURRENT_AUTHORITY.md`.

## INT-FORGE-054A-R2 — shared Forge conveyor / CLIENT parity

Packaged source-only parents:

- CLIENT CFv2.1.26 R1 / VC124 / `2.1.26-forge-parity-chat-settings-candidate-r1` / SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`;
- SERVER CFv2.1.24 R1 / VC82 / `2.1.24-forge-conveyor-lineage-candidate-r1` / SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`.

Shared candidate behavior includes Forge target selection, authoritative latest-source/manifest/SHA/lineage resolution, configurable SAF storage lanes, persistent Build Ledger state, success-artifact/failure-log download policy, and patch/checkpoint lineage. CLIENT mirrors the shared Forge baseline while preserving CLIENT-only Missions/legacy Dev Mode and SERVER-only inference/model/evidence authority.

No APK build/promotion/release/deployment/install is asserted by the source-only checkpoint.

## INT-FILE-059A — Forge File Lab / Archive Cartographer

Packaged candidates:

- CLIENT CFv2.1.27 R1 / VC125 / `2.1.27-file-lab-cartographer-candidate-r1` / SHA `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`;
- SERVER CFv2.1.25 R1 / VC83 / `2.1.25-file-lab-cartographer-candidate-r1` / SHA `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`.

Recorded candidate scope includes read-only inventory/map/search/preview/SHA-256, selective extraction, staged text revision with original preservation and new-output lineage, binary split/recombine, logical size-bounded ZIP sharding, SAF work/output/shard directories, and deterministic analyzer/map export surfaces.

Packaged checkpoint evidence records static `41/41`, ZIP CRC/integrity and deterministic-repack PASS, and shared parity/protocol checks PASS. No APK/device/release/install claim is inferred.

## INT-AI-060A — truth / reasoning / expression separation

Current Forge repository transport commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` carries:

- CLIENT CFv2.1.27 R1 / VC125 / `2.1.27-truth-reasoning-expression-separation-candidate-r1` / SHA `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`;
- SERVER CFv2.1.25 R1 / VC83 / `2.1.25-truth-reasoning-expression-separation-candidate-r1` / SHA `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`.

The candidate direction separates Truth Core invariants from reasoning/output budgets and profile expression shaping. Truthfulness, sovereignty, speaker grounding, evidence/authority precedence, uncertainty honesty, and action-result honesty remain outside profile controls. Profile/expression may shape presentation without becoming fact or authorization authority.

The 059A and 060A packages reused the same external version/revision identifiers with different source bytes. This is an explicit identity collision, not a replacement. Exact SHA/versionName/checkpoint provenance keeps them separate; the next candidate must advance version and/or revision.

## INT-CI-061A — Source Package Integrity / APK Router repair

Triggering run evidence: Source Package Integrity run `30658738049` failed after a Forge chunk upload because nested `.transport/<bundle>/evidence/<bundle>.sha256` was treated as a direct sidecar and converted into an invented nested ZIP path.

Main-branch repair now:

- maps changed source-tree members to canonical lane-root source identities using `tools/ci/resolve_changed_source_identities.py`;
- maps transport chunks/evidence to their lane-root `*.transport.json` identity;
- deduplicates transport members and fails closed when a transport member lacks a lane-root identity;
- resolves/reconstructs through the canonical source resolver before package verification;
- adds regression coverage in `test_resolve_changed_source_identities.py`;
- hardens APK Router to lane-root source/evidence push signals;
- adds manual CLIENT / SERVER / BOTH routing with ambiguity/release-commit guards;
- runs both resolver regression suites.

A separate APK Router screenshot showed `Validate source resolver` waiting for a GitHub-hosted runner. That state is runner scheduling/provisioning evidence and is not treated as a repository-code failure by itself.

No workflow was manually dispatched by INT-CI-061A, and the repository changes alone do not prove APK build success.

## Patch-note accounting lock

`../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` is now ACTIVE. Every future CLIENT/SERVER source update must synchronize patch history in the same bounded checkpoint, including package `ReleaseNotes.md`, `CHANGELOG.md`, `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` when present, repository component patch notes, and current candidate accounting when repository transport changes.

Repository ledgers:

- `../patch-notes/CLIENT_PATCH_NOTES.md`
- `../patch-notes/SERVER_PATCH_NOTES.md`

Patch notes remain navigation/index evidence rather than promotion authority.
