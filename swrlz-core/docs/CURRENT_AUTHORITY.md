# Current Authority — 2026-07-25

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current source packages

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.2_SWRLZ.zip`
- SHA-256: `80ae8f9d4bead7596d60e327e825dd94d96209373017fb514bb957153cc6aa2f`
- Android applicationId: `sh.swurlz.core`
- versionCode: `100`
- versionName: `2.1.2-repository-bootstrap-forge-v1`

### SERVER

- File: `sources/server/SERVER_CFv2.1.0_SWRLZ.zip`
- SHA-256: `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940`
- Android applicationId: `sh.swrlz.nodehost`
- versionCode: `50`
- versionName: `2.1.0-forge-parity-portable-repository-v1`

## Repository bootstrap capability

CLIENT CFv2.1.2 defaults Forge to this repository and `swrlz-core/...` lanes, and can expand a generic bootstrap ZIP into repository root with optional outer-ZIP removal.

## Validation boundary

The source packages and SHA-256 receipts are present and hash-matched in this bootstrap.
Compilation/device/integration success is **not** claimed by this bootstrap.

## Historical evidence

Documentation Rebuild v2 and the corrected CFv2.1.0 handoff are preserved under
`docs/rebuild-v2/` and `docs/handoffs/`. References to the previous
`ahazus420-stack/Swrlzcore` repository describe historical evidence and migration lineage;
they are not the current repository authority.
