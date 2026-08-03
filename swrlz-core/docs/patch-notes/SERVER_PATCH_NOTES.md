# SERVER Patch Notes

**Scope:** SERVER source-candidate lineage, repository transport history, and current prepared successors.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, installation, device acceptance, promotion, release, or deployment unless separate evidence is named.

## Current repository candidate — 2026-08-03

### CFv2.1.26 R27 — INT-STABILITY-068A

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R27`
- versionCode: `110`
- versionName: `2.1.26-tunnel-generation-lifecycle-r27`
- source SHA-256: `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1`
- metadata SHA-256: `10ace6898df22bb8ed53b99cf563edf8bec05cd66db6fc453bff1e17d497da6a`
- direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R26.zip`
- Forge transport commit: `1e48e2e4d6652fe9c9c0e1f25c32362b0051f677`
- repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R27.transport.json`
- Android build/device evidence: pending
- promotion: not promoted

Changes:

- assigns every isolated-tunnel attempt a unique generation and binding identity;
- prevents stale Binder callbacks, delayed unbinds, process-death callbacks, status events, and delayed evidence callbacks from affecting newer tunnel generations;
- requires confirmed STOP completion before restart and suppresses duplicate transition commands;
- moves tunnel START/STOP teardown work off the service main looper;
- coalesces tunnel status into one bounded IPC snapshot instead of multi-message diagnostic bursts;
- guards private tunnel-process memory callbacks from primary-process model and stability systems;
- preserves the pinned tunnel runtime, encrypted credentials, MCP, NODE_HOST, models, identity, trust, Truth Firewall, offline-first behavior, and process-isolation boundary.

Source-only verification recorded for R27: focused lifecycle verifier `41/41`, generation-policy harness PASS, targeted Kotlin compile PASS, compiler-regression precheck PASS, source manifest `985/985`, and source/metadata ZIP structure PASS. No Android build, installation, device acceptance, promotion, release, or deployment is asserted here.

## Recent direct-successor progression

| Candidate | VC | Checkpoint | Source SHA-256 | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R23 | 106 | INT-STABILITY-063A | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | startup/model stability source successor; Forge transported |
| CFv2.1.26 R24 | 107 | INT-STABILITY-065A | `20af0c617c5b8f96708fffc27d73ac6d81e473af4401aafcb170d0ec0057293f` | launch crash-loop breaker; Forge transported |
| CFv2.1.26 R25 | 108 | INT-STABILITY-066A | `5f195ae4c3e8f73cba974f81f8591f93c706fe546e0ed9b9af046df810602101` | isolated tunnel-process firewall; local source identity retained |
| CFv2.1.26 R26 | 109 | update-delivery protocol | `1088e51b8c559733b73a18abac7961bb51b14b58596725058f2a10b25e7f1b2c` | documentation/delivery protocol successor; Forge transported at `68a9f3b0d2cd9f8db04d5cd64995c82ade69810d` |
| CFv2.1.26 R27 | 110 | INT-STABILITY-068A | `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1` | current repository candidate; generation-safe tunnel lifecycle |

## Prior repository candidate — 2026-08-02

### CFv2.1.26 R21 — INT-FIX-060P

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R21`
- versionCode: `104`
- versionName: `2.1.26-nodehost-raw-loopback-route-proof-r21`
- source SHA-256: `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c`
- metadata SHA-256: `7f7f0e1baf8ff80837797aa132fd86587e31cc990d870796feb0cb28968e54f2`
- direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R20.zip`
- parent SHA-256: `b18aa2cbf9940a63e8c67ea98dc37f549bf95322301efba60ffa3fde271f8f28`
- Forge transport commit: `dbfeed2e8edd95d06bf7e6a775b3afd237a47989`
- repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R21.transport.json`
- Android build: succeeded through Forge/APK Router according to supplied workflow evidence
- promotion: not promoted

Changes:

