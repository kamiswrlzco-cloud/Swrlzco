# GitHub Actions Workflows

Executable GitHub Actions workflows live only in this repository-root directory:

```text
/.github/workflows/
```

Current SWRLZ lanes include:

- `swrlz-apk-router.yml` — routes CLIENT/SERVER source changes and produces bounded Android build evidence;
- `source-package-integrity.yml` — reconstructs and verifies changed source identities;
- `patch-note-accounting.yml` — audits candidate patch-note and lineage accounting;
- historical SERVER R8 patch-build lane — archived (non-executable) at `swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml`.

## Push changed-range rule

Source Package Integrity and Patch Note Accounting intentionally retain a shallow
`fetch-depth: 2` checkout. They both delegate push-range enumeration to
`swrlz-core/tools/ci/resolve_push_changed_paths.py`.

For an ordinary one-commit push, the existing shallow history is sufficient. For a
multi-commit push whose event `before` commit is not present, the helper fetches only
that exact boundary commit from `origin`, proves both boundary objects, and then runs
the complete `before..after` name-only diff. It fails closed if either declared object
cannot be proven. A zero `before` value retains the new-branch single-commit behavior.

The direct depth-2 regression lives in
`swrlz-core/tools/ci/test_resolve_push_changed_paths.py` and is invoked by both
workflows.

Workflow definitions, triggers, and successful unit tests are not build, package,
device, promotion, release, or deployment evidence. Record actual run/job conclusions
and exact source identities separately.
