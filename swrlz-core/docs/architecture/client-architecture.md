# Client Architecture (Android)

Overview:

The SWRLZ client is an Android application responsible for device interaction and mission execution. Key responsibilities:

- Observe the device UI (accessibility node tree).
- Plan and execute missions (actions) against the device using a mission runtime.
- Present user-facing controls via overlays and chat/bubble UI.
- Integrate with LLMs (Gemini) for mission planning and intent routing.
- Participate in node discovery and presence/networking for group scenarios.

Primary subsystems and evidence:

- Accessibility & Targeting — `SwurlzAccessibilityService.kt`:
  - Snapshots active window accessibility nodes and generates synthetic IDs (`n0`, `n1`, ...).
  - Primary matching is semantic (package, class, text, contentDescription, bounds).
  - Node actions: click, focus, set text via `ACTION_SET_TEXT`.
  - Status: IMPLEMENTED.

- Fallback Execution — gestures & coordinates:
  - If node is not clickable, service walks to clickable parent or synthesizes a gesture using `GestureDescription` (`tapPoint`, `scrollScreen`).
  - Status: IMPLEMENTED.

- Mission Runtime & Planner:
  - `MissionBus.kt`, `MissionRunnerService.kt`, and `GeminiMissionPlanner.kt` indicate integrated mission lifecycle and planner hooks into LLM provider.
  - Status: IMPLEMENTED (runtime present; planner integrated with Gemini client).

- Overlays & Bubbles:
  - `OverlayService.kt`, `InteractiveBubbleDockService.kt`, and bubble controllers provide persistent UI affordances and quick controls.
  - Status: IMPLEMENTED.

- Networking & Discovery:
  - `CoreNodeAutoDiscovery.kt`, `GroupClientApi.kt` provide discovery and group coordination primitives used by the client.
  - Status: IMPLEMENTED.

Targeting classification summary:

- Primary: Accessibility node tree semantic targeting (IMPLEMENTED).
- Secondary/fallback: Gesture coordinates via `dispatchGesture` (IMPLEMENTED).
- OCR: No evidence found in client source (UNKNOWN).
- Intents: No broad use found for core action execution (UNKNOWN).

