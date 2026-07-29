> **Authority note:** current promoted CLIENT source authority remains CLIENT CFv2.1.9; see `../CURRENT_AUTHORITY.md`. CLIENT CFv2.1.22 R1 is later source-candidate/evidence lineage and is not promoted by this document.

# Client Implementation Analysis

## Current candidate evidence — 2026-07-29

Repository transport includes CLIENT CFv2.1.22 R1:

- checkpoint: `INT-UX-039Q`;
- versionCode: `120`;
- versionName: `2.1.22-update-ledger-settings-theme-identity-candidate-r1`;
- source SHA-256: `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`;
- parent: `CLIENT_CFv2.1.21_SWRLZ_CANDIDATE_R2.zip`;
- parent SHA-256: `c4eb68554bc3c5bf95a0599c42da782ad3b948331cab3b08229eb73c3a9b089b`;
- repository Forge commit: `1d3fa542db0f700a1f35256be9317393d25bbc8c`.

The repository candidate manifest records source/static validation, including deterministic repackage, ZIP CRC, JSON/XML parsing, Command Center regression coverage, update-ledger smoke/compile checks, and UX regression checks. Android compilation was blocked before compilation because Gradle 8.7 was unavailable and `services.gradle.org` was unreachable; APK build remained pending.

The candidate progression includes Update Ledger interaction, Settings information architecture, and primary/complementary theme identity role work while preserving candidate-only authority. See `../checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md`.

This candidate does not replace promoted CLIENT CFv2.1.9 and no build/device/promotion claim is inferred from repository transport.

## Historical implementation analysis from Documentation Rebuild v2

The material below records older CLIENT evidence and remains useful for lineage. It is not a current-version description.

Summary:

- Primary platform: Android application (source present in `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core`).
- Primary targeting: Accessibility-based targeting via `SwurlzAccessibilityService.kt` (snapshotting accessibility node tree, synthetic node IDs, semantic matching). Status: IMPLEMENTED.  
- Fallback targeting: Gesture/coordinate fallback using `dispatchGesture` (`tapPoint`, `scrollScreen`). Status: IMPLEMENTED.
- Text input: Uses `AccessibilityNodeInfo.ACTION_SET_TEXT` when nodes are editable. Status: IMPLEMENTED.
- Overlays and bubble UI: `OverlayService.kt`, `InteractiveBubbleDockService.kt`, `ClientBubbleController.kt` present. Status: IMPLEMENTED.
- AI/LLM integration: `GeminiClient.kt` and `GeminiMissionPlanner.kt` present in `ai/`. Status: IMPLEMENTED historical/current-source evidence; this does not make Gemini the required current architecture provider.
- Mission runtime: `MissionBus.kt`, `MissionRunnerService.kt` and related data stores exist. Status: IMPLEMENTED.
- Networking / discovery: `CoreNodeAutoDiscovery.kt`, `GroupClientApi.kt`, `ClientPresenceRegistration.kt` present. Status: IMPLEMENTED.

Notable files (evidence):

- `android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt` (accessibility targeting, gestures)
- `android/app/src/main/java/sh/swurlz/core/bubble/ClientBubbleController.kt`
- `android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt`
- `android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt`
- `android/app/src/main/java/sh/swurlz/core/protocol/CommunicationEnvelopeV1.kt`
- `android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt`

Missing / Unknown in the historical source slice:

- No OCR code detected in client source (status: UNKNOWN).
- No explicit fallback to Intents for action execution detected (status: UNKNOWN).
