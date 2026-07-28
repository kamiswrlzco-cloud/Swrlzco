> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is CLIENT CFv2.1.9 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

# Status Matrix

This file is the canonical status matrix for major SWRLZ systems. It is populated from source evidence and audit artifacts.

| System | Component | Status | Evidence | Location |
|---|---|---:|---|---|
| Client | Accessibility targeting and snapshotting | IMPLEMENTED | `SwurlzAccessibilityService.kt` captures node tree, synthetic IDs, semantic matching | [CLIENT source](CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt) |
| Client | Gesture/coordinate fallback | IMPLEMENTED | `tapPoint`, `scrollScreen` using `dispatchGesture` | [CLIENT source](CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt) |
| Client | Overlays & bubble UI | IMPLEMENTED | `OverlayService.kt`, `ClientBubbleController.kt`, `InteractiveBubbleDockService.kt` | [CLIENT source](CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/overlay) |
| Client | Mission runtime & execution | IMPLEMENTED | `MissionBus.kt`, `MissionRunnerService.kt`, mission reports under package | [CLIENT source](CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/data) |
| Client | LLM / Gemini integration | IMPLEMENTED | `GeminiClient.kt`, `GeminiMissionPlanner.kt` present | [CLIENT source](CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/ai) |
| Client | Networking & discovery | IMPLEMENTED | `CoreNodeAutoDiscovery.kt`, `GroupClientApi.kt`, `ClientPresenceRegistration.kt` | [CLIENT source](CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/net) |
| Client | OCR | UNKNOWN | No OCR library or code paths detected in client sources | N/A |
| Build | Direct ZIP build input | IMPLEMENTED | APK Router resolver/verifier accepts lane-root ZIP without checksum/manifest sidecars and computes SHA-256 internally | `swrlz-core/tools/ci/resolve_swrlz_source.py`; `verify_swrlz_package_pair.py` |
| Build | Strict optional sidecar evidence | IMPLEMENTED | Supplied checksum/manifest evidence is validated; contradiction fails closed; missing evidence does not block build eligibility | `swrlz-core/tools/ci/verify_swrlz_package_pair.py` |
| Build | Chunked source reconstruction | IMPLEMENTED | `chunked-git-blobs-v1` validates sequential chunks, per-chunk size/SHA, and reconstructed whole ZIP size/SHA in runner temporary storage | `.github/workflows/swrlz-apk-router.yml`; `swrlz-core/tools/ci/resolve_swrlz_source.py` |
| Build | Chunk/ZIP-only regression coverage | IMPLEMENTED | Resolver suite covers ZIP-only build, sidecar mismatch, exact reconstruction, corruption rejection, and push selection | `swrlz-core/tools/ci/test_resolve_swrlz_source.py` |
| Client candidate | Forge-side chunk transport | EXPERIMENTAL | CLIENT CFv2.1.20 R1 source/static evidence exists; Android build evidence remains pending | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` |
| Server | Binary APK artifact | DOCUMENTED | `SERVER_CFv2.0.49_SWRLZ_DEBUG.apk` in historical package | /workspaces/Swrlzco/_server_extract/SERVER_CFv2.0.49_SWRLZ_DEBUG.apk |
| Server | Source code availability | DOCUMENTED | Server Kotlin source from historical authoritative GitHub extract, `sh.swrlz.nodehost` package | .reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ/app/src/main/java |
| Server | LAN pairing & authorization | IMPLEMENTED | `PairedLanAuthorizer.kt`: SHA-256 token validation, subnet checking (IPv4/IPv6) | .reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ/.../security/PairedLanAuthorizer.kt |
| Server | Communication envelope | IMPLEMENTED | `CommunicationEnvelopeV1.kt`: enums (RequestType, Route, Status), message routing logic | .reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ/.../protocol/CommunicationEnvelopeV1.kt |
| Server | Mission targeting contract | IMPLEMENTED | `MissionTargetContractV1.kt`: semantic node addressing, snapshot correlation | .reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ/.../protocol/MissionTargetContractV1.kt |
| WordMesh | Master engineering manual present | DOCUMENTED | `SWRLZ_WordMesh_Master_Engineering_Manual_v6.0.docx` extracted to `_wordmesh_doc/` | /workspaces/Swrlzco/_wordmesh_doc/ |
| WordMesh | Complete protocol/data model documentation | HIGH PRIORITY GAP | Manual references protocol but system docs lack architecture diagrams, sequence flows, state machines | TODO: extract critical sections |

Repository BUILD status does not imply CLIENT/SERVER candidate promotion. Current source authority remains defined by `../CURRENT_AUTHORITY.md`.
