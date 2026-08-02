# SERVER Patch Notes

**Scope:** SERVER source-candidate lineage and repository transport history.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, device acceptance, promotion, release, deployment, or installation unless separate evidence is named.

## Current Forge lineage

### CFv2.1.26 R13 — INT-FIX-060F — current repository candidate

- versionCode: `96`
- versionName: `2.1.26-runtime-operations-anr-fix-r13`
- source SHA-256: `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693`
- metadata SHA-256: `864c020c6e590d6db84b433e670e44eda633174167cccafa646aefe3f7223e52`
- direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R12.zip`
- parent SHA-256: `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f`
- Forge transport commit: `474e1336ee65c8088ea8c6ca8a7ce5b329a540f5`
- repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R13.transport.json`

Changes:
- repairs the ChatGPT Bridge & Tunnel settings ANR by moving Keystore, encrypted preferences, filesystem, SHA-256, ELF, version and commit validation off the Compose main thread;
- replaces repeated byte-at-a-time binary scans with one cancellable buffered verification pass and cached CHECKING/READY/DEGRADED state;
- automatically captures successful Forge APK artifacts to the project `apk/` lane and failed workflow logs/artifacts/receipts to the project `logs/` lane, creating missing lanes and retaining retry truth;
- adds Core-page Tunnel, Forge/GitHub, connection and SWRLIE local-model status/shortcut cards;
- discovers and load-probes all enabled compatible local models at launch while retaining one selected resident model;
- preserves the exact pinned tunnel runtime, foreground service, loopback MCP, offline-first behavior, trust separation and Truth Firewall.

Validation recorded by checkpoint evidence: focused runtime operations `70/70`, inherited messaging `52/52`, inherited compile repair `10/10`, tunnel verifier and fair-queue harnesses PASS, parser screen zero syntax diagnostics, source manifest `817/817`, ZIP CRC PASS. At this synchronization stop, Forge repository transport is established; no independently retrieved R13 Android-build or device-runtime result is claimed.

### CFv2.1.26 R12 — INT-TUNNEL-060D — pinned tunnel-runtime candidate

- versionCode: `95`
- source SHA-256: `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f`
- metadata SHA-256: `7f24e835dcc49edc7bc9305145928848d40ed77664c0b2966ef15672fea541e3`
- Forge transport commit: `9f6769c1a6ad6b9f1b5011e87d41fce9208f602a`

Changes:
- packages the approved `tunnel-client v0.0.10` ARM64 runtime as `app/src/main/jniLibs/arm64-v8a/libswrlz_tunnel.so`;
- pins runtime SHA-256 `2e4c628f46624330ccb58d3511e33218db32bc2bcd68ac02a5fb46371686b508`, size, ELF64/AArch64 identity, version and upstream commit;
- forces native extraction and launches through the existing `NodeHostService` foreground/`START_STICKY` authority;
- uses environment-backed app-private configuration and bounded sanitized diagnostics;
- degrades tunnel capability without disabling NODE_HOST, LAN, native MCP, Chat or local inference.

The project owner subsequently reached the R12 Tunnel Settings screen on-device and reported repeated hard ANR/crash behavior. That is defect evidence, not device acceptance, and directly motivated R13.

### CFv2.1.26 R11 — INT-FIX-060C — compile-repair candidate

- versionCode: `94`
- source SHA-256: `7110f94c989128150ae3b8f5059bade4c8e24c455fe1ba34726369644061fa82`
- metadata SHA-256: `13b5187b817e4c9b628a48e6827d9c11ce9bbc55bf85c11e4af15312ac9f3ed2`
- Forge transport commit: `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b`

Changes:
- repairs non-Unit reply polling inference;
- uses the validated non-null destination identity for inbox persistence;
- repairs cross-module nullable response narrowing;
- corrects the Compose `rememberSaveable` import.

The project owner reported successful Android builds for the R8/R11 pair through Forge. No exact workflow log/run ID is reasserted here.

### CFv2.1.26 R10 — INT-MSG-060A — plugin/message integration candidate

- versionCode: `93`
- source SHA-256: `02434e16eb3985d20537570ab8025bb061c7ae04cb13a8d3197e2b27d2152665`
- metadata SHA-256: `a58aab3e81e682520590ab7665cea05343199a3909278ed23d690b7576f1a72b`
- Forge transport commit: `388a1273d35cd484c6fdca60f895335865799295`