- replaces the native MCP tool client's Android `HttpURLConnection` hop with bounded raw IPv4 HTTP fixed to `127.0.0.1:8787`;
- preserves GET/POST methods, query parameters, JSON payload semantics, device-proof headers, timeouts, status/error parsing, and NODE_HOST trust/approval/mission/Forge gates;
- treats an authenticated non-preflight MCP `tools/call` as direct ChatGPT-route evidence independently from downstream NODE_HOST success;
- preserves the Android-resolved fixed-destination control-plane egress bridge, end-to-end TLS, static-bearer/no-OAuth mode, encrypted credential retention, full redacted diagnostics, identity, Truth Firewall, and foreground-service authority.

Device/plugin evidence established that ChatGPT reached the native MCP tool implementation. The earlier downstream cleartext failure occurred inside the Android MCP-to-NODE_HOST hop and was the defect repaired by R21.

### Patch-accounting boundary for R21

The R21 Android build can succeed while Patch Note Accounting fails because the workflows are independent. R21's immutable package-internal `CHANGELOG.md` and `ReleaseNotes.md` did not contain the exact canonical candidate/checkpoint/VC token combination required by the live accounting verifier. Repository documentation has now been synchronized beyond R21. Those immutable package-internal bytes remain historical debt only.

## Preserved prepared-successor history

### CFv2.1.26 R22 — INT-DOC-060P-REPAIR

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R22`
- versionCode: `105`
- versionName: `2.1.26-patch-accounting-repair-r22`
- source SHA-256: `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52`
- metadata SHA-256: `2ffdcde47c3cad22258ace69932021ae06623905459279b3f0f0c76285d26681`
- direct parent: R21
- repository transport: none established at preparation time

R22 is a documentation-only direct successor that adds exact package-internal accounting identity. It does not change Kotlin, Java, XML, native runtime, MCP, NODE_HOST, tunnel, credential, trust, or protocol behavior.

### CFv2.1.26 R23 — INT-STABILITY-063A

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R23`
- versionCode: `106`
- versionName: `2.1.26-model-startup-stability-r23`
- source SHA-256: `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17`
- metadata SHA-256: `670211b8d50b7d53673ee3840c5432ab626027c9d7ee6cc3c8ed6ae6f3b95fb0`
- direct parent: R22
- Forge transport commit: `eda264d24c681dc663eab5b90da3da969efe2438`

R23 makes `NodeHostService` the sole automatic model-runtime startup owner, changes normal startup to discovery-only indexing, moves fleet-wide native probing behind **PROBE ALL ENABLED**, preloads only the selected model when `keepModelLoaded` is enabled and memory admission passes, serializes heavy model startup after tunnel startup settles, adds unclean-start safe mode, memory/trim unload protection, and a redacted SERVER Stability Ledger with capture. It preserves model bytes, MCP, NODE_HOST, tunnel, TLS, credentials, trust, Truth Firewall, identity, and protocol boundaries.

Source-only verification recorded for R23: focused stability `32/32`, pure Kotlin policy harness PASS, parser screen zero syntax-class diagnostics, compiler-regression precheck PASS, source manifest `928/928`, package verification PASS.

## Active direct-successor progression — historical R9 through R23

