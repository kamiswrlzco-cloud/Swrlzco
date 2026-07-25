> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

# Server Implementation Analysis

Summary:

- Provided artifact: `SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` packaged inside `SERVER_CFv2.0.49_SWRLZ_debug_APK.zip` and extracted to `/workspaces/Swrlzco/_server_extract`.
- Provenance: `BUILD_PROVENANCE_REPORT.md` inside the package documents the build, source commit (`2b9f4b3fe9a08f5984282531651ec83d894e8db1`), selected source SHA-256, and final APK SHA-256.
- Source availability: The workspace server package (`SERVER_CFv2.0.49_SWRLZ_debug_APK.zip`) contains only the APK and provenance files. Authoritative server source was extracted from `.reference/swrlz-source/SOURCES/SERVER/SERVER_CFv2.0.49_SWRLZ.zip` to `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ`, where server source files now exist under `app/src/main/java/sh/swurlz/nodehost`.

Observed server evidence:

- Final APK: `/workspaces/Swrlzco/_server_extract/SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` (SHA-256: `aa2b0e9885afd509c4fec671bb0b3bd7c5d4ce059d26be83a1bbd563e54e6dfc` per provenance).
- Build provenance: `/workspaces/Swrlzco/_server_extract/BUILD_PROVENANCE_REPORT.md` — includes project root and workflow run details.
- SOURCE_RESOLUTION.json: points to canonical source zip and source SHA recorded during build.

Extracted server implementation (from `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ`):
- **Protocol contracts**: `sh.swrlz.nodehost.protocol.CommunicationEnvelopeV1` (Line 3+) — defines message routing and status tracking
- **Mission targets**: `sh.swrlz.nodehost.protocol.MissionTargetContractV1` (Line 3+) — semantic node targeting contract
- **Security**: `sh.swrlz.nodehost.security.PairedLanAuthorizer` — LAN authorization with pairing tokens
- **Runtime**: `sh.swrlz.nodehost.service.NodeHostService` (Line 30) — main service
- **Application**: `sh.swrlz.nodehost.NodeHostApplication` — app lifecycle

Key enums/routes (from CommunicationEnvelopeV1):
- `CommunicationRequestType { CHAT, MISSION, COMMAND, TOOL, APPROVAL, PROVIDER }`
- `CommunicationRoute { LOCAL, ONLINE, HYBRID, FALLBACK }`
- `CommunicationStatus { CREATED, RECEIVED, COMPLETED, REJECTED, FAILED }`
- `ConversationRouteDecision` (sealed interface) — routes incoming messages to missions or chat

Implications & next steps:

- Classification: Many server-side WordMesh components (Swurver orchestration, persistent graph storage, synchronization engine) are described in the WordMesh manual but cannot be labelled IMPLEMENTED without server source or decompiled analysis. Current classification: DOCUMENTED (by provenance) / UNKNOWN for implementation details.
- For deeper server analysis, obtain the server source zip referenced in `SOURCE_RESOLUTION.json` (`SOURCES/SERVER/SERVER_CFv2.0.49_SWRLZ.zip`) or request access to the repository commit `2b9f4b3fe9a0...` for source inspection.
- Alternatively, static analysis of the APK (decompilation) can reveal implementation details but may be partial and limited by obfuscation.
