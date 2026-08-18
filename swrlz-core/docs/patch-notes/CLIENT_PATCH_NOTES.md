# CLIENT R90 / VC216 — INT-FORGE-STATE-IMPORT-PERSISTENCE-184A

- Persistent Forge/import operation state across menu changes.
- See INT-FORGE-STATE-IMPORT-PERSISTENCE-184A_CLIENT_PATCH_NOTES.md for full details.

## 2026-08-18 — CLIENT R89 / VC215 — INT-AUTOFIX-EQ-INTEGRITY-183A

Forge META PACK integrity generator + scrollable Forge sub-menu selector, paired with SERVER R122 AutoFix v2 and direct Weight EQ read wrappers. No compile/APK/device acceptance claimed.

## 2026-08-18 — CLIENT R88 / VC214 — INT-RUNTIME-CHAT-AUTH-EXTERNAL-182A

Compact chat + local GENERATE + SERVER-owned Google authority/current-signer truth + group delegation + external SWRLZX intelligence contract. No compile/APK/device acceptance claimed.

# CLIENT CFv2.1.27 R87 / VC213 — INT-FIX-BUILD-AUTOFIX-GROUP-DELEGATION-181A

- Repairs the exact CLIENT R86 GitHub `:app:compileDebugKotlin` failure from workflow `32161206958`: `GoogleOAuthAppIdentity.kt` treated Android signature arrays as non-null even though the Kotlin platform type is nullable. Both modern and legacy certificate arrays now use `orEmpty()`, require a non-empty result, and then hash the first certificate.
- Pairs with SERVER R120 for same-active-group peer delegation. CLIENT chat continues using its existing natural-language tool-intent ingress; SERVER remains the authority/router.
- GPT/CLIENT -> CLIENT control is intended to be admitted only when source and target are proof-bound and share an ACTIVE SERVER-owned group. Cross-group routed control fails closed, while existing target capability, directory grant, mutation-plan and approval gates remain intact.
- R86 persistence/chat/Forge/Google improvements remain preserved.
- No Android compile or APK build was run for R87 by operator request. Fresh GitHub/APK/device evidence is required.

# CLIENT CFv2.1.27 R86 / VC212 — INT-MAJOR-CONTINUITY-FORGE-180A

- Major persistence pass: sticky foreground CLIENT runtime, `stopWithTask=false`, durable Forge watcher, process-exit diagnostics, and session/turn recovery across UI/process interruption.
- Chat polish: CLIENT remains the baseline, with top-deck readiness, no permanent permission strip, structured assistant paragraph/list rendering, and compact navigation.
- Google continuity repair: installed package/SHA-1 diagnostics, bounded Credential Manager reauth recovery, live/configured/loopback SERVER descriptor fallback, and canonical-signing update workflow.
- Forge transport moves to 8 MiB chunks; paired SERVER R119 owns Drive latest-first/concurrent download and artifact extraction repair.
- Compile/APK intentionally not run for this checkpoint; fresh GitHub/APK/device acceptance required.

# CLIENT CFv2.1.27 R85 / VC211 — INT-OBSERVATORY-SURFACE-PARITY-179B

- Preserves R84 SERVER-authoritative promotion/revocation gating.
- Replaces the simplified CLIENT Observatory with the SERVER-style canonical Conversation Observatory mirror.
- Adds live/past node, thread/scope/time/search filters, pins/bookmarks review, HISTORY/TRACE, visible audited OBSERVE LIVE, and redacted SERVER log-tail visibility.
- Uses paired SERVER R118 v2 Observatory routes with legacy read fallback.

# CLIENT CFv2.1.27 R84 — INT-ADMIN-OBSERVATORY-AUTHORITY-178B

- Makes Observatory visibility SERVER-authoritative. CLIENT continuously consumes `effectiveAdminAuthority`, `observatoryGranted`, and `effectiveCapabilities` from `/nodes/self/state`.
- Explicit SERVER admin promotion now reveals the `Observe` navigation item live; revocation/authority loss hides it and exits an open Observatory screen.
- CLIENT does not self-promote or infer privileged access from local UI state; SERVER R117 remains the authority source.
- Preserves R83 SERVER-owned Google account/Drive Forge preflight and all earlier CLIENT chat, memory, learned-knowledge, Storage Steward, and Forge behavior.

# CLIENT CFv2.1.27 R83 — INT-GOOGLE-AUTHORITY-FORGE-PREFLIGHT-175A

- SERVER-owned Google account configuration; CLIENT no longer edits Google OAuth setup.
- CLIENT uses only SERVER's public OAuth descriptor for Google account selection; Drive tokens never cross to CLIENT.
- Adds SERVER GDrive Forge preflight inventory: STORED / RECOGNIZED / PUBLISHED by component.
- Paired SERVER R113 / VC236.

## CLIENT R82 — Storage Steward Chat Cleanup (INT-STORAGE-STEWARD-CHAT-174A)

R82 integrates the Storage Steward retention blueprint into the CLIENT. Cleanup policy can be set and inspected through ordinary Chat or Settings; CLIENT and SERVER revisions are counted independently; lifecycle/cadence checks can notice cleanup eligibility without deleting anything. The user receives a complete proposed manifest and reclaimed-space estimate, and deletion remains approval-gated with an immediate fingerprint revalidation before any recognized reproducible ZIP/APK/AAB is removed. Ambiguous items, extracted directories, metadata/lineage/security/corpus evidence, and non-writable material remain protected or review-only. Policy is locally account-scoped while physical folder grants remain device-local; cross-device policy sync is not claimed. SERVER R112 is unchanged.

## CLIENT R80 — Forge Explicit-Source Resolver Repair (INT-FIX-FORGE-EXPLICIT-SOURCE-172A)

R80 is a narrow Forge reliability successor to R79. It preserves the R79 chat-context feature set and fixes an explicit-source resolver collision exposed by workflow `32068081337`: the router manually selected stale R76 while both a verified direct ZIP and an equivalent verified transport representation could resolve to that same canonical source. The resolver now prefers the verified direct artifact when the user explicitly names that ZIP, while transport-only builds and fail-closed ambiguity behavior remain intact. R80 advances to VC206 so the next Forge submission has a fresh candidate identity. SERVER R112 remains unchanged.

## CLIENT R79 — Chat Context Memory + Tags (INT-CHAT-CONTEXT-MEMORY-TAGS-171A)

R79 turns stored chat into a user-addressable context workspace. Responses can now carry temporary multi-tags, named pins/bookmarks, and user-created memory shards; active tag groups feed one reasoning turn and are consumed only after successful completion while history remains. Saved anchors can reopen a response across chat threads and can supply a bounded local neighborhood when referenced by name. The Chat UI gains response context actions, a context manager, and a collapsible top control deck so the message stream can reclaim vertical space. SERVER R112 and tool/truth/security authority remain unchanged. Fresh Auto Forge Android/APK/device acceptance is required.

## CLIENT R78 — Forge Identity Respin (INT-FIX-THEME-CONTRACT-MERGE-170B)

R78 is an identity-only successor to R77. It advances the Android/candidate identity to VC204 / `2.1.27-theme-contract-merge-fix-respin-r78` so the repaired client can be submitted as a fresh GitHub/Forge candidate instead of reusing the R77 identity. No feature or runtime behavior is changed; the complete R77 theme-contract repair and R76 Code 🫙 / Dragon Persona behavior remain preserved. Pair: SERVER R112. Fresh Auto Forge APK/device acceptance remains required.

## CLIENT R77 — Theme Contract Merge Compile Repair (INT-FIX-THEME-CONTRACT-MERGE-170A)

R77 is a narrow compiler-repair successor to R76. It restores the established ThemePack chrome/progress contract and built-in theme runtime configuration from R75, then overlays the complete R76 Dragon Persona contract so neither feature family is lost. The exact unresolved-reference class from workflow `32045319178` passes a local actual-source Kotlin compile harness. R76 Code 🫙 rendering, trust/execution ownership, Forge semantics, and external §wyrlzx boundaries are preserved. Pair: SERVER R112. Fresh Auto Forge APK/device acceptance remains required.

# INT-SERVICE-WORKFLOW-DRAGON-JAR-168A — CLIENT R76 / VC202 PATCH NOTES

## Code 🫙 send/render boundary repair
- Composer behavior now matches the operator contract exactly: selecting text and pressing 🫙 visibly inserts editable `[🫙]...[/🫙]` serialization in the input field.
- After SEND/history persistence, the same serialization is parsed into a real nested Code 🫙 UI segment inside the message bubble; raw jar markers are not normal sent-message presentation.
- Fixes the concrete R75 root cause: `detectLanguage()` contained an invalid Kotlin regex (`Unclosed character class`) which threw during rich parsing; the renderer caught that exception and fell back to raw serialized text.
- Marker canonicalization tolerates variation selectors and zero-width format characters around jar tokens, supports multiple containers, converges fenced Markdown onto the same code segment, and strips structural markers on malformed-display fallback rather than leaking them into chat.
- Historical/imported/user/assistant/LALM messages continue using the same non-destructive presentation model over immutable original provenance.

