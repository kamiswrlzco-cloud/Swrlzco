# INT-STABILITY-063A — SERVER Model Startup and Background Stability

Mode: source-only SERVER stabilization  
Lifecycle state: SERVER R23 candidate prepared; Forge/build/device evidence pending  
Status: implementation complete within approved source scope

## Objective

Prevent repeated SERVER process termination caused by redundant fleet-wide native LLM load probing during startup, and improve background survival under memory pressure without changing model files or weakening MCP, tunnel, trust, identity, or protocol boundaries.

## Candidate identity

- Candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R23`
- Logical candidate: `CFv2.1.26 R23`
- Version code: `VC106`
- Version name: `2.1.26-model-startup-stability-r23`
- Source SHA-256: `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17`
- Metadata SHA-256: `670211b8d50b7d53673ee3840c5432ab626027c9d7ee6cc3c8ed6ae6f3b95fb0`
- Direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R22.zip`
- Parent SHA-256: `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52`
- Repository transport: pending

## Confirmed facts

- The supplied R21 diagnostic contains five independent SERVER/tunnel process sessions in approximately 31 seconds; the first four end without orderly process-exit or service-shutdown evidence.
- Before this checkpoint, automatic fleet startup was invoked by `NodeHostApplication`, `NodeHostService`, and Chat composition.
- The fleet path native-load-probed every enabled compatible model and restored a selected resident model afterward.
- R21/R22 MCP, tunnel, control-plane egress, credential retention, NODE_HOST routing, trust, and Truth Firewall behavior are preserved.

## Assumption boundary

The evidence is consistent with native-memory pressure or Android low-memory termination, but no Android tombstone, fatal logcat stack, or LMKD kill reason was supplied. The exact process-death mechanism is not claimed as proven.

## Implementation summary

1. `NodeHostService` is the sole automatic model-runtime startup owner.
2. Normal startup performs discovery/indexing without fleet-wide native loading.
3. **PROBE ALL ENABLED** is an explicit operator action.
4. Automatic preload is selected-model-only, requires `keepModelLoaded=true`, and must pass a native-memory admission gate.
5. Heavy selected-model startup waits for tunnel startup to reach a terminal local startup state or timeout and then observes a settling interval.
6. An unclean previous foreground-service session triggers model safe mode on the next launch.
7. A periodic memory watchdog and Android trim/low-memory callbacks can release the resident model according to policy.
8. A rotating redacted SERVER Stability Ledger records service sessions, memory, model stages, trim signals, watchdog decisions, and unclean restart detection without prompts, messages, model contents, proofs, credentials, or tunnel payloads.
9. Settings expose stability-log capture, explicit fleet probing, and safe-mode clearance.

## Files changed

- `app/src/main/java/sh/swrlz/nodehost/NodeHostApplication.kt`
- `app/src/main/java/sh/swrlz/nodehost/service/NodeHostService.kt`
- `app/src/main/java/sh/swrlz/nodehost/ai/local/SwrlieLocalRuntime.kt`
- `app/src/main/java/sh/swrlz/nodehost/ui/ServerChatScreen.kt`
- `app/src/main/java/sh/swrlz/nodehost/ui/ServerProviderMeshSettingsPanel.kt`
- `app/src/main/java/sh/swrlz/nodehost/stability/ServerStabilityLedger.kt` — new
- `app/src/main/java/sh/swrlz/nodehost/stability/ServerStabilityPolicy.kt` — new
- candidate version, patch notes, lineage, receipt, validation, and evidence files

## Documentation impact set

- Categories: SERVER runtime, model lifecycle, diagnostics, candidate lineage, patch accounting, continuity handoff.
- Package-internal documentation: synchronized for R23.
- Repository documentation: records R23 as prepared source-only successor pending Forge transport; current repository pointer remains R21.
- Documentation gate: PASS for source-only delivery; repository candidate promotion pending transport evidence.

## Verification

- Focused stability verifier: `32/32 PASS`.
- Pure Kotlin stability-policy harness: PASS.
- Changed-source Kotlin parser screen: zero syntax-class diagnostics.
- SERVER compiler-regression precheck: PASS.
- Internal source manifest: `928/928 PASS`.
- Source ZIP CRC and package verification: PASS.
- Changed paths: 11 added / 11 modified / 0 removed.
- Pinned tunnel runtime unchanged.

## Build evidence

- Android compile: NOT RUN.
- APK build: NOT RUN.
- Forge transport: PENDING.
- Install/device acceptance: PENDING.

## Device evidence required

1. Repeated cold starts with multiple model files present.
2. Confirmation that startup does not fleet-load every model automatically.
3. Selected-model preload only when configured and admitted.
4. Background survival beyond the prior approximately one-hour failure window.
5. Capture and review of `SWRLZ_SERVER_STABILITY_106.ndjson`.

## Approval boundary

- Approval waiting: R23 Forge transport/build/device evidence.
- What approval would authorize: transport-documentation synchronization or a bounded evidence-driven repair.
- What approval would not authorize: promotion, release, deployment, trust elevation, live credential disclosure, model-file modification, or unrelated CLIENT/SERVER changes.
- Expected result: one stable SERVER startup, retained foreground operation, and evidence-backed background survival.
- Exact approval phrase: none until the next evidence result is available.
