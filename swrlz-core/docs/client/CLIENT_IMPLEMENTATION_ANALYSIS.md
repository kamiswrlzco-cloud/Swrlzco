> **Authority note:** current promoted CLIENT source authority remains CLIENT CFv2.1.9; see `../CURRENT_AUTHORITY.md`. Later CFv2.1.x packages described below are candidate/evidence lineage unless a separate promotion checkpoint says otherwise.

# Client Implementation Analysis

## Current candidate / transport evidence — 2026-07-31

### CLIENT CFv2.1.26 R1 — INT-FORGE-054A-R2

- versionCode: `124`;
- versionName: `2.1.26-forge-parity-chat-settings-candidate-r1`;
- source SHA-256: `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`;
- parent: CLIENT CFv2.1.25 R1, SHA `6ce26560dab4113d06bb1360c260dcc087fc2fa8b583f1583ada2bfe3688f5b2`.

This source-only checkpoint catches CLIENT up to the shared Forge baseline without erasing legitimate CLIENT-only roles. Shared behavior includes CLIENT/SERVER/BOTH/ASK/FILES targeting, authoritative newest-source discovery using component/version/manifest/SHA/lineage, configurable SAF project/source/artifact/log/model/mod/evidence lanes, persistent Build Ledger provenance, and default-on successful-artifact / failed-workflow-log download policy.

CLIENT-specific Missions and legacy Dev Mode remain CLIENT-only. SERVER inference/model/evidence authority remains SERVER-owned rather than being cloned into CLIENT. The candidate also carries local Chat continuity/history and paired-SERVER model-selection UI appropriate to CLIENT.

No APK build, installation, promotion, release, or deployment is inferred from this source-only checkpoint.

### Latest repository transport — CLIENT CFv2.1.27 R1

Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` added `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1` as verified `chunked-git-blobs-v1` transport:

- declared whole-source SHA-256: `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`;
- reconstructed size: 15,127,739 bytes;
- chunks: 4;
- checksum evidence: present under the transport evidence directory;
- separately packaged candidate manifest in this transaction: absent.

This establishes repository transport identity only. The transport record does not provide enough evidence to infer the candidate's internal checkpoint changes, versionCode, Android compilation, APK result, device behavior, promotion, release, deployment, or installation.

### CLIENT CFv2.1.22 R1 — earlier maintained candidate evidence

- checkpoint: `INT-UX-039Q`;
- versionCode: `120`;
- versionName: `2.1.22-update-ledger-settings-theme-identity-candidate-r1`;
- source SHA-256: `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`;
- parent: `CLIENT_CFv2.1.21_SWRLZ_CANDIDATE_R2.zip`;
- parent SHA-256: `c4eb68554bc3c5bf95a0599c42da782ad3b948331cab3b08229eb73c3a9b089b`;
- repository Forge commit: `1d3fa542db0f700a1f35256be9317393d25bbc8c`.

The repository candidate manifest records source/static validation, including deterministic repackage, ZIP CRC, JSON/XML parsing, Command Center regression coverage, update-ledger smoke/compile checks, and UX regression checks. Android compilation was blocked before compilation because Gradle 8.7 was unavailable and `services.gradle.org` was unreachable; APK build remained pending.

The candidate progression includes Update Ledger interaction, Settings information architecture, and primary/complementary theme identity role work while preserving candidate-only authority. See `../checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md`.

## CI / documentation synchronization

`INT-CI-DOC-060A` repairs Source Package Integrity selection so nested `.transport/.../evidence/*.sha256` files cannot be mistaken for lane-root source sidecars, and hardens APK Router lane-root/BOTH routing. That repair is staged on `checkpoint/int-ci-doc-060a-router-docs` until explicit merge approval.

Maintained CLIENT patch history now lives at [`PATCH_NOTES.md`](PATCH_NOTES.md). Future accepted CLIENT implementation checkpoints are documentation-incomplete until the affected CLIENT patch-note entry is synchronized. Already packaged candidate ZIPs remain immutable; repository patch notes repair missing historical narrative without changing old bytes/SHA/lineage.

`INT-FILE-059A` is approved for a shared Forge File Lab + Archive Cartographer foundation, but no current CLIENT package is claimed here to implement it until separate implementation/package evidence exists.

## Historical implementation analysis from Documentation Rebuild v2

The material below records older CLIENT evidence and remains useful for lineage. It is not a current-version description.

Summary:

- Primary platform: Android application (historical source under `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core`).
- Primary targeting: Accessibility-based targeting via `SwurlzAccessibilityService.kt` (snapshotting accessibility node tree, synthetic node IDs, semantic matching). Status: IMPLEMENTED.
- Fallback targeting: Gesture/coordinate fallback using `dispatchGesture` (`tapPoint`, `scrollScreen`). Status: IMPLEMENTED.
- Text input: Uses `AccessibilityNodeInfo.ACTION_SET_TEXT` when nodes are editable. Status: IMPLEMENTED.
- Overlays and bubble UI: `OverlayService.kt`, `InteractiveBubbleDockService.kt`, `ClientBubbleController.kt` present. Status: IMPLEMENTED.
- AI/LLM integration: historical source included `GeminiClient.kt` and `GeminiMissionPlanner.kt`; this is historical evidence and does not define the current provider architecture.
- Mission runtime: `MissionBus.kt`, `MissionRunnerService.kt` and related data stores exist. Status: IMPLEMENTED.
- Networking / discovery: `CoreNodeAutoDiscovery.kt`, `GroupClientApi.kt`, `ClientPresenceRegistration.kt` present. Status: IMPLEMENTED.

Notable historical files:

- `android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt`
- `android/app/src/main/java/sh/swurlz/core/bubble/ClientBubbleController.kt`
- `android/app/src/main/java/sh/swurlz/core/overlay/OverlayService.kt`
- `android/app/src/main/java/sh/swurlz/core/ai/GeminiClient.kt`
- `android/app/src/main/java/sh/swurlz/core/protocol/CommunicationEnvelopeV1.kt`
- `android/app/src/main/java/sh/swurlz/core/data/MissionBus.kt`

Missing / Unknown in the historical source slice:

- No OCR code detected in client source (status: UNKNOWN).
- No explicit fallback to Intents for action execution detected (status: UNKNOWN).
