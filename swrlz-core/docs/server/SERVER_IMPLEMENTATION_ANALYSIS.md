> **Authority note:** current promoted SERVER source authority remains SERVER CFv2.1.0 in `../CURRENT_AUTHORITY.md`. Later SERVER candidates are source-candidate/evidence lineage and must not be treated as promoted authority without a separate promotion checkpoint.

# Server Implementation Analysis

## Current candidate evidence — 2026-08-04

Current non-promoted repository transport is INT-FIX-075A SERVER CFv2.1.27 R2:

- versionCode: `130`;
- versionName: `2.1.27-swrlz-llm-studio-compile-repair-r2`;
- source SHA-256: `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`;
- metadata ZIP SHA-256: `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`;
- repository transport: `sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2.transport.json`;
- direct parent: SERVER CFv2.1.27 R1 / SHA `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`.

R1 introduced the first-party §wyrlz LLM contract/runtime, atomic training store, role-filtered product knowledge, teaching/evaluation paths, proof-bound CLIENT context/chat integration, and dedicated SERVER LLM Studio. R1 transport commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` and APK Router run `30950003262` prove exact source selection and package verification followed by a Kotlin compile failure at `ServerOperationsScreen.kt:16:43`.

R2 removes the invalid explicit Compose weight import, retains both contextual weight calls, and makes the established compiler-regression precheck mandatory in the paired verifier. It preserves the paired INT-AI-074A CLIENT source without publishing or changing the repository CLIENT lane, plus LLM behavior/contracts, Room schema 16, proof-bound admin access, identity, trust, Truth Firewall, offline-first behavior, and compatibility identifiers.

R2 has source/static/package evidence only. The configured publication push may start an exact-SHA Android rebuild automatically, but no R2 compile/APK/device result is claimed until the resulting run is observed.

### Preserved 2026-07-31 candidate snapshot

The preceding maintained repository snapshot identified INT-AI-060A SERVER CFv2.1.25 R1:

- versionCode: `83`;
- versionName: `2.1.25-truth-reasoning-expression-separation-candidate-r1`;
- source SHA-256: `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`;
- repository Forge commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`;
- repository transport: `sources/server/SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1.transport.json`.

INT-AI-060A separated non-profile Truth Core invariants, reasoning/output-budget controls, and expression/profile shaping. Truthfulness, user sovereignty, speaker grounding, authority boundaries, evidence precedence, epistemic skepticism, uncertainty honesty, and action-result honesty remain SWRLZ standards rather than profile flavor. The selected LLM remains replaceable reasoning equipment; Swurlzara remains an expression/profile lens.

Packaged evidence records SERVER static `56/56` PASS, compiler-regression PASS, standalone `SwrlzTruthCoreV1` Kotlin compilation PASS, and package/manifest integrity. Gradle/Android compilation was not established in that packaging environment because the Gradle distribution could not be reached.

### External identity collision

INT-FILE-059A previously packaged different source bytes as SERVER CFv2.1.25 R1:

- versionName: `2.1.25-file-lab-cartographer-candidate-r1`;
- source SHA-256: `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`.

That candidate adds the shared Forge File Lab/Archive Cartographer foundation. It is distinct from the historical 060A repository transport despite the reused external version/revision identity. Later candidates advanced version/revision and remain separated by exact SHA and checkpoint lineage.

### Shared Forge parent — SERVER CFv2.1.24 R1 / INT-FORGE-054A-R2

- versionCode: `82`;
- versionName: `2.1.24-forge-conveyor-lineage-candidate-r1`;
- source SHA-256: `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`;
- Forge transport commit: `737a86f81238cc189d9ae84330e5c1fd7e5ceb01`.

This candidate establishes the shared Forge conveyor, source/manifest/SHA/lineage selection, SAF directory lanes, success/failure artifact routing, Build Ledger, and machine-readable patch/checkpoint lineage used as the parity parent for CLIENT.

### Performance / Chat progression

| Candidate | VC | Source SHA-256 | Main source-candidate change |
|---|---:|---|---|
| CFv2.1.23 R1 / INT-PERF-052A | 81 | `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6` | bounded short-casual fast path with USER perspective protection and normal-route fallback |
| CFv2.1.22 R1 / INT-CHAT-051A | 80 | `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d` | compact Chat/status orb, model switching/recovery and asset restore foundation |
| CFv2.1.21 R1 / INT-PERF-050D | 79 | `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791` | authoritative narrow STATUS fast path |
| CFv2.1.20 R1 / INT-PERF-050B | 78 | `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915` | pure greeting fast path |
| CFv2.1.19 R2 / INT-CHAT-045C-R2 | 77 | `b15916669dd6b0ca601c86093092ed2b76a22c45823e773f4f5fa29e0c9f0fa9` | persisted asset scanning, model/EQ selectors, built-in/LAB EQs and per-response/export evidence |
| CFv2.1.18 R1 / INT-CHAT-045B | 75 | exact SHA retained in checkpoint package | smart landing/follow, feedback/ratings/comments, relational evidence and socket-panel inspector |
| CFv2.1.17 R1 / INT-CHAT-045A | 74 | `e3881840dc5134c9a88052b03a8959c9d9e70bf0d4447a87490de4bc0b21aaf3` | Room thread/message persistence, history metadata and persisted model/module asset directories |

