> **Migration note:** historical `.reference` entries remain lineage evidence. Current promoted source authority is CLIENT CFv2.1.9 / SERVER CFv2.1.0; see `../CURRENT_AUTHORITY.md`. Current candidate package/module evidence is tracked separately and does not imply promotion.

# Module Map (DRAFT)

This map connects source/package paths to architecture components and documentation.

Columns:
- Source Path / Package Evidence
- Component
- Plane (SWURVER / SWURLZER / SWRLZ CORE / MODEL / WORDMESH / SHARED / BUILD / TEST / LEGACY)
- Responsibility
- Status
- Related Documentation

Entries:

| Source Path / Package Evidence | Component | Plane | Responsibility | Status | Docs |
|---|---|---|---|---:|---|
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt` | Accessibility Service | SWURLZER | UI observation, node snapshotting, action execution | IMPLEMENTED / HISTORICAL | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt` | Mission Bus / Event Bus | SWURLZER | Mission event routing and local messaging | IMPLEMENTED / HISTORICAL | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/MissionRunnerService.kt` | Mission Runner | SWURLZER | Mission execution lifecycle and worker invocation | IMPLEMENTED / HISTORICAL | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt` | Historical Gemini provider | LEGACY | Historical provider client/planner; later CLIENT candidate removes Gemini from active planner/key/runtime/UI paths | HISTORICAL | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt` | Overlay Service & UI Dock | SWURLZER | Persistent overlay, bubble UI hosting | IMPLEMENTED / HISTORICAL | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `CLIENT CFv2.1.22 R1 candidate transport` | CLIENT Update Ledger / Settings / Theme identity | SWURLZER | UX/settings/theme-identity candidate progression | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` |
| `CLIENT CFv2.1.26 R1 candidate package` | Shared Forge parity / Chat / Settings | SWURLZER + SHARED | Mirrors shared Forge conveyor and Chat/Settings baseline while preserving Missions/legacy Dev Mode | SOURCE CANDIDATE | `docs/patch-notes/CLIENT_PATCH_NOTES.md` |
| `CLIENT CFv2.1.27 R1 INT-FILE-059A package evidence` | Forge File Lab / Cartographer | SWURLZER + SHARED | File/ZIP map/search/hash/preview, selective extraction, staged text revisions, split/recombine/shards, SAF lanes | PACKAGED SOURCE CANDIDATE | `docs/reference/CURRENT_CANDIDATE_LINEAGE.md` |
| `CLIENT CFv2.1.27 R1 INT-AI-060A current transport` | Truth/reasoning/expression client boundary | SWURLZER + SWRLZ CORE | Applies shared non-profile Truth Core boundary to CLIENT-facing provider requests and keeps profile as expression shaping | SOURCE CANDIDATE / CURRENT TRANSPORT | `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md`; `docs/patch-notes/CLIENT_PATCH_NOTES.md` |
| `.reference/swrlz-source/extracted/server/SERVER_CFv2.0.49_SWRLZ` | Historical Server source bundle | SWURVER | Historical server-side orchestration and APIs | IMPLEMENTED / HISTORICAL | `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` |
| `SERVER CFv2.1.9 R6: app/src/main/java/sh/swrlz/nodehost/ai/ServerProviderMeshRuntime.kt` | SERVER Provider Mesh Runtime | SWURVER + SWRLZ CORE | Routes advisory provider reasoning while preserving SWRLZ control-plane policy | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md` |
| `SERVER CFv2.1.9 R6: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrlieLocalRuntime.kt` | SWRLIE Local Runtime | SWURVER + MODEL | Local model load/inference orchestration behind SWRLIE provider interface | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md` |
| `SERVER CFv2.1.9 R6: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrlieModelVault.kt` | SWRLIE Model Vault | SWURVER + MODEL | GGUF staging, metadata/fingerprint/compatibility state, selected/known-good model management | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` |
| `SERVER CFv2.1.9 R6: app/src/main/java/sh/swrlz/nodehost/ai/local/SwrliePromptBudgeter.kt` | Prompt Budget Guard | SWRLZ CORE + MODEL | Reserves runtime/output budget and bounds compiled context | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md` |
| `SERVER CFv2.1.9 R6: app/src/main/java/sh/swrlz/nodehost/ai/context/ServerSelfKnowledgeResolver.kt` | Local Self-Knowledge Resolver | SWRLZ CORE + SWURVER | Supplies installed identity, role map, patch/runtime/model state without granting model authority | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md` |
| `SERVER CFv2.1.9 R6: app/src/main/java/sh/swrlz/nodehost/ui/ServerChatScreen.kt` | SERVER Chat + Machine Status Stack | SWURVER | Chat surface and authoritative SERVER/model/node/network/health status portals | SOURCE CANDIDATE / HISTORICAL BASELINE | `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` |
| `SERVER CFv2.1.17–2.1.23 candidate lineage` | Persistence/evidence + fast-path Chat progression | SWURVER + SWRLZ CORE | Room/history evidence, model/EQ assets, greeting/status/short-casual fast paths, compact Chat/status controls | SOURCE CANDIDATE | `docs/patch-notes/SERVER_PATCH_NOTES.md` |
| `SERVER CFv2.1.24 R1 candidate package` | Shared Forge conveyor / lineage | SWURVER + SHARED | Verified latest source selection, SAF lanes, Build Ledger, success/failure artifact routing, machine patch lineage | SOURCE CANDIDATE | `docs/patch-notes/SERVER_PATCH_NOTES.md` |
| `SERVER CFv2.1.25 R1 INT-FILE-059A package evidence` | Forge File Lab / Cartographer | SWURVER + SHARED | File/ZIP map/search/hash/preview, selective extraction, staged revisions, split/recombine/shards, analyzer map export | PACKAGED SOURCE CANDIDATE | `docs/reference/CURRENT_CANDIDATE_LINEAGE.md` |
| `SERVER CFv2.1.27 R2 INT-FIX-075A current transport` | §wyrlz LLM Studio compile-repair successor | SWRLZ CORE + SWURVER + MODEL | Preserves the R1 first-party LLM runtime/Studio and removes the compiler-evidenced invalid Compose import; mandatory regression gate added | SOURCE/STATIC/PACKAGE VERIFIED / CURRENT TRANSPORT / BUILD PENDING | `docs/checkpoints/INT-FIX-075A_SERVER_COMPILE_REPAIR_AND_PUBLICATION.md`; `docs/patch-notes/SERVER_PATCH_NOTES.md` |
| `SERVER CFv2.1.25 R1 INT-AI-060A historical transport` | Truth Core / reasoning / expression separation | SWRLZ CORE + SWURVER + MODEL | Centralizes non-profile truth/authority invariants and separates reasoning/output budget from profile expression | SOURCE CANDIDATE / HISTORICAL 2026-07-31 TRANSPORT | `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md`; `docs/patch-notes/SERVER_PATCH_NOTES.md` |
| `docs/architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md` | Identity/Profile/Reasoning contract | SWRLZ CORE | Defines SWRLZ primary identity, replaceable LLM/model role, Swurlzara lens role, intrinsic Truth Firewall | DOCUMENTED | same file |
| `docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` | Patch/lineage accounting contract | SHARED | Requires synchronized ReleaseNotes/CHANGELOG/machine index/repo patch notes per future candidate; forbids identity reuse | ACTIVE CONTRACT | same file |
| `_wordmesh_doc/` | WordMesh manual & extracted XML | WORDMESH | Historical architecture/runtime specification evidence | DOCUMENTED | `docs/wordmesh/WORDMESH_IMPLEMENTATION_GAP_ANALYSIS.md` |
| `/.github/workflows/swrlz-apk-router.yml` | APK Router | BUILD | Routes CLIENT/SERVER/BOTH, resolves/materializes source, verifies evidence, builds APK, records provenance | IMPLEMENTED / CHANGE PENDING CI RUN EVIDENCE | `docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md` |
| `/.github/workflows/source-package-integrity.yml` | Source Package Integrity | BUILD | Maps source-tree changes to lane-root identities and verifies direct/chunked source packages without inventing nested ZIPs | IMPLEMENTED / CHANGE PENDING CI RUN EVIDENCE | `docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md` |
| `swrlz-core/tools/ci/resolve_changed_source_identities.py` | Changed Source Identity Mapper | BUILD | Maps `.transport/<bundle>/...` chunk/evidence changes to lane-root `<bundle>.transport.json`; root sidecars to actual source identities | IMPLEMENTED / CHANGE PENDING CI RUN EVIDENCE | `docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md` |
| `swrlz-core/tools/ci/resolve_swrlz_source.py` | Source Resolver | BUILD | Resolves direct ZIP, current `chunked-git-blobs-v2` plus metadata bundle, or complete compatible v1 evidence; verifies chunks and reconstructs the whole ZIP in runner temporary storage | IMPLEMENTED | `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` |
| `swrlz-core/tools/ci/verify_swrlz_package_pair.py` | Source Evidence Verifier | BUILD | Treats ZIP as required build input and checksum/manifest as optional strict evidence | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |
| `swrlz-core/tools/ci/test_resolve_swrlz_source.py` | Resolver Regression Suite | TEST | Covers ZIP-only input, conflicting sidecars, exact chunk reassembly, corruption rejection, push transport selection | IMPLEMENTED | `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` |
| `swrlz-core/tools/ci/test_resolve_changed_source_identities.py` | Source Identity Mapping Regression Suite | TEST | Covers nested transport evidence/chunks, root direct/sidecar identity mapping, missing-root failure and dedupe | IMPLEMENTED / PENDING CI RUN EVIDENCE | `docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md` |

Notes:
- Candidate path entries may refer to package-level evidence because current candidates are transported as source archives rather than extracted into the maintained Git tree.
- INT-FILE-059A and INT-AI-060A reused the same external CLIENT/SERVER version+revision pairs for different source bytes; see `CURRENT_CANDIDATE_LINEAGE.md`. Do not conflate them.
- Update historical `.reference` source paths when promoted current source trees become directly addressable.
- BUILD/TEST entries describe repository behavior/evidence class and do not promote CLIENT/SERVER candidate source packages.