## Dragon theme/persona contract
- Mirrors the SERVER shared theme-persona contract so theme identity can provide the baseline dragon presentation personality while custom node/user profile instructions layer on top later.
- Default built-in theme resolves to `ANCIENT_DRAGON`; variant themes carry their own presentation-only persona metadata.
- CLIENT theme/persona metadata never alters tool schemas, truth, trust, authority, confirmation, or execution semantics.

## Preservation / validation boundary
- R75 execution ownership, group/trust presentation, active-GGUF exclusion, Forge behavior, and SERVER_LOCAL pairing remain preserved.
- Canonical `SWRLZ-LALM-001A.§wyrlzx` remains external and unmodified.
- Actual CLIENT jar parser source passes a dedicated Kotlin harness including the exact leaked-marker screenshot sentence and malformed/Unicode cases.
- Local Gradle compilation cannot start because this workspace cannot resolve `services.gradle.org`; fresh Auto Forge/APK/device evidence remains required.

---

# INT-TRUST-LALM-FORGE-RICH-167A — CLIENT R75 / VC201 PATCH NOTES

## Rich Code 🫙
- `[🫙]...[/🫙]` remains durable internal serialization only. Normal chat renders the contained range as a nested code-container card inside the surrounding message.
- Fenced Markdown and jar serialization converge on the same rich renderer with language label, monospace body, `COPY`, and `🫙 REMOVE`.
- The composer visually hides storage markers while preserving correct selection mapping and durable wrap/unwrap state.
- Historical/imported USER/assistant/LALM structure edits remain non-destructive overlays over immutable original content; malformed/legacy structures fall back safely.

## Execution ownership
- CLIENT protocol handling accepts only explicit `CLIENT_LOCAL` jobs.
- The old Android→SERVER `/providers/reason` relay is removed from CLIENT_LOCAL. Until a true on-device executor exists, CLIENT_LOCAL ACKs then fails closed with `CLIENT_LOCAL_EXECUTOR_NOT_CONFIGURED`.
- SERVER-owned canonical §wyrlzx inference uses SERVER R110 `SERVER_LOCAL` and therefore does not depend on Android selection/trust.

## Model/UI
- Active CLIENT model inventory hides GGUF/provenance-only entries. Historical update-ledger evidence remains readable but does not create runtime execution authority.
- Pairs with SERVER R110 group-scoped trust, direct SERVER_LOCAL execution, correlation diagnostics, canonical §wyrlzx auto-selection/background preload, and tile-scoped Auto Fix successor loop.

## Boundary
- Model bytes remain external; `SWRLZ-LALM-001A.§wyrlzx` is not bundled or mutated.
- Fresh Android compile/APK/device acceptance is not claimed by this source package.

---

# CLIENT R74 / VC200 — INT-LALM-ASYNC-LOG-AUTOFIX-CONTAINER-166A

Poisoned R73 jar-overlay recovery/quarantine, hardened v3 jar rendering/selection, READ_CHUNK routing repair, and async local LALM provider polling.

# CLIENT R73 — Durable 🫙 Message Containers + Paired Conversational LALM
Checkpoint: `INT-LALM-CHAT-OBSERVATORY-164A` · VC199 · `2.1.27-lalm-chat-containers-r73`

- Replaces the R72 crash-prone secondary code-structure editor with a single portable structural syntax: `[🫙]selected text[/🫙]`.
- Composer 🫙 acts directly on the current `TextFieldValue`: non-empty selection wraps exactly that range; cursor/selection anywhere touching an existing container unwraps that whole container.
- Historical/imported/user/assistant/LALM plain-text segments are selectable in-place. Pressing the message 🫙 control persists a non-destructive effective-text overlay and immediately recomposes the message; original provenance stays recoverable.
- Rendered containers expose `🫙 REMOVE` plus COPY-content-only. Legacy/imported fenced Markdown continues to render and can be unwrapped through the same control path.
- Adds unit coverage for exact wrapping, inside-container unwrapping, intersection unwrapping, and imported fenced-code unwrapping.
- Preserves R72 progressive history/cache behavior, direct newest-message thread opening, wide timestamped chat, admin Observatory mirror, Google configuration path, and the device-proven GPT↔Android LALM transport.
- Pairs with SERVER R107, which repairs conversational generation selection, same-device bootstrap authorization, native provider health reporting, and LALM Observatory readability.
- Fresh R73 compile/APK/device acceptance remains external Auto Forge evidence and is not claimed by this source checkpoint.

# CLIENT R72 — R71 UI Compile Repair
Checkpoint: `INT-RUNTIME-STREAM-OBSERVATORY-COMPILE-163B` · VC198 · `2.1.27-stream-history-observatory-compile-r72`

- Auto Forge selected and verified R71 correctly, then `:app:compileDebugKotlin` exposed four source-call errors in `ClientShellScreen.kt`.
- The live LALM committed-text bubble now calls `ChatBubble` with explicit `threadId` and `message` arguments, using the live request ID as an isolated structure-overlay namespace.
- `SettingLine` now provides an empty default trailing composable so read-only Observatory rows compile without dummy call-site lambdas.
- R71 progressive history, instant-newest thread opening, wide timestamped rich chat, 🫙 code containers, Google public-ID configuration, and admin-gated SERVER Observatory behavior are preserved unchanged.
- SERVER R106 remains the paired SERVER and is not revised by this compile repair.
- Fresh R72 Android compile/APK/device acceptance remains external Auto Forge evidence and is not claimed by this source checkpoint.

# CLIENT R71 — Runtime Streaming, History & Admin Observatory
Checkpoint: `INT-RUNTIME-STREAM-OBSERVATORY-163A` · VC197 · `2.1.27-stream-history-observatory-r71`

- App-scoped IO history runtime publishes recent thread headers first, keeps the cache alive across menu changes, and progressively exposes older headers without repeating a cold history load on every HISTORY press.
- Existing threads initialize the lazy chat list directly at the newest message instead of visibly animating through the entire historical timeline.
- Chat messages use near-full usable width, retain per-message timestamps, parse fenced Markdown code into 🫙 code containers, and provide copy-code-only controls.
- Users can select a range in the composer or an existing/historical message and convert it into a code container. Historical/imported records keep immutable original provenance; the structured presentation is a removable local overlay.
- The AI fallback/bootstrap path resolves those structure overlays so selected code is represented as fenced code/data rather than silently flattened.
- CLIENT Observatory is visible only while SERVER reports this node as ACTIVE `SWRLZ_ADMIN_OPERATOR`, TRUSTED and BOUND. The app-scoped Observatory runtime continues hydrating node, thread and SERVER-log state while menus change.
- Google OAuth web client ID can come from compatible build aliases or a user-entered public identifier in Account & Sync. Local-only operation remains supported.
- R70/R69 GPT→Android LALM transport behavior and R68 bounded archive/account safeguards are preserved.
- Fresh R71 Android compile/install/device validation is external Auto Forge evidence and is not claimed by this source checkpoint.

# Release Notes — CLIENT CFv2.1.27 R67

## INT-CLIENT-BUILD-COMPAT-160A
CLIENT R67 is a build-compatibility successor to R66. APK Router successfully resolved R66, verified its strict metadata/checksum pair, and marked it build-eligible, but Gradle stopped at AAR metadata validation because `androidx.credentials:credentials:1.6.0`, `credentials-play-services-auth:1.6.0`, and transitive AndroidX Core 1.15.0 require API 35; Credential Manager additionally requires Android Gradle Plugin 8.6.0 or newer.

R67 preserves R66 runtime/features and changes only the Android build floor:
- AGP `8.5.2` → `8.6.1`
- `compileSdk` `34` → `35`
- `targetSdk` remains `34`
- Gradle wrapper remains `8.7`
- Credential Manager remains stable `1.6.0`

Paired SERVER remains R101; no SERVER source change is required. APK/device success remains pending a fresh APK Router run.

# Release Notes — CLIENT CFv2.1.27 R65

## INT-SEMANTIC-TOOL-MERGE-JERRY-158A
CLIENT R65 is the presentation/continuation companion to SERVER R100. It keeps R64's durable TOOL/MISSION envelope normalization unchanged while making semantic clarification and Jerry/self-preservation states explicit in the chat status surface. Clarification questions are still normal completed assistant turns, so the user's next message can resume the same SERVER thread; the client does not treat that answer as approval or execution authority.

No APK build/install/device success is claimed by this source checkpoint.

# 2.1.27 Tool Executor Bridge — R64

