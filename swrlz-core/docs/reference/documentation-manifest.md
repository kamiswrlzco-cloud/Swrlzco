# Documentation Manifest and Package Accounting

**Migration generation:** New official `Swrlzco/swrlz-core` bootstrap  
**Prepared:** 2026-07-26  
**Last policy synchronization:** 2026-07-31 — INT-CI-061A  
**Last distributed architecture synchronization:** 2026-07-28 — INT-DOC-AI-040A  
**Last update architecture synchronization:** 2026-07-28 — INT-DOC-UPD-040C-040D  
**Last SWRLIE runtime/candidate synchronization:** 2026-07-31 — INT-AI-060A + INT-CI-061A documentation sync
**Last SERVER candidate synchronization:** 2026-08-04 — INT-FIX-075A

## Current promoted source baseline

| Role | Package | SHA-256 |
|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` |

Later source candidates do not alter this table until an explicit promotion checkpoint succeeds.

## Current candidate lineage pointer

The current post-041H source-candidate lineage is maintained in `CURRENT_CANDIDATE_LINEAGE.md` and the component patch-note files:

- `../patch-notes/CLIENT_PATCH_NOTES.md`
- `../patch-notes/SERVER_PATCH_NOTES.md`

Current component pointers are maintained independently. INT-FIX-075A changes only the SERVER pointer; the CLIENT row remains unchanged pending its own separately governed synchronization.

| Component | Candidate | VC | SHA-256 | Checkpoint | Promotion |
|---|---|---:|---|---|---|
| CLIENT | CFv2.1.27 R1 | 125 | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | INT-AI-060A | candidate only |
| SERVER | CFv2.1.27 R2 | 130 | `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` | INT-FIX-075A | current repository candidate; source/static/package verified; build pending; not promoted |

SERVER R1 / VC129 / SHA `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc` remains preserved failed-build parent lineage. Transport commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` and run `30950003262` prove exact source selection followed by Kotlin compile failure; they do not establish an APK.

INT-FILE-059A previously packaged different bytes under the same external CLIENT CFv2.1.27 R1 / SERVER CFv2.1.25 R1 identities. That collision is explicitly recorded in `CURRENT_CANDIDATE_LINEAGE.md`; the sources are distinguished by exact SHA-256, versionName and checkpoint provenance. The next candidate must advance version and/or revision.

## Historical 041H candidate baseline

### CLIENT CFv2.1.22 candidate

| Candidate | VC | SHA-256 | Repository Forge commit | Promotion |
|---|---:|---|---|---|
| CLIENT CFv2.1.22 R1 | 120 | `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5` | `1d3fa542db0f700a1f35256be9317393d25bbc8c` | not promoted |

CLIENT CFv2.1.22 R1 repository transport includes checksum and candidate-manifest evidence. The manifest records source/static verification, Android compile blocked before compilation because Gradle 8.7 was unavailable and `services.gradle.org` was unreachable, and APK build pending. It does not replace promoted CLIENT CFv2.1.9.

### SERVER CFv2.1.9 SWRLIE candidates

| Candidate | VC | SHA-256 | Repository Forge commit | Promotion |
|---|---:|---|---|---|
| SERVER CFv2.1.9 R1 | 59 | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | `55654e3bca3b80445bb0873d545966a8a7131a29` | not promoted |
| SERVER CFv2.1.9 R2 | 60 | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | `2ea339f972178e71819225def7f7a0d33c48636e` | not promoted |
| SERVER CFv2.1.9 R3 | 61 | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | `54c64be91e0fdc0bf229a1389518707eec150356` | not promoted |
| SERVER CFv2.1.9 R4 | 62 | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1` | not promoted |
| SERVER CFv2.1.9 R5 | 63 | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7` | not promoted |
| SERVER CFv2.1.9 R6 | 64 | `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf` | `cb073ca4c008109aec9da4ad6f111657d31bc421` | not promoted |

Transport/checksum evidence proves repository source identity only. It does not by itself prove Android compilation, APK build, device behavior, integration, release, deployment, installation, or promotion.

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

