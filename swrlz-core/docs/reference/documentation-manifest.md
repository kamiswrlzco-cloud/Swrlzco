# Documentation Manifest and Package Accounting

**Migration generation:** Official `Swrlzco/swrlz-core` bootstrap  
**Prepared:** 2026-07-26  
**Last policy synchronization:** 2026-07-31 — INT-CI-DOC-060A branch preparation  
**Last distributed architecture synchronization:** 2026-07-28 — INT-DOC-AI-040A  
**Last update architecture synchronization:** 2026-07-28 — INT-DOC-UPD-040C-040D  
**Last SWRLIE runtime/candidate synchronization:** 2026-07-29 — INT-DOC-AI-041H  
**Last Forge/candidate/patch-note synchronization:** 2026-07-31 — INT-FORGE-054A-R2 + INT-CI-DOC-060A

## Current promoted source baseline

| Role | Package | SHA-256 |
|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` |

Later source candidates do not alter this table until an explicit promotion checkpoint succeeds.

## Recent CLIENT candidate lineage

| Candidate | VC | SHA-256 | Evidence state |
|---|---:|---|---|
| CLIENT CFv2.1.22 R1 | 120 | `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5` | Forge commit `1d3fa542db0f700a1f35256be9317393d25bbc8c`; checksum+candidate-manifest transport evidence; source/static validation; recorded compile attempt blocked before compilation |
| CLIENT CFv2.1.24 R1 | 122 | `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55` | Forge Transport V2 candidate lineage; not promoted here |
| CLIENT CFv2.1.25 R1 | 123 | `6ce26560dab4113d06bb1360c260dcc087fc2fa8b583f1583ada2bfe3688f5b2` | provider/behavior-cleanup parent for later shared Forge work; not promoted here |
| CLIENT CFv2.1.26 R1 | 124 | `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` | `INT-FORGE-054A-R2` source-only Forge parity/Chat-Settings candidate; no build/promotion claim |
| CLIENT CFv2.1.27 R1 | unknown from transport alone | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`; 15,127,739-byte / 4-chunk transport; checksum evidence, no separately packaged candidate manifest; transport identity only |

## Recent SERVER candidate lineage

### SERVER CFv2.1.9 SWRLIE sequence

| Candidate | VC | SHA-256 | Repository Forge commit | Promotion |
|---|---:|---|---|---|
| SERVER CFv2.1.9 R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | `55654e3bca3b80445bb0873d545966a8a7131a29` | not verified |
| SERVER CFv2.1.9 R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | `2ea339f972178e71819225def7f7a0d33c48636e` | not verified |
| SERVER CFv2.1.9 R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | `54c64be91e0fdc0bf229a1389518707eec150356` | not verified |
| SERVER CFv2.1.9 R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1` | not verified |
| SERVER CFv2.1.9 R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7` | not verified |
| SERVER CFv2.1.9 R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | `cb073ca4c008109aec9da4ad6f111657d31bc421` | not verified |

R1/R2 repository transport includes candidate-manifest evidence. R3-R6 transport commits establish source transport/checksum identity but do not contain their separately packaged candidate manifests. Project-owner/operator evidence separately reports a successful R5 Android build; a later user-supplied screenshot showed SERVER CFv2.1.9 VC64. Those are distinct evidence classes and do not silently promote the source.

### Later SERVER sequence

