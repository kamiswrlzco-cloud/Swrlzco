# SWRLZ-Core Three Deep Analyses and Phase Integration History

Date: 2026-08-01  
Scope: Forge source packaging, GitHub CI resolution, Android storage behavior, and build-artifact continuity

## Purpose

This document defines the three major deep-analysis streams carried out during the current SWRLZ Forge and CI modernization. It records the conclusions, the first integrated phase, every subsequent implementation phase, what was delivered for Kamilion, and what remains unproven.

## Deep Analysis 1 — Source identity, metadata authority, and transport

### Initial problem

Source ZIPs, checksum files, manifests, evidence, and Git transport had evolved independently. Android extraction could place metadata in a child directory, generic archive classifiers could mistake metadata or evidence ZIPs for Android source, and the repository resolver did not consistently verify direct and chunked packages through one authority model.

### Findings

- Filenames are routing hints, not integrity authority.
- A source is build-eligible only when computed SHA-256, size, component, filename, versionCode, and revision agree with trusted metadata.
- Metadata and evidence archives must be protected classes, not generic source archives.
- Direct ZIP and chunked transport must converge on the same verified source identity.
- Partial loose evidence must fail closed.
- Legacy compatibility is necessary only as a bounded bootstrap path.

### Phase 1 integration — INT-FORGE-064A

The first integrated phase established:

- one source ZIP plus one metadata ZIP;
- exactly two metadata entries at archive root;
- one combined evidence ZIP;
- schema-2 chunk transport binding source and metadata identities;
- direct/chunked resolver parity;
- strict metadata and evidence path safety;
- complete legacy checksum + manifest fallback.

This phase created the contract foundation used by every later phase.

## Deep Analysis 2 — End-to-end Forge automation and provenance

### Initial problem

Forge needed to determine whether a package was CLIENT or SERVER, select matching evidence, avoid duplicate commits, survive transient GitHub errors, describe exactly what it was uploading and building, and follow the resulting workflow artifact back into the Android project directory.

### Findings

- Source discovery, verification, routing, upload, workflow watch, and artifact handling must share one durable identity.
- CLIENT and SERVER support the same Forge capability and therefore require synchronized updates.
- Equal-ranked identities with different hashes are conflicts, not candidates for guessing.
- A workflow artifact ZIP is transport; the actual APK must be safely extracted and verified.
- The Project root and the incoming Downloads inbox are distinct authorities.
- GitHub notices, summaries, and artifacts should describe the exact source package and build target.

### Integrated phases

#### INT-FORGE-064B

Added automatic source classification, version/revision ranking, one-action upload, evidence selection, conflict blocking, durable transaction reuse, and workflow-success precedence to CLIENT.

#### INT-FORGE-064C

Ported the shared capability to SERVER and codified the dual-update rule.

#### INT-FORGE-064D

Moved incoming source discovery to Downloads, retained Project root for outputs, recognized metadata ZIPs without extraction, preserved legacy companion recovery, added exact source/build descriptions, and safely stored the actual APK under `Download/<projectName>/apk/`.

#### INT-CI-064E

Installed repository support for schema-2 transport and metadata bundles, prevented historical unsupported transports from poisoning current builds, and retained fail-closed handling for current/explicit unsupported packages.

#### INT-FIX-064F

Used real compiler evidence to correct two SERVER package namespace declarations and add package-path regression protection.

## Deep Analysis 3 — Android storage responsiveness and CI compatibility

### Initial problem

Project-root selection caused a several-second black screen. Rescan could produce repeated Android “not responding” dialogs. Android does not permit selecting the public Download root through the ordinary folder-tree picker. In parallel, CI consumers drifted from the resolver's internal API and metadata identity rules.

### Findings

