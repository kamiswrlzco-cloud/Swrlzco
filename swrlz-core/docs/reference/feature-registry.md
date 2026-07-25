> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is CLIENT CFv2.1.2 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

# Feature Registry (DRAFT)

This registry catalogs major features, owners, implementation status, and source locations.

Columns:
- Feature
- Component
- Owner Plane
- Implementation Status
- Source Location (authoritative / extracted)
- Documentation
- Notes

Initial entries:

| Feature | Component | Owner Plane | Status | Source Location | Docs | Notes |
|---|---|---|---:|---|---|---|
| Accessibility snapshotting | Accessibility Service | SWURLZER | IMPLEMENTED | `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt` | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Uses semantic matching, resource-id and coordinate fallback |
| Mission orchestration | MissionRunnerService + MissionBus | SWURLZER | IMPLEMENTED | `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/MissionRunnerService.kt` / `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt` | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Event-driven mission lifecycle, persistent workers |
| LLM integration (Gemini) | GeminiClient / GeminiMissionPlanner | SWURLZER | IMPLEMENTED | `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt` | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Provider hooks present; model selection delegated to config |
| Overlay UI / Bubbles | OverlayService / ClientBubbleController | SWURLZER | IMPLEMENTED | `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt` | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Interactive dock, touch passthrough handling |

How to use:
- For each feature, add a link to the authoritative source path and the commit SHA.
- Mark status with one of the canonical values and add short evidence notes.