- `versionCode`: `190`
- `versionName`: `2.1.27-tool-executor-schema-observatory-r64`
- Generic allowlisted TOOL/MISSION envelopes are normalized into canonical Archive/Directory/Log VFS requests instead of disappearing after durable inbox cursor advancement.
- `swrlz_archive_repack` normalizes to `REPACK_SELECTED` for the local conversation-only ZIP workflow.
- Unsupported routed tool envelopes return explicit correlated error evidence.
- R63 Forge live inbox auto-selection and exact-plan destructive safety remain preserved.
- Android APK/device acceptance remains separate evidence.

# 2.1.27 Exact Filename + App-Private Directory Toggle — R59

- `versionCode`: `185`
- `versionName`: `2.1.27-approval-private-root-r59`
- File-backed Directory VFS creation now preserves the exact requested leaf filename; `SWRLZ_TEST_1MB.bin` no longer intentionally passes through MIME-based extension synthesis that could create `.bin.bin`.
- Adds an OFF-by-default `CLIENT App-Private Data` toggle in Archives & Data and Permission Centre. It exposes only this app's own sandbox (`/data/user/0/sh.swurlz.core`) as opaque grant `client-app-private`.
- Android sandbox truth is explicit: the whole `/data/user/0` tree and other apps' private directories remain inaccessible to a normal non-root app.
- App-private access is READ-ONLY, recovery-disabled, never auto-defaulted, and marked as a sensitive scope in CLIENT advertisements.
- R58 Downloads actual-write advertisement, exact-plan destructive approval, recovery semantics, Deep Dig, and durability work remain preserved.
- Device acceptance remains pending until APK Router/device testing.

# 2.1.27 Fixable Issues Phase 1 — R58

- `versionCode`: `184`
- `versionName`: `2.1.27-fixable-issues-phase1-r58`
- Built-in Android Downloads now advertises actual filesystem write authority only when enabled + All Files + root `canWrite()` are all true; exact-plan destructive approval remains mandatory and recovery remains disabled.
- Downloads authority changes trigger immediate best-effort SERVER re-advertisement instead of waiting only for the next heartbeat.
- Adds per-shard resumable conversation-only archive research receipts with `INDEX_READY` / `BODY_PARTIAL` / `BODY_RECONCILED` coverage truth and hostile 25-boundary resume tests.
- Adds AtomicFile-backed active LALM stream recovery journal; process death preserves partial committed presentation separately and never promotes it to completed history.
- CLIENT chat-history snapshots now use AtomicFile commit/backup recovery. Whole-history write amplification remains a separate P1 migration item.
- Failed/cancelled streamed text is labeled `PARTIAL COMMITTED PREFIX · NOT A COMPLETED TURN`.
- Source/harness checkpoint only; Android compile/APK/device acceptance remains separate.


## INT-DIRECTORY-DOWNLOADS-ROUTING-148A — CLIENT R57

See `INT-DIRECTORY-DOWNLOADS-ROUTING-148A_IMPLEMENTATION_REPORT.md` and patch notes for the built-in Android Downloads toggle / approval-mode routing repair and validation evidence.

# INT-LIVE-ACTION-PERMISSION-UX-147A — CLIENT CFv2.1.27 R56 · VC182

- `versionName`: `2.1.27-live-action-storage-permissions-r56`
- Parent: CLIENT R55 SHA-256 `ef9b116db29666b31d7eef587af7b48a7b408b71cae730df0843653bd28b429c`.
- Persistent CLIENT notification card consumes live action state; separate Android tool notifications and right-side bubble mirroring are independently toggleable.
- Notification verbosity applies to every surface while preserving safety-critical approval/failure visibility.
- Permission Centre and Archives & Data add scoped Downloads/default-directory onboarding plus a Directory Analysis master switch; mutating operations still require explicit grant identity.
- R55 recovery, concurrency, append, Deep Dig and destructive-safety behavior is preserved; 54/54 preservation assertions pass.
- Source/static candidate only. Gradle 8.7 wrapper acquisition is unavailable in this sandbox; no APK/install/deployment/promotion claim.

# INT-DEEP-DIG-OPERATIONAL-CONTROL-145A — CLIENT CFv2.1.27 R54 · VC180

- `versionName`: `2.1.27-deep-dig-control-r54`
- Parent: CLIENT R53 SHA-256 `c63df10f663af89fb2cd369c5d089d224f660ace963749d099276c52a2eef8ad`.
- Pair: SERVER R85 / VC208.
- Adds one-pass `CORPUS_AGGREGATE` role/corpus totals for messages, characters, words, lexical tokens, estimated model tokens and 160-character SMS equivalents.
- Adds seedless `NEOLOGISM_ANALYZE` with root/stylization/edit-near clustering, recurrence, first/last evidence and user↔assistant mutual-adoption evidence; strong labels require creative morphology/family evidence.
- Optimizes single-word FUZZY search by preparing messages once and comparing against token vocabulary rather than whole-body edit distance; date bounds accept YYYY-MM-DD and normalize accidental epoch seconds.
- Directory/Archive VFS adds exact live mutation-plan hash approval; bounded destructive inventory fails closed if it cannot be fully verified. Directory adds safe idempotent `APPEND_TEXT`.
- Adds CLIENT tool-action notifications and TOOLS logger controls without exposing hidden reasoning or secrets.
- Source/static candidate only. Gradle compilation was blocked before toolchain execution because the wrapper distribution host is unavailable in this sandbox; no APK/install/device/deployment/promotion claim.

# INT-TUNNEL-LALM-NODE-ADMIN-144A — CLIENT CFv2.1.27 R53 · VC179

- `versionName`: `2.1.27-observation-freshness-r53`
- Pairs with SERVER R83.
- Adds the paired safe V2 execution-state vocabulary for permission preflight, capability discovery, state validation, mutation-triggered revalidation, and result verification.
- Preserves R52 Deep Dig corpus search/aggregation/timeline/concept-lineage/thread reconstruction.
- Hidden reasoning remains excluded; the added trace is operational telemetry only.
- Evidence boundary: source/static only; no APK/device/deployment claim.

# INT-DEEP-DIG-ANALYSIS-FABRIC-143A — CLIENT CFv2.1.27 R52 · VC178

- `versionName`: `2.1.27-deep-dig-r52`
- Parent: CLIENT R51 SHA-256 `6c7bda0ca55deae9448c01c2a9c9fc7d8829810e192b4cba3bdab491e4726338`
- Pair: SERVER R81 / VC204.
- Archive VFS gains bounded GPT-export Deep Dig operations: exact/regex/fuzzy/transparent lexical-semantic message search, aggregation, timeline, concept-lineage evidence, messageId/parentId thread reconstruction and magic-byte entry identification.
- Filters are message-grounded where possible: role, recorded model slug, date range, title, conversation ID, message length and per-message attachment presence; results retain snippets and archive/conversation/message provenance.
- Aggregation separates matching messages from unique message IDs/conversations/days and groups by role/month/conversation with first/last occurrence evidence.
- Transparent evidence profiles surface candidate support/concern/encouragement/disagreement/correction/humor/creative/technical/identity/persona/preference/promise/unresolved-task evidence without asserting psychological or relational conclusions.
- Existing persistent ArchiveIndexStore reuse is complemented by a bounded query-result cache keyed to the archive/index/query fingerprint; this is not mislabeled as a full FTS/vector index.
- R51 directory allocation and transactional mutable Archive VFS are preserved. Source/static checkpoint only; Gradle 8.7 download was blocked before compilation by `UnknownHostException`. No APK/install/deployment/promotion claim.

# INT-LALM-CAPABILITY-FABRIC-142A — CLIENT CFv2.1.27 R51 · VC177

- `versionName`: `2.1.27-capability-fabric-r51`
- Parent: CLIENT R50 SHA-256 `bd87ba3d35a3337fc50d4e087b59c250c20e9549fbe092b510f405f5af15461a`
- Pair: SERVER R80 / VC203.
- Adds write-aware Archive VFS selection and transactional top-level ZIP mutation: WRITE_TEXT, MKDIR, COPY, MOVE, RENAME, DELETE and REPACK with structural/SHA verification plus rollback protection. Nested archive-in-archive mutation fails closed; nested reads remain supported.
- Adds bounded Directory VFS `ALLOCATE` up to 4 GiB with sparse-seek or zero-fill execution and exact resulting-size verification, avoiding unnecessary tunnel transfer for large local test files.
- CLIENT presence now advertises `archive.write` separately from `archive.read`; archive and directory mutation remain local-grant + capability + explicit-consequential-confirmation gated.
- Preserves R50 semantic orchestration, schema-2 operational stream, evidence gating and STOP/retry quiescence.
- Source/static checkpoint only; no APK/install/device/deployment/promotion claim.

# INT-LALM-TOOL-ORCHESTRATION-141A — CLIENT CFv2.1.27 R50 · VC176

