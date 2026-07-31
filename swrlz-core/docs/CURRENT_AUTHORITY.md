# Current Authority — 2026-07-31

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Android applicationId: `sh.swurlz.core`
- versionCode: `107`
- versionName: `2.1.9-package-pair-repair-v1`
- Checkpoint: `INT-THEME-035D`
- Status: package pair and repository CLIENT debug build verified; device acceptance pending

### SERVER

- File: `sources/server/SERVER_CFv2.1.0_SWRLZ.zip`
- SHA-256: `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940`
- Android applicationId: `sh.swrlz.nodehost`
- versionCode: `50`
- versionName: `2.1.0-forge-parity-portable-repository-v1`

## Current candidate pointer — not promoted authority

Current post-041H CLIENT/SERVER candidate lineage is maintained in `reference/CURRENT_CANDIDATE_LINEAGE.md`, with component-level history in:

- `patch-notes/CLIENT_PATCH_NOTES.md`
- `patch-notes/SERVER_PATCH_NOTES.md`

As of 2026-07-31, repository Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` carries the current INT-AI-060A transport identities:

- CLIENT CFv2.1.27 R1 — SHA-256 `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`;
- SERVER CFv2.1.25 R1 transport filename `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1.transport.json` — SHA-256 `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`.

INT-FILE-059A previously packaged different source bytes under the same external CLIENT CFv2.1.27 R1 / SERVER CFv2.1.25 R1 identifiers. That identity collision is documented explicitly in `reference/CURRENT_CANDIDATE_LINEAGE.md`; the sources must not be conflated. The next candidate must advance version and/or revision.

None of this changes the promoted rows above.

## Later candidate lineage — historical 041H baseline, not promoted authority

The repository also contains earlier candidate/evidence lineage. These entries are intentionally separated from promoted source authority.

### CLIENT CFv2.1.22 candidate

| Revision | VC | Source SHA-256 | Repository Forge commit | Authority status |
|---|---:|---|---|---|
| R1 | 120 | `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5` | `1d3fa542db0f700a1f35256be9317393d25bbc8c` | candidate only |

CLIENT CFv2.1.22 R1 is checkpoint `INT-UX-039Q`, with parent `CLIENT_CFv2.1.21_SWRLZ_CANDIDATE_R2.zip`. Repository transport includes checksum and candidate-manifest evidence. Its candidate manifest records source/static validation but Android compilation was blocked before compilation because the required Gradle distribution was unavailable; APK build remained pending. This candidate therefore does not replace promoted CLIENT CFv2.1.9 authority.

### SERVER CFv2.1.9 SWRLIE candidates

| Revision | VC | Source SHA-256 | Repository Forge commit | Authority status |
|---|---:|---|---|---|
| R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | `55654e3bca3b80445bb0873d545966a8a7131a29` | candidate only |
| R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | `2ea339f972178e71819225def7f7a0d33c48636e` | candidate only |
| R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | `54c64be91e0fdc0bf229a1389518707eec150356` | candidate only |
| R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1` | candidate only |
| R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7` | candidate only |
| R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | `cb073ca4c008109aec9da4ad6f111657d31bc421` | candidate only |

R1-R6 transport/checksum presence establishes the candidate source identity represented by those Forge commits. R1/R2 repository transport includes candidate-manifest evidence; R3-R6 repository transport does not contain the separately packaged candidate manifests. Transport evidence does **not** by itself establish Android compilation, APK build, device behavior, integration, promotion, release, deployment, or installation.

Project-owner/operator evidence separately reports a successful R5 Android build. A later user-supplied device screenshot shows SERVER CFv2.1.9 VC64 rendering the current Chat/Command Center surface. That screenshot is device-visible working-state evidence for VC64, but it is not treated as exact source-SHA → CI workflow → APK provenance or as promotion evidence.

See `checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md` for R1-R5 progression and the later dense-chat/identity synchronization record for R6 and subsequent architecture clarifications.

## CLIENT checkpoint boundary

CLIENT CFv2.1.9 preserves the complete CFv2.1.8 declarative ThemePack presentation implementation. It repairs package/application identity and the canonical sidecar-manifest contract after CI stopped before compilation on the CFv2.1.8 manifest. CFv2.1.8 remains preserved as failed package-pair lineage; CFv2.1.7 remains the preceding implementation rollback baseline.

Theme selection remains local and presentation-only. SERVER, protocol, trust, Truth Firewall, identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility automation, and offline-first behavior are unchanged by that CLIENT checkpoint.

## Validation boundary

The CLIENT CFv2.1.9 source package, SHA-256 receipt, and manifest pass both local and repository package-pair verification. Automatic Source Package Integrity run `30223152048` and APK Router run `30223152052` passed. The resulting debug APK has SHA-256 `0f7312dd346c6eb587b0ec44ab28b9dd30e9371799c26dbbe657fdc354fba419`.

Its source-behavior diff from CFv2.1.8 is limited to build/package identity and documentation. The promoted SERVER authority entry above remains CFv2.1.0; later candidate lineage is documented separately and is not promoted by this authority synchronization.

Device behavior, release signing, distribution, installation, and deployment success are **not** claimed unless separately evidenced for the applicable candidate/version.

## Historical evidence

Documentation Rebuild v2 and the corrected CFv2.1.0 handoff are preserved under `docs/rebuild-v2/` and `docs/handoffs/`. References to the previous `ahazus420-stack/Swrlzcore` repository describe historical evidence and migration lineage; they are not the current repository authority.