| Candidate | VC | Checkpoint | Source SHA-256 | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R9 | 92 | INT-FORGE-064G | `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f` | verified source/metadata baseline |
| CFv2.1.26 R10 | 93 | INT-MSG-060A | `02434e16eb3985d20537570ab8025bb061c7ae04cb13a8d3197e2b27d2152665` | workflow compile failure |
| CFv2.1.26 R11 | 94 | INT-FIX-060C | `7110f94c989128150ae3b8f5059bade4c8e24c455fe1ba34726369644061fa82` | source verification; owner-reported Android build success |
| CFv2.1.26 R12 | 95 | INT-TUNNEL-060D | `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f` | pinned tunnel runtime; device ANR evidence |
| CFv2.1.26 R13 | 96 | INT-FIX-060F | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | repository transport `474e1336`; runtime operations repair |
| CFv2.1.26 R14 | 97 | INT-FIX-060H | `d11bd43ec028f44aa374b218edc53237e5763e087a6278762448a5c4bef7cea0` | native MCP-before-tunnel/no-OAuth bridge |
| CFv2.1.26 R15 | 98 | INT-FIX-060J | `b69a264f225c6f03b840158f3b1896fe6e185364eb4f30e3d0bbadf6b3fc9638` | Termux-proven MCP compatibility port |
| CFv2.1.26 R16 | 99 | INT-FIX-060K | `8706ceccfba63a88128e1245f944fcdda1dcd4afc86546e693a9696ee1cbe8d7` | explicit IPv4 MCP binding |
| CFv2.1.26 R17 | 100 | INT-TUNNEL-DIAGNOSTICS-001E | `c45f5fd5aa8c5bac60061db7c9d5cee98517739f33206efda83a7b7598e952bf` | redacted tunnel ledger/capture; first compile failed |
| CFv2.1.26 R18 | 101 | INT-FIX-060L | `0bf66150022ba2f35943accfb55ee03f135b936c2e441c1e0fa6cb70696ae404` | Process PID compile repair |
| CFv2.1.26 R19 | 102 | INT-FIX-060M | `356f501da34946896829d82342068318d0327ce5bf6cdf96f8649a0703e52efb` | raw MCP preflight, credential retention, local tunnel READY proof |
| CFv2.1.26 R20 | 103 | INT-FIX-060N | `b18aa2cbf9940a63e8c67ea98dc37f549bf95322301efba60ffa3fde271f8f28` | Android-resolved control-plane egress/truthful readiness |
| CFv2.1.26 R21 | 104 | INT-FIX-060P | `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c` | prior repository candidate; build succeeded |
| CFv2.1.26 R22 | 105 | INT-DOC-060P-REPAIR | `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52` | documentation-only successor |
| CFv2.1.26 R23 | 106 | INT-STABILITY-063A | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | model-startup/background-stability successor |

## Pinned tunnel-runtime evidence

The packaged ARM64 tunnel-client remains pinned across the active tunnel lineage:

- SHA-256: `2e4c628f46624330ccb58d3511e33218db32bc2bcd68ac02a5fb46371686b508`
- size: `18,546,850` bytes
- runtime: tunnel-client `v0.0.10`, arm64-v8a

## Earlier/divergent history retained by SHA

### CFv2.1.25 R1 — INT-AI-060A

- versionCode: `83`
- versionName: `2.1.25-truth-reasoning-expression-separation-candidate-r1`
- source SHA-256: `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`
- Forge transport commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`

### CFv2.1.25 R1 — INT-FILE-059A identity collision

- source SHA-256: `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`

These candidates reused an external version/revision label for different bytes and remain distinct by exact SHA and checkpoint provenance.

## Earlier preserved SERVER milestones

- CFv2.1.24 R1 / VC82 / SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` — shared Forge conveyor and provenance foundation.
- CFv2.1.23 R1 / VC81 / SHA `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6` — bounded casual-short fast path.
- CFv2.1.22 R1 / VC80 / SHA `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d` — compact Chat/status and model discovery improvements.
- CFv2.1.21 R1 / VC79 / SHA `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791` — authoritative status fast path.
- CFv2.1.20 R1 / VC78 / SHA `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915` — greeting-only deterministic fast path.
- CFv2.1.19 R2 / VC77 / SHA `b15916669dd6b0ca601c86093092ed2b76a22c45823e773f4f5fa29e0c9f0fa9` — persisted model/module scanning and evidence controls.

## Mandatory accounting rule

Every later SERVER candidate must update package-internal `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file, `../reference/CURRENT_CANDIDATE_LINEAGE.md`, and the non-promoted candidate pointer in `../CURRENT_AUTHORITY.md`. The Patch Note Accounting workflow is independent from source integrity and Android builds; one gate can pass while another fails.
