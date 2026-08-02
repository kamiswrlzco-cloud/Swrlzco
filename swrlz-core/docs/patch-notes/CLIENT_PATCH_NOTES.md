# CLIENT Patch Notes

**Scope:** CLIENT source-candidate lineage and repository transport history.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, device acceptance, promotion, release, deployment, or installation unless separate evidence is named.

## Current repository candidate — 2026-08-02

### CFv2.1.26 R8 — INT-FIX-060C

- canonical candidate: `CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8`
- versionCode: `131`
- versionName: `2.1.26-client-node-messaging-compile-fix-r8`
- source SHA-256: `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912`
- metadata SHA-256: `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391`
- direct parent: `CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R7.zip`
- parent SHA-256: `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e`
- Forge transport commit: `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b`
- repository identity: `sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8.zip`
- build evidence: project owner reported successful Android build through Forge
- promotion: not promoted

Changes:

- repairs AndroidX Security Crypto `1.0.0` compatibility through the supported alias-based `MasterKeys` API;
- preserves encrypted app-private device proof, protocol-2 registration/heartbeat/disconnect, and generic message send/inbox/reply behavior;
- preserves CLIENT as the local Android/control authority while SERVER remains heavyweight reasoning/model/network authority;
- preserves offline-first behavior, identity, trust, Truth Firewall, and CLIENT/SERVER authority separation.

Validation recorded by checkpoint evidence: focused compiler repair `10/10`, inherited static/migration `52/52`, plugin mock suite `10/10`, repaired resolver/mapper `22/22` with zero skips, source manifest `705/705`, ZIP CRC PASS.

## 2026-08-02 synchronization note

INT-STABILITY-063A changes SERVER model-startup/background-memory behavior only. CLIENT R8 remains the current repository CLIENT candidate byte-exact. No CLIENT source, metadata, version code, runtime behavior, or promoted authority changed in this synchronization.

The current SERVER repository candidate is R21/VC104 and the prepared SERVER stability successor is R23/VC106. Those SERVER updates do not transfer SERVER-only inference/model lifecycle or control-plane authority into CLIENT.

## Active direct-successor progression

| Candidate | VC | Checkpoint | Source SHA-256 | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R6 | 129 | INT-FORGE-064G | `09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136` | verified source/metadata baseline; repaired resolver fixture PASS |
| CFv2.1.26 R7 | 130 | INT-MSG-060A | `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e` | workflow reached Kotlin and exposed security-crypto API mismatch |
| CFv2.1.26 R8 | 131 | INT-FIX-060C | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | current repository candidate; owner-reported Android build success |

### R7 — plugin/message integration

- added persistent Android Keystore-backed CLIENT device proof;
- added proof-bound protocol-2 registration, heartbeat, and disconnect;
- added generic message send, per-node inbox, and correlated reply behavior;
- retained CLIENT as request/control node and did not move SERVER inference or trust authority into CLIENT.

R7 remains failed-build lineage rather than being silently rewritten.

### R6 — accepted direct-parent baseline

- versionCode: `129`
- source SHA-256: `09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136`
- metadata SHA-256: `39021fb0efc77de30369417655326f695d276029873a78c3d3d3326982733eb6`

R6 is the verified direct baseline used by INT-MSG-060A. Its real source/metadata fixture passes the repaired CI resolver contract. This row does not claim promotion or installation.

## Divergent historical lineage retained by SHA

### CFv2.1.27 R1 — INT-AI-060A

- versionCode: `125`
- versionName: `2.1.27-truth-reasoning-expression-separation-candidate-r1`
- source SHA-256: `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`
- Forge transport commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`

This lineage mirrors shared Truth Core boundaries for SERVER-facing reasoning requests while keeping profile use as expression shaping rather than fact authority. It is not the direct parent of current R8.

### CFv2.1.27 R1 — INT-FILE-059A identity collision

- versionCode: `125`
- source SHA-256: `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`

This candidate reused the same external version/revision as INT-AI-060A for different source bytes. The two sources remain distinct by exact SHA and checkpoint provenance.

## Earlier preserved CLIENT milestones

- CFv2.1.26 R1 / VC124 / SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` — shared Forge conveyor parity, SAF lanes, Build Ledger, artifact/failure-log controls, Chat/Settings catch-up, and machine-readable lineage.
- CFv2.1.25 R1 — removed Gemini from active CLIENT planner/key/runtime/UI paths, hid dormant public provider controls, and retained local-first/provider-neutral routing.
- CFv2.1.24 R1 / VC122 / SHA `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55` — Model Rack Transport V2.
- CFv2.1.23 R1 — CLIENT Model Rack controls and declarative `.swrlzmod` import foundation; prompt/EQ behavior live while LoRA remained fail-closed.
- CFv2.1.22 R1 / VC120 / SHA `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5` — Update Ledger, Settings, and theme-identity progression.

## CLIENT-specific preservation rule

Shared SERVER/CLIENT Forge, Chat, and Settings foundations should remain behaviorally compatible where the capability is shared. CLIENT-only Missions, legacy Dev Mode, and legitimate CLIENT controls remain CLIENT-specific. SERVER-only inference/model/evidence authority must not be cloned into CLIENT merely for visual parity.

## Package-internal documentation debt

The immutable R8 source ZIP contains a current `CHANGELOG.md`, but its `ReleaseNotes.md` and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` reflect earlier package-local history. R8 remains explicitly grandfathered by exact SHA under the patch-accounting contract; this repository update does not rewrite the immutable source ZIP.

## Mandatory accounting rule

Every later CLIENT candidate must update package-internal `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file, `../reference/CURRENT_CANDIDATE_LINEAGE.md`, and the non-promoted candidate pointer in `../CURRENT_AUTHORITY.md`. Patch Note Accounting remains separate from source integrity and Android builds.
