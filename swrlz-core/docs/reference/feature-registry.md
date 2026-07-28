> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is CLIENT CFv2.1.9 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

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
| Precheck + Promotion Gate | Engineering validation pipeline | CLIENT + SERVER | PLANNED | Candidate/checkpoint workflow; not current source authority | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Verify parent, acceptance tests, disposable candidate, compile/repair loop, documentation gate, immutable candidate revisions, expected-SHA evidence matching |
| Adaptive conversation workspace | CLIENT Chat UI | CLIENT | EXPERIMENTAL | CFv2.1.19 candidate lineage; promotion pending | `docs/checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md` | Conversation-first layout, keyboard-aware chrome, compact provider mesh; candidate build evidence remains separate from repository authority |
| Persistent Forge transfers | Forge transfer subsystem | CLIENT + SERVER role-aware | PLANNED | INT-FORGE-039K | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Transfer owner independent of Compose lifecycle; shared progress state; pause/cancel/retry; ZIP companion SHA + manifest auto-pair settings |
| Chat-initiated Forge package discovery | Command Center + Local Artifact Resolver + Forge | CLIENT | PLANNED | INT-FORGE-039L | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Natural-language latest-valid CLIENT/SERVER/BOTH discovery, package triple verification, canonical destination preview, verified staging |
| Conversational local file organizer | Local Artifact Resolver + File Organization Planner/Executor | CLIENT | PLANNED | INT-FILE-039M | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Plan-first organization, folder suggestions/creation, ambiguity chooser, package-family moves, operation journal, undo, SAF-scoped roots |
| Multi-folder Keep Organized | Background folder observation + notifications | CLIENT | PLANNED | INT-FILE-039M | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | User-selected watched folders, messiness thresholds, Organize/Review/Snooze notifications, per-folder rules and conservative ask-first defaults |

How to use:
- For each feature, add a link to the authoritative source path and the commit SHA.
- Mark status with one of the canonical values and add short evidence notes.
- Candidate or approved/planned work must not be represented as current verified source authority.
