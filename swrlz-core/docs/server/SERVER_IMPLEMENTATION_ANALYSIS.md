> **Authority note:** current promoted SERVER source authority remains SERVER CFv2.1.0 in `../CURRENT_AUTHORITY.md`. SERVER CFv2.1.9 R1-R6 are later source-candidate/evidence lineage and must not be treated as promoted authority without a separate promotion checkpoint.

# Server Implementation Analysis

## Current candidate evidence — 2026-07-29

Repository transport lineage now contains SERVER CFv2.1.9 SWRLIE candidates R1-R6:

| Rev | VC | Source SHA-256 | Main source-candidate change |
|---|---:|---|---|
| R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | model-independent local SWRLIE inference/no-model foundation, llama.cpp boundary, exact external Q4_0 bootstrap target, manual private Model Vault |
| R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | first-class SERVER Chat, Provider Mesh/SWRLIE advisory route, Command Center insertion, nested Settings IA/Back hierarchy |
| R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | local startup model recovery/load, adaptive/copyable Chat, double-Enter send, response follow/LATEST, horseshoe Update Ledger, tone-never-implies-approval guard |
| R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | multi-GGUF staging/probing/safe switching, adaptive context/inference controls, prompt-budget guard, code-native bounded Swurlzara compiler |
| R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | local SWRLZ self-knowledge resolver, shared Update Ledger retrieval, live model/runtime/context grounding, explicit USER/SWRLZ/SWRLIE/Swurlzara role map |
| R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | Chat machine/status stack with tappable status portals over existing authoritative SERVER/model/node/network/health state |

R6 repository Forge commit: `cb073ca4c008109aec9da4ad6f111657d31bc421`.

See `../checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md`, `../checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md`, `../architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md`, and `../architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md`.

### Current evidence boundary

The repository Forge uploads establish exact candidate source transport/checksum identities. R1/R2 uploads also include candidate-manifest evidence. R3-R6 repository transport commits do not contain their separately packaged candidate manifests.

Project-owner/operator evidence separately reports a successful R5 Android build. A later user-supplied device screenshot shows SERVER CFv2.1.9 VC64 and the current Chat/Command Center surface. That screenshot is device-visible working-state evidence for VC64, but it does not by itself establish exact R6 source-SHA → CI workflow → APK provenance or promotion.

Do not infer promotion, release, deployment, or installation authority from source transport or operator/device working-state evidence.

The R1-R6 candidate architecture preserves the rule that SWRLZ owns intrinsic Truth Firewall behavior, approvals, command/tool routing, node/file/mission/Forge authority, provenance, and execution policy. SWRLIE remains advisory reasoning. The selected LLM is a replaceable reasoning engine, and Swurlzara is a replaceable expression/profile lens rather than the SWRLZ primary identity.

### Current Chat UX follow-up

The current VC64 Chat surface still has a large status/Command Center footprint. A later consolidated proposal, `INT-CHAT-041G`, would compact status, move commands behind a dragon-triggered vertical popup, and expose real operational Response Processing stages without fake percentage completion or private chain-of-thought disclosure. That source implementation is not claimed by this documentation update.

## Historical implementation analysis from Documentation Rebuild v2

The material below records older SERVER evidence and remains useful for lineage. It is not a current-version description.

### Summary

- Provided artifact: `SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` packaged inside `SERVER_CFv2.0.49_SWRLZ_debug_APK.zip` and extracted to `/workspaces/Swrlzco/_server_extract`.
- Provenance: `BUILD_PROVENANCE_REPORT.md` inside the package documents the build, source commit (`2b9f4b3fe9a08f5984282531651ec83d894e8db1`), selected source SHA-256, and final APK SHA-256.
- Source availability: The workspace server package (`SERVER_CFv2.0.49_SWRLZ_debug_APK.zip`) contains only the APK and provenance files. Historical server source was extracted from `.reference/swrlz-source/SOURCES/SERVER/SERVER_CFv2.0.49_SWRLZ.zip` to `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ`, where server source files exist under `app/src/main/java/sh/swurlz/nodehost`.

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
