# CLIENT Patch Notes

**Scope:** CLIENT source-candidate lineage and repository transport history.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, device acceptance, promotion, release, deployment, or installation unless separate evidence is named.

## Current Forge lineage

### CFv2.1.26 R8 — INT-FIX-060C — current repository candidate

- versionCode: `131`
- versionName: `2.1.26-client-node-messaging-compile-fix-r8`
- source SHA-256: `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912`
- metadata SHA-256: `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391`
- direct parent: `CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R7.zip`
- parent SHA-256: `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e`
- Forge transport commit: `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b`
- repository identity: `sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8.zip`

Changes:
- repairs AndroidX Security Crypto `1.0.0` compatibility by using the supported alias-based `MasterKeys` API;
- preserves encrypted app-private device proof, protocol-2 registration/heartbeat/disconnect, and generic message send/inbox/reply behavior;
- preserves offline-first, identity, trust, Truth Firewall, and CLIENT/SERVER authority separation.

Validation recorded by checkpoint evidence: focused compiler repair `10/10`, inherited static/migration `52/52`, plugin mock suite `10/10`, resolver/mapper `22/22` with zero skips, source manifest `705/705`, ZIP CRC PASS. The project owner later reported a successful Android build through Forge; no exact run ID/log archive is asserted by this documentation sync.

### CFv2.1.26 R7 — INT-MSG-060A — plugin/message integration candidate

- versionCode: `130`
- source SHA-256: `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e`
- metadata SHA-256: `8a1b1417cc4e3d4b76a777660c979307a8e255fca641064651079ad61cad3512`
- Forge transport commit: `388a1273d35cd484c6fdca60f895335865799295`

Changes:
- adds persistent Android Keystore-backed CLIENT device proof;
- adds proof-bound protocol-2 registration, heartbeat and disconnect behavior;
- adds generic message send, per-node inbox and correlated reply client behavior;
- keeps CLIENT as a request/control node and does not move SERVER inference or trust authority into CLIENT.

Workflow `30722649056` reached Kotlin compilation and exposed the security-crypto API mismatch later repaired by R8. R7 is therefore preserved as failed-build lineage, not silently rewritten.

### CFv2.1.26 R6 — accepted direct-parent baseline

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

Changes:
- mirrors the shared Truth Core boundary used by SERVER-facing reasoning requests;
- keeps truth/authority standards outside personality/profile controls;
- preserves profile use as expression shaping rather than fact authority;
- removes profile-owned reasoning/provider/context semantics from active runtime shaping while retaining compatibility where required.

This lineage is not the direct parent of current R8. It remains separate by exact SHA and checkpoint provenance.

### CFv2.1.27 R1 — INT-FILE-059A — identity collision history

- versionCode: `125`
- versionName: `2.1.27-file-lab-cartographer-candidate-r1`
- source SHA-256: `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`

This candidate reused the same external version/revision as INT-AI-060A for different source bytes. The two sources must never be conflated.

## Earlier preserved CLIENT milestones

### CFv2.1.26 R1 — INT-FORGE-054A-R2

- versionCode: `124`
- source SHA-256: `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`

Shared Forge conveyor parity, SAF lanes, Build Ledger, artifact/failure-log controls, Chat/Settings catch-up, and machine-readable patch/checkpoint lineage while preserving CLIENT-only Missions and legacy Dev Mode.

### CFv2.1.25 R1 — provider cleanup / Model Rack parity

Removes Gemini from active CLIENT planner/key/runtime/UI paths, hides dormant public GPT/OpenAI controls, and preserves local-first/provider-neutral routing.

### CFv2.1.24 R1 — Model Rack Transport V2

- versionCode: `122`
- source SHA-256: `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55`

Bounded chunked model/module transport with retries while preserving SERVER model authority.

### CFv2.1.23 R1 — INT-AI-041F-A-R8

CLIENT Model Rack controls and declarative `.swrlzmod` import foundation. Prompt/EQ behavior is live; LoRA remains fail-closed and later module types remain reserved for explicit checkpoints.

### CFv2.1.22 R1 — INT-UX-039Q

- versionCode: `120`
- source SHA-256: `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`
- Forge transport commit: `1d3fa542db0f700a1f35256be9317393d25bbc8c`

Update Ledger, Settings and Theme-identity progression with checksum/candidate-manifest evidence. Android compilation remained pending in that checkpoint.

---

## CLIENT-specific preservation rule

Shared SERVER/CLIENT Forge, Chat and Settings foundations should remain behaviorally compatible where the capability is shared. CLIENT-only Missions, legacy Dev Mode, and legitimate CLIENT controls remain CLIENT-specific. SERVER-only inference/model/evidence authority must not be cloned into CLIENT merely for visual parity.

## Package-internal documentation debt

The immutable R8 source ZIP contains a current `CHANGELOG.md`, but its `ReleaseNotes.md` still opens at the older R1 lineage and its `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` still identifies R4/VC127. Those exact R8 bytes are preserved; this repository note does not rewrite the source ZIP. R8 is grandfathered only as an explicitly recorded documentation-debt baseline. The next CLIENT candidate must synchronize every internal patch-history surface before it is documentation-complete.

## Mandatory accounting rule

Every later CLIENT candidate must update the package's `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file and `../reference/CURRENT_CANDIDATE_LINEAGE.md`. The separate Patch Note Accounting workflow audits this rule on every source or documentation update. See `../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`.
