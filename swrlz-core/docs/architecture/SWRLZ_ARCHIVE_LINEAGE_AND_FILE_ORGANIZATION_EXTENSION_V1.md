# SWRLZ Archive Lineage and File Organization Extension v1

**Status:** approved design direction / planned implementation extension to `conversational-artifact-forge-and-file-organization-v1.md`. This document does not claim device file scanning or organization is implemented.

## Purpose

Extend INT-FILE-039M so SWRLZ can recognize archives and their extracted descendants as lineage-aware artifact families instead of treating every loose file as unrelated.

Primary use case:

- a source ZIP is downloaded;
- the ZIP is extracted directly into Downloads or another user-authorized folder;
- hundreds of source files appear loose at the root;
- SWRLZ should recognize that the loose tree likely came from that archive, explain the evidence, and propose a reversible cleanup/organization plan.

## 1. Archive inspection without execution

SWRLZ should inspect supported archives in place where possible rather than extracting them just to understand them.

For ZIP-like containers, the resolver may collect:

- archive identity and SHA-256;
- entry paths;
- entry sizes;
- entry hashes when required;
- timestamps/metadata where trustworthy;
- known package/version/manifests contained inside;
- SWRLZ package-family identity where applicable.

Archive contents are data to inspect, never implicit executable authority.

## 2. Extracted-tree lineage detection

Given an archive and loose filesystem objects, the resolver should compare multiple signals.

### Strong evidence

- loose-file SHA-256 equals streamed archive-entry SHA-256;
- relative path matches the archive entry;
- byte size matches;
- embedded manifest/version/package identity agrees.

### Supporting evidence

- directory topology strongly matches;
- filenames and sizes cluster with the archive;
- creation/modification times cluster around a plausible extraction event;
- known SWRLZ source structure matches;
- multiple related files appeared together.

Filename equality alone is weak evidence.

## 3. Confidence and evidence classes

Lineage conclusions must distinguish certainty levels.

Example:

```text
Likely extracted archive:
SERVER_CFv2.1.9_SWRLZ_CANDIDATE_R5.zip

Loose objects associated: 509
Exact content matches:    503
Modified descendants:       4
Missing archive entries:     2
Confidence: VERY HIGH
```

Suggested confidence vocabulary:

- `EXACT` — complete verified path/content match for the asserted set;
- `VERY_HIGH` — overwhelming multi-signal evidence with bounded discrepancies;
- `HIGH` — strong structure/hash/metadata agreement;
- `POSSIBLE` — partial evidence; user review required;
- `UNRESOLVED` — insufficient evidence.

Confidence is advisory and must not be presented as cryptographic proof when it is not.

## 4. Modified descendants

An extracted tree may be edited after extraction.

SWRLZ must not collapse modified descendants into "duplicate" merely because they share names/paths with archive entries.

Example:

```text
Derived from: SERVER CFv2.1.9 R5 source
Exact matches: 506
Modified: 3

Modified descendants:
- app/.../ServerChatScreen.kt
- app/.../SwrlieRuntime.kt
- README.md
```

The appropriate result is lineage plus divergence, not deletion.

## 5. Archive absent, extracted tree present

When the original archive is no longer present, SWRLZ may still infer a probable package/source family from:

- recognizable source topology;
- embedded version/build metadata;
- package/application identifiers;
- manifests/checksum receipts;
- known prior archive fingerprints stored in the local artifact index;
- repository/package lineage already known to SWRLZ.

Such inference must remain labeled as inferred/likely unless exact provenance can be reconstructed.

## 6. Multiple archive explosions in one folder

The resolver should cluster loose files into probable package families rather than treating one crowded folder as one dataset.

Example:

```text
Package family A
SERVER CFv2.1.8 R3
218 associated files

Package family B
SERVER CFv2.1.9 R2
493 associated files

Package family C
SERVER CFv2.1.9 R5
509 associated files

Unresolved
17 files
```

A file may remain unresolved rather than being forced into the nearest family.

## 7. Planner output

Archive lineage analysis feeds the existing plan-first organizer.

Useful actions may include:

- `VIEW FILES`;
- `VERIFY LINEAGE`;
- `MOVE AS GROUP`;
- `ARCHIVE WORKING COPY`;
- `LEAVE HERE`;
- `REVIEW CLEANUP`.

Deletion remains a distinct destructive action subject to the applicable approval policy.

## 8. Recommended destinations

A detected extracted SWRLZ source tree may be proposed for a lineage-aware working location such as:

```text
SWRLZ/
└── Working/
    └── SERVER/
        └── CFv2.1.9/
            └── R5/
```

The original ZIP should normally remain an independent source artifact unless the user explicitly chooses a different retention rule.

## 9. Safety boundaries

Archive analysis must account for hostile or pathological containers.

Requirements include:

- never execute archive contents as part of inspection;
- reject or quarantine traversal paths such as `../` escaping the virtual archive root;
- treat symlinks conservatively;
- bound recursive archive depth;
- bound expanded-size/entry-count work and detect ZIP-bomb-style expansion ratios;
- prefer streaming hash/metadata inspection over temporary full extraction;
- distinguish APK/container inspection from APK installation;
- keep archive inspection separate from move/delete/Forge authority.

## 10. Shared resolver integration

The intended Local Artifact Resolver grows into:

```text
Local Artifact Resolver
├── Filesystem Scanner
├── Archive Inspector
├── Archive Lineage Resolver
├── Package Family Classifier
├── Duplicate Hash Resolver
├── Extracted-Tree Detector
├── Provenance Graph
└── Cleanup Planner
```

Forge and `/files (scan)` should consume the same lineage model so repository packaging and local organization do not invent incompatible artifact identities.

## 11. Evidence boundary

This is an architecture extension for INT-FILE-039M.

It does not authorize or claim:

- scanning the user's actual storage;
- moving/renaming/deleting files;
- background automatic organization;
- archive execution;
- APK installation;
- GitHub/Forge writes;
- Android build/device acceptance.
