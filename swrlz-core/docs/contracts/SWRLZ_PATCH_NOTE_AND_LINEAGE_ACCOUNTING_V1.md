# SWRLZ Patch Note and Lineage Accounting Contract V1

**Status:** ACTIVE and CI-audited documentation/packaging contract  
**Applies to:** CLIENT and SERVER source candidates after 2026-07-31  
**Enforcement baseline:** INT-DOC-065A, 2026-08-01  
**Authority boundary:** documentation and candidate-lineage accounting; does not promote, build, release, deploy, install, or elevate trust.

## Requirement

Every CLIENT or SERVER source update must carry a patch-note record in the same bounded checkpoint that creates the source candidate. A source candidate is not documentation-complete when implementation changes but any patch-history surface remains at a parent version.

For each candidate, record at minimum:

- component (`CLIENT` or `SERVER`);
- checkpoint ID;
- source filename / logical identity;
- versionCode and versionName;
- revision/candidate identity;
- parent source identity and parent SHA-256 when known;
- exact source SHA-256 once packaged;
- implementation changes;
- changed paths or bounded subsystem list;
- contract/protocol impact;
- validation actually performed;
- explicit not-claimed boundary;
- repository transport/Forge commit when uploaded.

## Required synchronized surfaces

Every source candidate must synchronize all patch-history surfaces that exist in that component package:

1. `ReleaseNotes.md` — human-readable candidate notes;
2. `CHANGELOG.md` — chronological implementation history;
3. `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` — machine-readable exact candidate/parent identity;
4. repository component patch notes under `docs/patch-notes/`;
5. `docs/reference/CURRENT_CANDIDATE_LINEAGE.md` when candidate transport changes;
6. `docs/CURRENT_AUTHORITY.md` current-candidate pointer without changing promoted authority.

A package-internal surface must identify the exact candidate being packaged. Merely containing an older note somewhere in the file is not compliance.

## Definition of documentation-complete

A candidate is documentation-complete only when:

- source/metadata identity is verified;
- package `CHANGELOG.md` names the candidate, VC and checkpoint;
- package `ReleaseNotes.md` names the candidate, VC and checkpoint;
- package lineage JSON names the exact candidate, versionCode, versionName, parent and parent SHA when known;
- repository CLIENT/SERVER patch notes contain the candidate, SHA and checkpoint;
- current candidate lineage contains the candidate and SHA;
- current authority points to the candidate only as candidate evidence unless separately promoted.

## CI accounting workflow

`.github/workflows/patch-note-accounting.yml` runs the independent **SWRLZ Patch Note Accounting** audit on:

- CLIENT/SERVER source-lane updates;
- repository patch-note updates;
- current candidate/authority accounting updates;
- this contract's updates.

The audit is intentionally separate from Source Package Integrity and APK Router:

- source integrity continues to mean source/evidence integrity;
- build routing continues to mean build routing;
- patch-note debt appears as its own explicit workflow result;
- a documentation failure cannot be mislabeled as source corruption or Android build failure.

The audit does not automatically rewrite source ZIPs, manifests, patch notes, authority, or lineage. It fails closed and names the missing/stale surfaces until an authorized documentation synchronization commit resolves them.

## Current grandfathered documentation debt

The following exact immutable source SHAs predate enforcement and have explicitly recorded internal documentation debt:

- CLIENT R8 SHA `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912`:
  - current `CHANGELOG.md`;
  - stale `ReleaseNotes.md` opening at R1;
  - stale lineage JSON identifying R4/VC127.
- SERVER R13 SHA `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693`:
  - current `CHANGELOG.md`;
  - stale `ReleaseNotes.md` opening at R3;
  - stale lineage JSON identifying R5/VC88.

These exceptions apply only to the exact listed SHAs and only as documented debt. They do not declare the stale files correct. The next candidate for either component receives no exception and must synchronize every surface.

## Update cadence rule

Patch-note and lineage synchronization is a required step of **every update**, not a periodic cleanup. The checkpoint cannot be declared closed until the documentation status is stated explicitly:

- `PASS` — all surfaces synchronized;
- `DEBT_RECORDED` — only an exact grandfathered SHA listed above;
- `FAIL` — missing or stale surfaces; candidate remains documentation-incomplete.

## Identity discipline

Do not reuse the same component version + candidate revision for different source bytes.

If different packages accidentally share an external version/revision, they remain distinct by SHA-256 and provenance and must be documented as an identity collision. The next candidate must advance version and/or revision rather than silently overwrite or conflate history.

Transport duplicate suffixes are not sufficient authority to decide whether packages are semantically identical. SHA-256 plus candidate lineage decide identity.

## Evidence hierarchy

Patch notes are navigation/index evidence, not stronger authority than the source package, checksum, manifest, accepted contracts, implementation files, or validated checkpoint evidence. A patch note may point to those sources but may not convert an unbuilt/uninstalled candidate into a built/installed one.

## Truth Firewall rules

- Never claim a build because source transport exists.
- Never claim installation because an APK was built or downloaded.
- Never claim promotion without an explicit promotion checkpoint.
- Never silently rewrite prior patch history; append corrections with lineage.
- Never mutate an already-hashed source ZIP merely to make its old documentation look current; create a properly advanced successor when source bytes must change.
- Unknown evidence remains unknown.