- `versionName`: `2.1.27-tool-orchestration-r50`
- Parent: CLIENT R49 SHA-256 `78eb12adc0780bedbcf8a75963bd91e15e7020470ec31bffdb0c653c662e44f9`
- Pair: SERVER R79 / VC202.
- Routes actionable Forge/GitHub and File Analysis Lab language through the typed SERVER tool-control path while preserving bare Forge UI navigation.
- Protocol V2 schema 2 adds safe STATUS telemetry for suite/operation/capability/risk/plan/execution/evidence/answer state; hidden reasoning remains excluded.
- Tool-plan UI distinguishes review, waiting-for-executor, evidence-ready and rejected states; `NOT_REQUIRED` confirmation never implies execution.
- STOP/retry/replacement uses bounded SERVER cancellation-drain coordination to prevent stale native ownership from becoming an immediate retry `LALM_BUSY` race.
- Deterministic capability-catalog answers can complete without native decode.
- Source/static checkpoint only; no APK/install/device/workflow/deployment/promotion claim.

# INT-LALM-INTERACTIVE-MEMORY-137A — CLIENT CFv2.1.27 R47 · VC173

Pairs with SERVER R75. CLIENT keeps one protocol-2/schema-1 LALM stream, accepts content-free heartbeat phases during bounded reference-CPU work, preserves first-token/first-text/start-to-finish timing, and renders opaque memory decisions plus explicit plan-scoped tool review outside assistant-authored content.

- `versionName`: `2.1.27-lalm-interactive-memory-r47`
- Reference-CPU prefill/generation no longer terminates with `LALM_REFERENCE_CPU_INTERACTIVE_GUARD` on the paired V2 route.
- Memory IDs/content-safe decisions and tool plan/result correlation are additive safe-default fields; older schema-1 payloads still decode.
- `APPROVE PLAN` records approval only. The UI explicitly says that approval is not invocation or success; a separate capability-authorized executor must record result evidence.
- CLIENT logs every validated stream event and terminal/decision outcome without prompt or assistant content.
- No APK build, install, device test, workflow, deployment, executor run, or production promotion is claimed.

# INT-LALM-STREAM-TRUTH-136A — CLIENT CFv2.1.27 R46 · VC172

Pairs with SERVER R74. CLIENT now consumes one additive protocol-2/schema-1 LALM stream for direct and generated answers, supplies thread/ingress context, renders operational phases outside assistant content, and shows/persists start-to-finish plus first-text timing. Event logs correlate endpoint, request, thread, sequence, route, Truth Capsule ID, and timing without recording prompt or response content.

The V1 completed route remains an older-SERVER compatibility fallback. No APK, Android compile, install, device, workflow, release, deployment, or production-promotion result is claimed; Gradle verification was blocked before compilation because Gradle 8.7 was uncached and its distribution host was unreachable.

# INT-LALM-ROUTING-RUNTIME-135A — CLIENT CFv2.1.27 R45 · VC171

- candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R45`
- parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R44` · SHA-256 `cf945429cfbb3e6f2c2890407848047b2cb33ab9c76b04124221ca94fdc05223`
- sibling: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R73`
- versionName: `2.1.27-lalm-routing-r45`
- checkpoint: `INT-LALM-ROUTING-RUNTIME-135A`

## Live SERVER route repair

- The SERVER endpoint proven healthy by process reconciliation is now the operational endpoint for Core, Chat and LALM APIs while its heartbeat remains fresh and ONLINE.
- The configured Core Node URL remains the durable preference and fallback; the runtime override is not persisted as a silent configuration rewrite.
- LALM stream startup records `stream_endpoint_resolved` with request/thread correlation so future transport failures show the exact route actually used.
- This repairs the field condition where registration/heartbeat succeeded over `127.0.0.1:8787` but Chat still opened its stream against a stale LAN address such as `192.168.1.181:8787`.

## Evidence boundary

CLIENT R44 already built successfully in workflow `31747287191`. R45 changes CLIENT routing behavior and therefore requires a new authoritative APK Router build. No installation, promotion or deployment is claimed by source preparation.

# INT-REGISTRATION-LALM-134A — CLIENT CFv2.1.27 R44 · VC170

- candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R44`
- parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R43` · SHA-256 `f75003c06f2cfe905b61323f3fabed1ea4713cd061ea8d00b54cc802be7d3c8c`
- sibling: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R71`
- versionName: `2.1.27-registration-lalm-r44`
- checkpoint: `INT-REGISTRATION-LALM-134A`

## Changes

- Startup registration reconciliation now performs a bounded local loopback probe before falling back to the configured LAN endpoint. A co-resident SWRLZ SERVER that answers with a valid SWRLZ registration/heartbeat response is selected for the session.
- `PROOF_REBIND_REQUIRED` / `PROOF_MISMATCH` recovery now emits distinct `proof_rebind_begin` and `proof_rebind_end` diagnostic evidence with protocol code, status, elapsed time and canonical node identity.
- Duplicate CLIENT chat snapshot saves are de-duplicated at the diagnostic layer so one logical message commit does not appear twice merely because Compose/state persistence called `saveMessages` twice.
- R43 hierarchical Developer Logger controls and the persistent `CLIENT · CFv2.1.27 · R44 / VC170` revision footer are preserved.

## Evidence boundary

The change is prepared from R43 source. Android compilation/signing remains the APK Router acceptance gate. No installation, promotion or deployment is claimed by source preparation.

# INT-DEVLOGGER-FORGE-133A — CLIENT CFv2.1.27 R43 · VC169

- candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R43`
- checkpoint: `INT-DEVLOGGER-FORGE-133A`
- versionCode: `169`
- direct parent: CLIENT R42 / SHA `60a602529905ab30435a7668c7a6fe999c673ed0b81e31a955ac9da74baffc28`
- sibling prepared with this feature update: SERVER R70
- changes: hierarchical Developer Logger master/menu/submenu switches; bounded rotating log clear/export controls; visible CLIENT revision in the persistent footer; stale direct-build workflow identity refreshed.
- preserved: R42 registration reconciliation, LALM stream diagnostics, archive/analysis behavior, Truth Firewall and approval boundaries.
- Android build: pending authoritative APK Router rebuild.

## CLIENT R42 — INT-FIX-CLIENT-LOGGER-COMPOSE-132B

Authoritative APK Router workflow `31732692488` reached `:app:compileDebugKotlin` and exposed one CLIENT-only compile blocker in the new full-log Settings panel: the explicit `androidx.compose.foundation.layout.weight` import resolved to an internal `RowColumnParentData` helper in this Compose toolchain. R42 removes that import and preserves the R41 observability, registration continuity, LALM diagnostics, and SERVER R68 pairing unchanged. SERVER is intentionally not incremented.

## CLIENT R41 — INT-OBSERVABILITY-RECONNECT-LALM-132A

Full-pair update paired with SERVER R68. Adds an app-private rotating NDJSON full diagnostic log with Settings export, detailed chat/LALM stream events, and registration/rebind/heartbeat traces. Repairs in-place update reconnect by reconciling persisted enrollment on process start rather than trusting a stale `ONLINE` preference after the process-local heartbeat job has died; the heartbeat loop can also re-register after conclusive registration-loss responses. Provider status now recognizes canonical `lalm` SERVER identity and avoids false `NO SERVER MODEL`/SERVER-offline presentation caused by the R67 provider rename. Explicit manual disconnect remains authoritative and no raw device proof or credential is written to logs.

## CLIENT R39 — INT-ANALYSIS-LAB-130A

Pairs with SERVER R65. Implements all three parked Analysis Lab export improvements: exact conversation shard classification (`conversations.json` / `conversations-\d{3,}.json`), separate `shared_conversations.json` references, exclusion of `conversation_asset_file_names.json`, ZIP-magic mounting of opaque `.dat` attachments with filename/MIME metadata used only as hints, and bounded provenance-preserving development-cycle analytics. R38 LALM PROBING UX, persistent Archive Index, streaming and safety gates are preserved. Android APK Router/device acceptance remains pending.

## CLIENT R38 — INT-AI-SWRLZX-013A

Adds truthful native-model probing UX: when SERVER reports the SWRLIE/LALM provider as PROBING before Model Rack selection is committed, Chat shows the discovered LALM model with `PROBING` instead of incorrectly saying `NO SERVER MODEL`. Preserves R37 Archive Index behavior and streaming client runtime. Paired with SERVER R64 / VC187.

## CLIENT R37 — INT-BUILD-VERSION-129A

Version-only canonical refresh of R36. Advances CLIENT to R37 / VC163 with a clean canonical source filename while preserving the R36 persistent Archive VFS index, FD-native ZIP/ZIP64 seek, direct indexed entry reads, LALM contracts, and all runtime behavior unchanged. Paired with SERVER R63 / VC186.

## CLIENT R36 — INT-ARCHIVE-INDEX-128A

Fixes the giant-archive Archive VFS timeout path exposed by the 6.25 GiB `§wyrlzx.zip` export. CLIENT now builds one persistent SQLite outer-archive catalog in the background, advertises `BUILDING/READY/FAILED/STALE` index state, and serves root `INFO/TREE/LIST` plus conversation-candidate discovery from the local catalog instead of rescanning the source ZIP on every tunnel request.

A new pure-Kotlin ZIP/ZIP64 central-directory parser reads the granted SAF file descriptor directly, bypassing the fragile `/proc/self/fd -> ZipFile` reopen path. Seekable providers record each entry's local-header offset so `READ`/conversation operations can jump directly to the requested entry and inflate only its compressed bytes. Non-seekable providers fall back to one background sequential indexing pass; request threads return retryable `ARCHIVE_INDEX_BUILDING` rather than spending the 300-second tunnel window walking gigabytes. Nested archives remain bounded/on-demand after the outer catalog is READY.

Focused JVM regression evidence passes ZIP64 entry-count parsing (66,001+ entries) and direct DEFLATE seek/read. Core Archive VFS Kotlin compiles against Android/API stubs. Full Android Gradle compilation could not start because the wrapper distribution host is unavailable in this environment; authoritative APK/workflow/device acceptance remains pending. SERVER R61 is the paired sibling and adds fail-fast routing from the CLIENT-advertised archive index state while leaving archive bytes on the CLIENT.

## CLIENT R35 — INT-AI-SWRLZX-012B

Repairs the authoritative GitHub Kotlin compile blockers exposed after 012A: Ktor stream cleanup now supplies the required cancel cause argument, and suspend CLIENT-context capture now executes inside the existing coroutine before stream start. SERVER R60 pairs with the explicit serializer repair. LALM parity semantics and production gates are unchanged; authoritative Android rebuild is pending.


## CLIENT R34 — INT-AI-SWRLZX-012A

Exact canonical GGUF↔LALM format/tensor/tokenizer/reference numerical parity is proven on real pinned bytes. `swrlzx.lalm.parity.v1` now requires structured legacy-engine/device evidence before production parity can be marked. Android/device promotion remains pending.
# INT-AI-SWRLZX-011A — CLIENT R33 / VC159

R33 pairs with SERVER R58 on the first-party LALM native architecture reference execution foundation. CLIENT carries the byte-identical runtime/operator contracts and 011A conversion/bring-up evidence so Model Rack and future parity surfaces share the same semantics, but CLIENT does not gain model-execution or promotion authority. Exact canonical model execution/tokenizer parity, GGUF↔LALM parity, Android performance and production promotion remain open.

# INT-AI-SWRLZX-010A — CLIENT R32 / VC158

R32 pairs with SERVER R57 on `SWRLZ-LALM-001A` real-model bring-up. The UI now distinguishes the SWRLZ-native LALM family from LFM source provenance and reports the 010A bring-up phase, source readiness, target presence, parity state and selection state. The exact 229 MB source conversion remains pending direct source-byte verification; CLIENT does not gain model execution or promotion authority.

# INT-AI-SWRLZX-009A — CLIENT R31 / VC157

R31 pairs with SERVER R56 for checkpoint-9 advanced runtime. CLIENT carries the byte-identical `swrlzx.advanced-runtime.v1` and Model Rack contracts and now displays the SERVER-negotiated advanced runtime state: enabled capabilities plus explicit target-only/CPU fallbacks. The CLIENT does not gain model execution authority. Full optimized-LFM2 tensor KV/prefix reuse, production speculative/accelerator execution and Android device/thermal acceptance remain open.

# INT-AI-SWRLZX-008A — CLIENT R30 / VC156

R30 pairs with SERVER R55 on immutable SWRLZX model evolution. CLIENT carries the byte-identical evolution contract and V3 paired-LAN control routes, can inspect logical active/known-good identities and candidate stages, and exposes request helpers for registration, evaluation, explicit promotion and rollback. Training completion never promotes a candidate, hidden reasoning cannot be training truth, and unknown/unimplemented overlay application remains fail-closed. Exact optimized LFM2 Android parity/deployment remains open.

# INT-AI-SWRLZX-007A — CLIENT R29 / VC155

R29 pairs with SERVER R54 on SWRLZX native-default Model Rack migration. CLIENT now receives model `format` and `runtimeRole`, presents SWRLZX as the native/default contract, labels GGUF as bounded legacy emergency compatibility, and preserves explicit rollback/activation controls. The exact optimized 229 MB SWRLZX model/device parity gate remains open.

# INT-AI-SWRLZX-006A — CLIENT R28 / VC154

R28 completes the CLIENT side of live SWRLZX response streaming. Successful V2 chat responses are parsed incrementally through Ktor `bodyAsChannel()`/bounded NDJSON lines and applied to an exact sequence/identity state machine. An application-scoped stream runtime exposes microbatched 32 ms `StateFlow` snapshots to a transient Compose assistant bubble, handles RESET/cancel/failure/reconnect semantics, and persists assistant text only after terminal COMPLETED.

The existing V1 completed-response call remains as an explicit 404/405/501 compatibility fallback. One automatic retry is allowed only before committed text; post-delta replay is fail-closed until a resume-offset contract exists. SERVER R53 preserves R52 transport behavior and pairs the 006A lineage. Android device/LAN/process-death acceptance remains pending.

# INT-AI-SWRLZX-005A — CLIENT R27 / VC153

R27 pairs with SERVER R52 and carries the byte-identical `swrlz_llm_stream_v2` contract, wire/authority/ADR documentation, and transport evidence boundary. SERVER R52 can now flush committed model deltas over authenticated chunked NDJSON with bounded backpressure, cancellation and disconnect cleanup.

CLIENT network consumption is intentionally unchanged in 005A: the existing completed-response path remains the compatibility behavior. `bodyAsChannel()` parsing, stream state and live Compose rendering belong to 006A.

# INT-AI-SWRLZX-004A — CLIENT R26 / VC152

Checkpoint 004A adds the first native SWRLZX token-streaming foundation. The native reference executor/engine now emits token and draft events incrementally, uses strict cross-token UTF-8 assembly, and supports decode-boundary cancellation. A deterministic streaming Truth Firewall holds a bounded tail and is the only layer allowed to produce presentation-safe `CommittedDelta`; rejected drafts emit `Reset(regenerate=true)`.

This candidate does **not** yet stream over SERVER HTTP or render live CLIENT chat. Those remain 005A/006A. GGUF remains the compatibility fallback and optimized-LFM2/device acceptance remains open.

# INT-AI-SWRLZX-003A — CLIENT R25 / VC151

CLIENT R25 directly succeeds R24 SHA-256 `aee8af624f4e348cf6bbb0ef9958da81846b5288f172c049feb17b173c54aa76` and pairs with SERVER R50. It carries the byte-matched SWRLZX runtime/graph/tokenizer/quantizer contracts, checkpoint documents and verification tooling needed to understand the SERVER native-runtime state without moving model execution authority onto CLIENT.

Streaming transport/UI remains checkpoint 005A/006A work; CLIENT R25 does not claim local native model execution.

# CLIENT CFv2.1.27 R24 / VC150 — INT-AI-SWRLZX-002A

R24 pairs with SERVER R49 on the deterministic GGUF → SWRLZX conversion bridge. It carries the byte-identical shared conversion/provenance contract, exact optimized-source identity, conversion mapping documentation and verification tooling so future CLIENT inspection/stream negotiation sees the same source-to-container lineage as SERVER.

The CLIENT does **not** switch its chat/runtime path to SWRLZX in 002A. Native model execution begins only after checkpoint 003A parity evidence.

# CLIENT CFv2.1.27 R23 / VC149 — INT-AI-SWRLZX-001A

## Native SWRLZX container foundation

R23 pairs with SERVER R48 to establish the shared first-party `.§wyrlzx`/`.swrlzx` model-container contract. The CLIENT does not run or convert the model yet; it receives the same parser/schema contract now so future model inspection, streaming capability negotiation and runtime status use one exact file definition on both sides.

- Adds byte-identical `swrlzx-contract` core/metadata sources shared with SERVER R48.
- Defines authoritative SWRLZX magic, fixed V1 header/TOC, required manifest/tensor-directory/lineage/integrity sections and reserved stream/runtime section IDs.
- Adds section SHA-256, deterministic root digest, alignment/non-overlap/bounds checks and architecture-neutral tensor descriptors.
- Adds the staged roadmap through GGUF conversion, native inference, incremental Truth Firewall streaming, SERVER transport, CLIENT live rendering, GGUF deprecation and immutable model-generation evolution.
- Preserves R22 Selective Directory VFS, Archive VFS, Forge transfer and all existing trust/permission/Truth Firewall boundaries.
- No GGUF conversion, neural inference change, live response streaming, APK/device acceptance, model training or deployment is claimed by 001A.

# CLIENT CFv2.1.27 R22 / VC148 — INT-OBSERVATORY-DIR-VFS-126A

## Selective Directory VFS + bounded recovery

R22 pairs with SERVER R46 and preserves the R21 forensic baseline. A new **Archives & Data → Selective Directory VFS** section lets the user grant exact Android directory trees without exposing their SAF URI/device path to SERVER or ChatGPT.

- Grants start READ-ONLY. Write and deleted-file-recovery authority are separate local toggles and are revoked immediately when the grant is removed.
- Background protocol-2 worker now accepts fail-closed `swrlz-directory-query-v1` operations only with the exact requested `directory.read`, `directory.write`, or `directory.recovery.read` capability.
- Supports bounded info/tree/list/read/search and whole-directory structural analysis, plus confirmed create/write/mkdir/copy/move/delete operations trapped inside the selected grant. `..`, absolute/escaping paths, cross-grant operations and root deletion are rejected.
- Copy/move are bounded to 5,000 entries / 256 MiB per operation; text writes are bounded to 4 MiB; remote responses remain <=512 KiB.
- Recovery scan can inspect Android MediaStore trash records scoped to the selected external-storage tree and trash/temp/orphan-like remnants already visible inside the grant. Restore is best-effort into the same grant. Raw deleted flash/block recovery is explicitly unavailable on stock Android due to sandbox/FBE/TRIM boundaries unless a future privileged helper is enabled.
- Registration/heartbeat advertise only opaque grant ID/name/readiness/write/recovery bits; local URIs stay local. R19 Archive VFS and R21 Forge hardening remain intact.

## Validation boundary

Source/static validation is recorded in this candidate. GitHub Actions remains the compile/stable-sign gate if Gradle dependency bootstrap is unavailable. Device/tunnel acceptance is pending.

# INT-FORENSIC-REPAIR-125A

CLIENT R21 / VC147 forensic hardening pass. Repairs stale runtime identity, content-binds Forge pending transactions, rejects transaction-marker reconciliation unless staged paths verify exactly, revalidates repository mutation preconditions across branch races, retries automated Forge once after OAuth refresh, and replaces large GitHub Actions artifact/log ByteArrays with bounded file-backed streaming and APK extraction. R20 registration/Archive VFS behavior is preserved.

# R20 — Registration Hot-Path Isolation

Live R19 device evidence showed discovery reachable while enrollment timed out. R20 makes connection establishment independent of Archive VFS readiness.

- Registration sends identity/proof/capabilities only; archive advertisements begin on the immediate heartbeat after registration.
- Registration read timeout increases from 1.5 s to a bounded 5 s; heartbeat uses 2.5 s.
- Archive presence no longer opens every SAF document on each heartbeat. Persisted URI read permission is the cheap readiness signal; actual Archive VFS query opens remain authoritative.
- The first heartbeat is immediate, then the existing 10 s cadence continues.
- R19 Archive VFS engine, nested ZIP/ZIP64 reads, streaming conversation parser, R18 MAX/AUTO transfer behavior, proof recovery and Truth Firewall are preserved.

Paired SERVER: R44 / VC167.

# CLIENT CFv2.1.27 R19 / VC145 — INT-ARCHIVE-VFS-123A

R19 turns CLIENT into a local Archive VFS node. Large ZIP/ZIP64 exports remain on-device and can be progressively mapped/read through bounded SERVER/ChatGPT queries without uploading or extracting the entire archive.

## Changes
- Adds **Archives & Data** settings with Android document-picker registration and persistable read access; local document URIs are never advertised.
- Advertises only opaque `archiveId`, name, size, format/readiness and index status during registration/heartbeat.
- Adds a background protocol-2 archive query worker using `archive.read` / `archive.vfs.v1`, durable inbox cursors and correlated replies.
- Adds generic Archive VFS ZIP/ZIP64 info/tree/list/direct-read operations with nested `!` paths and cursor pagination.
- Adds streaming `JsonReader` conversation catalog and per-conversation retrieval for OpenAI-style exports without loading giant JSON arrays into memory.
- Enforces 512 KiB response ceiling, 256 KiB text windows, bounded message/tree counts, provenance and machine-readable errors.

## Validation boundary
The archive engine deliberately does not perform full archive extraction or 7 GB transfer. GitHub Actions remains the APK compile/sign gate; large-export acceptance is pending device testing.

# CLIENT CFv2.1.27 R18 / VC144 — INT-TRANSFER-MAX-TUNNEL-121A

## Accepted live R39/R17 evidence

The matched R39/R17 100 MiB localhost benchmark passed `DEVICE_BINARY_STREAM_V2` using one payload request. End-to-end time was 21,141 ms at 4,959,916 B/s (~4.73 MiB/s overall), with the streaming request itself completing in 17,764 ms. This is roughly a 4.7x overall improvement over the prior R38/R16 100 MiB request-per-chunk run (~98.7 s / ~1.01 MiB/s).

## R18 changes

- Expands local stream benchmark choices to 256 KiB, 512 KiB, 1 MiB, 2 MiB, 4 MiB, `AUTO`, and `MAX`.
- `AUTO` resolves by payload size (512 KiB for small, 1 MiB at 10 MiB, 2 MiB at 50 MiB, 4 MiB at 100 MiB); `MAX` resolves to 4 MiB.
- Streaming-v2 remains one payload HTTP request. Older SERVER peers still use the existing <=512 KiB resumable fallback chunk ceiling.
- Corrects the stream SHA diagnostic key from `incrementalShaVerified` to SERVER's authoritative `incrementalSha256Verified`.
- Benchmark summaries now include resolved buffer size, SERVER read count, fsync/checkpoint milliseconds, sync count, request timing, and explicit SHA verification status.
- Generic staged-file streaming can consume SERVER-advertised stream buffers up to 4 MiB without whole-file allocation.
- R18 pairs with SERVER R40 tunnel/native-file settings so the next acceptance can compare localhost MAX/AUTO against the ChatGPT/plugin `SERVER_HTTPS_PULL` lane.

## Validation boundary

Android Gradle compilation was attempted but could not begin because `services.gradle.org` is unreachable from this environment. GitHub Actions remains the compile/sign gate. No R18/R40 MAX/tunnel speed claim is made before device acceptance.

# CLIENT CFv2.1.27 R17 / VC143 — INT-STREAM-BOOTSTRAP-120A

## One-body binary stream + localhost/tunnel benchmark parity

R17 pairs with SERVER R39 after R38/R16 live tests passed 1/10/100 MiB and isolated request-per-chunk overhead as the dominant remaining cost. The 100 MiB / 256 KiB test completed 400 chunks at ~1.01 MiB/s with average RTT 220.70 ms, while SERVER work averaged only 25.71 ms.

- Generic staged-file uploads prefer SERVER-advertised `DEVICE_BINARY_STREAM_V2`: one `application/octet-stream` request carries the remaining file from a bounded file reader instead of creating a whole-file byte array or issuing hundreds of HTTP requests.
- The loopback benchmark now uses one payload HTTP request when R39 streaming is available. The 4/64/256 KiB selector becomes the CLIENT writer buffer size; older SERVER builds retain binary-chunk/Base64 fallback.
- Benchmark summaries record transport, payload request count, CLIENT buffer count, stream/request RTT, SERVER time, outside-SERVER time, fsync count, presence timing and `/start` timing so localhost and tunnel/plugin acceptance can be compared directly.
- Streaming requests receive a long bounded wall-clock budget while retaining a 120-second idle socket timeout, avoiding the generic 60-second request cutoff for legitimate large/tunnel transfers.
- R16 proof-aware heartbeat/rebind recovery, SERVER trust/admin authority, staged SHA verification, resumable fallback, offline-first behavior and Truth Firewall boundaries remain preserved.
- Parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R16` SHA-256 `2b3ffffc804c32b580d4b07d3c9b9f5d9f7498fb0f6ddef8ed16f8a5e7b69645`. Paired SERVER: R39 / VC162.
- Local Android compilation was attempted but could not begin because `services.gradle.org` is unreachable in this environment. GitHub Actions remains the compile/sign gate; tunnel speed acceptance remains external.

