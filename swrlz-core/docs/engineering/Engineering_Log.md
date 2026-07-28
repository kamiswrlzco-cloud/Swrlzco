# CLIENT Engineering Log

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

Advanced the CLIENT-only source successor to CFv2.1.8 / versionCode 106. The implementation replaces the default legacy launcher, completes per-theme identity/chrome mappings, introduces reusable full-shell ThemePack backdrop/Kapanion/panel renderers, contains progress artwork inside one calibrated track, and stages the Jester ignition sequence. Existing distinct Kapanion assets were reused; no Jester art was copied into other families and no AI-generated replacement art was required.

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
