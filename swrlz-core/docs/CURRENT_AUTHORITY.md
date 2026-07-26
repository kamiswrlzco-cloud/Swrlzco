# Current Authority — 2026-07-26

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current source packages

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Android applicationId: `sh.swurlz.core`
- versionCode: `107`
- versionName: `2.1.9-package-pair-repair-v1`
- Checkpoint: `INT-THEME-035D`
- Status: package pair verified locally with the repository verifier; repository CI compilation and device acceptance pending

### SERVER

- File: `sources/server/SERVER_CFv2.1.0_SWRLZ.zip`
- SHA-256: `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940`
- Android applicationId: `sh.swrlz.nodehost`
- versionCode: `50`
- versionName: `2.1.0-forge-parity-portable-repository-v1`

## CLIENT checkpoint boundary

CLIENT CFv2.1.9 preserves the complete CFv2.1.8 declarative ThemePack presentation
implementation. It repairs package/application identity and the canonical sidecar-manifest
contract after CI stopped before compilation on the CFv2.1.8 manifest. CFv2.1.8 remains
preserved as failed package-pair lineage; CFv2.1.7 remains the preceding implementation
rollback baseline.

Theme selection remains local and presentation-only. SERVER, protocol, trust, Truth Firewall,
identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility
automation, and offline-first behavior are unchanged.

## Validation boundary

The CLIENT CFv2.1.9 source package, SHA-256 receipt, and manifest are present and pass the
repository package-pair verifier locally. Its source-behavior diff from CFv2.1.8 is limited
to build/package identity and documentation. The SERVER authority entry above is preserved
from the repository baseline and was not modified or revalidated by this CLIENT-only checkpoint.
Repository CI compilation, APK assembly, device behavior, release, and deployment success are
**not** claimed.

## Historical evidence

Documentation Rebuild v2 and the corrected CFv2.1.0 handoff are preserved under
`docs/rebuild-v2/` and `docs/handoffs/`. References to the previous
`ahazus420-stack/Swrlzcore` repository describe historical evidence and migration lineage;
they are not the current repository authority.
