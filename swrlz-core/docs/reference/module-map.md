> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is CLIENT CFv2.1.2 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

# Module Map (DRAFT)

This map connects authoritative source paths to architecture components and documentation.

Columns:
- Source Path
- Component
- Plane (SWURVER / SWURLZER / WORDMESH / SHARED / BUILD / TEST / LEGACY)
- Responsibility
- Status
- Related Documentation

Entries (initial):

| Source Path | Component | Plane | Responsibility | Status | Docs |
|---|---|---|---|---:|---|
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt` | Accessibility Service | SWURLZER | UI observation, node snapshotting, action execution | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt` | Mission Bus / Event Bus | SWURLZER | Mission event routing and local messaging | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/MissionRunnerService.kt` | Mission Runner | SWURLZER | Mission execution lifecycle and worker invocation | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt` | LLM Integration | SWURLZER | LLM provider client and mission planner integration | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt` | Overlay Service & UI Dock | SWURLZER | Persistent overlay, bubble UI hosting | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ` | Server source bundle | SWURVER | Server-side orchestration and APIs | IMPLEMENTED | `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` |
| `_wordmesh_doc/` | WordMesh manual & extracted XML | WORDMESH | Canonical architecture and runtime specification | DOCUMENTED | `docs/wordmesh/WORDMESH_IMPLEMENTATION_GAP_ANALYSIS.md` |

Notes:
- Update the `Source Path` to point to exact authoritative clone paths once files are extracted from the `.reference` archives.
- Status values: IMPLEMENTED, PARTIAL, PLANNED, UNKNOWN, DEPRECATED.
