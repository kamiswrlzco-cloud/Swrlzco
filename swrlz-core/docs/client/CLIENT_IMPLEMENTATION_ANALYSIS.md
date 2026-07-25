> **Migration note:** this analysis originated from Documentation Rebuild v2 and contains historical evidence paths. Current source authority is CLIENT CFv2.1.2; see `../CURRENT_AUTHORITY.md` or the nearest equivalent path before treating any historical version/path as current.

# Client Implementation Analysis

Summary:

- Primary platform: Android application (source present in `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core`).
- Primary targeting: Accessibility-based targeting via `SwurlzAccessibilityService.kt` (snapshotting accessibility node tree, synthetic node IDs, semantic matching). Status: IMPLEMENTED.  
- Fallback targeting: Gesture/coordinate fallback using `dispatchGesture` (`tapPoint`, `scrollScreen`). Status: IMPLEMENTED.
- Text input: Uses `AccessibilityNodeInfo.ACTION_SET_TEXT` when nodes are editable. Status: IMPLEMENTED.
- Overlays and bubble UI: `OverlayService.kt`, `InteractiveBubbleDockService.kt`, `ClientBubbleController.kt` present. Status: IMPLEMENTED.
- AI/LLM integration: `GeminiClient.kt` and `GeminiMissionPlanner.kt` present in `ai/`. Status: IMPLEMENTED.
- Mission runtime: `MissionBus.kt`, `MissionRunnerService.kt` and related data stores exist. Status: IMPLEMENTED.
- Networking / discovery: `CoreNodeAutoDiscovery.kt`, `GroupClientApi.kt`, `ClientPresenceRegistration.kt` present. Status: IMPLEMENTED.

Notable files (evidence):

- `android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt` (accessibility targeting, gestures)
- `android/app/src/main/java/sh/swurlz/core/bubble/ClientBubbleController.kt`
- `android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt`
- `android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt`
- `android/app/src/main/java/sh/swurlz/core/protocol/CommunicationEnvelopeV1.kt`
- `android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt`

Missing / Unknown:

- No OCR code detected in client source (status: UNKNOWN).
- No explicit fallback to Intents for action execution detected (status: UNKNOWN).
