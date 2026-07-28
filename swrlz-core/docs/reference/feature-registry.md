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
| LLM integration (Gemini) | GeminiClient / GeminiMissionPlanner | SWURLZER | IMPLEMENTED | `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt` | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Historical/current-source evidence entry; does not override the approved local/private-node-first architecture direction |
| Overlay UI / Bubbles | OverlayService / ClientBubbleController | SWURLZER | IMPLEMENTED | `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt` | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Interactive dock, touch passthrough handling |
| Precheck + Promotion Gate | Engineering validation pipeline | CLIENT + SERVER | IMPLEMENTED | Checkpoint/candidate engineering process; does not itself promote source | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Verify parent, acceptance tests, disposable candidate, compile/repair loop, documentation gate, immutable candidate revisions, expected-SHA evidence matching |
| Adaptive conversation workspace | CLIENT Chat UI | CLIENT | EXPERIMENTAL | CFv2.1.19 candidate lineage; promotion pending | `docs/checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md` | Conversation-first layout, keyboard-aware chrome, compact provider mesh; candidate build evidence remains separate from repository authority |
| Chunked source reconstruction | APK Router resolver + workflow | BUILD | IMPLEMENTED | `.github/workflows/swrlz-apk-router.yml`; `swrlz-core/tools/ci/resolve_swrlz_source.py` | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` | Direct ZIP or `chunked-git-blobs-v1`; verifies every chunk and reconstructed whole ZIP before build |
| ZIP-only build eligibility | APK Router verifier | BUILD | IMPLEMENTED | `swrlz-core/tools/ci/verify_swrlz_package_pair.py` | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` | ZIP is required build input; checksum/manifest optional; supplied contradictions fail closed |
| Forge-side chunk transport | CLIENT Forge | CLIENT | EXPERIMENTAL | CLIENT CFv2.1.20 candidate R1; later candidate/build evidence is separate from promoted authority | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | AUTO/DIRECT/CHUNKED source transport and resumable chunk planning exist in candidate lineage; not promoted authority |
| Persistent Forge transfers | Forge transfer subsystem | CLIENT + SERVER role-aware | PLANNED | INT-FORGE-039K | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Transfer owner independent of Compose lifecycle; shared progress state; pause/cancel/retry; SHA + manifest auto-pair settings |
| Chat-initiated Forge package discovery | Command Center + Local Artifact Resolver + Forge | CLIENT | PLANNED | INT-FORGE-039L | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Natural-language latest-valid CLIENT/SERVER/BOTH discovery, optional evidence validation, canonical destination preview, verified staging |
| Conversational local file organizer | Local Artifact Resolver + File Organization Planner/Executor | CLIENT | PLANNED | INT-FILE-039M | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Plan-first organization, folder suggestions/creation, ambiguity chooser, package-family moves, operation journal, undo, SAF-scoped roots |
| Multi-folder Keep Organized | Background folder observation + notifications | CLIENT | PLANNED | INT-FILE-039M | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | User-selected watched folders, messiness thresholds, Organize/Review/Snooze notifications, per-folder rules and conservative ask-first defaults |
| Distributed intelligence architecture | CLIENT + SERVER + MODEL | CLIENT + SERVER | DOCUMENTED / PLANNED | Architecture contract only; implementation evidence remains component-specific | `docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` | Defines LOCAL/LAN/ONLINE modes, CLIENT domain sovereignty, SERVER heavyweight reasoning/network role, task-scoped disclosure, and model-independent SWRLZ identity |
| Shared SWRLZ context contract | Missions context + Chat + SERVER reasoning | CLIENT + SERVER | PLANNED | Future contract extraction/generalization; existing CLIENT Missions context is foundation evidence only | `docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` | Reuse device/app/screen/delta/capability context across Missions, Chat, Diagnostics, SERVER, and SWRLIE without creating duplicate truth systems |
| SERVER Chat parity | Shared Chat workspace + role-specific capabilities | SERVER | PLANNED | Future bounded checkpoint | `docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` | Same core Chat/Command Center semantics as CLIENT, with SERVER/node/reasoning/Forge capabilities rather than a separate incompatible chat stack |
| SWRLIE reasoning provider | Reasoning Gateway + pluggable engines/runtimes | SERVER + MODEL | PLANNED | Future bounded checkpoints; no model selected or integrated by this docs checkpoint | `docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` | SWRLZ survives model removal/swap/failure; SWRLIE is first-party provider identity while underlying model/runtime/lineage remain explicit |
| SERVER network/Forge authority | Authenticated CLIENT intent + SERVER validation/execution | CLIENT + SERVER | PLANNED | Future bounded checkpoint | `docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` | Open-web research, heavy external analysis, GitHub/Forge writes, and model lifecycle route through SERVER; CLIENT retains local execution authority |
| Persistent Model Vault | Independent MODEL product lifecycle | SERVER + MODEL | PLANNED | Future bounded checkpoint | `docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` | Keeps large weights outside CLIENT/SERVER source/APK lifecycle; supports verification, independent updates, rollback, and reinstall recovery where storage policy permits |

How to use:
- For each feature, add a link to the authoritative source path and the commit SHA.
- Mark status with one of the canonical values and add short evidence notes.
- Candidate or approved/planned work must not be represented as current verified source authority.