---

# CLIENT CFv2.1.27 R16 / VC142 — INT-TRUST-REINSTALL-119A

## Reinstall proof rebind + canonical node recovery

R16 pairs with SERVER R38 after R15/R37 evidence isolated a stale proof binding: heartbeat was fast, but Forge `/start` failed `PROOF_NOT_BOUND` and Core remained `NOT_ENROLLED / REGISTRATION_FAILED / DISCOVERY_ONLY`.

- Normal registration remains fail-closed; CLIENT attempts `proofRecovery=true` only after SERVER explicitly returns `PROOF_REBIND_REQUIRED` (or legacy `PROOF_MISMATCH`).
- The retry reuses the stable device recovery binding and current installation ID, then stores SERVER's canonical node ID on success.
- Transfer preflight recognizes proof-rebind-required state, performs the controlled registration recovery once, retries BUSY heartbeat, and only then proceeds to `/forge/uploads/start`.
- R15 timed/exportable benchmark diagnostics and R14 raw-binary streaming are preserved.
- SERVER remains authoritative for accepting the rebind and suspending/reapproving any prior admin authority.

# CLIENT CFv2.1.27 R15 / VC141 — INT-TRANSFER-PRESENCE-118A

## Timed presence recovery + zero-chunk diagnostics

R15 pairs with SERVER R37 after the matched R14/R36 localhost test still failed before transferring a single chunk.

