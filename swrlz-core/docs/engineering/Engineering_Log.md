# SWRLZ Engineering Log

## 2026-08-04 — INT-FIX-075A

### Objective

Repair the single compiler-evidenced SERVER defect in CFv2.1.27 R1, prevent recurrence in the paired §wyrlz LLM verification lane, publish the immutable R2 source/metadata pair, and synchronize repository history.

### Source lineage

- Failed parent: SERVER CFv2.1.27 R1 / VC129 / SHA-256 `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`.
- R1 repository transport: commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9`.
- R1 build evidence: GitHub Actions run `30950003262` verified the exact package, reached `:app:compileDebugKotlin`, and failed at `ServerOperationsScreen.kt:16`.
- Repair successor: SERVER CFv2.1.27 R2 / VC130 / SHA-256 `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`.
- Metadata ZIP SHA-256: `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`.
- The paired INT-AI-074A CLIENT CFv2.1.27 R1 source remains unchanged and is not part of this repository publication; the repository CLIENT lane remains separately governed.

### Facts

- `SOURCE IMPLEMENTED`
- `STATIC VERIFICATION PASS`
- `PACKAGE ONLY` before repository publication
- `BUILD NOT RUN` for R2 before publication
- `RUNTIME NOT TESTED`

### Requirements

- Preserve R1 as immutable failed-build lineage.
- Remove the invalid explicit Compose weight import while retaining contextual weight behavior.
- Make the established compiler-regression precheck mandatory.
- Publish only the exact verified R2 package pair and synchronized SERVER documentation.
- Keep promoted authority, CLIENT, contracts, Room schema, trust, Truth Firewall, and local/remote behavior unchanged.

### Engineering decisions

- Use the repository's accepted `chunked-git-blobs-v2` representation; the lane-root transport manifest remains the source identity and reconstructs the byte-exact 48,587,996-byte ZIP.
- Treat automatic push-triggered workflows as build/evidence producers, not preexisting success.
- Record R35–R45 navigation debt while preserving each candidate's original evidence boundary.

### Engineering changes

- Removed `import androidx.compose.foundation.layout.weight` from `ServerOperationsScreen.kt`; both `Modifier.weight(1f)` calls remain.
- Integrated the compiler-regression precheck into the paired INT-AI-074A verifier.
- Advanced SERVER identity to VC130 / `2.1.27-swrlz-llm-studio-compile-repair-r2`.
- Added the exact R2 chunk transport and metadata bundle to the SERVER source lane.
- Updated current authority, candidate lineage, SERVER patch notes, checkpoint/release/evidence records, and this engineering log.

### Verification performed

- SERVER compiler-regression precheck: PASS.
- Paired static gate: 113/113 PASS.
- INT-FIX-075A repair gate: 28/28 PASS.
- Kotlin/KTS string scan: 397 files, zero violations.
- Internal source manifest: 1,191/1,191 PASS.
- Immutable package pair: 26/26 PASS.
- R1→R2 inventory: 7 added, 12 modified, 0 removed.

### Runtime evidence

R2 Android compilation, APK generation, installation, device acceptance, and integration acceptance remain pending. Publication may automatically start Source Package Integrity, Patch Note Accounting, and APK Router workflows; their actual run IDs and outcomes must be recorded separately.

### Known issues

- `FOLLOW-UP REQUIRED` — verify that CI resolves exact R2 SHA-256 `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` and record the first actual build result.

### Exclusions

No CLIENT change, manual workflow dispatch/rerun, APK installation, promotion, release, or deployment.

### Follow-up

After repository publication, bind the exact source-publication commit and automatic workflow evidence to this checkpoint without upgrading pending build/device claims.

## 2026-07-29 — INT-DOC-AI-041H dense-chat identity/model synchronization

### Repository evidence reviewed

Latest maintained evidence now includes:

- CLIENT CFv2.1.22 R1 / VC120 / SHA `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5` / Forge commit `1d3fa542db0f700a1f35256be9317393d25bbc8c`;
- SERVER CFv2.1.9 R6 / VC64 / SHA `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` / Forge commit `cb073ca4c008109aec9da4ad6f111657d31bc421`.

CLIENT R1 repository transport includes checksum+candidate-manifest evidence. SERVER R6 repository transport includes checksum+verified chunk transport but no separately packaged candidate manifest.

Project-owner/operator evidence reports a successful SERVER R5 Android build. A later user-supplied screenshot shows SERVER CFv2.1.9 VC64 and the current Chat/Command Center surface; this is device-visible working-state evidence but is not exact source-SHA → CI → APK provenance or promotion evidence.

### Identity architecture correction

The dense-chat review established the canonical identity invariant:

- SWRLZ / Swurlz = persistent primary identity;
- selected LLM = replaceable reasoning engine;
- Swurlzara = replaceable expression/profile lens;
- SWRLIE = first-party reasoning/provider interface;
- SERVER = runtime/inference host.

Model/profile swaps must not silently reassign primary identity.

Truth Firewall is intrinsic SWRLZ epistemic/authority anatomy rather than model/profile equipment. Changing models, profiles, or plugins cannot remove it or turn style/confidence into permission.

See `docs/architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md`.

### Behavioral evaluation update

`SWRLZ-LFM-EVAL-001A2` was approved as evaluation/documentation-only work preserving frozen v1 and expanding coverage for natural Chat, SWRLZ identity, Swurlzara lens behavior, role separation, grounding, instruction internalization, profile leak resistance, memory transfer, technical/practical reasoning, truthful absurdity, task presets, formatting, and equipped-gear self-reflection.

No Behavioral-EQ v2 freeze artifact is claimed by this docs synchronization.

### Operator-reported Q4_K_M vs Q8_0 result

Parallel work-chat evaluation was reported by the project owner:

- frozen suite: Q4_K_M `20/72`, Q8_0 `19/72`;
- smoke test: both `5/12`;
- size: Q4_K_M `218.69 MiB`, Q8_0 `361.65 MiB`;
- Q4_K_M ran faster in the reported test;
- Q4_K_M was selected as the base for `SWRLZ-LFM-OPT-001A.gguf`.

This is a narrow benchmark win and not evidence that Q4_K_M universally beats Q8_0. This repository documentation records the operator report; it does not independently verify or publish the optimized GGUF artifact.

### Current planned directions recorded

- `INT-AI-041E`: local per-response Feedback Ledger with explicit positive/negative/neutral/unrated semantics, optional stars/tags/notes, lineage, and no automatic training/external telemetry.
- `INT-AI-041F`: balanced lightweight base + independently versioned neural/Skill/knowledge/specialist feature-plugin architecture with base lineage, compatibility, resource/conflict, and rollback rules.
- `INT-CHAT-041G`: compact Chat status, dragon-triggered vertical Command Center popup, and real operational Response Processing stages with corrected identity labels; no fake percent or chain-of-thought display.

These remain separately approval/implementation-gated.

### Authority boundary

INT-DOC-AI-041H is documentation-only. Current promoted source authority remains CLIENT CFv2.1.9 and SERVER CFv2.1.0. This checkpoint does not train/merge/quantize model weights, modify CLIENT/SERVER source, build an APK, trigger workflows, promote candidates, release, deploy, or install anything.

See:

- `docs/checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md`
- `docs/architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md`
- `docs/CURRENT_AUTHORITY.md`

## 2026-07-29 — INT-DOC-AI-040B-R1-R5 SWRLIE runtime synchronization

### Repository evidence reviewed

After the 2026-07-28 architecture/update documentation sync, SWRLZ Forge uploaded five SERVER CFv2.1.9 SWRLIE candidate revisions to `main` as verified chunk transports:

- R1 / VC59 / SHA `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` / Forge commit `55654e3bca3b80445bb0873d545966a8a7131a29`;
- R2 / VC60 / SHA `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` / Forge commit `2ea339f972178e71819225def7f7a0d33c48636e`;
- R3 / VC61 / SHA `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` / Forge commit `54c64be91e0fdc0bf229a1389518707eec150356`;
- R4 / VC62 / SHA `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` / Forge commit `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1`;
- R5 / VC63 / SHA `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` / Forge commit `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7`.

R1/R2 repository transport includes candidate-manifest evidence. R3-R5 transport commits prove the source ZIP identity/checksum represented by the transport but do not include the separately packaged candidate manifests.

### Candidate progression documented

R1 establishes model-independent local SWRLIE inference/no-model fallback and the external exact Q4_0 bootstrap target. R2 adds first-class SERVER Chat and settings hierarchy. R3 adds local startup auto-load/recovery, adaptive/copyable Chat, Update Ledger and tone-never-implies-approval. R4 adds multi-GGUF staging/safe switching, adaptive context/inference controls, prompt budgeting, and code-native Swurlzara compilation. R5 adds local self-knowledge, shared Update Ledger retrieval, and live model/runtime/context grounding.

### Architecture decisions synchronized

Maintained docs now also record:

- SWRLZ Skills belong upstream of any LLM/profile and survive model swaps;
- Skills, Memory, and Self Knowledge are distinct systems;
- the smallest certified model should establish the behavioral floor while heavier models extend capability;
- model quality is evaluated against latency/RAM/storage/context/energy, not size alone;
- personality controls may expand beyond named profiles but remain subordinate to Truth Firewall/approval/provenance/execution authority;
- Android, PC, and dedicated-node packs share one SWRLZ architecture with different capability envelopes;
- dynamic simulations should use validated structured state/DSL rather than arbitrary model-generated executable code;
- INT-FILE-039M should recognize archive/extracted-tree lineage, modified descendants, and multiple exploded package families before proposing cleanup.

### Authority boundary

This documentation synchronization does not change `docs/CURRENT_AUTHORITY.md`. SERVER CFv2.1.9 R1-R5 remain candidate/evidence lineage. No Android build, device/integration acceptance, promotion, release, deployment, installation, Skills implementation, web enablement, model training, or device file operation is claimed by this docs checkpoint.

See:

- `docs/checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md`
- `docs/architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md`
- `docs/architecture/SWRLZ_ARCHIVE_LINEAGE_AND_FILE_ORGANIZATION_EXTENSION_V1.md`

## 2026-07-28 — INT-FORGE-039F + INT-FORGE-039N repository CI application

### Applied repository behavior

The approved repository CI counterpart for deterministic chunked source transport and ZIP-only build eligibility is now applied on `main`.

Applied commit chain:

- `2c0c2d76af164324b2db4f931ff8592f833626f7` — source resolver accepts direct ZIP or verified `chunked-git-blobs-v1`, reconstructs the original ZIP in runner temporary storage, and treats sidecar evidence as optional;
- `08b3eec90389051b6e597a55569afacc9a3b4e81` — package verifier permits ZIP-only build input while failing closed on supplied checksum/manifest contradictions;
- `9ed835d06ae35f0b299c3231c0401c69a5c0fd2a` — resolver regression suite covers ZIP-only input, mismatched evidence, exact chunk reconstruction, corruption rejection, and transport-manifest push selection;
- `9d166a62cbdfeacb35dec242502bc92907940515` — APK Router workflow integrates runner-temp reconstruction, optional evidence arguments, `.transport.json` source routing, and source-kind provenance.

### Validation boundary

Before application, the patch matched the exact live CI file revisions. Resolver tests passed 8/8 and patched Python CI tools compiled locally. Chunk reconstruction separately reproduced SERVER CFv2.1.8 R3 whole-ZIP SHA-256 `506d83b058bf8127092a8d08c20c61f763bbb97e4847d8f6ce4d3f5c0df7c451`.

No workflow was manually dispatched by this checkpoint. No APK, release, deployment, installation, or CLIENT/SERVER source promotion is claimed.

CLIENT CFv2.1.20 candidate R1 contains the corresponding Forge-side chunk/evidence implementation but remains source/static verified and Android-build pending. SERVER CFv2.1.8 R3 source is unchanged by the repository transport fix.

Current repository source authority remains the versions recorded by `docs/CURRENT_AUTHORITY.md`.

See `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` and `docs/checkpoints/INT-FORGE-039F-039N_DOCUMENTATION_IMPACT_SET.md`.

## 2026-07-27 — INT-DOC-FILE-039M engineering synchronization

### Authority boundary

Repository source authority remains the versions recorded by `docs/CURRENT_AUTHORITY.md`. Later CLIENT CFv2.1.19 and SERVER CFv2.1.8 work is candidate/evidence lineage and is not promoted by this documentation update.

### Validation process adopted

Normal implementation work now uses a Precheck + Promotion Gate: verify the parent, establish baseline evidence when the toolchain is available, define acceptance/regression tests, work in disposable candidates, run compile/repair loops, complete applicable build/contract/security checks, synchronize affected documentation, and promote only after evidence is green.

Candidate artifacts are immutable revisions (`R1`, `R2`, ...). Different bytes must not reuse a candidate identity. Build results count only when the workflow-resolved source SHA equals the expected candidate SHA.

### Current compiler evidence

CLIENT CFv2.1.19 adaptive Chat work remains candidate lineage. Earlier Material3 `ModalBottomSheet` opt-in evidence produced a narrow regression precheck; a repeated build of the old candidate demonstrated the need for immutable candidate names and expected-SHA matching.

SERVER CFv2.1.8 R1 workflow `30314210205` reached `:app:compileDebugKotlin` and exposed four bounded blockers: cross-module nullable smart-cast use, stale `SwrlzTheme(family=...)` API use, cross-file access to private `SectionLabel`, and explicit `foundation.layout.weight` import. Later R2 repaired those four compiler-evidenced defects; R3 preserved those repairs while correcting the external candidate manifest schema. SERVER candidate promotion remains evidence-gated.

### Approved Forge/file architecture

INT-FORGE-039K is approved/planned to move long-running Forge transfers out of Compose screen lifecycle ownership, preserve an active transaction across navigation, and expose pause/cancel/retry/progress state. Source ZIP selection should independently auto-pair both checksum and manifest companions by default.

INT-FORGE-039L is approved/planned for Chat-driven latest-valid CLIENT/SERVER/BOTH package discovery, source identity plus supplied-evidence verification, destination preview, and Forge staging.

INT-FILE-039M is approved/planned for a shared Local Artifact Resolver plus a safe conversational file organizer. The design includes plan-first moves, suggested/created folders, ambiguity dialogs, explicit remembered organization rules, package-family moves, operation journaling, undo, Storage Access Framework roots, and UI-lifecycle-independent execution.

The Keep Organized extension allows multiple user-selected folders to be watched with independent thresholds/rules and conservative background notifications such as Organize / Review / Snooze. Automatic handling applies only to behavior the user has explicitly configured; ambiguous placement remains ask-first.

See `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` and `docs/checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md`.

## 2026-07-26 — INT-THEME-035D

### Objective

Repair the canonical CLIENT source ZIP/checksum/manifest contract after repository
promotion exposed a manifest-schema mismatch before compilation.

### Source lineage

PR #1 promoted CLIENT CFv2.1.8 to `main` at merge commit
`bc80d7a4d28d656f640ac1a511b9ae340e8b45ee`.

### Facts

- Source Package Integrity run `30222384992` selected CFv2.1.8 and failed at manifest verification.
- APK Router run `30222384996` passed resolver tests, selected the same CFv2.1.8 ZIP/SHA pair, and failed at the same verification gate.
- The CFv2.1.8 ZIP and SHA matched.
- The manifest used `sourcePackage` and `bytes` instead of canonical `zip` and `size_bytes`, and omitted `verified: true`.
- Kotlin/Android compilation was skipped and no APK artifact was produced.

### Engineering changes

Advanced the packaging/identity successor to CLIENT CFv2.1.9 / versionCode 107.
CFv2.1.8 theme behavior is unchanged. The new manifest retains rich checkpoint metadata
and adds the exact repository verifier contract. Failed CFv2.1.8 evidence remains preserved.

### Verification performed

- behavior diff limited to Android/package identity and documentation;
- 688-entry ZIP CRC and path/root safety: pass;
- deterministic repackage byte comparison: pass;
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`;
- repository package-pair verifier: pass locally.

