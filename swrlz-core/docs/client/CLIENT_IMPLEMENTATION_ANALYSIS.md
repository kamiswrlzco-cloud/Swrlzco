> **Authority note:** current promoted CLIENT source authority remains CLIENT CFv2.1.9; see `../CURRENT_AUTHORITY.md`. Later CLIENT candidates are source-candidate/evidence lineage only and are not promoted by this document.

# Client Implementation Analysis

## Current candidate evidence — 2026-07-31

Current repository transport is CLIENT CFv2.1.27 R1 from INT-AI-060A:

- versionCode: `125`;
- versionName: `2.1.27-truth-reasoning-expression-separation-candidate-r1`;
- source SHA-256: `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`;
- repository Forge commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`;
- transport: `sources/client/CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1.transport.json`.

INT-AI-060A mirrors the shared non-profile Truth Core boundary into CLIENT-facing reasoning/provider requests, keeps personality/expression external to factual authority, and preserves CLIENT as a requester/capability surface rather than SERVER model authority. Packaged evidence records static `47/47` PASS and package/manifest integrity. Gradle/Android compilation was not established in that packaging environment because the Gradle distribution could not be reached.

### External identity collision

INT-FILE-059A previously packaged a different CLIENT CFv2.1.27 R1:

- versionName: `2.1.27-file-lab-cartographer-candidate-r1`;
- source SHA-256: `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`.

That package adds the shared Forge File Lab/Archive Cartographer foundation. It is distinct from the current 060A repository transport despite sharing external version/revision numbers. The next CLIENT candidate must advance version and/or revision.

### Shared Forge parent — CLIENT CFv2.1.26 R1 / INT-FORGE-054A-R2

- versionCode: `124`;
- versionName: `2.1.26-forge-parity-chat-settings-candidate-r1`;
- source SHA-256: `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`.

This candidate mirrors baseline Forge conveyor capabilities from SERVER while preserving CLIENT-only Missions and legacy Dev Mode. Shared Chat/Forge/Settings capability trails SERVER where appropriate; SERVER-only inference/model/evidence authority is not cloned into CLIENT.

### Earlier current-generation progression

- CLIENT CFv2.1.25 R1: provider cleanup/Model Rack behavior-shard parity; Gemini removed from active CLIENT planner/key/runtime/UI paths, public GPT/OpenAI controls hidden, dormant compatibility retained.
- CLIENT CFv2.1.24 R1: Model Rack Transport V2; source SHA `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55`.
- CLIENT CFv2.1.23 R1: Model Rack/EQ/reasoning controls and declarative `.swrlzmod` import foundation.
- CLIENT CFv2.1.22 R1 / INT-UX-039Q: VC120, source SHA `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`, Forge commit `1d3fa542db0f700a1f35256be9317393d25bbc8c`.

Detailed per-update notes are maintained in `../patch-notes/CLIENT_PATCH_NOTES.md`; current cross-component lineage is in `../reference/CURRENT_CANDIDATE_LINEAGE.md`.

### Current evidence boundary

Source transport/package evidence does not imply APK build, device acceptance, promotion, release, deployment, or installation. CLIENT-specific Missions/legacy Dev Mode remain legitimate CLIENT-only surfaces. Shared capability parity does not change SERVER authority over hosted inference/model state.

## Historical implementation analysis from Documentation Rebuild v2

The material below records older CLIENT evidence and remains useful for lineage. It is not a current-version description.

Summary:

- Primary platform: Android application (source present in `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core`).
- Primary targeting: Accessibility-based targeting via `SwurlzAccessibilityService.kt` (snapshotting accessibility node tree, synthetic node IDs, semantic matching). Status: IMPLEMENTED.  
- Fallback targeting: Gesture/coordinate fallback using `dispatchGesture` (`tapPoint`, `scrollScreen`). Status: IMPLEMENTED.
- Text input: Uses `AccessibilityNodeInfo.ACTION_SET_TEXT` when nodes are editable. Status: IMPLEMENTED.
- Overlays and bubble UI: `OverlayService.kt`, `InteractiveBubbleDockService.kt`, `ClientBubbleController.kt` present. Status: IMPLEMENTED.
- AI/LLM integration: `GeminiClient.kt` and `GeminiMissionPlanner.kt` exist in the historical extracted slice. Status: HISTORICAL IMPLEMENTED evidence only; current candidate architecture removed Gemini from active CLIENT planner/key/runtime/UI paths.
- Mission runtime: `MissionBus.kt`, `MissionRunnerService.kt` and related data stores exist. Status: IMPLEMENTED.
- Networking / discovery: `CoreNodeAutoDiscovery.kt`, `GroupClientApi.kt`, `ClientPresenceRegistration.kt` present. Status: IMPLEMENTED.

Notable historical files (evidence):

- `android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt`
- `android/app/src/main/java/sh/swurlz/core/bubble/ClientBubbleController.kt`
- `android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt`
- `android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt`
- `android/app/src/main/java/sh/swurlz/core/protocol/CommunicationEnvelopeV1.kt`
- `android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt`

Missing / Unknown in the historical source slice:

- No OCR code detected in client source (status: UNKNOWN).
- No explicit fallback to Intents for action execution detected (status: UNKNOWN).
