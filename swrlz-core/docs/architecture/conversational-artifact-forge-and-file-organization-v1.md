# Conversational Artifact, Forge, and File Organization Architecture v1

Status: **APPROVED REQUIREMENTS / PLANNED IMPLEMENTATION**

This document records the current SWRLZ design for Chat-driven Forge package discovery, persistent Forge transfers, local artifact resolution, and safe background file organization. It does **not** promote any unverified CLIENT or SERVER candidate and does not change repository source authority.

## 1. Shared Local Artifact Resolver

SWRLZ should use one reusable local artifact-resolution layer for both Forge and file organization.

Responsibilities:

- identify CLIENT, SERVER, APK, documentation, diagnostic, media, and generic files;
- group canonical source package families as one logical unit: source ZIP + matching SHA-256 + matching manifest;
- resolve semantic version and immutable candidate revision;
- distinguish candidate, promoted/stable, historical, and unknown lineage;
- verify SHA-256 and manifest binding before Forge staging;
- preserve provenance and never treat a newer-looking filename as newer valid authority by filename alone.

Selection order for `latest valid` is: correct component, highest semantic version, highest candidate revision, complete package family, checksum valid, manifest valid, package identity valid.

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
- later chunked transport can reuse the same transaction layer.

Forge package selection gains independent settings, default ON:

- auto-pair checksum;
- auto-pair manifest.

Selecting a canonical source ZIP should resolve the matching SHA-256 and manifest as one package triple. Mismatch or missing companion state blocks verified staging rather than fabricating evidence.

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
2. discover candidate package families in authorized local storage;
3. verify ZIP + SHA-256 + manifest binding;
4. preview resolved package identity and destination;
5. stage CLIENT to `swrlz-core/sources/client/` and SERVER to `swrlz-core/sources/server/`;
6. hand the verified staging plan to the persistent Forge transfer subsystem;
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

ZIP + SHA-256 + manifest belonging to one SWRLZ source package should move as one logical unit. A package family must not be split accidentally during organization.

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