- Heartbeat responses retain HTTP status, SERVER protocol code, and elapsed milliseconds.
- Transfer preflight automatically re-registers only when SERVER explicitly returns `NOT_REGISTERED`, then retries the BUSY heartbeat once; transport/auth/admin failures remain fail-closed and visible.
- Loopback NDJSON begins before presence preflight, so failures before `/forge/uploads/start` now leave a viewable/exportable CLIENT log.
- Benchmark results expose presence, registration-recovery and `/start` timing plus the exact failure stage.
- Benchmark status is isolated from generic/source-pair picker status so unrelated selection messages no longer overwrite the actual loopback failure.
- R14 raw-binary streaming, verified-transfer binary path, Dispatchers.IO boundaries, SHA verification, resumability and Base64 fallback are preserved.

# CLIENT CFv2.1.27 R14 / VC140 — INT-TRANSFER-STREAM-117A

- Replaces the preferred same-device CLIENT→SERVER payload path with authenticated raw-binary chunks while retaining the R13 JSON/Base64 route as compatibility fallback for older SERVER builds.
- Sends a proof-bound BUSY heartbeat before generic, loopback-benchmark, and canonical source-pair transfers so a stale presence lease fails or recovers in ~1.5 s instead of letting `/forge/uploads/start` sit until the 60 s request timeout.
- Generic uploads continue to stage once and hash once, then use SERVER-advertised binary chunk capability/path and resumable offsets; bounded retries preserve idempotent lost-response reconciliation.
- Canonical source+metadata transactions prefer `/v1/transfers/chunks/write-binary` with raw bytes and exact per-chunk SHA-256; 404/405 against an older SERVER transparently falls back to the verified Base64 route.
- Public transfer entry points and blocking content/file work are constrained to `Dispatchers.IO`; large files remain chunked/streamed rather than loaded into one whole-file byte array.
- Forge → SERVER benchmark is relabeled `LOCAL STREAM TRANSFER BENCHMARK` and measures `/start → raw binary chunks → commit` on `127.0.0.1:8787`, with transport-aware NDJSON evidence.
- Preserves R13 staging/retry/abort behavior, SERVER verification authority, explicit Forge approval/dispatch boundaries, offline-first behavior, Truth Firewall, and stable-signing workflow expectations.
- Parent source: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R13` SHA-256 `e2cba3996cd45c123e7b90e09d005f2b36504373a3a8a60dbc9e906e054a64c1`. Paired SERVER: R36 / VC159.
- Source/static candidate; Android compile was attempted locally but the Gradle 8.7 distribution could not be fetched in this offline workspace. APK/device acceptance remains the next GDrive→Forge/GitHub test.

---

# INT-FORGE-081A — Dragon Master Workshop and conveyor repair

- repaired malformed ForgeConveyorStateStore Kotlin braces;
- documented §wyrlz / §wyrlix / §wyrver identity roles;
- added Workshop Presence, Invitation Invocations, Dragon Master Theme Zero, §wyrlish, Heat, voice, Theme Anchors, Chronicle, and roadmap boundaries;
- preserved offline-first behavior, Truth Firewall, lineage, approval gates, and compatibility identifiers;
- no APK/build/install/release/deploy claim.

# CLIENT CFv2.1.27 Candidate R5 — Adaptive Forge Project Conveyor Foundation (2026-08-05)

- Adds the adaptive Forge Project Target and operating-mode contracts.
- Adds resumable approval-aware conveyor stages and need-based file-analysis specialist routing.
- Adds fact/inference/projection/recommendation findings, Architecture Genome snapshots, persistent local conveyor state, and thresholded Council review/event models.
- Preserves existing Forge transport, package identity, compatibility identifiers, offline-first behavior, Truth Firewall, and approval boundaries.
- Source/static foundation only; no build, notification dispatch, workflow, GitHub write, install, promotion, release, or deployment is claimed.

# CFv2.1.27 R2 — Forge Progress Truth (2026-08-05)

- Shows byte transfer, GitHub blob acceptance, repository finalization, and completion as separate phases.
- Prevents a 100% byte-send display from being interpreted as a completed repository transaction.
- Preserves 4 MiB resumable source chunking.

# CLIENT CFv2.1.27 Candidate R1 — §wyrlz LLM Bridge

Chat now asks the §wyrlz LLM running on the paired §wyrlzer by default. This replaces the old “I can reason locally first” placeholder with an actual proof-bound answer path while keeping explicit remote-provider choices under the existing approval policy.

CLIENT supplies only useful allowlisted troubleshooting context—version, device/Android model, permission states, connection-check state, and interface preferences. Secrets, URLs, proofs, credentials, content, files, and installed-app data are not part of the contract.

The launcher/app label and primary conversation surfaces now display `§wyrlz`. Internal package/protocol/lineage identifiers remain unchanged for compatibility.

Source-only candidate. Android compilation, APK/device acceptance, workflow, GitHub write, promotion, release, deployment, and installation remain pending separate approval.

---

# CLIENT CFv2.1.26 Candidate R1 — INT-FORGE-054A-R2

- Mirrors the shared Forge build conveyor from SERVER: ASK/CLIENT/SERVER/BOTH/FILES, `BUILD LATEST VERIFIED`, authoritative source-triple resolution, persisted SAF directories, default-on successful-artifact/failure-log downloads, and build ledger provenance.
- Keeps CLIENT Forge usable as the practical updater for repeated SERVER source/build iterations while preserving CLIENT-only legacy Dev Mode, Missions, and client-side capabilities.
- Adds CLIENT-local persistent chat threads with history/new/rename/delete controls and a compact Chat header; SERVER reasoning/evidence remains SERVER-authoritative.
- Adds machine-readable patch/checkpoint lineage and explicit CLIENT/SERVER feature-parity documentation.
- Source-only candidate: no Gradle compile, APK build, GitHub write/workflow, release, deployment, or installation is claimed.

---

# CFv2.1.24 R1 — INT-FORGE-042B

- Forge Transport V2: 4 MiB protected-source chunks, bounded transient per-blob retries, 401 auth/repository reprobe, verified resume, richer diagnostics.
- Repairs missing `@Composable` on `ChatSettingsChoiceGroup` from the CFv2.1.23 R1 build failure.

# CLIENT CFv2.1.23 Candidate R1 — Modular Model Rack + Expression EQ

Brain & AI now includes a paired SERVER model-rack panel. It shows installed GGUFs, identifies the exact optimized SWRLZ Q4, stores separate Speed/Reasoning Depth/Expression EQ profiles for each model hash, toggles prompt/EQ packs and offers profile/model rollback.

Reasoning Depth is labeled honestly: it changes response budget, profile density and validation emphasis; it does not add learned intelligence. The nine EQ sliders shape expression, not truth or authority. SERVER remains authoritative and LAN changes require registered paired control.

The shared source/static/model-identity gates pass `36/36`. Android compilation/APK/device evidence is pending because Gradle 8.7 could not be obtained in this workspace. The GGUF is never bundled in CLIENT.

---

# CLIENT CFv2.1.20 Candidate R1 — Resilient Forge Source Transport

Large protected source ZIPs can now use verified chunk transport instead of one oversized REST Git-blob request. Build eligibility requires the source ZIP only; checksum and manifest companions are optional evidence and remain strict when supplied.

This source candidate does not claim an Android build yet. The official repository router patch is included as a source-only handoff and has not been committed or pushed.

---

# CLIENT CFv2.1.18 — Forge Rescue Profile-Store Compile Repair

Checkpoint: `INT-FIX-039G`

- Repairs the `ClientProfileStore.resolveClientToServer` provider-profile expression that blocked `compileDebugKotlin` in workflow `30302109949`.
- Changes the incorrect function-symbol nullable access `providerProfileId?.let` to the declared `providerId?.let`.
- Audits SERVER CFv2.1.7 profile-store Kotlin; the corresponding SERVER paths are already correct, so SERVER remains unchanged.
- Preserves the CFv2.1.17 default-theme Forge rescue payload and GitHub credential/write-preflight repair.
- Source/static verification only; successful compilation remains pending the next authorized build/workflow.

---

# CLIENT CFv2.1.17 — Forge Rescue / Default-Theme Bootstrap

Checkpoint: `INT-FORGE-039E`

This source-only rescue successor is intentionally transport-light. It preserves the current CLIENT code lineage while exposing only the canonical default `Glitch Dragon Glass` ThemePack at runtime and removing optional ThemePack/ignition payloads from the package so the Forge uploader repair can itself be transported through older CLIENT builds.

## Forge repair

- Preflight now proves authentication, repository read, and `Contents: write` before a large transfer by creating a tiny unreferenced Git blob. The probe does not modify a branch/tree/file.
- A 401 during a later repository operation is no longer automatically interpreted as proof that the credential is revoked. Forge re-probes authentication and preserves the credential when the re-probe succeeds.
- 422 `input was too large` is classified as a transport-size failure, not an authentication failure.
- Sanitized GitHub request ID / accepted-permission evidence is included when supplied by GitHub.

## Temporary bootstrap theme boundary

- Runtime registry selectable set: `Glitch Dragon Glass` only.
- Alternate launcher aliases are removed from the bootstrap Android manifest.
- Optional theme progress, ignition, launcher, Kapanion, and legacy alternate identity artwork is omitted.
- The full declarative ThemePack definitions remain in source lineage for restoration; this bootstrap edition is not a design rollback.
- ThemePack authority/trust/protocol/mission semantics are unchanged.

## Evidence boundary

Source/static/package verification only. No Gradle build, APK, device acceptance, GitHub upload, workflow, commit, push, release, deployment, or installation is claimed.

## CFv2.1.27 · INT-FILE-059A · Forge File Lab / Archive Cartographer
- Mirrors SERVER baseline Forge **FILE LAB** capability in CLIENT.
- Adds deterministic file SHA-256 inspection and ZIP structural mapping without bulk extraction to storage.
- Adds path/type search, bounded text-content search, text preview, and selective entry extraction.
- Adds staged text editing with explicit new-output commit and lineage manifest; originals are unchanged.
- Adds byte-exact ~500 MiB binary split manifests/recombination and logical ~500 MiB ZIP shards.
- Adds configurable File Lab working/output/shard SAF directory lanes with Downloads fallback where Android supports it.
- CLIENT-only Missions and legacy Dev Mode remain preserved; no SERVER-only inference authority is copied into CLIENT.
- Source-only checkpoint; no APK build, install, GitHub write, workflow dispatch, release, or deployment claimed.


## INT-FORGE-064A — CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R2

- Adds automatic protected source + metadata ZIP pairing.
- Adds strict metadata archive and evidence archive validation.
- Adds chunked-git-blobs-v2 and shared workflow resolver/verifier support.
- Preserves complete legacy loose sidecars for the one-time bootstrap.
- Source-only candidate: no Android build, install, promotion, release, or deployment.
- Lineage disclosure: built from the verified CFv2.1.27 descendant implementation base because the byte-exact accepted CFv2.1.26 archive was not available in the active runtime; File Lab surfaces are preserved.


## INT-FIX-064A-CLIENT-R3 — CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R3

- Adds the four missing GitHub Forge imports identified by workflow `30700898714`.
- Preserves the INT-FORGE-064A source/metadata ZIP pairing and evidence-bundle implementation.
- Advances Android identity to versionCode `126` and versionName `2.1.26-forge-metadata-bundle-compile-fix-r3`.
- Source-only repair; no APK build, install, promotion, release, or deployment.
## INT-FORGE-064B-CLIENT-R4 — CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R4

- Adds project-root package discovery and genuine CLIENT/SERVER/BOTH auto-detection.
- Selects the newest valid source package by verified versionCode/revision and rejects equal-rank hash conflicts.
- Supports two-file metadata pairs and three-file legacy triples.
- Stages matching checkpoint evidence and performs scan-stage-upload from one explicit action.
- Reconciles transient GitHub 5xx outcomes and reuses unresolved transaction IDs to prevent duplicate commits.
- Gives authoritative workflow success precedence over stale local failure presentation.
- Advances CLIENT to VC127. Source-only; Android workflow compilation is pending.

## CLIENT CFv2.1.27 Candidate R3 — Documentation Reconciliation
Documentation-only successor to R2. Adds current paired continuity, standardized checkpoint documentation workflow, and explicit approval gates. No runtime code, Android identity, build, or acceptance claim changes.

## CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R4 — INT-FIX-078A
- Repairs the metadata manifest contract for Forge strict parsing and automatic source/archive companion selection.
- Adds canonical `sourceZip.filename`, `sourceZip.sha256`, and `sourceZip.sizeBytes` fields with required component, versionCode, revision, and verified identity.
- Keeps runtime and Android identity unchanged; source-only package successor.


## INT-FORGE-082A

- Added duplicate-aware Forge source routing and exact component workflow dispatch.
- Removed unrelated-run fallback from component build monitoring.
- Preserved source-only, approval-gated, offline-first, Truth Firewall, and lineage boundaries.

## CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R11 — INT-FIX-CLIENT-BUILD-112A

- Repairs GitHub workflow `31266574472` CLIENT `compileDebugKotlin` failure at `ServerForgeTransferClient.kt:401`.
- Root cause: `Prefs.coreNodeConfig(context)` is suspend, but R10 `loopbackConnection(context)` was non-suspend.
- Correct fix: `loopbackConnection` is now suspend; its only caller `runLoopbackLegacyBenchmark` was already suspend. No `runBlocking` or blocking DataStore bridge is introduced.
- Preserves the R10 transfer profiler, same-phone loopback benchmark, SHA-256 verification, authenticated upload protocol, and CLIENT Forge authority boundary.
- SERVER R33 compiled successfully in the same BOTH workflow and remains unchanged.
- Advances CLIENT Android identity to versionCode `137` and versionName `2.1.27-client-build-repair-r11`.
- Source package is statically verified; authoritative Android compile/build remains the next GitHub Actions run.

## CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R12 — INT-FIX-FORGE-ZIP-MODE-113A

- Repairs GitHub workflow `31268220792`, which resolved and SHA-verified CLIENT R11 but failed before Gradle because extracted source directories inherited non-traversable ZIP mode `0600`.
- Repackages the CLIENT source tree with canonical Unix directory mode `0755`; readable regular-file modes and executable-file bits are preserved.
- Hardens the shared GitHub APK Router extractor to normalize access/traversal after unzip before Android Gradle root discovery, preventing malformed ZIP mode metadata from producing a false `No Android Gradle project root found` failure.
- Preserves the R11 `loopbackConnection` suspend-boundary compiler repair and transfer-profiler behavior.
- Records that stable Android/OAuth signing already depends on the repository `SWRLZ_DEV_KEYSTORE_*` secrets; absent secrets continue to yield `runner/default-source-signing` and a changing debug certificate.
- Advances CLIENT Android identity to versionCode `138` and versionName `2.1.27-forge-zip-mode-repair-r12`.
- Source/package validation only; authoritative Android compilation remains the next GitHub Actions run.

## CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R13 — INT-FIX-FORGE-FIRST-CHUNK-114A

- Repairs a device-observed generic Forge upload stall where SERVER created the upload session but received `0` bytes and `0` chunks.
- Stages the selected content URI once into app-private cache before opening the SERVER session and computes SHA-256 from those staged bytes.
- Reduces generic JSON/base64 chunks from 256 KiB to 64 KiB and adds three bounded attempts per chunk with lost-acknowledgement `nextOffset` reconciliation.
- Adds best-effort authenticated upload abort on fatal post-start failures; SERVER R33 compatibility is preserved when that route is unavailable.
- Deletes temporary staged bytes on all completion/failure paths.
- Advances CLIENT Android identity to versionCode `139` and versionName `2.1.27-forge-first-chunk-r13`.
- GitHub workflow/signing infrastructure is intentionally outside this checkpoint.

## CLIENT R61 — selected archive repack + diagnostic/admin log pull

- Conversation-only archive material can now be repacked locally from exact selected source entries into a separate verified ZIP.
- Full SWRLZ runtime tracing is optional and remains OFF by default; secret redaction is enforced at the log sink.
- ACTIVE proof-bound GPT admin traffic can request the registered CLIENT diagnostic log manifest and pull bounded SHA-verified chunks through `logs.read`.
- This does not grant generic app-private filesystem access and does not expose raw vault secrets or private chain-of-thought.

## INT-FORGE-LIVE-INBOX-AUTOSELECT-154A — CLIENT R63

Forge now treats automatic Downloads selection as a live inbox rather than a one-shot screen-entry scan. New source/metadata arrivals trigger a bounded rescan while Forge is visible, and a newer rejected candidate blocks silent fallback to an older pair with an explicit verification reason. Source ZIP SHA-256 remains authoritative and is revalidated uncached before upload.
