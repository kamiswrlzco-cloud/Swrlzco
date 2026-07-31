> **Authority note:** current promoted SERVER source authority remains SERVER CFv2.1.0 in `../CURRENT_AUTHORITY.md`. Later SERVER packages described below are source-candidate/evidence lineage and must not be treated as promoted authority without a separate promotion checkpoint.

# Server Implementation Analysis

## Current candidate / transport evidence — 2026-07-31

### SERVER CFv2.1.24 R1 — INT-FORGE-054A-R2

- versionCode: `82`;
- versionName: `2.1.24-forge-conveyor-lineage-candidate-r1`;
- source SHA-256: `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`;
- parent: SERVER CFv2.1.23 R1, SHA `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6`.

This source-only checkpoint adds the shared Forge build-conveyor/lineage baseline: CLIENT/SERVER/BOTH/ASK/FILES targeting, authoritative newest-source discovery using component/version/manifest/SHA/lineage, configurable SAF project/source/artifact/log/model/mod/evidence lanes, user-initiated verify/upload/build/watch flow, persistent Build Ledger provenance, and default-on successful-artifact / failed-workflow-log download policy.

SERVER keeps its broader runtime/inference/model/evidence responsibilities. Shared Forge behavior is mirrored to CLIENT without collapsing role boundaries.

No APK build, installation, promotion, release, or deployment is inferred from this source-only checkpoint.

### Latest repository transport — SERVER CFv2.1.25 R1-1

Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` added repository transport identity `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1` as verified `chunked-git-blobs-v1` transport:

- declared whole-source SHA-256: `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`;
- reconstructed size: 40,710,681 bytes;
- chunks: 10;
- checksum evidence: present under the transport evidence directory;
- separately packaged candidate manifest in this transaction: absent.

This establishes repository transport identity only. The transport record does not provide enough evidence to infer the candidate's internal checkpoint changes, versionCode, Android compilation, APK result, device behavior, promotion, release, deployment, or installation.

### Recent performance / Chat candidate sequence

| Candidate | VC | Source SHA-256 | Main bounded change |
|---|---:|---|---|
| CFv2.1.20 R1 | 78 | `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915` | `INT-PERF-050B` pure-greeting fast path |
| CFv2.1.21 R1 | 79 | `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791` | `INT-PERF-050D` narrow authoritative status fast path |
| CFv2.1.22 R1 | 80 | `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d` | `INT-CHAT-051A` compact Chat control/status orb, direct model selection/recovery, persisted asset discovery |
| CFv2.1.23 R1 | 81 | `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6` | `INT-PERF-052A` conservative short-casual fast path with USER/SWRLZ perspective guard |
| CFv2.1.24 R1 | 82 | `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` | `INT-FORGE-054A-R2` shared Forge conveyor/lineage candidate |

Device evidence for 050B separately demonstrated a very fast greeting route relative to the earlier full-prompt path; that does not imply all normal reasoning requests share greeting-fast-path latency.

### Earlier SERVER CFv2.1.9 SWRLIE sequence

| Rev | VC | Source SHA-256 | Main source-candidate change |
|---|---:|---|---|
| R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | model-independent local SWRLIE inference/no-model foundation, llama.cpp boundary, exact external Q4_0 bootstrap target, manual private Model Vault |
| R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | first-class SERVER Chat, Provider Mesh/SWRLIE advisory route, Command Center insertion, nested Settings IA/Back hierarchy |
| R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | local startup model recovery/load, adaptive/copyable Chat, double-Enter send, response follow/LATEST, horseshoe Update Ledger, approval-tone guard |
| R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | multi-GGUF staging/probing/safe switching, adaptive context/inference controls, prompt-budget guard, code-native bounded Swurlzara compiler |
| R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | local SWRLZ self-knowledge resolver, shared Update Ledger retrieval, live model/runtime/context grounding, explicit USER/SWRLZ/SWRLIE/Swurlzara role map |
| R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | Chat machine/status stack with tappable status portals over existing authoritative SERVER/model/node/network/health state |

R6 repository Forge commit: `cb073ca4c008109aec9da4ad6f111657d31bc421`.

R1/R2 repository transport includes candidate-manifest evidence. R3-R6 repository transport commits contain source transport/checksum identity but not the separately packaged candidate manifests. Project-owner/operator evidence separately reports a successful R5 Android build; a later user-supplied screenshot showed SERVER CFv2.1.9 VC64 and the then-current Chat/Command Center surface. Neither fact silently promotes those candidates.

The candidate architecture preserves the rule that SWRLZ owns intrinsic Truth Firewall behavior, approvals, command/tool routing, node/file/mission/Forge authority, provenance, and execution policy. SWRLIE remains advisory reasoning. The selected LLM is a replaceable reasoning engine; Swurlzara is a replaceable expression/profile lens rather than the primary SWRLZ identity.

## CI / documentation synchronization

`INT-CI-DOC-060A` repairs Source Package Integrity selection so nested `.transport/.../evidence/*.sha256` files cannot be mistaken for lane-root source sidecars, and hardens APK Router lane-root/BOTH routing. The repair is staged on `checkpoint/int-ci-doc-060a-router-docs` until explicit merge approval.

Maintained SERVER patch history now lives at [`PATCH_NOTES.md`](PATCH_NOTES.md). Future accepted SERVER implementation checkpoints are documentation-incomplete until the affected SERVER patch-note entry is synchronized. Already packaged candidate ZIPs remain immutable; repository patch notes repair missing historical narrative without changing old bytes/SHA/lineage.

`INT-FILE-059A` is approved for a shared Forge File Lab + Archive Cartographer foundation, but no current SERVER package is claimed here to implement it until separate implementation/package evidence exists.

## Historical implementation analysis from Documentation Rebuild v2

The material below records older SERVER evidence and remains useful for lineage. It is not a current-version description.

### Summary

- Provided historical artifact: `SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` packaged inside `SERVER_CFv2.0.49_SWRLZ_debug_APK.zip`.
- Historical provenance report recorded source commit, selected source SHA-256, and final APK SHA-256.
- Historical server source existed under `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ`.

### Extracted historical server implementation

- **Protocol contracts**: `sh.swrlz.nodehost.protocol.CommunicationEnvelopeV1` — message routing and status tracking.
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
