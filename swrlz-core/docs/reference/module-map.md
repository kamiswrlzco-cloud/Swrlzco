> **Migration note:** historical `.reference` entries remain lineage evidence. Current promoted source authority is CLIENT CFv2.1.9 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md`. SERVER CFv2.1.9 R1-R5 entries below are candidate-module evidence, not promotion.

# Module Map (DRAFT)

This map connects source paths to architecture components and documentation.

Columns:
- Source Path
- Component
- Plane (SWURVER / SWURLZER / SWRLZ CORE / MODEL / WORDMESH / SHARED / BUILD / TEST / LEGACY)
- Responsibility
- Status
- Related Documentation

Entries:

| Source Path | Component | Plane | Responsibility | Status | Docs |
|---|---|---|---|---:|---|
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt` | Accessibility Service | SWURLZER | UI observation, node snapshotting, action execution | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt` | Mission Bus / Event Bus | SWURLZER | Mission event routing and local messaging | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/MissionRunnerService.kt` | Mission Runner | SWURLZER | Mission execution lifecycle and worker invocation | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt` | LLM Integration | SWURLZER | Historical provider client and mission planner integration | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt` | Overlay Service & UI Dock | SWURLZER | Persistent overlay, bubble UI hosting | IMPLEMENTED | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ` | Historical Server source bundle | SWURVER | Historical server-side orchestration and APIs | IMPLEMENTED / HISTORICAL | `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ai/ServerProviderMeshRuntime.kt` | SERVER Provider Mesh Runtime | SWURVER + SWRLZ CORE | Routes advisory provider reasoning while preserving SWRLZ control-plane policy | SOURCE CANDIDATE | `docs/checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrlieLocalRuntime.kt` | SWRLIE Local Runtime | SWURVER + MODEL | Local model load/inference orchestration behind SWRLIE provider identity | SOURCE CANDIDATE | `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrlieModelVault.kt` | SWRLIE Model Vault | SWURVER + MODEL | GGUF staging, metadata/fingerprint/compatibility state, selected/known-good model management | SOURCE CANDIDATE | `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrliePromptBudgeter.kt` | Prompt Budget Guard | SWRLZ CORE + MODEL | Reserves runtime/output budget before native inference and bounds compiled identity/context | SOURCE CANDIDATE | `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrlieRuntimeSettings.kt` | SWRLIE Runtime Settings | SWURVER + MODEL | Presets/context/output/sampling/thread/keep-loaded resource configuration | SOURCE CANDIDATE | `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ai/context/ServerSelfKnowledgeResolver.kt` | Local Self-Knowledge Resolver | SWRLZ CORE + SWURVER | Supplies installed identity, role map, patch/runtime/model state to local SWRLIE without granting authority | SOURCE CANDIDATE | `docs/checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/update/ServerUpdateLedgerRepository.kt` | Update Ledger Repository | SWURVER | Shared packaged update-history parser/retrieval source for UI and local self-knowledge | SOURCE CANDIDATE | `docs/checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ui/ServerChatScreen.kt` | SERVER Chat | SWURVER | First-class Chat UI, provider controls, adaptive/copyable conversation surface | SOURCE CANDIDATE | `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` |
| `SERVER CFv2.1.9 R5: app/src/main/java/sh/swrlz/nodehost/ui/ServerUpdateLedgerDialog.kt` | Update Ledger UI | SWURVER | Horseshoe-opened local revision/patch-note surface consuming shared repository | SOURCE CANDIDATE | `docs/checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md` |
| `_wordmesh_doc/` | WordMesh manual & extracted XML | WORDMESH | Canonical architecture and runtime specification | DOCUMENTED | `docs/wordmesh/WORDMESH_IMPLEMENTATION_GAP_ANALYSIS.md` |
| `/.github/workflows/swrlz-apk-router.yml` | APK Router | BUILD | Routes CLIENT/SERVER source identities, materializes resolved source, verifies optional evidence, builds APK, records provenance | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |
| `swrlz-core/tools/ci/resolve_swrlz_source.py` | Source Resolver | BUILD | Resolves direct ZIP or `chunked-git-blobs-v1`, verifies chunks, reconstructs whole ZIP in runner temporary storage, computes source identity | IMPLEMENTED | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` |
| `swrlz-core/tools/ci/verify_swrlz_package_pair.py` | Source Evidence Verifier | BUILD | Treats ZIP as required build input and checksum/manifest as optional strict evidence | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |
| `swrlz-core/tools/ci/test_resolve_swrlz_source.py` | Resolver Regression Suite | TEST | Covers ZIP-only input, conflicting sidecars, exact chunk reassembly, corruption rejection, and push transport selection | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |

Notes:
- Candidate path entries use the R5 source ZIP's internal path because the candidate is stored in repository transport form rather than extracted into the maintained Git tree.
- Update historical `.reference` source paths when promoted current source trees become directly addressable.
- BUILD/TEST entries describe repository behavior and do not promote CLIENT/SERVER candidate source packages.
