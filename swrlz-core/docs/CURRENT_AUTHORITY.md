# Current Authority — 2026-08-01

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

The promoted rows below are intentionally unchanged. A newer candidate, successful build, downloaded APK, installed APK, device screenshot, or defect report does not promote a candidate by itself.

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

The current active Forge candidate lineage is maintained in `reference/CURRENT_CANDIDATE_LINEAGE.md`.

| Component | Candidate | VC | Source SHA-256 | Repository transport | Status boundary |
|---|---|---:|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | commit `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | owner-reported Android build success; not promoted |
| SERVER | CFv2.1.26 R13 | 96 | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | commit `474e1336ee65c8088ea8c6ca8a7ce5b329a540f5` | repository source candidate; Android/device result not independently established here |

Current metadata SHA-256 values:

- CLIENT R8: `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391`;
- SERVER R13: `864c020c6e590d6db84b433e670e44eda633174167cccafa646aefe3f7223e52`.

SERVER R12 is preserved as direct-parent/device-defect evidence: the project owner reported repeated ANR behavior when opening ChatGPT Tunnel Settings. R13 is the source successor intended to repair that defect. Neither statement promotes R12 or R13.

## Candidate documentation entry points

- `reference/CURRENT_CANDIDATE_LINEAGE.md` — exact current and parent candidate identities;
- `patch-notes/CLIENT_PATCH_NOTES.md` — CLIENT candidate history;
- `patch-notes/SERVER_PATCH_NOTES.md` — SERVER candidate history;
- `contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory per-update documentation accounting;
- `checkpoints/INT-DOC-065A_PATCH_NOTE_CATCHUP_AND_ENFORCEMENT.md` — current catch-up and enforcement checkpoint.

## Historical candidate evidence

Earlier candidate/evidence lineages—including the INT-AI-060A / INT-FILE-059A external identity collision, the 041H baseline, SWRLIE R1-R6 progression, Documentation Rebuild v2 and corrected CFv2.1.0 handoff—remain preserved in repository history and the applicable files under `docs/checkpoints/`, `docs/rebuild-v2/`, and `docs/handoffs/`.

Those historical records are not rewritten into current parentage. Exact source SHA-256 and checkpoint provenance decide identity.

## CLIENT checkpoint boundary

Promoted CLIENT CFv2.1.9 preserves the complete CFv2.1.8 declarative ThemePack presentation implementation and repairs package/application identity and canonical sidecar-manifest behavior. Theme selection remains local and presentation-only. SERVER, protocol, trust, Truth Firewall, identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility automation, and offline-first behavior remain separate.

## Validation boundary

- Promoted authority changes only through an explicit promotion checkpoint.
- Repository source transport does not prove Android compilation.
- Android build success does not prove installation or device acceptance.
- Installation does not prove trust elevation, promotion, release, or deployment.
- Patch notes are navigation/accounting evidence and cannot strengthen an unsupported claim.
- Unknown evidence remains unknown.
