# INT-CI-076A — Multi-Commit Push Changed-Range Repair

**Mode:** IMPLEMENT / PUBLISH

**Lifecycle state:** REPOSITORY_PUBLISHED / CHANGED_RANGE_VERIFIED / ACCEPTED_WITH_FOLLOW_UP

**Components:** BUILD / CI / TOOLING / DOCUMENTATION only

**Baseline repository head:** `3d37cf5eadd6eea5a5cba8e796d3a02002fde634`

## Objective

Repair Source Package Integrity and Patch Note Accounting so a multi-commit push can
enumerate the exact GitHub event `before..after` range even when `fetch-depth: 2` does
not contain the event-base commit.

## Success criteria

- Both affected workflows use one shared changed-range implementation.
- Shallow checkout remains bounded; full repository history is not fetched by default.
- A missing event-base commit is fetched by exact object ID and proven before diffing.
- Missing or invalid declared boundaries fail closed.
- Regression coverage reproduces a three-commit repository, depth-2 checkout, and
  two-commit push range whose base is initially absent.
- The historical failed range `193fe261...e9a28b65` resolves all 83 changed paths and
  maps to the exact SERVER R2 lane-root identity.
- CLIENT and SERVER application source/package bytes remain unchanged.

## Confirmed facts

- Source Package Integrity run `30965115656` and Patch Note Accounting run
  `30965115160` both used `fetch-depth: 2`.
- Their push declared `before=193fe26155c26c07f77fec9bda212c84d8e7b5f9`
  and `after=e9a28b6584698fa5992e1dd74a6b6818dd1f38cb`.
- Both failed in changed-range enumeration with `fatal: bad object 193fe261...` and
  exit code 128 before package verification or patch-accounting audit.
- Later one-commit SERVER Forge upload `52f20eda...` passed Source Package Integrity,
  Patch Note Accounting, and APK Router. Later one-commit CLIENT Forge upload
  `3d37cf5e...` passed Source Integrity and APK Router; its Patch Note Accounting run
  `30969188766` reached the audit and failed on separate CLIENT patch/lineage evidence
  gaps, not on changed-range resolution.

## Requirements

- Integrate; do not overwrite.
- Preserve exact source/package lineage and promoted authority.
- Do not weaken patch-note enforcement to conceal the independent CLIENT accounting
  failure.
- Keep application behavior, identity, trust, Truth Firewall, offline-first behavior,
  local/remote routing, and protocol versions unchanged.

## Sources of truth inspected

- Repository `main` through `3d37cf5eadd6eea5a5cba8e796d3a02002fde634`.
- Current workflow definitions and CI helper/test implementations.
- Failed job logs from runs `30965115656` and `30965115160`.
- Current one-commit workflow evidence for Forge commits `52f20eda...` and
  `3d37cf5e...`, including failed Patch Note Accounting run `30969188766`.
- Current authority, status matrix, SERVER patch/implementation records, INT-FIX-075A
  receipt/evidence, and active patch-note accounting contract.

## Engineering changes

1. Added `resolve_push_changed_paths.py` as the shared, fail-closed push-range helper.
2. Retained shallow checkout and added exact fetch of only an absent boundary commit.
3. Replaced duplicated inline `git show` / `git diff` blocks in both workflows.
4. Added five direct tests: depth-2 two-commit recovery, one-commit no-fetch,
   zero-before handling, invalid-boundary rejection, and unavailable-boundary rejection.
5. Added the new helper and regression suite to both workflow triggers/test lanes.
6. Added each workflow's own path and relevant CI tools to Patch Note Accounting's
   trigger set so future CI repairs validate themselves.

## Documentation impact set

- CHECKPOINT / DELIVERY RECEIPT
- FORGE / REPOSITORY / CI
- KNOWN ISSUES / LIMITATIONS
- PROVENANCE / LINEAGE
- AUTHORITY / INDEX
- CHANGELOG / SERVER PATCH-NOTE FOLLOW-UP (CI-only; no SERVER source change)

