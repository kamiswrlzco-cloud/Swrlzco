# Current Authority — 2026-08-03

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

The promoted rows below are intentionally unchanged. A newer candidate, successful build, downloaded APK, installed APK, device screenshot, route proof, admin-registry assignment, or defect report does not promote a candidate by itself.

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Android applicationId: `sh.swrlz.core`
- versionCode: `107`
- versionName: `2.1.9-package-pair-repair-v1`
- Checkpoint: `INT-THEME-035D`
- Status: package pair and repository CLIENT debug build verified; device acceptance pending

### SERVER

- File: `sources/server/SERVER_CFv2.1.0_SWRLZ.zip`
- SHA-256: `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940`
- Android applicationId: `sh.swrlz.nodehost`
- versionCode: `50`
- versionName: `2.1.0-forge-parity-portable-repository-v1`

## Current candidate pointer — not promoted authority

The current repository-transported Forge candidate lineage is maintained in `reference/CURRENT_CANDIDATE_LINEAGE.md`.

| Component | Candidate | VC | Source SHA-256 | Metadata SHA-256 | Repository transport | Status boundary |
|---|---|---:|---|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391` | commit `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | owner-reported Android build success; not promoted |
| SERVER | CFv2.1.26 R34 | 117 | `9cafb443adfcf8dc250eefc7e8894c50190418f9604de7e151356a0e6a12f9cb` | `34cf10cdcdea4c2beeb5c39b91067743dab74019f3d5eafa0d7962a2551569e3` | commit `c92e124656fd1d9b0c2b039d29c8b508a54de309` | `SWYRLZ-SERVER-UI-HANDOFF-001-B`; repository transported; build result pending; not promoted |

R34 replaces the prior non-promoted SERVER candidate pointer because its exact chunked Forge transport is established. It does not change promoted SERVER authority.

## Current SERVER candidate interpretation

- Candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R34`
- Logical identity: `CFv2.1.26 R34`
- versionCode: `117`
- versionName: `2.1.26-chat-interface-cleanup-r34`
- checkpoint: `SWYRLZ-SERVER-UI-HANDOFF-001-B`
- source SHA-256: `9cafb443adfcf8dc250eefc7e8894c50190418f9604de7e151356a0e6a12f9cb`
- metadata SHA-256: `34cf10cdcdea4c2beeb5c39b91067743dab74019f3d5eafa0d7962a2551569e3`
- repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R34.transport.json`
- Forge transport commit: `c92e124656fd1d9b0c2b039d29c8b508a54de309`
- promotion: not promoted

R34 implements the bounded Chat-interface cleanup and related presentation amendments: active-thread and LLM-status header, functional thread navigation, compact composer, upward dragon menu, GitHub Actions first in Forge, precise mobile-data/local-link wording, and visible `Swyrlz` / `Swyrler` terminology on primary SERVER surfaces.

R34 preserves package names, protocol identifiers, database identifiers, source filenames, capability IDs, lineage, `server-root`, the persistent node-admin registry, capability-bearing mission routing, tunnel process isolation/lifecycle, identity, trust, Truth Firewall, offline-first behavior, and protocol discipline.

## Build and workflow evidence boundary

- Forge transport of R34 succeeded and established exact source identity.
- Patch Note Accounting run `30846388129` failed because the three repository accounting documents still stopped at an older SERVER candidate; this document, `reference/CURRENT_CANDIDATE_LINEAGE.md`, and `patch-notes/SERVER_PATCH_NOTES.md` now carry the exact R34 source SHA, candidate, and checkpoint.
- APK Router run `30846388177` was canceled during GitHub checkout after approximately five minutes. It did not reach component routing, source resolution, Gradle configuration, Kotlin compilation, APK packaging, or artifact upload.
- Therefore the canceled APK Router run is not evidence of an R34 source defect and is not a failed Android build result.

## SERVER runtime authority boundary

The permanent SERVER-owned internal principal remains:

- principal ID: `server-root`
- principal type: `SERVER_INTERNAL`
- authority: `ROOT_CONTROL_PLANE`
- externally assignable: `false`
- source of proof: process identity plus SERVER installation identity

`server-root` remains authoritative over registry and policy enforcement, but destructive or consequential operations remain policy- or user-approval-gated. A promoted node-admin remains a bounded client principal and never becomes server-root.

## Current evidence interpretation

- CLIENT R8 remains the current repository CLIENT candidate.
- SERVER R34 is the current repository SERVER candidate by exact Forge transport identity.
- R31 established persistent admin promotion/revocation and internal server-root authority.
- R32 established capability-bearing message/mission routing.
- R33 established truthful Core status semantics and accepted Core ordering.
- R34 established the bounded Chat-interface cleanup and visible terminology transition.
- Source transport and repository accounting do not establish Android build success, installation, runtime acceptance, promotion, release, or deployment.

## Candidate documentation entry points

- `reference/CURRENT_CANDIDATE_LINEAGE.md` — current and historical candidate identities;
- `patch-notes/CLIENT_PATCH_NOTES.md` — CLIENT candidate history;
- `patch-notes/SERVER_PATCH_NOTES.md` — SERVER candidate and implementation history;
- `contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory documentation accounting;
- package-internal `SWRLZ_SERVER_UPDATE_DELIVERY_PROTOCOL.md` — two-package handoff and standing log-repair workflow;
- package-internal `SWRLZ_SERVER_INTERFACE_FORGE_MEMORY_HANDOFF_v1.0.docx` — controlling interface/Forge/memory/permission requirements.

## Validation boundary

- Promoted authority changes only through an explicit promotion checkpoint.
- Repository source transport does not prove Android compilation.
- Android build success does not prove installation or device acceptance.
- Installation does not prove trust elevation, promotion, release, or deployment.
- Runtime server-root authority does not promote a source package.
- Node-admin assignment does not grant server-root identity.
- Remote route evidence does not grant mission, approval, Forge, release, or deployment authority.
- Patch notes are navigation/accounting evidence and cannot strengthen an unsupported claim.
- Unknown evidence remains unknown.