### INT-DOC-UPD-040C-040D — live pack and runtime update architecture

`INT-DOC-UPD-040C-040D` adds the runtime/live-pack architecture, update/pack manifest contract, and checkpoint synchronization. It defines stable signed runtime products versus non-executable live packs, SERVER-owned discovery, content-addressed reuse, staged generations, rollback and separate Android package-replacement semantics.

### INT-DOC-AI-040B-R1-R5 — SWRLIE runtime candidate synchronization

This docs-only checkpoint synchronized SERVER CFv2.1.9 R1-R5: local inference/no-model foundation, first-class SERVER Chat/Settings, local startup auto-load/adaptive Chat/Update Ledger, multi-GGUF Model Vault and safe switching, adaptive inference/prompt budgeting, code-native Swurlzara, local self-knowledge and runtime/model grounding.

### INT-DOC-AI-041H — dense-chat identity/model synchronization

`INT-DOC-AI-041H` records the identity law:

- SWRLZ/Swurlz is the persistent primary identity;
- the LLM is a replaceable reasoning engine;
- Swurlzara is a replaceable expression/profile lens;
- SWRLIE is the first-party reasoning/provider interface;
- Truth Firewall is intrinsic SWRLZ epistemic/authority behavior.

It catches the older documentation baseline through CLIENT CFv2.1.22 R1 and SERVER CFv2.1.9 R6/VC64.

### INT-FORGE-054A-R2 — shared Forge conveyor / CLIENT mirror

Current package evidence records SERVER CFv2.1.24 R1 and CLIENT CFv2.1.26 R1 as the shared Forge conveyor/lineage and CLIENT parity parent candidates. CLIENT-specific Missions/legacy Dev Mode remain CLIENT-specific; SERVER-only inference authority remains SERVER-only.

### INT-FILE-059A — File Lab / Archive Cartographer packaged candidate

Package evidence records shared CLIENT/SERVER File Lab capabilities: read-only map/search/hash/preview, selective extraction, staged text revisions preserving originals, binary split/recombine, logical shard archives, SAF working/output/shard lanes, and deterministic analyzer/map export surfaces. These packages were not promoted.

### INT-AI-060A — truth/reasoning/expression separation

Package evidence records a shared non-profile Truth Core boundary, reasoning/output-budget separation, and expression/profile shaping that does not own factual truth. Current repository transport for the 060A CLIENT/SERVER packages is recorded above. Gradle/Android compilation was not established by the packaging environment.

### INT-CI-061A — router/integrity/patch-note synchronization

`../checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md` records the source-integrity root cause/fix, APK Router hardening, current candidate synchronization, external identity collision, and mandatory patch-note accounting contract.

`../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` requires every future CLIENT/SERVER source candidate to synchronize human release notes, changelog, machine-readable patch lineage, repository component patch notes, and current candidate accounting when applicable.

## Version and build-input policy

Current promoted source authority remains the source package + exact checksum under `sources/`, subject to later supersession by a newer explicitly verified/promoted package.

APK **build eligibility is a separate evidence class**. Repository CI may attempt a build from a valid CLIENT/SERVER source ZIP without a supplied checksum or package manifest. CI calculates the source ZIP SHA-256 itself. When checksum or package-manifest evidence is supplied, it must validate exactly; contradictory supplied evidence blocks the build.

Large source archives may be transported as verified chunks described by `*.transport.json`. The transport manifest/chunks are transport evidence, not promotion authority. CI verifies each chunk, reconstructs the original ZIP in runner temporary storage, and verifies whole size/SHA-256 before compilation.

A successful build from ZIP-only or reconstructed chunk transport does not by itself promote the ZIP to current authority. Promotion remains a separate checkpoint requiring the applicable package, build, lineage, documentation, and runtime evidence.

CLIENT CFv2.1.9 package verification and CI debug build remain evidenced under `../evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md`. Device testing and runtime acceptance remain evidence-gated.

The promoted rows remain CLIENT CFv2.1.9 and SERVER CFv2.1.0 until a separate promotion checkpoint changes authority.