Architecture, application contracts/protocols/schemas, CLIENT/SERVER version identities,
and source packages are intentionally unchanged.

## Local verification

- CI unit discovery: 35 tests passed; one repository fixture skipped because the
  sparse local checkout did not materialize that historical CLIENT fixture.
- New changed-range suite: 5/5 passed.
- Exact historical range: 83 changed paths resolved; one exact identity selected:
  `SERVER → swrlz-core/sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2.transport.json`.
- Current SERVER R2 transport reconstructed and package-pair verified at source SHA-256
  `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` and metadata
  SHA-256 `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`.
- Repository diff, workflow YAML parsing, and bounded-path exclusion gate: PASS.

## Workflow evidence

**Status:** `REPOSITORY PUBLISHED` / `MULTI-COMMIT CHANGED RANGE VERIFIED` /
`PATCH ACCOUNTING FOLLOW-UP REQUIRED`.

- CI implementation commit: `94744cad5cd6e88111f84fee155d026be6dc8836`.
- Initial documentation commit: `36c2e3f991ecd0dcbba49ebbf38a94631a0cd495`.
- Workflow-evidence commit: `eb7cd508ad964211fa60ff201958263b84be379e`.
- One fast-forward moved `main` from `3d37cf5e...` across both commits. With
  `fetch-depth: 2`, the event-base was absent exactly as intended.
- Source Package Integrity run `31013714578`: SUCCESS. Its 27 tests passed; the helper
  fetched missing base `3d37cf5e...`, resolved all 17 changed paths, selected no
  application source identities, and completed the no-source verification path.
- Patch Note Accounting run `31013714668`: its nine tests and changed-range step passed;
  the helper fetched the same missing base and resolved all 17 paths. The workflow then
  failed in the downstream audit on the separately preserved CLIENT accounting debt.
- That audit reported SERVER R2 PASS and CLIENT CFv2.1.27 R1 FAIL for three exact gaps:
  package `ReleaseNotes.md`, repository `CLIENT_PATCH_NOTES.md`, and
  `CURRENT_CANDIDATE_LINEAGE.md`.
- Evidence-commit Patch Note Accounting run `31014176783` reconfirmed the boundary:
  nine tests PASS, 11-path one-commit range PASS, SERVER R2 PASS, and the same three
  CLIENT accounting gaps FAIL.

No `fatal: bad object` occurred in either repaired range step.

## Provenance and lineage

- Defect evidence remains immutable in runs `30965115656` and `30965115160`.
- INT-CI-076A is a CI/tooling successor; it does not supersede or repackage SERVER R2.
- Current baseline includes later Forge commits `52f20eda...` and `3d37cf5e...`; both
  remain untouched.
- Rollback boundary: revert the CI/tooling successor while retaining the prior workflow
  definitions and all source transports.

## Known issues

- CLIENT CFv2.1.27 R1 Forge upload commit `3d37cf5e...` has independent patch-accounting
  debt proven by run `30969188766`: package `ReleaseNotes.md` and repository current
  lineage/authority surfaces do not name exact source SHA-256
  `2c43d60454d16defda959e482bd03b40ce29a1898d71a966fa67ef30333aabe5`.
- INT-CI-076A does not repair or suppress that CLIENT documentation defect.
- Patch Note Accounting remains red by design until that separately authorized CLIENT
  package/repository documentation repair is completed.
- Device/runtime acceptance for SERVER R2 remains pending and unrelated.

## Exclusions

No CLIENT/SERVER application-source change, source repackaging, APK build/install,
manual workflow rerun/dispatch, promotion, release, deployment, or CLIENT patch-history
repair is included.

## Approval boundary

The project owner approved `INT-CI-076A MULTI-COMMIT-PUSH-DIFF-DEPTH-REPAIR-AND-GATE-VALIDATION`.
That approval covers this bounded implementation, synchronized CI documentation,
publication, and normally configured push-triggered validation only.
