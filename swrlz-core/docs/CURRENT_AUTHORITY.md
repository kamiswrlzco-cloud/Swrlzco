# Current Authority — 2026-07-26

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current source packages

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.8_SWRLZ.zip`
- SHA-256: `d344e683cc76756020b1a02e118b2417c03d6552eeb032dd5dd91058c0f7f055`
- Android applicationId: `sh.swurlz.core`
- versionCode: `106`
- versionName: `2.1.8-theme-chrome-runtime-repair-v1`
- Checkpoint: `INT-THEME-035C`
- Status: source-only implementation verified; compilation and device acceptance pending

### SERVER

- File: `sources/server/SERVER_CFv2.1.0_SWRLZ.zip`
- SHA-256: `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940`
- Android applicationId: `sh.swrlz.nodehost`
- versionCode: `50`
- versionName: `2.1.0-forge-parity-portable-repository-v1`

## CLIENT checkpoint boundary

CLIENT CFv2.1.8 extends the declarative ThemePack presentation system across the CLIENT
shell and repairs launcher, startup, preview-progress, and Jester ignition behavior.
The immutable CFv2.1.7 parent remains beside it as the rollback baseline.

Theme selection remains local and presentation-only. SERVER, protocol, trust, Truth Firewall,
identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility
automation, and offline-first behavior are unchanged.

## Validation boundary

The CLIENT CFv2.1.8 source package and SHA-256 receipt are present and hash-matched.
It also has a package manifest and source-only checkpoint evidence. The SERVER authority entry
above is preserved from the repository baseline and was not modified or revalidated by this
CLIENT-only checkpoint.
Compilation, tests, APK assembly, device behavior, workflow execution, and release success are
**not** claimed.

## Historical evidence

Documentation Rebuild v2 and the corrected CFv2.1.0 handoff are preserved under
`docs/rebuild-v2/` and `docs/handoffs/`. References to the previous
`ahazus420-stack/Swrlzcore` repository describe historical evidence and migration lineage;
they are not the current repository authority.
