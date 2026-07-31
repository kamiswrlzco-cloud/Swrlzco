# SWRLZ Patch Note and Lineage Accounting Contract V1

**Status:** ACTIVE documentation/packaging contract  
**Applies to:** CLIENT and SERVER source candidates after 2026-07-31  
**Authority boundary:** documentation and candidate-lineage accounting; does not promote, build, release, deploy, or install a candidate.

## Requirement

Every CLIENT or SERVER source update must carry a patch-note record in the same bounded checkpoint that creates the source candidate. A source candidate is not documentation-complete when its implementation changes but its patch history is left at the parent version.

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
- explicit not-claimed boundary (for example APK build, device test, promotion, release, deployment, installation);
- repository transport/Forge commit when the candidate is uploaded.

## Required synchronized surfaces

A future source candidate must synchronize all patch-history surfaces that exist in that component package:

1. `ReleaseNotes.md` — human-readable release/candidate notes;
2. `CHANGELOG.md` — chronological implementation history;
3. `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` — machine-readable lineage/index data;
4. repository component patch notes under `docs/patch-notes/`;
5. current candidate lineage/documentation index when repository transport changes.

If a historical package lacks one of these surfaces, do not fabricate that it existed. Record the gap and add the surface in the next authorized candidate.

## Identity discipline

Do not reuse the same component version + candidate revision for different source bytes.

If different source packages accidentally share the same external version/revision, they remain distinct by SHA-256 and provenance and must be documented as an identity collision. The next candidate must advance version and/or revision rather than silently overwrite or conflate the earlier source.

Transport duplicate suffixes (for example a filename suffix added by an upload client) are not sufficient authority to decide whether two packages are semantically identical. SHA-256 + candidate lineage decide identity.

## Evidence hierarchy

Patch notes are navigation/index evidence, not stronger authority than the source package, checksum, manifest, accepted contracts, or validated checkpoint evidence. A patch note may point to those sources but may not convert an unbuilt/uninstalled candidate into a built/installed one.

## Truth Firewall rules

- Never claim a build because source transport exists.
- Never claim installation because an APK was built or downloaded.
- Never claim promotion without an explicit promotion checkpoint.
- Never silently rewrite prior patch history; append corrections with lineage.
- Unknown evidence remains unknown.
