# Conversational Artifact, Forge, and File Organization Architecture v1

Status: **APPROVED REQUIREMENTS / PARTIAL IMPLEMENTATION**

This document records the current SWRLZ design for Chat-driven Forge package discovery, persistent Forge transfers, local artifact resolution, safe background file organization, chunked source transport, and build-input evidence policy. It does **not** promote any unverified CLIENT or SERVER candidate and does not change repository source authority.

## 1. Shared Local Artifact Resolver

SWRLZ should use one reusable local artifact-resolution layer for both Forge and file organization.

Responsibilities:

- identify CLIENT, SERVER, APK, documentation, diagnostic, media, and generic files;
- group a source ZIP with any matching SHA-256 and package manifest as one logical package family without requiring sidecars to exist;
- resolve semantic version and immutable candidate revision;
- distinguish candidate, promoted/stable, historical, and unknown lineage;
- calculate source ZIP SHA-256 locally and validate supplied checksum/manifest evidence;
- preserve provenance and never treat a newer-looking filename as newer valid authority by filename alone.

Selection order for `latest valid` is: correct component, highest semantic version, highest candidate revision, source identity valid, and every supplied evidence companion valid. Missing checksum/manifest evidence does not make a ZIP ineligible for a build attempt. Promoted/current authority remains separately evidence-gated.

## 2. INT-FORGE-039K — Persistent Forge Transfer Ownership

Status: **APPROVED / PLANNED**

Forge transfers must not be owned by a Compose screen lifecycle. Navigating Forge -> Settings/Chat/Missions must not cancel an active upload.

Planned properties:

- transfer owner independent of composition;
- foreground transfer notification for long-running uploads;
- shared transaction ID and observable progress state;
- pause/cancel/retry/reconnect semantics;
- UI screens observe the same active transaction rather than creating duplicates;
- credential failure and transfer failure remain separately classified;
- chunked transport reuses the same intended transaction layer.

Forge package selection gains independent settings, default ON:

- auto-pair checksum;
- auto-pair manifest.

Selecting a canonical source ZIP should resolve matching SHA-256 and manifest companions when available. Missing companions are informational for build eligibility; supplied mismatches block rather than being ignored or fabricated.

## 3. INT-FORGE-039L — Chat-Initiated Package Discovery + Verified Forge Staging

Status: **APPROVED / PLANNED**

Examples:

- `forge latest client`
- `forge latest server`
- `forge latest client and server`
- `forge latest stable client`
- `forge latest candidate server`
- `forge client 2.1.19 r2`

Natural language maps to canonical capabilities underneath. CLIENT and SERVER remain independent package authorities even when both are selected.

Flow:

1. resolve requested component and selector;
2. discover candidate source identities in authorized local storage;
3. calculate ZIP identity and validate any supplied SHA-256/manifest evidence;
4. preview resolved package identity, evidence state, and destination;
5. stage CLIENT to `swrlz-core/sources/client/` and SERVER to `swrlz-core/sources/server/`;
6. hand the staging plan to the persistent Forge transfer subsystem;
7. actual repository write remains a distinct Forge action governed by configured confirmation and trust rules.

## 4. INT-FILE-039M — Conversational Local File Organizer

Status: **APPROVED / PLANNED**

Examples:

- `organize my Downloads folder`
- `put these workflow logs somewhere organized`
- `make a folder for SWRLZ APKs and sort them`
- `find the latest SERVER source package`
- `undo that Downloads organization`

The planner inspects first and proposes a reversible organization plan. It may create folders when useful, but ambiguous placement is surfaced to the user.

### Folder choice UX

When several existing folders are plausible, present a compact chooser. When one destination is strongly preferred from context, ask whether that destination is acceptable and offer a different-folder option.

Confirmed organization rules may be remembered as explicit user rules. Guesses do not silently become permanent policy.

### Package-family behavior

A source ZIP and any matching SHA-256/manifest companions belong to one logical SWRLZ package family. When companions exist, organization should move the recognized family together and must not split it accidentally. A ZIP without companions remains a valid source artifact rather than an incomplete filesystem object.

### Safe operation model

- plan first;
- user confirmation for ambiguous or destructive actions;
- no silent overwrite;
- move journal with original and destination URI;
- undo support where the filesystem operation remains reversible;
- persisted Android Storage Access Framework permissions scoped to roots the user explicitly grants;
- UI lifecycle must not own long-running file operations.

