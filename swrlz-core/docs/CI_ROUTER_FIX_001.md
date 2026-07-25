# CI Router Fix 001 — runner context scope

The initial migrated router placed `runner.temp` expressions in workflow-level `env`,
where the `runner` context is unavailable during workflow validation.

Fix:

- Keep repository-static paths in workflow-level `env`.
- Move `SWRLZ_BUILD_WORK_DIR` and `SWRLZ_ARTIFACT_ROOT` into the
  `Build selected Android component` step `env`, where the runner context is available.

Observed symptom:

- Workflow rejected before job graph creation.
- GitHub annotation: `Unrecognized named-value: 'runner'`.
- No runner job/log archive exists for that invalid run.

This patch changes no source-package authority or build-request state.
