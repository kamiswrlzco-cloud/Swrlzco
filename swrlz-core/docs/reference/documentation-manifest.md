# Documentation Manifest and Package Accounting

**Migration generation:** New official `Swrlzco/swrlz-core` bootstrap  
**Prepared:** 2026-07-26  
**Last policy synchronization:** 2026-07-28 — INT-FORGE-039F + INT-FORGE-039N  
**Last architecture documentation synchronization:** 2026-07-28 — INT-DOC-AI-040A  
**Last update architecture synchronization:** 2026-07-28 — INT-DOC-UPD-040C-040D

## Current source baseline

| Role | Package | SHA-256 |
|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` |

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

This documentation addition is **architecture evidence only**. It does not alter current CLIENT/SERVER source authority, does not prove any planned component is implemented, and does not constitute build, device, integration, release, or deployment evidence.

### INT-DOC-UPD-040C-040D — live pack and runtime update architecture

`INT-DOC-UPD-040C-040D` adds:

- `../architecture/SWRLZ_RUNTIME_AND_LIVE_PACK_UPDATE_ARCHITECTURE_V1.md`
- `../contracts/SWRLZ_UPDATE_AND_PACK_MANIFEST_CONTRACT_V1.md`
- `../checkpoints/INT-DOC-UPD-040C-040D_UPDATE_ARCHITECTURE_SYNC.md`

This documentation defines the intended split between stable signed CLIENT/SERVER/Launcher runtime products and non-executable live packs that may be downloaded, verified, staged, and activated while SWRLZ continues running. It records SERVER-owned normal internet update discovery, source-provider abstraction, content-addressed object reuse, immutable staged generations, rollback, and separate Android package-replacement semantics for executable runtime changes.

It also records the SWRLIE base-plus-modules direction: a relatively stable base model with independently versioned adapters, knowledge, configuration, and specialist modules where technically appropriate. The neural model remains advisory; SWRLZ retains Truth Firewall, command routing, approval policy, tool schemas, node trust, file authority, Forge validation, update trust, activation, and rollback authority.

`INT-PACK-040C` and `INT-UPD-040D` remain **planned implementation checkpoints**. This docs sync does not approve or claim their implementation. `INT-AI-040B` remains the separately approved bounded 350M local-inference implementation scope.

This update documentation is **architecture/contract evidence only**. It does not alter `CURRENT_AUTHORITY.md`, source packages, workflows, build tools, model weights, release assets, APKs, device state, or deployments.

## Version and build-input policy

Current promoted source authority remains the source package + exact checksum under `sources/`, subject to later supersession by a newer explicitly verified package or repository HEAD.

APK **build eligibility is a separate evidence class**. Repository CI may attempt a build from a valid CLIENT/SERVER source ZIP without a supplied checksum or package manifest. CI calculates the source ZIP SHA-256 itself. When checksum or package-manifest evidence is supplied, it must validate exactly; contradictory supplied evidence blocks the build.

Large source archives may be transported as verified chunks described by `*.transport.json`. The transport manifest/chunks are not source authority. CI verifies each chunk, reconstructs the original ZIP in runner temporary storage, and verifies whole size/SHA-256 before compilation.

A successful build from ZIP-only input does not by itself promote the ZIP to current authority. Promotion remains a separate checkpoint requiring the applicable package, build, lineage, documentation, and runtime evidence.

CLIENT CFv2.1.9 package verification and CI debug build are evidenced under `../evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md`. Device testing and runtime acceptance remain evidence-gated.

CLIENT CFv2.1.9 is the package-pair/identity successor under `INT-THEME-035D`. It preserves CFv2.1.8 application behavior and corrects the canonical manifest contract. CFv2.1.8 and its failed workflow evidence remain preserved as lineage. The CFv2.1.7 parent package remains available as the preceding implementation rollback baseline.

The SERVER row is preserved from the repository baseline and was not revalidated by that CLIENT-only checkpoint.

Repository CI transport/build-input policy application is recorded in `../checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md`; it does not alter the source-baseline table above.
