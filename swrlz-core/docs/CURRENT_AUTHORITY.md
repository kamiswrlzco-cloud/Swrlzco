# Current Authority — 2026-07-31

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

The promoted-source rows below are intentionally unchanged by later candidate uploads or this documentation/CI repair. Promotion requires its own evidence-gated checkpoint.

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

## Later candidate lineage — not promoted authority

The repository and accepted checkpoint evidence contain later candidate lineage. These entries are intentionally separated from promoted source authority.

### CLIENT candidate lineage

| Candidate | VC | Source SHA-256 | Evidence / status |
|---|---:|---|---|
| CFv2.1.22 R1 | 120 | `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5` | `INT-UX-039Q`; Forge commit `1d3fa542db0f700a1f35256be9317393d25bbc8c`; checksum+candidate-manifest transport evidence; source/static validation; recorded compile attempt blocked before compilation |
| CFv2.1.24 R1 | 122 | `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55` | Forge Transport V2 candidate lineage; protected chunk transport/retry diagnostics; not promoted by this document |
| CFv2.1.25 R1 | 123 | `6ce26560dab4113d06bb1360c260dcc087fc2fa8b583f1583ada2bfe3688f5b2` | behavior-shard/provider-cleanup parent for later Forge-parity work; not promoted by this document |
| CFv2.1.26 R1 | 124 | `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` | `INT-FORGE-054A-R2`; source-only shared Forge conveyor / Chat-Settings parity candidate; no APK build or promotion claim in this authority sync |
| CFv2.1.27 R1 | unknown from repository transport alone | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | latest Forge repository transport at commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`; 15,127,739-byte verified chunk transport with checksum evidence, no separately packaged candidate manifest in that transaction; transport identity only |

`INT-FORGE-054A-R2` gives CLIENT the shared Forge conveyor baseline while preserving CLIENT-only Missions, legacy Dev Mode, and CLIENT-side execution roles; it does not transfer SERVER-only inference/model/evidence authority into CLIENT.

### SERVER SWRLIE / later candidate lineage

| Candidate | VC | Source SHA-256 | Evidence / status |
|---|---:|---|---|
| CFv2.1.9 R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | candidate only; Forge commit `55654e3bca3b80445bb0873d545966a8a7131a29` |
| CFv2.1.9 R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | candidate only; Forge commit `2ea339f972178e71819225def7f7a0d33c48636e` |
| CFv2.1.9 R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | candidate only; Forge commit `54c64be91e0fdc0bf229a1389518707eec150356` |
| CFv2.1.9 R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | candidate only; Forge commit `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1` |
| CFv2.1.9 R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | candidate only; Forge commit `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7` |
| CFv2.1.9 R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | candidate only; Forge commit `cb073ca4c008109aec9da4ad6f111657d31bc421` |
| CFv2.1.20 R1 | 78 | `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915` | `INT-PERF-050B` greeting fast path source candidate; device evidence separately showed the fast greeting route working |
| CFv2.1.21 R1 | 79 | `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791` | `INT-PERF-050D` status fast path source candidate |
| CFv2.1.22 R1 | 80 | `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d` | `INT-CHAT-051A` compact Chat control-orb/model-asset recovery candidate |
| CFv2.1.23 R1 | 81 | `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6` | `INT-PERF-052A` conservative casual-short fast path source candidate |
| CFv2.1.24 R1 | 82 | `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` | `INT-FORGE-054A-R2`; source-only shared Forge conveyor/lineage candidate; no APK build or promotion claim in this authority sync |
| CFv2.1.25 R1 repository identity `-1` | unknown from repository transport alone | `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` | latest Forge repository transport at commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`; 40,710,681-byte verified chunk transport with checksum evidence, no separately packaged candidate manifest in that transaction; transport identity only |

R1-R6 transport/checksum presence establishes candidate source identity represented by those Forge commits. R1/R2 repository transport includes candidate-manifest evidence; R3-R6 repository transport does not contain the separately packaged candidate manifests. Transport evidence does **not** by itself establish Android compilation, APK build, device behavior, integration, promotion, release, deployment, or installation.

Project-owner/operator evidence separately reports a successful R5 Android build. A later user-supplied device screenshot shows SERVER CFv2.1.9 VC64 rendering the then-current Chat/Command Center surface. That screenshot is device-visible working-state evidence for VC64, not exact source-SHA → CI workflow → APK provenance or promotion evidence.

## Current CI/documentation repair — INT-CI-DOC-060A

Source Package Integrity run `30658738049` failed because the prior workflow recursively interpreted nested `.transport/.../evidence/*.sha256` files as lane-root source sidecars and derived nonexistent nested ZIP paths. The `checkpoint/int-ci-doc-060a-router-docs` branch contains a bounded repair that limits direct source selection to lane-root identities/evidence and hardens APK Router lane-root routing plus manual/request `BOTH` support.

A separate APK Router screenshot showed a resolver job waiting for a GitHub-hosted runner. That waiting condition is scheduling evidence, not proof of Router-code failure.

Until the checkpoint branch is explicitly merged and separately validated, the repair is **prepared branch state**, not main-branch runtime evidence.

## Patch-note authority / completeness rule

Maintained component ledgers now live at:

- `docs/client/PATCH_NOTES.md`
- `docs/server/PATCH_NOTES.md`

Accepted future source updates must synchronize the affected component ledger before documentation is complete. Shared CLIENT/SERVER checkpoints update both ledgers. Already packaged ZIPs remain immutable; missing historical narrative is repaired in repository documentation rather than by changing old ZIP bytes.

Patch notes are evidence navigation, not authority. They do not replace source ZIP/SHA identity, accepted manifests/contracts, or stronger build/device/promotion evidence.

## Approved scope not yet implementation-evidenced here

`INT-FILE-059A` is approved for a shared CLIENT/SERVER Forge File Lab + Archive Cartographer foundation: read-only inventory/search/hash/map/preview/selective extraction, staged text/archive-entry edits with explicit commit/new checksum/lineage, binary split/exact recombination, logical sharding with manifests/provenance, configurable SAF work/output/shard directories, and deterministic analyzer APIs for later SWRLZ evidence retrieval.

Approval alone is not proof that any current candidate implements `INT-FILE-059A`.

## CLIENT checkpoint boundary

CLIENT CFv2.1.9 preserves the complete CFv2.1.8 declarative ThemePack presentation implementation. It repairs package/application identity and the canonical sidecar-manifest contract after CI stopped before compilation on the CFv2.1.8 manifest. CFv2.1.8 remains preserved as failed package-pair lineage; CFv2.1.7 remains the preceding implementation rollback baseline.

Theme selection remains local and presentation-only. SERVER, protocol, trust, Truth Firewall, identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility automation, and offline-first behavior were unchanged by that promoted CLIENT checkpoint.

## Historical validation boundary

The promoted CLIENT CFv2.1.9 source package, SHA-256 receipt, and manifest passed local/repository package-pair verification. Automatic Source Package Integrity run `30223152048` and APK Router run `30223152052` passed, producing a debug APK with SHA-256 `0f7312dd346c6eb587b0ec44ab28b9dd30e9371799c26dbbe657fdc354fba419`.

Later candidate and transport entries above do not silently replace those promoted rows. Device behavior, release signing, distribution, installation, and deployment success are **not** claimed unless separately evidenced for the applicable candidate/version.

## Historical evidence

Documentation Rebuild v2 and the corrected CFv2.1.0 handoff are preserved under `docs/rebuild-v2/` and `docs/handoffs/`. References to the previous `ahazus420-stack/Swrlzcore` repository describe historical evidence and migration lineage; they are not the current repository authority.