| Candidate | VC | SHA-256 | Evidence state |
|---|---:|---|---|
| SERVER CFv2.1.20 R1 | 78 | `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915` | `INT-PERF-050B` greeting fast-path candidate; separate device fast-path evidence exists |
| SERVER CFv2.1.21 R1 | 79 | `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791` | `INT-PERF-050D` status fast-path candidate |
| SERVER CFv2.1.22 R1 | 80 | `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d` | `INT-CHAT-051A` compact Chat control/model-asset candidate |
| SERVER CFv2.1.23 R1 | 81 | `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6` | `INT-PERF-052A` conservative short-casual fast-path candidate |
| SERVER CFv2.1.24 R1 | 82 | `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` | `INT-FORGE-054A-R2` source-only Forge conveyor/lineage candidate; no build/promotion claim |
| SERVER CFv2.1.25 R1 repository identity `-1` | unknown from transport alone | `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` | Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`; 40,710,681-byte / 10-chunk transport; checksum evidence, no separately packaged candidate manifest; transport identity only |

The transport/checksum records prove repository presence and exact transported whole-ZIP identity. They do not by themselves prove Android compilation, APK build, device behavior, integration, release, deployment, installation, or promotion.

## 2026-07-31 CI/documentation synchronization — INT-CI-DOC-060A

Source Package Integrity run `30658738049` exposed a selector defect: recursive source-lane matching let nested `.transport/.../evidence/*.sha256` files masquerade as lane-root checksum sidecars, producing nonexistent nested ZIP paths and `Missing ZIP` failure.

The checkpoint branch `checkpoint/int-ci-doc-060a-router-docs` prepares these fixes:

- Source Package Integrity direct-source selection restricted to lane-root CLIENT/SERVER source identities/evidence;
- nested transport chunks/evidence excluded from direct package-pair selection;
- APK Router push routing restricted to lane-root source identities/evidence;
- manual/request `BOTH` target support while keeping build matrix components CLIENT/SERVER;
- explicit rejection of an ambiguous single manual `source_zip` with `BOTH`;
- current documentation and per-component patch-note ledgers synchronized.

A separate APK Router screenshot showed a resolver job waiting for a GitHub-hosted runner. That queue state is external scheduling evidence and is not labelled a workflow logic defect here.

Until explicit merge and validation, the 060A repair is branch state only. No rerun, APK build, promotion, release, deployment, or installation is claimed.

## Mandatory patch-note accounting

Maintained ledgers:

- `../client/PATCH_NOTES.md`
- `../server/PATCH_NOTES.md`

Future accepted source-update checkpoints are documentation-incomplete until the affected component ledger records checkpoint/version/parent/source SHA/change summary/evidence boundary. Shared CLIENT/SERVER checkpoints update both ledgers.

Already packaged ZIPs are immutable evidence and must not be modified merely to retrofit internal changelog text. Repository-level patch notes fill historical narrative gaps without changing old package bytes or source identity.

Patch notes remain subordinate to canonical source ZIP/SHA, accepted manifests/contracts, and stronger build/device/promotion evidence.

## Approved scope not yet implementation-evidenced

`INT-FILE-059A` is approved for a shared CLIENT/SERVER Forge File Lab + Archive Cartographer foundation: read-only inventory/search/hash/structural map/preview/selective extraction; staged text/archive-entry editing with explicit commit/new checksum/parent lineage; binary split/exact recombination; logical size-bounded shards with manifests/provenance/recovery metadata; configurable SAF work/output/shard directories; and deterministic analyzer APIs for later SWRLZ evidence retrieval.

Approval is not implementation/package evidence.

## Counting policy

Report these separately whenever producing handoffs or releases:

- `workspace_source_count`
- `packaged_source_count`
- `documentation_file_count`
- `excluded_file_count`
- `package_entry_count`

## Imported documentation

The maintained `docs/` seed was imported from `SWRLZ_Documentation_Rebuild_v2_FULL.zip`.

The following were intentionally **not promoted into active repository authority**:

- `.reference/` extracted historical source-tree duplicates
- `_wordmesh_doc/` raw extracted Office/XML internals

Historical rebuild reports were retained under `docs/rebuild-v2/`.

## Maintained architecture additions

### INT-DOC-AI-040A — distributed intelligence

`INT-DOC-AI-040A` adds `../architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` as the canonical design consolidation for intended distributed CLIENT/SERVER/SWRLIE architecture: operating modes, authority boundaries, SERVER-heavy reasoning/network direction, model independence, Model Vault/model-lineage direction, node-hosting, Forge delegation, and learning-telemetry design.

This documentation addition is architecture evidence only. Later source candidates implement parts of the direction but do not retroactively make 040A implementation evidence.

### INT-DOC-UPD-040C-040D — live pack and runtime update architecture

Maintained artifacts:

- `../architecture/SWRLZ_RUNTIME_AND_LIVE_PACK_UPDATE_ARCHITECTURE_V1.md`
- `../contracts/SWRLZ_UPDATE_AND_PACK_MANIFEST_CONTRACT_V1.md`
- `../checkpoints/INT-DOC-UPD-040C-040D_UPDATE_ARCHITECTURE_SYNC.md`

They define stable signed runtime products versus non-executable live packs, SERVER-owned update discovery, source-provider abstraction, content-addressed reuse, immutable staged generations, rollback, and separate Android package-replacement semantics. Neural reasoners remain advisory; SWRLZ retains Truth Firewall, routing, approvals, trust, file/Forge/update activation and rollback authority.

`INT-PACK-040C` and `INT-UPD-040D` remain separately implementation-gated unless newer evidence explicitly supersedes that state.

### INT-DOC-AI-040B-R1-R5 — SWRLIE runtime candidate synchronization

Maintained artifacts:

- `../checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md`
- `../architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md`
- `../architecture/SWRLZ_ARCHIVE_LINEAGE_AND_FILE_ORGANIZATION_EXTENSION_V1.md`

They synchronize local SWRLIE inference/no-model behavior, SERVER Chat/Settings, startup/model recovery, Model Vault/safe switching, prompt/context control, Swurlzara compilation, self-knowledge/runtime grounding, Skills placement, hardware tiers, Simulation Forge direction, and archive-lineage-aware file organization.

### INT-DOC-AI-041H — dense-chat identity/model synchronization

Maintained artifacts:

- `../architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md`
- `../checkpoints/INT-DOC-AI-041H_DENSE_CHAT_IDENTITY_MODEL_SYNC.md`

Canonical identity law remains:

- SWRLZ/Swurlz = persistent primary identity;
- selected LLM = replaceable reasoning engine;
- Swurlzara = replaceable expression/profile lens;
- SWRLIE = first-party reasoning/provider interface;
- Truth Firewall = intrinsic SWRLZ epistemic/authority behavior.

No profile/model swap may silently rewrite primary identity or authority.

## Version and build-input policy

Promoted source authority remains the explicitly promoted source package + exact checksum under `sources/`, subject to later supersession by a newer evidence-gated promotion.

APK **build eligibility is a separate evidence class**. Repository CI may attempt a build from a valid CLIENT/SERVER source ZIP without a supplied checksum/package manifest and compute the whole ZIP SHA-256 itself. When checksum or package-manifest evidence is supplied, it must validate exactly; contradictory supplied evidence blocks the build.

Large source archives may be transported as verified chunks described by lane-root `*.transport.json`. The transport manifest/chunks are not independent source authority. CI verifies declared chunks, reconstructs the original ZIP in runner temporary storage, and verifies whole size/SHA-256 before compilation.

A successful build from ZIP-only or reconstructed chunk transport does not by itself promote the ZIP. Promotion remains a separate checkpoint requiring applicable source/build/lineage/documentation/runtime evidence.

CLIENT CFv2.1.9 package verification and CI debug build remain evidenced under `../evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md`. Later candidates remain candidate/evidence lineage until a separate promotion checkpoint changes authority.
