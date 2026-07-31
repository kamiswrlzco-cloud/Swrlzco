# INT-CI-DOC-060A — Router / Source-Integrity Repair and Patch-Notes Synchronization

**Prepared:** 2026-07-31  
**Working branch:** `checkpoint/int-ci-doc-060a-router-docs`  
**Target branch:** `main` only after explicit merge approval  
**Scope:** GitHub CI routing/integrity repair plus maintained documentation/patch-note synchronization  

## Triggering evidence

The 2026-07-31 SWRLZ Forge upload at commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` added verified chunk transports for two later candidates:

- CLIENT `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1`, declared whole-source SHA-256 `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`, 15,127,739 bytes, 4 chunks;
- SERVER repository transport identity `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1`, declared whole-source SHA-256 `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`, 40,710,681 bytes, 10 chunks.

Both transport records include nested checksum evidence under `.transport/<candidate>/evidence/` and do not include a separately packaged candidate manifest in that Forge transaction.

Source Package Integrity run `30658738049` failed because the old workflow recursively watched source-lane descendants and treated nested transport checksum evidence as though it were a lane-root source sidecar. The resolver transformed paths such as:

```text
swrlz-core/sources/client/.transport/<candidate>/evidence/<candidate>.sha256
```

into a nonexistent sibling ZIP path under the nested evidence directory, then failed with `Missing ZIP`.

This is a workflow-selection defect, not evidence that the transported whole ZIP checksum itself was wrong.

A separate APK Router screenshot showed `Validate source resolver` waiting for a GitHub-hosted `ubuntu-latest` runner. That waiting state is runner scheduling evidence only; it is **not** by itself proof of a Router logic failure.

## Repair prepared on the checkpoint branch

### Source Package Integrity

`.github/workflows/source-package-integrity.yml` now:

- watches only lane-root CLIENT/SERVER source identity/evidence files;
- refuses nested `.transport/` chunks/evidence as direct source candidates;
- permits manual verification only for lane-root CLIENT/SERVER ZIPs;
- derives companion ZIP identity only from lane-root sidecars;
- fails clearly when a lane-root sidecar references a missing sibling ZIP;
- leaves chunk/evidence verification to the APK Router source resolver during transport reconstruction.

The repair prevents a nested transport checksum from being reinterpreted as a direct source package.

### APK Router

`.github/workflows/swrlz-apk-router.yml` is hardened to:

- accept manual `CLIENT`, `SERVER`, or `BOTH` routing;
- make `BOTH` resolve each component independently and reject one explicit `source_zip` applied ambiguously to both;
- route push changes only from lane-root source ZIP/transport/sidecar identity files;
- ignore nested `.transport/` chunk/evidence paths as independent build routes;
- allow request target `BOTH` while preserving CLIENT/SERVER-only matrix build components;
- retain existing resolver tests, canonical source resolution, package verification, Android build, signing/provenance, artifact upload, and manual-only release-commit behavior.

No claim is made here that the Router screenshot's hosted-runner wait can be repaired in repository code; GitHub-hosted runner availability is external scheduling state.

## Patch-notes synchronization rule

Two maintained component ledgers are established:

- `docs/client/PATCH_NOTES.md`
- `docs/server/PATCH_NOTES.md`

From this checkpoint forward, an accepted CLIENT or SERVER source-update checkpoint is not documentation-complete until the corresponding component patch notes include, when known:

1. checkpoint / candidate identity;
2. versionCode and versionName;
3. parent lineage;
4. exact source SHA-256;
5. concise implementation/change summary;
6. evidence class and validation boundary;
7. explicit non-claims for build/device/promotion/release/deployment/installation where those states are not proven.

A shared checkpoint that changes both CLIENT and SERVER must update both ledgers. Component-specific work updates only the affected component ledger.

Already packaged historical ZIPs are immutable evidence. Their internal changelog files are not rewritten after packaging merely to synchronize documentation, because doing so would change package bytes/SHA/lineage. Missing historical detail is instead repaired in the repository-level ledgers, and future packages should carry synchronized internal changelog/release-note/lineage data before packaging.

Patch notes are navigation/evolution evidence, not source authority. Canonical source ZIP identity, checksums, accepted manifests/contracts, and accepted build/device/promotion evidence retain precedence.

## Recent lineage synchronized

Repository documentation is being brought forward through:

- CLIENT CFv2.1.26 R1 / VC124 / `INT-FORGE-054A-R2`, source SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`;
- SERVER CFv2.1.24 R1 / VC82 / `INT-FORGE-054A-R2`, source SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`;
- latest repository transport identities CLIENT CFv2.1.27 R1 and SERVER CFv2.1.25 R1-1 from commit `ac6e58c...` without inventing their internal implementation details;
- approved `INT-FILE-059A` File Lab / Archive Cartographer scope as approval state only, not implementation evidence.

`INT-FORGE-054A-R2` added the shared Forge conveyor/parity direction: verified newest-source selection, CLIENT/SERVER/BOTH/ASK targeting, configurable SAF lanes, build ledger, default-on artifact/failure-log download behavior, and machine-readable patch/checkpoint lineage while preserving CLIENT-only and SERVER-only role boundaries.

## Evidence / authority boundary

This checkpoint branch contains GitHub workflow and documentation changes. Until explicitly merged:

- `main` is unchanged by these branch edits;
- the failed Source Package Integrity run has not been rerun;
- no APK Router run has been manually dispatched;
- no APK build is claimed from this checkpoint;
- no CLIENT/SERVER candidate is promoted;
- no release, deployment, or installation is authorized or claimed.

After merge, validation of the original failure mode should use a separately authorized workflow rerun or a new source transaction whose exact selected source identities are recorded.