Changes:
- adds authenticated protocol-2 generic message send, per-node inbox and append-only correlated reply routes;
- adds durable idempotent Room persistence, authorized cursors, serialized inference and per-node round-robin fairness;
- adds native `client-swurlz` MCP on `127.0.0.1:8788` with bounded authentication/origin/request controls;
- places MCP, message worker and tunnel lifecycle beneath the existing `NodeHostService` foreground authority;
- adds tunnel settings/configuration while preserving truthful DEGRADED behavior when runtime or credentials are absent.

Workflow `30722649056` reached Kotlin compilation and exposed the four SERVER compile defects later repaired by R11. R10 remains failed-build lineage.

### CFv2.1.26 R9 — accepted direct-parent baseline

- versionCode: `92`
- source SHA-256: `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f`
- metadata SHA-256: `a43e469ff292009deea70cf1f77b9134136b88bd5e77b7c679f8d9af4542f94f`

R9 is the verified direct SERVER baseline used by INT-MSG-060A. This row does not claim promotion or installation.

## Earlier/divergent history retained by SHA

### CFv2.1.25 R1 — INT-AI-060A

- versionCode: `83`
- versionName: `2.1.25-truth-reasoning-expression-separation-candidate-r1`
- source SHA-256: `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`
- Forge transport commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`

Truth Core / reasoning-control / expression-profile separation. This lineage is historical and is not the direct parent of current R13.

### CFv2.1.25 R1 — INT-FILE-059A — identity collision history

- versionCode: `83`
- versionName: `2.1.25-file-lab-cartographer-candidate-r1`
- source SHA-256: `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`

This candidate reused the same external version/revision as INT-AI-060A for different source bytes. The two sources must never be conflated.

## Earlier preserved SERVER milestones

### CFv2.1.24 R1 — INT-FORGE-054A-R2

- versionCode: `82`
- source SHA-256: `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`
- Forge transport commit: `737a86f81238cc189d9ae84330e5c1fd7e5ceb01`

Shared Forge build conveyor, source/manifest/SHA selection, SAF lanes, Build Ledger, success-artifact/failure-log controls and machine-readable lineage.

### CFv2.1.23 R1 — INT-PERF-052A

- versionCode: `81`
- source SHA-256: `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6`
- Forge transport commit: `faf6a249d08c976354c9437eb7073ea0fbe98fb0`

Bounded casual-short fast path with USER perspective preservation and normal-route fallback.

### CFv2.1.22 R1 — INT-CHAT-051A

- versionCode: `80`
- source SHA-256: `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d`
- Forge transport commit: `7b508ba7f218b94eaaaf5514484f58fd48761326`

Compact Chat/status control orb and strengthened persisted GGUF/SWRLZMOD discovery.

### CFv2.1.21 R1 — INT-PERF-050D

- versionCode: `79`
- source SHA-256: `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791`

Narrow authoritative status fast path.

### CFv2.1.20 R1 — INT-PERF-050B

- versionCode: `78`
- source SHA-256: `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915`
- Forge transport commit: `fca443bbc8555d7de236d39c0034557fcd1e5b93`

Greeting-only deterministic fast path with normal-route fallback.

### CFv2.1.19 R2 — INT-CHAT-045C-R2

- versionCode: `77`
- source SHA-256: `b15916669dd6b0ca601c86093092ed2b76a22c45823e773f4f5fa29e0c9f0fa9`

Persisted GGUF/SWRLZMOD scanning, Chat model/EQ controls, evidence records and SAF export.

### CFv2.1.18 R1 — INT-CHAT-045B

Smart Chat landing/follow behavior, reactions/ratings, relational Room evidence and per-thread export foundation.

### CFv2.1.17 R1 — INT-CHAT-045A

- versionCode: `74`
- source SHA-256: `e3881840dc5134c9a88052b03a8959c9d9e70bf0d4447a87490de4bc0b21aaf3`

Room thread/message persistence and model/module directory foundation.

---

## Package-internal documentation debt

The immutable R13 source ZIP contains a current `CHANGELOG.md`, but its `ReleaseNotes.md` still opens at the older R3 lineage and its `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` still identifies R5/VC88. Those exact R13 bytes are preserved; this repository note does not rewrite the source ZIP. R13 is grandfathered only as an explicitly recorded documentation-debt baseline. The next SERVER candidate must synchronize every internal patch-history surface before it is documentation-complete.

## Mandatory accounting rule

Every later SERVER candidate must update the package's `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file and `../reference/CURRENT_CANDIDATE_LINEAGE.md`. The separate Patch Note Accounting workflow audits this rule on every source or documentation update. See `../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`.
