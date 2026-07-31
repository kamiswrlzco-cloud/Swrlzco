# SWRLZ Current Status Overlay — 2026-07-31

This file is the maintained current-status overlay for changes newer than the older rebuild-derived `status-matrix.md` / `feature-registry.md` rows. It does not erase historical evidence and does not change promoted source authority in `../CURRENT_AUTHORITY.md`.

## Candidate / transport status

| Area | Component | State | Evidence boundary |
|---|---|---|---|
| Shared Forge conveyor | CLIENT | SOURCE CANDIDATE | CLIENT CFv2.1.26 R1 / VC124 / SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`; `INT-FORGE-054A-R2`; source-only candidate, no build/promotion claim here |
| Shared Forge conveyor | SERVER | SOURCE CANDIDATE | SERVER CFv2.1.24 R1 / VC82 / SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`; `INT-FORGE-054A-R2`; source-only candidate, no build/promotion claim here |
| Latest Forge transport | CLIENT | TRANSPORT IDENTITY | CFv2.1.27 R1 / SHA `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`; Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`; checksum evidence only in transaction; no internal-change/build/promotion inference |
| Latest Forge transport | SERVER | TRANSPORT IDENTITY | CFv2.1.25 R1 repository identity `-1` / SHA `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`; Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`; checksum evidence only in transaction; no internal-change/build/promotion inference |
| File Lab / Archive Cartographer | CLIENT + SERVER | APPROVED / NOT YET IMPLEMENTATION-EVIDENCED | `INT-FILE-059A`; read/search/hash/map/preview/selective extraction, staged edits, split/recombine, logical shards/provenance, SAF work/output/shard dirs, deterministic analyzer APIs |

## Forge shared baseline — INT-FORGE-054A-R2

Candidate implementation direction now includes:

- ASK / CLIENT / SERVER / BOTH / FILES targeting;
- latest-source discovery based on component/version/manifest/SHA/lineage rather than filename/mtime alone;
- configurable SAF project root, CLIENT source, SERVER source, APK artifact, failed-log, LLM model, SWRLZMOD, and evidence lanes;
- user-initiated verify/upload/build/watch flow through existing GitHub transport;
- successful-artifact auto-download default ON;
- failed-workflow-log auto-download default ON;
- persistent Build Ledger separating source found/verified/uploaded/requested/running/success/downloaded/install-pending/installed and failure/log-downloaded states;
- manual verified source override;
- CLIENT mirrors the shared Forge baseline while preserving CLIENT-only Missions/legacy Dev Mode and SERVER-only inference/model/evidence authority.

## CI repair — INT-CI-DOC-060A branch state

Source Package Integrity run `30658738049` failed because the previous recursive selector treated nested transport checksum evidence as direct lane-root sidecar evidence, derived a nonexistent nested ZIP path, and failed `Missing ZIP`.

Prepared branch repair:

- direct source integrity selection is lane-root only;
- nested `.transport/` chunks/evidence cannot become direct source package candidates;
- APK Router push routing is lane-root only;
- Router supports manual/request `BOTH` while keeping CLIENT/SERVER matrix components;
- one explicit manual `source_zip` is rejected with `BOTH` to avoid ambiguous cross-component routing.

Branch: `checkpoint/int-ci-doc-060a-router-docs`.

No workflow rerun or APK build is claimed from the branch repair. A Router screenshot showing `Validate source resolver` waiting for a GitHub-hosted runner is treated as runner scheduling state, not automatically as a Router-code defect.

## Patch-note status

Maintained component ledgers:

- `../client/PATCH_NOTES.md`
- `../server/PATCH_NOTES.md`

Future accepted implementation checkpoints must update the affected ledger before documentation is complete. Shared checkpoints update both. Patch notes do not replace source SHA/manifest/contract/build/device/promotion authority.

## Truth / identity invariants retained

- SWRLZ/Swurlz remains persistent primary identity.
- Selected LLM remains a replaceable reasoning engine.
- Swurlzara remains a replaceable expression/profile lens.
- SWRLIE remains the first-party reasoning/provider interface.
- Truth Firewall, authorization, provenance, node/file/mission/Forge authority, local-vs-remote distinctions, and protocol discipline remain SWRLZ-owned constraints rather than profile/model settings.