## 5. Multi-Folder Keep Organized

Status: **APPROVED REQUIREMENT / PLANNED**

Users may register multiple authorized folders such as Downloads, Documents, SWRLZ Sources, Screenshots, or project-specific folders.

Each watched folder can independently configure:

- monitoring enabled/disabled;
- notification-only vs ask-to-organize vs user-approved automatic handling of known rules;
- organization rules and preferred destinations;
- messiness thresholds;
- notification cooldown/snooze behavior;
- handling of ambiguous files;
- duplicate/conflict policy.

Default behavior should be conservative: detect and suggest, then ask before organization when a rule is not already explicitly confirmed.

### Background notification example

`Downloads is getting crowded. I found 23 files with 16 that match saved organization rules. Organize now?`

Notification actions may include:

- Organize;
- Review;
- Snooze.

Background checks should use Android-appropriate scheduled work rather than a permanently busy polling loop. Offline-first behavior is preserved.

### Messiness signal

The implementation may combine user-configurable signals such as:

- uncategorized file count;
- total file count;
- recent growth since the last scan;
- old files remaining at the root;
- recognized package families/logs/media that already have confirmed destinations.

The score is advisory and must not be presented as objective system truth.

## 6. Truth, Trust, and Lineage Boundaries

- CLIENT and SERVER lineage remain separate.
- Candidate artifacts are immutable and revisioned (`R1`, `R2`, ...); different bytes must never reuse one candidate identity.
- Build evidence counts only when the workflow-resolved SHA equals the expected candidate SHA.
- Static checks, compilation, build, device validation, repository promotion, release, and deployment are distinct evidence states.
- ZIP-only build eligibility does not equal package promotion or current authority.
- Supplied contradictory checksum/manifest evidence fails closed.
- File organization does not grant Forge authority.
- Forge discovery does not imply repository write authorization.
- SERVER-owned provider secrets remain SERVER-owned.
- Truth Firewall, local/remote distinctions, identity, trust, permissions, protocol versions, and offline-first behavior remain authoritative constraints.

## 7. Precheck + Promotion Gate

Normal implementation checkpoints use:

1. verify authoritative parent;
2. baseline compile/test where toolchain is available;
3. define acceptance/regression tests;
4. implement in disposable candidate workspace;
5. compile/repair loop;
6. applicable tests and debug build;
7. contract/security/lineage checks;
8. Documentation Gate;
9. version/package only after applicable validation.

Concrete compiler failures should become narrow regression checks where practical. Failed candidate revisions remain evidence and do not become promoted source authority.

## 8. INT-FORGE-039F + INT-FORGE-039N — Chunked Transport and ZIP-Only Build Eligibility

Status: **REPOSITORY CI IMPLEMENTED / CLIENT RUNTIME CANDIDATE**

Repository CI on `main` implements two source-input paths:

### Direct ZIP

A lane-root CLIENT/SERVER `.zip` is sufficient input for an APK build attempt. CI computes the ZIP SHA-256 itself. Matching checksum and package-manifest sidecars are optional; when supplied, they must validate exactly or the build fails closed.

### Chunked source transport

A lane-root `*.transport.json` may describe `chunked-git-blobs-v1` transport. Chunk files remain inside the selected component lane. The CI resolver verifies sequential indexes, every chunk size and SHA-256, reconstructs the original ZIP in runner temporary storage, and verifies whole ZIP size and SHA-256 before compilation.

Chunk objects and transport manifests are transport/provenance, not independent source authority.

### Push routing and provenance

The APK Router treats `.zip` and `.transport.json` as build-triggering source identities. Sidecar-only changes do not independently request an Android build. Build provenance records direct-vs-chunked source kind and available evidence paths.

### Runtime implementation boundary

CLIENT CFv2.1.20 candidate R1 contains the corresponding Forge-side transport/evidence work, but Android compilation/build evidence for that candidate remains pending. INT-FORGE-039K persistent lifecycle ownership is still planned and is not implied by repository chunk support.

See `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md` for applied repository evidence and `docs/checkpoints/INT-FORGE-039F-039N_DOCUMENTATION_IMPACT_SET.md` for the Documentation Gate impact classification.