- Persisted URI work, `DocumentFile` traversal, folder creation, ZIP inspection, and hashing must not run on the UI thread.
- Automatic and manual scans must not overlap.
- CLIENT and SERVER classification should reuse one filesystem snapshot.
- Scan-time hash caching is safe only when full uncached verification occurs immediately before upload.
- Public Downloads can be a default location, but access must be explicitly user-authorized on modern Android.
- Metadata ZIPs are evidence, never independent source identities.
- Stable resolver APIs are contracts for workflows and must survive internal refactors.

### Integrated phase — INT-FORGE-064G

Both CLIENT and SERVER received:

- public Downloads default behavior with explicit Android authorization;
- optional custom SAF inbox;
- asynchronous project-root setup;
- responsive setup and scan states;
- one-pass root and bounded child snapshot;
- single-flight scanning;
- unchanged-document hash cache;
- full uncached pre-upload revalidation.

### Pending phase — INT-CI-064H

The Source Package Integrity workflow exposed two remaining CI compatibility defects:

- missing `resolve_source` compatibility entry point;
- `_METADATA.zip` misclassified as a second source identity.

This pending phase is CI-only and does not require new CLIENT or SERVER candidates.

## Full phase map

| Phase | Primary result | CLIENT identity | SERVER identity | Evidence status |
|---|---|---|---|---|
| 064A | Metadata bundle and resolver contract | R2 / VC125 | R4 / VC87 | Source/static |
| 064A-R3 | CLIENT import repair | R3 / VC126 | unchanged | CLIENT later reported buildable |
| 064B | CLIENT automatic project-root Forge | R4 / VC127 | unchanged | CLIENT user-reported build success |
| 064C | Shared capability dual sync | R4 retained | R5 / VC88 | Source/static |
| 064D | Downloads pipeline and exact provenance | R5 / VC128 | R6 / VC89 | Source/static |
| 064E | CI schema-2/bootstrap shield | unchanged | R7 / VC90 | CI reached compiler |
| 064F | SERVER namespace repair | unchanged | R8 / VC91 | Source/static; build result not established here |
| 064G | Storage responsiveness and public Downloads | R6 / VC129 | R9 / VC92 | Source/static |
| 064H | Integrity workflow compatibility | no new candidate | no new candidate | Pending approval/application |

## What has been completed for Kamilion

- Canonical source, metadata, and evidence packaging.
- Exact SHA-256 and manifest cross-verification.
- Direct and chunked transport support.
- Legacy loose-sidecar bootstrap compatibility.
- Automatic CLIENT/SERVER/BOTH detection.
- Shared CLIENT/SERVER Forge parity.
- One-action verify, stage, upload, and workflow watch.
- Conflict blocking and duplicate-transaction prevention.
- Exact source/build descriptions in Forge and prepared workflow provenance.
- Public Downloads inbox semantics.
- Project-root output layout and project-name derivation.
- Safe workflow artifact inspection and actual APK extraction.
- Historical transport quarantine in CI.
- SERVER compiler namespace repair.
- Nonblocking project-root setup and serialized one-pass rescans.
- Explicit Android storage-access boundary.
- Current migration documentation and response-format standard.

## Principles preserved throughout

- Offline-first operation.
- Truth Firewall and fail-closed integrity behavior.
- Identity and lineage disclosure.
- Local versus remote distinction.
- Protocol-version discipline.
- Integrate rather than overwrite.
- No silent permission grant.
- No promotion or release merely because a source ZIP exists.

## Remaining work

1. Apply `INT-CI-064H-INTEGRITY-COMPAT` after explicit approval.
2. Obtain clean Source Package Integrity evidence for CLIENT R6 and SERVER R9.
3. Run Android build workflows for current candidates under explicit authorization.
4. Download and hash resulting artifacts.
5. Perform installation/device acceptance separately.
6. Promote only after acceptance evidence and a separate approval boundary.

## Evidence hierarchy

Strongest evidence is, in order:

1. canonical source bytes and SHA-256;
2. metadata manifest and checksum agreement;
3. repository commit and resolver output;
4. workflow logs and artifact hashes;
5. installation/device acceptance evidence;
6. promotion/release record.

No lower evidence tier should be presented as a higher tier.
