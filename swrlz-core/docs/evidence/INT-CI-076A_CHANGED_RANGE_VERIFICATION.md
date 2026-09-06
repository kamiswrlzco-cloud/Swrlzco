# INT-CI-076A Changed-Range Verification

## Trigger evidence

| Workflow | Run | Failing step | Exact boundary | Result |
|---|---:|---|---|---|
| Source Package Integrity | `30965115656` | Resolve changed or selected source identities | `193fe261...e9a28b65` | `fatal: bad object 193fe261...`; exit 128 |
| Patch Note Accounting | `30965115160` | Resolve changed source identities | `193fe261...e9a28b65` | `fatal: bad object 193fe261...`; exit 128 |

Both jobs completed checkout and their pre-range unit tests. Neither reached its
substantive package-verification or repository-audit step.

## Repair verification

| Check | Result |
|---|---|
| Shared helper import/CLI | PASS |
| Depth-2 checkout with missing two-commit base | PASS; exact base fetched |
| One-commit range | PASS; no fetch |
| Zero-before/new-branch range | PASS |
| Invalid boundary | PASS; fails closed |
| Unavailable boundary | PASS; fails closed |
| HEAD/worktree preservation after boundary fetch | PASS |
| Full local CI unit discovery | 35 PASS / 1 absent-fixture skip |
| Historical failed range path resolution | 83 paths / PASS |
| Historical range source-identity mapping | exact SERVER R2 transport / PASS |
| SERVER R2 source/package identity regression | exact SHA/package pair / PASS |

## Independent current-head evidence

The one-commit CLIENT upload at head `3d37cf5e...` produced Source Package Integrity
run `30969188749`, which succeeded, and Patch Note Accounting run `30969188766`, whose
range-resolution step succeeded. Its later audit step failed on explicit CLIENT
patch-history/current-lineage omissions for source SHA-256
`2c43d60454d16defda959e482bd03b40ce29a1898d71a966fa67ef30333aabe5`.
That is separate enforcement evidence and is not reclassified as an INT-CI-076A failure.

## Publication evidence

| Evidence | Result |
|---|---|
| Implementation commit | `94744cad5cd6e88111f84fee155d026be6dc8836` |
| Initial documentation head | `36c2e3f991ecd0dcbba49ebbf38a94631a0cd495` |
| Push range | `3d37cf5e...36c2e3f9`; two commits; 17 CI/tooling/docs paths |
| Source Package Integrity `31013714578` | SUCCESS |
| Source Integrity tests | 27 PASS |
| Source Integrity missing-base recovery | fetched exact `3d37cf5e...`; 17 paths; PASS |
| Source identities selected | none; application source changes = 0 |
| Patch Note Accounting `31013714668` tests | 9 PASS |
| Patch Accounting missing-base recovery | fetched exact `3d37cf5e...`; 17 paths; PASS |
| Patch Accounting downstream audit | FAIL on independent CLIENT debt; SERVER R2 PASS |
| Workflow-evidence commit | `eb7cd508ad964211fa60ff201958263b84be379e` |
| Evidence-sync audit `31014176783` | 9 tests PASS; 11-path range PASS; SERVER R2 PASS; same CLIENT debt FAIL |

The downstream CLIENT audit identifies source SHA-256
`2c43d60454d16defda959e482bd03b40ce29a1898d71a966fa67ef30333aabe5`
and three missing exact-accounting surfaces: package `ReleaseNotes.md`, repository
`CLIENT_PATCH_NOTES.md`, and `CURRENT_CANDIDATE_LINEAGE.md`. The repaired range step is
therefore verified even though the complete enforcement workflow correctly remains red.

Neither repaired job emitted `fatal: bad object` during changed-range resolution.
The evidence-sync run also completed changed-range resolution without that defect.

## Non-claims

This evidence does not establish CLIENT/SERVER application-source modification, Android
compilation, APK installation, device/runtime acceptance, promotion, release, deployment,
or repair of the independent CLIENT patch-accounting debt.
