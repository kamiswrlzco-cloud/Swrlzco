#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS = ROOT / '.github/workflows'


class Phase5WorkflowContractTests(unittest.TestCase):
    def text(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding='utf-8')

    def test_active_workflows_use_pinned_runner_and_no_embedded_token_remote(self):
        for name in (
            'swrlz-apk-router.yml',
            'source-package-integrity.yml',
            'patch-note-accounting.yml',
            'swrlz-ci-tooling-validation.yml',
        ):
            text = self.text(name)
            self.assertNotIn('ubuntu-latest', text, name)
            self.assertNotIn('x-access-token:', text, name)

    def test_router_has_one_pass_hydration_and_no_accounting_gate(self):
        router = self.text('swrlz-apk-router.yml')
        self.assertIn('matrix.checkout_patterns', router)
        self.assertIn('Plan one-pass candidate hydration', router)
        self.assertIn('source_hydration_ms', router)
        self.assertNotIn('Check patch-note and lineage accounting', router)
        self.assertIn('FORGE_FAILURE_CONTEXT.json', router)
        self.assertIn('gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb', router)
        self.assertIn('cache-provider: basic', router)
        self.assertIn('Validate preinstalled Java 17', router)
        self.assertNotIn('actions/setup-java@', router)
        self.assertIn('java_setup_ms', router)
        self.assertIn('Inspect preinstalled Android SDK', router)
        self.assertIn("if: steps.android-sdk-preflight.outputs.fallback_required == 'true'", router)
        self.assertIn('id: setup-android', router)
        self.assertIn('sdkmanager', router)
        self.assertNotIn('android-actions/setup-android@', router)
        self.assertIn('cache-encryption-key: ${{ secrets.SWRLZ_GRADLE_CACHE_ENCRYPTION_KEY }}', router)
        self.assertIn('SWRLZ_GRADLE_CONFIGURATION_CACHE', router)
        self.assertIn('android_sdk_setup_ms', router)
        self.assertIn('APKSIGNER: ${{ steps.android-sdk.outputs.apksigner }}', router)
        self.assertNotIn('find "${ANDROID_HOME:-$HOME}" -type f -name apksigner', router)


    def test_tooling_validator_hydrates_contract_inputs_and_smokes_fast_path(self):
        validation = self.text('swrlz-ci-tooling-validation.yml')
        self.assertIn('.github/workflows', validation)
        self.assertIn('swrlz-core/history', validation)
        self.assertIn('gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb', validation)
        self.assertIn('cache-provider: basic', validation)
        self.assertIn('Smoke test preinstalled Java 17 fast path', validation)
        self.assertNotIn('actions/setup-java@', validation)
        self.assertIn('Smoke test preinstalled Android SDK fast path', validation)
        self.assertIn('SDKMANAGER=', validation)

    def test_success_artifact_upload_precedes_best_effort_attestation(self):
        router = self.text('swrlz-apk-router.yml')
        upload = router.index('Upload canonical stable APK and provenance artifact')
        attest = router.index('Attest canonical stable APK provenance')
        self.assertLess(upload, attest)
        attest_tail = router[attest:]
        self.assertIn('continue-on-error: true', attest_tail)

    def test_integrity_uses_preplanned_exact_checkout(self):
        integrity = self.text('source-package-integrity.yml')
        self.assertIn('matrix.checkout_patterns', integrity)
        self.assertIn('Plan one-pass candidate hydration', integrity)
        self.assertIn('Expand integrity self-check route', integrity)
        self.assertIn('plan_swrlz_integrity_route.py', integrity)
        self.assertIn('resolve_swrlz_latest_identity.py', integrity)
        self.assertIn('verify_swrlz_package_pair.py', integrity)
        self.assertGreaterEqual(integrity.count('persist-credentials: false'), 2)


    def test_candidate_planner_never_uses_full_lane_fallback(self):
        planner = (ROOT / 'swrlz-core/tools/ci/plan_swrlz_candidate_checkout.py').read_text(encoding='utf-8')
        self.assertIn('exact-latest-candidate', planner)
        self.assertIn('resolve_latest_identity', planner)
        self.assertNotIn('full-lane-fallback', planner)

    def test_release_publication_rebases_and_retries(self):
        router = self.text('swrlz-apk-router.yml')
        self.assertIn('for attempt in 1 2 3; do', router)
        self.assertIn('git rebase "origin/$GITHUB_REF_NAME"', router)
        self.assertIn('Release publication remained non-fast-forward after 3 attempts.', router)

    def test_accounting_is_diagnostic_only(self):
        accounting = self.text('patch-note-accounting.yml')
        self.assertGreaterEqual(accounting.count('continue-on-error: true'), 2)
        self.assertIn('diagnostic only', accounting)

    def test_historical_r8_workflow_is_not_executable(self):
        self.assertFalse((WORKFLOWS / 'swrlz-server-r8-patch-build.yml').exists())
        self.assertTrue((ROOT / 'swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
