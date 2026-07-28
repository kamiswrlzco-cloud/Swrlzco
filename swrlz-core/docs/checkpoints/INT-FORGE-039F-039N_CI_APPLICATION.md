# INT-FORGE-039F + INT-FORGE-039N — Repository CI Application

Date: 2026-07-28  
Status: **IMPLEMENTED — repository CI transport/build-input support; CLIENT runtime remains candidate/build-pending**

## Objective

Apply the repository-side counterpart for the approved Forge transport and build-input contracts:

- INT-FORGE-039F — deterministic chunked source transport with verified reconstruction;
- INT-FORGE-039N — source ZIP required for APK build eligibility, checksum and package manifest optional evidence, supplied contradictions fail closed.

This checkpoint changes repository CI behavior only. It does not promote a CLIENT or SERVER candidate and does not change `docs/CURRENT_AUTHORITY.md`.

## Evidence that motivated the transport change

Device Forge evidence for SERVER CFv2.1.8 candidate R3 showed that the package triple passed local validation and a tiny manifest Git blob was created, while the 40,290,065-byte source ZIP streamed to 100% and then the repository operation returned 401. Immediate authentication re-probe remained valid. The resulting engineering requirement is to avoid depending on one large Git blob operation for large source archives while preserving exact whole-ZIP identity.

## Applied repository files

The following files were updated on `main`:

1. `.github/workflows/swrlz-apk-router.yml`
2. `swrlz-core/tools/ci/resolve_swrlz_source.py`
3. `swrlz-core/tools/ci/verify_swrlz_package_pair.py`
4. `swrlz-core/tools/ci/test_resolve_swrlz_source.py`

Application commit chain:

- `2c0c2d76af164324b2db4f931ff8592f833626f7` — chunk-aware resolver and optional evidence;
- `08b3eec90389051b6e597a55569afacc9a3b4e81` — ZIP-only build eligibility with strict supplied evidence;
- `9ed835d06ae35f0b299c3231c0401c69a5c0fd2a` — chunk reconstruction and ZIP-only resolver tests;
- `9d166a62cbdfeacb35dec242502bc92907940515` — APK Router workflow integration.

## Repository CI behavior now implemented

### Direct source

A CLIENT or SERVER `.zip` at the lane root is a build-eligible source identity by itself.

- checksum missing: allowed;
- package manifest missing: allowed;
- supplied checksum: validated against calculated ZIP SHA-256;
- supplied package manifest: parsed and validated against ZIP basename, SHA-256, optional size, and `verified: true`;
- conflicting supplied evidence: build is blocked.

The workflow computes source SHA-256 regardless of whether a checksum sidecar was supplied.

### Chunked source transport

A lane-root `*.transport.json` may represent the source ZIP using transport `chunked-git-blobs-v1`.

The resolver:

1. validates transport schema, component, whole ZIP identity, whole size, verification flag, and non-empty chunk list;
2. requires sequential chunk indexes;
3. constrains every chunk/evidence path to the selected component lane;
4. verifies every chunk exists and matches declared size and SHA-256;
5. reconstructs the ZIP under runner temporary storage;
6. verifies reconstructed whole size and SHA-256 before the Android build sees it;
7. validates optional checksum/manifest evidence when the transport manifest declares those evidence paths.

Chunks are transport objects only. The reconstructed ZIP in runner temporary storage is the build input and its whole SHA-256 remains the source identity.

### Router behavior

Push routing now treats source identities as:

- `swrlz-core/sources/client/*.zip`
- `swrlz-core/sources/client/*.transport.json`
- `swrlz-core/sources/server/*.zip`
- `swrlz-core/sources/server/*.transport.json`

Checksum/manifest-only repository changes do not independently request an Android build.

The build job records source kind, checksum evidence, manifest evidence, and transport manifest provenance.

## Pre-application validation

Before repository writes, the patch was applied against the exact live file revisions and validated locally:

- resolver unit tests: **8 / 8 pass**;
- Python compilation of patched CI tools: **pass**;
- direct ZIP without sidecars: **pass**;
- conflicting checksum: **fails closed**;
- conflicting manifest: **fails closed**;
- exact chunk reconstruction: **pass**;
- corrupted chunk: **fails closed**;
- transport-manifest push selection: **pass**.

A separate source/static simulation split SERVER CFv2.1.8 R3 into five deterministic chunks and reconstructed the original whole-ZIP SHA-256 `506d83b058bf8127092a8d08c20c61f763bbb97e4847d8f6ce4d3f5c0df7c451`.

## CLIENT runtime boundary

CLIENT CFv2.1.20 candidate R1 contains the corresponding Forge-side chunking and optional-evidence implementation, but it remains a candidate. Its local Android compilation was blocked before Kotlin compilation because Gradle 8.7 was unavailable in the local cache and the environment could not resolve `services.gradle.org`.

Therefore this checkpoint does **not** claim CLIENT compile, APK, device, release, or promotion success.

## Authority boundary

Repository CI support is implemented. Source authority remains whatever `docs/CURRENT_AUTHORITY.md` records until a later promotion checkpoint provides matching build/runtime evidence.

This checkpoint does not:

- change CLIENT/SERVER protocol versions;
- change trust, Truth Firewall, identity proof, mission authority, permissions, or local/remote semantics;
- dispatch a workflow manually;
- release, deploy, install, or promote any candidate;
- treat optional sidecars as optional when they are actually supplied but contradictory.
