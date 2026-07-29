# Documentation Manifest and Package Accounting

**Migration generation:** New official `Swrlzco/swrlz-core` bootstrap  
**Prepared:** 2026-07-26  
**Last policy synchronization:** 2026-07-28 — INT-FORGE-039F + INT-FORGE-039N  
**Last distributed architecture synchronization:** 2026-07-28 — INT-DOC-AI-040A  
**Last update architecture synchronization:** 2026-07-28 — INT-DOC-UPD-040C-040D  
**Last SWRLIE runtime/candidate synchronization:** 2026-07-29 — INT-DOC-AI-040B-R1-R5

## Current promoted source baseline

| Role | Package | SHA-256 |
|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` |

Later source candidates do not alter this table until an explicit promotion checkpoint succeeds.

## Latest SERVER SWRLIE candidate lineage in repository transport

| Candidate | VC | SHA-256 | Repository Forge commit | Promotion |
|---|---:|---|---|---|
| SERVER CFv2.1.9 R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | `55654e3bca3b80445bb0873d545966a8a7131a29` | not verified |
| SERVER CFv2.1.9 R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | `2ea339f972178e71819225def7f7a0d33c48636e` | not verified |
| SERVER CFv2.1.9 R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | `54c64be91e0fdc0bf229a1389518707eec150356` | not verified |
| SERVER CFv2.1.9 R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1` | not verified |
| SERVER CFv2.1.9 R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7` | not verified |

The transport/checksum records prove the repository presence and exact candidate ZIP identity represented by those Forge commits. They do not by themselves prove Android compilation, APK build, device behavior, integration, release, deployment, or promotion.

R1 and R2 Forge uploads include candidate-manifest evidence in their transport evidence sets. R3-R5 Forge uploads recorded checksum + transport identity but did not add the separately packaged candidate manifest files to repository transport evidence. Documentation must not silently treat absent repository manifests as present.

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

`INT-DOC-AI-040A` adds `../architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md` as the canonical design consolidation for the intended distributed CLIENT/SERVER/SWRLIE architecture. It documents operating modes, authority boundaries, SERVER-heavy reasoning/network direction, model independence, Model Vault/model-lineage direction, node-hosting, Forge delegation, and learning-telemetry design.

This documentation addition is architecture evidence only. Later 040B source candidates now implement part of the design, but 040A itself did not alter source authority.

### INT-DOC-UPD-040C-040D — live pack and runtime update architecture

`INT-DOC-UPD-040C-040D` adds:

- `../architecture/SWRLZ_RUNTIME_AND_LIVE_PACK_UPDATE_ARCHITECTURE_V1.md`
- `../contracts/SWRLZ_UPDATE_AND_PACK_MANIFEST_CONTRACT_V1.md`
- `../checkpoints/INT-DOC-UPD-040C-040D_UPDATE_ARCHITECTURE_SYNC.md`

This documentation defines the intended split between stable signed CLIENT/SERVER/Launcher runtime products and non-executable live packs that may be downloaded, verified, staged, and activated while SWRLZ continues running. It records SERVER-owned normal internet update discovery, source-provider abstraction, content-addressed object reuse, immutable staged generations, rollback, and separate Android package-replacement semantics for executable runtime changes.

It also records the SWRLIE base-plus-modules direction: a relatively stable base model with independently versioned adapters, knowledge, configuration, and specialist modules where technically appropriate. The neural model remains advisory; SWRLZ retains Truth Firewall, command routing, approval policy, tool schemas, node trust, file authority, Forge validation, update trust, activation, and rollback authority.

`INT-PACK-040C` and `INT-UPD-040D` remain planned implementation checkpoints. The 040B R1-R5 source-candidate lineage does not imply those updater checkpoints are implemented.

### INT-DOC-AI-040B-R1-R5 — SWRLIE runtime candidate synchronization

This docs-only checkpoint adds:

- `../checkpoints/INT-DOC-AI-040B-R1-R5_SWRLIE_RUNTIME_SYNC.md`
- `../architecture/SWRLZ_SWRLIE_RUNTIME_CAPABILITY_AND_SKILLS_EVOLUTION_V1.md`
- `../architecture/SWRLZ_ARCHIVE_LINEAGE_AND_FILE_ORGANIZATION_EXTENSION_V1.md`

It synchronizes maintained documentation with SERVER CFv2.1.9 R1-R5 source-candidate progression:

- local SWRLIE inference/no-model foundation;
- first-class SERVER Chat/Settings IA;
- local startup auto-load, adaptive/copyable Chat, Update Ledger, approval-tone guard;
- multi-GGUF Model Vault, safe switching, adaptive context/inference controls, prompt-budget guard, code-native Swurlzara;
- local self-knowledge, shared Update Ledger retrieval, and live runtime/model grounding.

It also records design decisions that remain planned: SWRLZ Skills upstream of the LLM/profile, monotonic model capability tiers, personality control plane, hardware-tier packs, structured Simulation Forge/LLMware, specialist media models, and archive-lineage-aware file organization.

This synchronization does not alter `CURRENT_AUTHORITY.md`, promote R1-R5, add model weights, execute workflows/builds, enable web access, train models, or authorize device file changes.

## Version and build-input policy

Current promoted source authority remains the source package + exact checksum under `sources/`, subject to later supersession by a newer explicitly verified package or repository HEAD.

APK **build eligibility is a separate evidence class**. Repository CI may attempt a build from a valid CLIENT/SERVER source ZIP without a supplied checksum or package manifest. CI calculates the source ZIP SHA-256 itself. When checksum or package-manifest evidence is supplied, it must validate exactly; contradictory supplied evidence blocks the build.

Large source archives may be transported as verified chunks described by `*.transport.json`. The transport manifest/chunks are not source authority. CI verifies each chunk, reconstructs the original ZIP in runner temporary storage, and verifies whole size/SHA-256 before compilation.

A successful build from ZIP-only or reconstructed chunk transport does not by itself promote the ZIP to current authority. Promotion remains a separate checkpoint requiring the applicable package, build, lineage, documentation, and runtime evidence.

CLIENT CFv2.1.9 package verification and CI debug build are evidenced under `../evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md`. Device testing and runtime acceptance remain evidence-gated.

The SERVER promoted row remains CFv2.1.0. SERVER CFv2.1.9 R1-R5 are candidate/evidence lineage only until a separate promotion checkpoint changes authority.

Repository CI transport/build-input policy application is recorded in `../checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md`; it does not alter the source-baseline table above.
