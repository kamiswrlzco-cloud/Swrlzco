# Current Authority — 2026-08-03

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

The promoted rows below are intentionally unchanged. A newer candidate, successful build, downloaded APK, installed APK, device screenshot, remote-route proof, or defect report does not promote a candidate by itself.

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Android applicationId: `sh.swurlz.core`
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
| SERVER | CFv2.1.26 R27 | 110 | `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1` | `10ace6898df22bb8ed53b99cf563edf8bec05cd66db6fc453bff1e17d497da6a` | commit `1e48e2e4d6652fe9c9c0e1f25c32362b0051f677` | INT-STABILITY-068A; repository transported; Android build/device acceptance pending; not promoted |

R27 replaces the prior non-promoted SERVER candidate pointer because its exact chunked Forge transport is established. It does not change promoted SERVER authority.

## Current SERVER candidate interpretation

- R27 is `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R27`, VC110, checkpoint `INT-STABILITY-068A`.
- Exact source SHA-256: `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1`.
- Exact metadata SHA-256: `10ace6898df22bb8ed53b99cf563edf8bec05cd66db6fc453bff1e17d497da6a`.
- Repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R27.transport.json`.
- Forge transport commit: `1e48e2e4d6652fe9c9c0e1f25c32362b0051f677`.
- R27 repairs generation races across tunnel status query, STOP, restart, retry, Binder death, delayed callbacks, and remote-process evidence handling.
- The private `:swrlz_tunnel` process boundary, bounded resources, explicit activation, encrypted credentials, MCP, NODE_HOST, models, identity, trust, Truth Firewall, offline-first behavior, and local/remote distinctions remain preserved.
- Source/static verification does not prove Android build success, installation, device survival, promotion, release, or deployment.

## Current evidence interpretation

- CLIENT R8 remains the current repository CLIENT candidate.
- SERVER R27 is the current repository SERVER candidate by exact Forge transport identity.
- Earlier device/plugin evidence established that ChatGPT reached native SERVER MCP tools; route evidence did not elevate identity, trust, proof, mission, approval, Forge, release, or deployment authority.
- R23-R27 progressively addressed startup model loading, launch crash loops, tunnel process isolation, update-delivery continuity, and generation-safe tunnel query/restart lifecycle behavior.
- The reported tunnel query/off-on/retry crash is the device defect targeted by R27. Actual device acceptance remains pending until the exact R27 APK is built, installed, and tested.

## Candidate documentation entry points

- `reference/CURRENT_CANDIDATE_LINEAGE.md` — exact current and parent candidate identities;
- `patch-notes/CLIENT_PATCH_NOTES.md` — CLIENT candidate history;
- `patch-notes/SERVER_PATCH_NOTES.md` — SERVER candidate and tunnel/MCP/stability history;
- `contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory documentation accounting;
- package-internal `SWRLZ_SERVER_UPDATE_DELIVERY_PROTOCOL.md` — two-package handoff and standing log-repair workflow carried by current SERVER sources.

## Historical candidate evidence

Earlier candidate/evidence lineages—including the INT-AI-060A / INT-FILE-059A external identity collision, the 041H baseline, SWRLIE R1-R6 progression, Documentation Rebuild v2, CFv2.1.0 handoff, and R9-R26 SERVER progression—remain preserved in repository history and the applicable documents under `docs/checkpoints/`, `docs/rebuild-v2/`, `docs/handoffs/`, `docs/reference/`, and `docs/patch-notes/`.

Exact source SHA-256 and checkpoint provenance decide identity. Historical records are not rewritten into false current parentage.

## CLIENT checkpoint boundary

Promoted CLIENT CFv2.1.9 preserves the complete CFv2.1.8 declarative ThemePack presentation implementation and repairs package/application identity and canonical sidecar-manifest behavior. Theme selection remains local and presentation-only. SERVER, protocol, trust, Truth Firewall, identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility automation, and offline-first behavior remain separate.

## Validation boundary

- Promoted authority changes only through an explicit promotion checkpoint.
- Repository source transport does not prove Android compilation.
- Android build success does not prove installation or device acceptance.
- Installation does not prove trust elevation, promotion, release, or deployment.
- Remote route evidence does not grant trust, mission, approval, admin, Forge, release, or deployment authority.
- Patch notes are navigation/accounting evidence and cannot strengthen an unsupported claim.
- Unknown evidence remains unknown.
