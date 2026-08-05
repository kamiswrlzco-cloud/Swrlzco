# INT-FIX-075A — SERVER CFv2.1.27 R2 Compile Repair and Publication

**Mode:** IMPLEMENT / PUBLISH

**Lifecycle state:** IMPLEMENTATION_VERIFIED / DOCUMENTATION_SYNCED / REPOSITORY_TRANSPORTED / BUILD_PENDING

**Component:** SERVER only

**Candidate:** `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2`

**Android identity:** VC130 / `2.1.27-swrlz-llm-studio-compile-repair-r2`

## Objective

Repair the one Kotlin compiler defect proven in immutable R1, close the static-verification gap that allowed it through, publish the exact R2 package pair to the established SERVER source lane, and synchronize repository history without changing promoted authority.

## Success criteria

- R1 remains preserved as failed-build parent lineage.
- The explicit internal Compose weight import is absent and both contextual weight calls remain.
- The compiler-regression precheck is mandatory in the paired verifier.
- The byte-exact R2 ZIP reconstructs from a verified `chunked-git-blobs-v2` transport.
- The metadata ZIP matches source SHA, size, filename, version, revision, and VC.
- Repository authority, lineage, patch notes, engineering history, release/evidence records, and this receipt name exact R2.
- Automatic workflows are reported only from actual post-publication evidence.

## Confirmed facts

- R1 source ZIP SHA-256 is `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`.
- R1 transport commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` carried that exact source.
- APK Router run `30950003262` verified R1 and failed at `:app:compileDebugKotlin` on `ServerOperationsScreen.kt:16:43`.
- R2 source ZIP SHA-256 is `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`; size is 48,587,996 bytes.
- R2 metadata ZIP SHA-256 is `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`.
- R2 source-publication commit is `ece8bda4ae572fe585e662484c8469e84ad923ef`.
- The paired INT-AI-074A CLIENT CFv2.1.27 R1 source is unchanged and is not part of this repository publication; the repository CLIENT lane remains separately governed.

## Requirements

- Integrate; do not overwrite.
- Preserve offline-first behavior, identity, trust, Truth Firewall, proof-bound admin authorization, local/remote distinctions, lineage, and protocol discipline.
- Keep the promoted SERVER authority at CFv2.1.0 unless a later explicit promotion checkpoint changes it.
- Do not interpret repository transport as build, APK, installation, device, promotion, release, or deployment evidence.

## Engineering changes

1. Removed `import androidx.compose.foundation.layout.weight` from `ServerOperationsScreen.kt`.
2. Preserved both `Modifier.weight(1f)` calls inside `Row` content.
3. Made `scripts/verify_server_compile_regressions.py` mandatory in `tools/verify_int_ai_074a.py`.
4. Parameterized the paired verifier for the R2 SERVER identity while retaining the fixed CLIENT R1 expectation.
5. Added the bounded INT-FIX-075A repair verifier and synchronized package documentation/evidence.
6. Added a 68-part `chunked-git-blobs-v2` repository transport plus the exact two-file metadata ZIP.
7. Restored maintained repository navigation for R35–R45, R1, and R2.

## Documentation impact set

- AUTHORITY / INDEX
- CHECKPOINT / DELIVERY RECEIPT
- CHANGELOG / RELEASE NOTE
- BUILD / PACKAGING
- KNOWN ISSUES / LIMITATIONS
- PROVENANCE / LINEAGE

Architecture, LLM contracts, protocol/schema, capabilities, and CLIENT documentation remain unchanged because this repair changes no accepted behavior or wire surface.

## Verification

- SERVER compiler-regression precheck: PASS.
- Paired static gate: 113/113 PASS.
- INT-FIX-075A repair gate: 28/28 PASS.
- Kotlin/KTS string scan: 397 files / zero violations.
- Internal source manifest: 1,191/1,191 PASS.
- Immutable package pair: 26/26 PASS.
- R1→R2 inventory: 7 added / 12 modified / 0 removed.
- Repository CI unit suite: 30 tests PASS / one absent-fixture skip.
- Repository transport reconstruction/package-pair verification: PASS.
- Repository patch-note accounting for exact R2 identity: PASS.

## Build evidence

**Status:** `BUILD NOT RUN` for R2 before publication. The configured push may start Source Package Integrity, Patch Note Accounting, and APK Router automatically. A later evidence update must record their exact run IDs and results.

## Device evidence

**Status:** `RUNTIME NOT TESTED`. No APK installation, launch, device behavior, or integration acceptance is claimed.

## Provenance and lineage

- Failed parent: R1 / VC129 / exact SHA and run listed above.
- Repair successor: R2 / VC130.
- Unchanged, unpublished sibling for this checkpoint: paired INT-AI-074A CLIENT CFv2.1.27 R1.
- Rollback boundary: R1 remains inspectable evidence but is not a build-success rollback; promoted SERVER authority is unchanged.

## Current disposition

`SOURCE IMPLEMENTED` / `STATIC VERIFICATION PASS` / `DOCUMENTATION SYNCED` / `REPOSITORY TRANSPORTED` / `BUILD PENDING`.

## Approval boundary

The project owner authorized committing and pushing the exact R2 source/metadata pair and synchronized repository documentation. That approval includes normally configured push-triggered workflows, but excludes CLIENT changes, manual workflow dispatch/rerun, APK installation, promotion, release, and deployment.