### Runtime evidence

PR #2 merged at `77be6f4f93ff73c0f9cbd2b3c5d6f401bcb893ef`.
Source Package Integrity run `30223152048` passed the exact manifest gate that
rejected CFv2.1.8. APK Router run `30223152052` passed resolver tests, routed
CLIENT only, verified the selected source, completed `:app:assembleDebug`, and
uploaded artifact `8637844750`. The downloaded APK is 56,667,850 bytes with
SHA-256 `0f7312dd346c6eb587b0ec44ab28b9dd30e9371799c26dbbe657fdc354fba419`.
Signing mode is `runner/default-source-signing`. Device evidence remains pending.
No SERVER build, release, deployment, or installation is claimed.

## 2026-07-26 — INT-THEME-035C

Verified canonical parent `CLIENT_CFv2.1.7_SWRLZ.zip` at SHA-256 `bc5b941e9b0c86e28581d8f6019b6c54722243279ef666aa3c35c4f97745fe76`.

Advanced the source successor to CLIENT CFv2.1.8 / versionCode 106. The implementation replaces the default legacy launcher, completes per-theme identity/chrome mappings, introduces reusable full-shell ThemePack backdrop/Kapanion/panel renderers, contains progress artwork inside one calibrated track, and stages the Jester ignition sequence. Existing distinct Kapanion assets were reused; no Jester art was copied into other families and no AI-generated replacement art was required.

