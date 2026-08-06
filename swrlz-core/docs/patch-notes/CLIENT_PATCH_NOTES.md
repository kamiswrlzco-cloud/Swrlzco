# CLIENT Patch Notes

**Scope:** CLIENT / §wyrlix source-candidate lineage and repository transport history.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, device acceptance, promotion, release, deployment, or installation unless separate evidence is named.

## Current prepared repository candidate — 2026-08-05

### CFv2.1.27 R8 — INT-FORGE-082A

- canonical candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R8`
- display role: §wyrlix / CLIENT
- versionCode: `134`
- version: `2.1.27`
- revision: `R8`
- checkpoint: `INT-FORGE-082A`
- source SHA-256: `dcc68cd54c213c81cd3b9fc4d0b7789ba377719cc074ad052fc9a9d57abb1f64`
- metadata bundle SHA-256: `73a3e732293376db2482c208cbe58e7b515053f4cc49ca8f38bef3906923036e`
- direct parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R7.zip`
- repository identity when transported: `sources/client/CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R8.zip` or its canonical transport descriptor
- evidence workflow: `31069235859`
- build state: source-only successor; no Android build success claimed
- promotion: not promoted

Changes:

- repairs stale CLIENT source selection by requiring explicit component/source dispatch when Forge requests an APK build;
- adds duplicate-aware upload behavior so an exact repository duplicate can still be built without creating a duplicate source commit;
- preserves independent CLIENT/SERVER lane handling during mixed uploads;
- prevents CLIENT artifact monitoring from accepting an unrelated SERVER artifact;
- preserves local-first behavior, approval gates, identity, trust, Truth Firewall, lineage, compatibility identifiers, and CLIENT/SERVER authority separation.

## Immediate failed-build lineage

### CFv2.1.27 R5 — INT-FORGE-079A

- workflow run: `31069235859`
- result: manual CLIENT dispatch resolved stale repository CLIENT R5 rather than the later prepared CLIENT source;
- failure: malformed doubled Kotlin braces in `ForgeConveyorStateStore.kt` caused CLIENT compilation failure;
- boundary: immutable failed-build evidence; not promoted.

### CFv2.1.27 R7 — INT-FORGE-081A

- direct parent of R8;
- repaired the malformed `ForgeConveyorStateStore.kt` source and integrated Dragon Master Workshop, Invitation Invocation, §wyrlish, §wyrlix/§wyrver naming, theme-anchor, presence, and roadmap documentation;
- source-only evidence; no Android build success claimed.

## Preserved earlier current repository lineage

The earlier repository candidate remains historical evidence and is not rewritten:

- `CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8`
- versionCode `131`
- checkpoint `INT-FIX-060C`
- source SHA-256 `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912`
- owner-reported Android build success; not promoted.

Earlier detailed CLIENT history remains recoverable through repository history and package-internal lineage records. This reconciliation advances the non-promoted candidate accounting pointer only; it does not erase prior candidate evidence or change promoted authority.

## Mandatory accounting rule

Every later CLIENT candidate must update package-internal `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file, `../reference/CURRENT_CANDIDATE_LINEAGE.md`, and the non-promoted candidate pointer in `../CURRENT_AUTHORITY.md`. Patch Note Accounting remains separate from source integrity, Android builds, device acceptance, promotion, release, and deployment.
