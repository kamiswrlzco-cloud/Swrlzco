# Mission Action Resolution (Draft)

This document describes the observed action resolution hierarchy used by the client runtime when executing mission actions against the device UI.

Overview
- The client attempts to resolve an abstract action (tap/type/scroll) to a concrete UI target using a cascade of strategies. Evidence: `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/SwurlzAccessibilityService.kt`, `.reference/swrlz-source/extracted/client/CLIENT_CFv2.0.69_SWRLZ/android/app/src/main/java/sh/swurlz/core/service/MissionRunnerService.kt`.

Resolution hierarchy (observed):

1. Semantic node selection
   - Use accessibility node tree metadata and high-confidence semantic matches (content description, role, class, text) when available.
   - Implementation: `validatedNode()` method (Line 173, SwurlzAccessibilityService.kt)
2. Resource-id matching
   - Prefer `viewResourceName`/`resource-id` when present and stable.
3. Visible text / partial text match
   - Match visible labels, buttons, and text nodes.
4. Content description / hints
   - Use `content-desc` or accessibility hints when available.
5. Ancestor / relative matching
   - Find target by relation to a nearby stable anchor node (parent, sibling, list item index).
6. Coordinate-based gesture fallback
   - When no node can be reliably identified, perform `dispatchGesture()` or system gesture tap at calculated coordinates.
   - Implementation: `tapPoint(x, y)` (Line 144), `scrollScreen(direction)` (Line 205), `dispatchGesture()` (Line 148)
7. OCR / visual heuristics (if present)
   - If implemented, optionally run OCR to find text on screen and translate to coordinates.

Exact client methods (authoritative source):
- `snapshot(maxNodes: Int = 80): Snapshot` (Line 64) — capture accessibility tree
- `tapNode(...)` (Line 121) — tap a specific node
- `tapPoint(x: Float, y: Float): Boolean` (Line 144) — tap at coordinates
- `typeText(...)` (Line 151) — set text using `ACTION_SET_TEXT` (Line 170)
- `scrollScreen(direction: String): Boolean` (Line 205) — scroll using gesture

Action verification and retries
- After performing an action, the client validates expected state changes via a short re-snapshot of the accessibility tree and status checks. If validation fails, retries are attempted with degraded resolution strategies (e.g., widen search scope, use coordinates).

Notes and recommendations
- Document exact method names and code locations in the authoritative clone and include example call sequences.
- Add a flow diagram and code snippets showing `snapshot()` → `findNode()` → `tapNode()` → `validate()`.
