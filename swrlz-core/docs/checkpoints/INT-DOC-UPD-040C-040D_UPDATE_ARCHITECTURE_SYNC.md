# INT-DOC-UPD-040C-040D — Live Pack + Runtime Update Architecture Documentation Sync

**Checkpoint class:** Documentation-only  
**Date:** 2026-07-28  
**Repository:** `kamiswrlzco-cloud/Swrlzco`  
**Scope:** `swrlz-core/docs/**` only

## User authorization

User instruction for this checkpoint:

> "Ok document this properly in the GitHub in the proper docs then"

This authorization applies to documentation integration only. It does not approve 040C or 040D implementation, source modification, builds, releases, deployment, installation, or automatic updating on any device.

## Documents added

- `docs/architecture/SWRLZ_RUNTIME_AND_LIVE_PACK_UPDATE_ARCHITECTURE_V1.md`
- `docs/contracts/SWRLZ_UPDATE_AND_PACK_MANIFEST_CONTRACT_V1.md`
- this checkpoint record

## Maintained documents synchronized

- `docs/DOCUMENTATION_INDEX.md`
- `docs/reference/feature-registry.md`
- `docs/reference/status-matrix.md`
- `docs/reference/documentation-manifest.md`

## Architecture captured

This documentation records the intended separation between:

- stable signed CLIENT/SERVER/Launcher runtime products;
- hot-loadable non-executable SWRLZ live packs;
- SWRLIE base-model and modular adapter/knowledge/config product evolution.

It also records that SWRLZ, not the neural model, owns Truth Firewall, command routing, approval policy, tool schemas, node trust, file authority, Forge validation, update trust, activation, rollback, and cleanup policy.

## Live-pack direction

The planned Live Pack Manager is SERVER-owned for normal internet discovery and remote fetch work. It is intended to:

1. discover signed update indexes/manifests;
2. compare installed generations and object hashes;
3. reuse unchanged trusted objects;
4. download only missing/changed objects where practical;
5. verify signature, SHA-256, size, lineage, dependencies, contract compatibility, and capabilities;
6. stage a complete new generation without mutating the active generation;
7. health-check/load as applicable;
8. atomically activate;
9. preserve rollback state;
10. clean unreferenced objects only under policy.

Representative pack classes include model base, model adapter, knowledge, theme, tool schema, device data, and declarative config.

Downloaded packs are not a general executable-code channel. Kotlin/DEX/native/runtime implementation changes remain signed runtime/APK updates.

## SWRLIE modular model direction

The initial 350M GGUF target is treated as a relatively stable base. Normal SWRLIE evolution should prefer independently versioned adapters, knowledge, routing/config, and specialist modules when technically appropriate, so ordinary updates do not require repeatedly downloading the full base model.

The design explicitly avoids claiming that small training changes to a monolithic GGUF guarantee proportionally small binary deltas.

## Runtime updater direction

A separate signed runtime update supervisor is planned for CLIENT/SERVER/Launcher APK updates.

The documented flow separates:

- source/static evidence;
- compile evidence;
- APK/build evidence;
- device evidence;
- integration evidence;
- promotion/release/deployment authority.

A successful Forge/CI build may become eligible for an allowed DEV/CANDIDATE channel only when the applicable update contract and policy permit it. It does not automatically become STABLE, current source authority, released, deployed, or installed.

SERVER is intended to perform normal internet update discovery/download work. The target device independently validates package identity, signing identity, hashes, version/channel eligibility, protocol compatibility, approvals/policy, storage, and safe execution state before installation.

Runtime downloads and staging may occur while SWRLZ runs. Actual APK/runtime replacement remains distinct from hot pack activation and may require process replacement/relaunch.

## Hosting/source direction

The documentation records an abstract `UpdateSourceAdapter` so update trust and identity are independent of hosting provider.

Initial recommended roles:

- GitHub repository — source, contracts, manifests, documentation, provenance, long-term project truth;
- release/artifact channel — immutable distributable artifacts when separately authorized;
- Hugging Face private repository/bucket — model-development workspace and upstream/experimental artifacts, not automatic production authority;
- future object store/CDN or authenticated LAN/private node — replaceable distribution backends.

## Checkpoint relationship

### INT-AI-040B

The approved 350M local-inference foundation remains the current bounded implementation scope. This documentation does not expand that approval into updater work.

### INT-PACK-040C

Planned future implementation checkpoint for the generic Live Pack Manager. **Not implemented or approved for implementation by this docs checkpoint.**

### INT-UPD-040D

Planned future implementation checkpoint for signed CLIENT/SERVER/Launcher runtime update discovery, staging, verification, package replacement, relaunch/resume, and post-update health verification. **Not implemented or approved for implementation by this docs checkpoint.**

## Evidence classification

This checkpoint provides **documentation / architecture evidence only**.

It does not claim:

- Live Pack Manager implementation;
- incremental model delivery implementation;
- model-adapter training;
- update signing infrastructure;
- auto-update implementation;
- Launcher updater implementation;
- CI/build verification for 040C/040D;
- device/integration verification;
- publication of update manifests/artifacts;
- runtime installation;
- release or deployment.

## Authority boundary

This checkpoint does not change `docs/CURRENT_AUTHORITY.md`.

Current CLIENT/SERVER source authority and all candidate/build/device/integration/promotion evidence remain governed by their existing records. No source package, workflow, build tool, authority pointer, release asset, model weight, APK, or deployment target is changed by this checkpoint.