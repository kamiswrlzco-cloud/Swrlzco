> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is CLIENT CFv2.1.9 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

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
| `/.github/workflows/swrlz-apk-router.yml` | APK Router | BUILD | Routes CLIENT/SERVER source identities, materializes resolved source, verifies optional evidence, builds APK, records provenance | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |
| `swrlz-core/tools/ci/resolve_swrlz_source.py` | Source Resolver | BUILD | Resolves direct ZIP or `chunked-git-blobs-v1`, verifies chunks, reconstructs whole ZIP in runner temporary storage, computes source identity | IMPLEMENTED | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` |
| `swrlz-core/tools/ci/verify_swrlz_package_pair.py` | Source Evidence Verifier | BUILD | Treats ZIP as required build input and checksum/manifest as optional strict evidence | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |
| `swrlz-core/tools/ci/test_resolve_swrlz_source.py` | Resolver Regression Suite | TEST | Covers ZIP-only input, conflicting sidecars, exact chunk reassembly, corruption rejection, and push transport selection | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |

Notes:
- Update historical `.reference` source paths when current authoritative source trees become directly addressable.
- Status values: IMPLEMENTED, PARTIAL, PLANNED, UNKNOWN, DEPRECATED.
- BUILD/TEST entries describe current repository HEAD behavior and do not promote CLIENT/SERVER candidate source packages.