The authority diff remains presentation-only. SERVER, protocol, network, trust, identity proof, permission, mission, Forge transaction, accessibility automation, local/remote, and offline-first sources are unchanged.

Source-only integrity evidence is recorded in `docs/checkpoints/INT-THEME-035C_CLIENT_THEME_CHROME_RUNTIME_REPAIR.md`. At initial packaging time, Gradle, tests, APK, device acceptance, workflow execution, release, and deployment were not run or claimed. Later repository CI failure evidence and the package-pair successor are recorded under INT-THEME-035D.

## 2026-07-26 — INT-THEME-035B

Workflow run `30216145763` resolved and verified `CLIENT_CFv2.1.6_SWRLZ.zip`, and resolver unit tests passed 6/6. Kotlin compilation then failed at `ThemedProgress.kt:175` and `:190` because nested Compose `Box` scopes could not implicitly resolve the enclosing `BoxWithConstraints.maxWidth`.

Advanced the source successor to CLIENT CFv2.1.7 / versionCode 105 and captured the outer width as `availableWidth` before both nested scopes. The two fill images now use `Modifier.width(availableWidth)`. No build was run in this checkpoint; static repair/package verification only.

## 2026-07-26 — INT-THEME-035A

Parent `CLIENT_CFv2.1.5_SWRLZ.zip` was verified at SHA-256 `c7ed3942c9a14a110ea3a085316011b3522153e757d09614050aa15d20f9ac58` and retained as rollback.

Implemented the source-only declarative ThemePack checkpoint as CLIENT CFv2.1.6 / versionCode 104:

- shared contract and validation;
- stable legacy migration plus seven new built-ins;
- deterministic 101-resource runtime visual catalog;
- independent local CLIENT selection and staged preview;
- launcher/Kapanion/bubble/notification identity;
- Jester startup reference and safe fallbacks;
- truthful layered progress and reduced-motion behavior;
- architecture, contract, checkpoint, implementation, and release documentation.

Static XML/JSON, asset integrity, shared-contract, alias, changed-source lexical, and authority-scope checks passed. Gradle, APK, device, GitHub, commit, push, release, and deployment actions were not run.

Repository documentation publication is pending a separately authorized source promotion.