Detailed per-update notes are maintained in `../patch-notes/SERVER_PATCH_NOTES.md`; current cross-component lineage is in `../reference/CURRENT_CANDIDATE_LINEAGE.md`.

### Historical 041H baseline

Repository transport previously established SERVER CFv2.1.9 SWRLIE candidates R1-R6:

| Rev | VC | Source SHA-256 | Main source-candidate change |
|---|---:|---|---|
| R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | model-independent local SWRLIE inference/no-model foundation, llama.cpp boundary, exact external Q4_0 bootstrap target, manual private Model Vault |
| R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | first-class SERVER Chat, Provider Mesh/SWRLIE advisory route, Command Center insertion, nested Settings IA/Back hierarchy |
| R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | local startup model recovery/load, adaptive/copyable Chat, response follow/LATEST, Update Ledger, approval-tone guard |
| R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | multi-GGUF staging/probing/safe switching, adaptive inference, prompt-budget guard, bounded Swurlzara compiler |
| R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | local SWRLZ self-knowledge resolver, shared Update Ledger retrieval, model/runtime grounding and explicit role map |
| R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | Chat machine/status stack with tappable portals over authoritative SERVER/model/node/network/health state |

R6 repository Forge commit: `cb073ca4c008109aec9da4ad6f111657d31bc421`.

### Current evidence boundary

Repository transport/checksum establishes candidate source identity, not Android compilation, APK build, device behavior, promotion, release, deployment or installation. Project-owner/operator/device evidence remains separate and must not be silently converted into exact source-SHA → CI → APK provenance.

SWRLZ owns intrinsic Truth Firewall behavior, approvals, command/tool routing, node/file/mission/Forge authority, provenance and execution policy. SWRLIE/LLM reasoning remains advisory; expression/profile shaping does not own factual truth.

## Historical implementation analysis from Documentation Rebuild v2

The material below records older SERVER evidence and remains useful for lineage. It is not a current-version description.

### Summary

- Provided artifact: `SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` packaged inside `SERVER_CFv2.0.49_SWRLZ_debug_APK.zip` and extracted to `/workspaces/Swrlzco/_server_extract`.
- Provenance: `BUILD_PROVENANCE_REPORT.md` inside the package documents the build, source commit (`2b9f4b3fe9a08f5984282531651ec83d894e8db1`), selected source SHA-256, and final APK SHA-256.
- Source availability: the historical server source was extracted from `.reference/swrlz-source/SOURCES/SERVER/SERVER_CFv2.0.49_SWRLZ.zip` to `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ`, where server source files exist under `app/src/main/java/sh/swurlz/nodehost`.

### Observed historical server evidence

- Final APK: `/workspaces/Swrlzco/_server_extract/SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` (SHA-256: `aa2b0e9885afd509c4fec671bb0b3bd7c5d4ce059d26be83a1bbd563e54e6dfc` per provenance).
- Build provenance: `/workspaces/Swrlzco/_server_extract/BUILD_PROVENANCE_REPORT.md` — includes project root and workflow run details.
- SOURCE_RESOLUTION.json: points to canonical source zip and source SHA recorded during build.

### Extracted historical server implementation

From `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ`:

- **Protocol contracts**: `sh.swrlz.nodehost.protocol.CommunicationEnvelopeV1` — defines message routing and status tracking.
- **Mission targets**: `sh.swrlz.nodehost.protocol.MissionTargetContractV1` — semantic node targeting contract.
- **Security**: `sh.swrlz.nodehost.security.PairedLanAuthorizer` — LAN authorization with pairing tokens.
- **Runtime**: `sh.swrlz.nodehost.service.NodeHostService` — main service.
- **Application**: `sh.swrlz.nodehost.NodeHostApplication` — app lifecycle.

Historical `CommunicationEnvelopeV1` evidence includes:

- `CommunicationRequestType { CHAT, MISSION, COMMAND, TOOL, APPROVAL, PROVIDER }`
- `CommunicationRoute { LOCAL, ONLINE, HYBRID, FALLBACK }`
- `CommunicationStatus { CREATED, RECEIVED, COMPLETED, REJECTED, FAILED }`
- `ConversationRouteDecision` sealed routing structure.

### Historical implications

Many server-side WordMesh components were described in the WordMesh manual but could not be labelled IMPLEMENTED from the old v2.0.49 evidence alone. That historical gap does not erase later source-candidate evidence, but each newer feature still requires its own evidence class rather than being backfilled from architecture documents.
