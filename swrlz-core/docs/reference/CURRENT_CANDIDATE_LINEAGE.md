# Current CLIENT / SERVER Candidate Lineage — 2026-08-01

This file tracks the newest source-candidate and repository-transport lineage independently from promoted authority. `../CURRENT_AUTHORITY.md` remains the promotion authority until an explicit promotion checkpoint changes it.

## Current repository candidates

| Component | Logical candidate | VC | Source SHA-256 | Checkpoint | Forge commit | Repository identity |
|---|---|---:|---|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | INT-FIX-060C | `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | `sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8.zip` |
| SERVER | CFv2.1.26 R13 | 96 | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | INT-FIX-060F | `474e1336ee65c8088ea8c6ca8a7ce5b329a540f5` | `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R13.transport.json` |

Metadata identities:

- CLIENT R8 metadata SHA-256: `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391`;
- SERVER R13 metadata SHA-256: `864c020c6e590d6db84b433e670e44eda633174167cccafa646aefe3f7223e52`.

The SERVER transport is `chunked-git-blobs-v2`; the lane-root `.transport.json` is the repository source identity. Nested chunks and metadata are evidence members, not independent source candidates.

## Active direct-successor progression

### CLIENT

| Candidate | VC | Source SHA-256 | Parent / relationship | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R6 | 129 | `09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136` | accepted baseline | real source/metadata resolver fixture PASS |
| CFv2.1.26 R7 | 130 | `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e` | direct successor of R6 | workflow `30722649056` compile failure |
| CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | direct successor of R7 | source verification PASS; owner-reported Android build success |

### SERVER

| Candidate | VC | Source SHA-256 | Parent / relationship | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R9 | 92 | `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f` | accepted baseline | verified source/metadata baseline |
| CFv2.1.26 R10 | 93 | `02434e16eb3985d20537570ab8025bb061c7ae04cb13a8d3197e2b27d2152665` | direct successor of R9 | workflow `30722649056` compile failure |
| CFv2.1.26 R11 | 94 | `7110f94c989128150ae3b8f5059bade4c8e24c455fe1ba34726369644061fa82` | direct successor of R10 | source verification PASS; owner-reported Android build success |
| CFv2.1.26 R12 | 95 | `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f` | direct successor of R11 | pinned tunnel source PASS; owner-reported device ANR in Tunnel Settings |
| CFv2.1.26 R13 | 96 | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | direct successor of R12 | source verification PASS; Android/device result not independently established here |

## Capability progression in the active line

- CLIENT R7 and SERVER R10 introduced proof-bound protocol-2 registration and generic message send/inbox/correlated reply behavior.
- SERVER R10 added durable idempotent persistence, fair serialized inference, native loopback MCP, and foreground-service-owned tunnel lifecycle.
- CLIENT R8 and SERVER R11 repaired the first Android/Kotlin compile failures without changing the approved protocol or authority boundaries.
- SERVER R12 packaged and pinned the exact approved `tunnel-client v0.0.10` ARM64 runtime.
- SERVER R13 repaired the Tunnel Settings ANR, added automatic Forge artifact/log capture, Core-page operational cards, and launch-time model-rack discovery/load probing.

Detailed component notes are maintained in:

- `../patch-notes/CLIENT_PATCH_NOTES.md`
- `../patch-notes/SERVER_PATCH_NOTES.md`

## Build and device evidence boundary

- The project owner reported successful Android builds for CLIENT R8 and SERVER R11 through the Forge pipeline. This documentation sync does not invent a run ID or artifact SHA that was not supplied.
- The project owner later reported that an installed SERVER R12 repeatedly became unresponsive when opening ChatGPT Tunnel Settings. That is direct defect evidence and motivated R13; it is not device acceptance or promotion.
- SERVER R13 repository upload is established by Forge commit `474e1336ee65c8088ea8c6ca8a7ce5b329a540f5`. No independently retrieved R13 Android build or device result is asserted at this stop.

## Package-internal patch-history debt

The exact current source bytes are immutable evidence and are not rewritten by documentation synchronization.

- CLIENT R8: `CHANGELOG.md` contains the R8 entry, but `ReleaseNotes.md` still opens at R1 and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` still identifies R4/VC127.
- SERVER R13: `CHANGELOG.md` contains the R13 entry, but `ReleaseNotes.md` still opens at R3 and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` still identifies R5/VC88.

These two exact SHAs are grandfathered only as explicit documentation-debt baselines. The next CLIENT or SERVER candidate must synchronize all package-internal and repository patch-history surfaces before its documentation audit can pass.

## Divergent historical lineage

Earlier repository documentation tracked INT-AI-060A source transports that are not direct parents of the current R8/R13 line:

| Component | Candidate | VC | Source SHA-256 | Forge commit |
|---|---|---:|---|---|
| CLIENT | CFv2.1.27 R1 | 125 | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` |
| SERVER | CFv2.1.25 R1 | 83 | `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` | `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` |

INT-FILE-059A separately packaged different bytes under the same external CLIENT CFv2.1.27 R1 / SERVER CFv2.1.25 R1 labels. Those identity collisions remain distinct by SHA-256 and checkpoint provenance and must never be treated as current-parent lineage.

## Patch-note accounting enforcement

`../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` is active. The `SWRLZ Patch Note Accounting` workflow audits every source or patch-documentation update. It is intentionally separate from Source Package Integrity and APK Router so documentation debt is visible without falsifying source integrity or build evidence.

## Evidence boundary

- Repository transport/checksum proves repository source identity, not Android compilation or APK success.
- Packaged static validation proves only the validation recorded by that checkpoint.
- Device screenshots/operator reports are working-state evidence only to the degree explicitly stated.
- Candidate lineage does not change promoted authority.
- Downloaded, built, installed, accepted, promoted, released and deployed are distinct states.
