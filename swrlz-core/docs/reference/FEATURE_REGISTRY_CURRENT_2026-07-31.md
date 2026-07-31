# SWRLZ Current Feature Registry Overlay — 2026-07-31

This overlay records current post-041H feature/candidate state without rewriting the older rebuild-derived `feature-registry.md`. Promoted authority remains governed by `../CURRENT_AUTHORITY.md`.

| Feature | Component | Owner Plane | Status | Current evidence / notes |
|---|---|---|---|---|
| Shared Forge build conveyor | CLIENT + SERVER | SWRLZ Forge | SOURCE CANDIDATE | INT-FORGE-054A-R2; CLIENT CFv2.1.26 R1 SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`; SERVER CFv2.1.24 R1 SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`; shared target/source/SAF/Build-Ledger/artifact-log behavior with role-specific boundaries |
| Forge File Lab / Archive Cartographer | CLIENT + SERVER | SWRLZ Forge / File authority | PACKAGED SOURCE CANDIDATE | INT-FILE-059A; CLIENT SHA `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`; SERVER SHA `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`; read/map/search/hash/preview/selective extract, staged edits, binary split/recombine, logical sharding, SAF work/output/shard lanes, deterministic analyzer exports |
| Truth / reasoning / expression separation | CLIENT + SERVER | SWRLZ Core + SWRLIE | CURRENT REPOSITORY SOURCE TRANSPORT | INT-AI-060A; CLIENT SHA `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`; SERVER SHA `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`; truth/sovereignty/speaker/evidence/uncertainty/action-result standards outside profile authority; profile shapes expression, not facts |
| Current candidate identity accounting | CLIENT + SERVER | Lineage / Truth Firewall | IMPLEMENTED DOCUMENTATION CONTRACT | 059A and 060A reused external CFv2.1.27 R1 / CFv2.1.25 R1 values with different bytes; collision preserved by exact SHA/versionName/checkpoint; next candidate must advance version and/or revision |
| Mandatory patch-note accounting | CLIENT + SERVER | Documentation / Packaging | ACTIVE CONTRACT | `SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`; every future candidate synchronizes `ReleaseNotes.md`, `CHANGELOG.md`, `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` when present, repository component patch notes, and current candidate accounting |
| Source Package Integrity canonical identity routing | Build | CI | REPOSITORY FIX APPLIED / RUNTIME VALIDATION STILL SEPARATE | INT-CI-061A maps changed nested transport members to lane-root source identities with `resolve_changed_source_identities.py`; prevents invented nested evidence ZIPs; no workflow-rerun result claimed by documentation alone |
| APK Router CLIENT / SERVER / BOTH routing | Build | CI / Forge | REPOSITORY FIX APPLIED / RUNTIME VALIDATION STILL SEPARATE | INT-CI-061A; resolver suites, lane-root push classification, manual BOTH, explicit-source ambiguity guard, BOTH release-commit guard, existing build/sign/provenance/artifact flow preserved |
| CLIENT shared Forge parity | CLIENT | CLIENT + Forge | SOURCE CANDIDATE | CLIENT mirrors shared Forge/Chat/Settings baseline while preserving Missions, legacy Dev Mode and CLIENT-side roles; SERVER-only model/inference/evidence authority is not cloned for parity |
| SERVER reasoning/model authority | SERVER | SERVER + SWRLIE | PRESERVED ARCHITECTURE / SOURCE CANDIDATE LINEAGE | Later shared Forge/File/Truth changes do not transfer SERVER-owned inference/model/evidence responsibility to CLIENT |
| Greeting/status/casual short fast routing | SERVER | SWRLZ Core / SWRLIE | SOURCE CANDIDATE + SELECTED DEVICE EVIDENCE | INT-PERF-050B / 050D / 052A sequence; deterministic/narrow routes reduce unnecessary prompt work while explanatory/action requests retain normal reasoning path |
| Persistent Chat / evidence / asset selection | SERVER | Chat + SERVER | SOURCE CANDIDATE | 045A/045B/045C progression: Room history, reactions/evidence, model/EQ/module/runtime lineage, persisted GGUF/SWRLZMOD discovery, evidence export |

## Authority rules

- `SOURCE CANDIDATE` does not mean promoted source.
- `PACKAGED SOURCE CANDIDATE` does not mean APK built or installed.
- Repository transport/checksum proves source identity, not Android compilation.
- Profiles may change expression, not Truth Firewall, evidence, permission, provenance, file/Forge authority, or action-result truth.
- CLIENT/SERVER parity applies only to shared capabilities; legitimate component-specific roles remain distinct.
