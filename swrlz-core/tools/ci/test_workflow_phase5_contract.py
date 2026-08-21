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

    def test_accounting_is_diagnostic_only(self):
        accounting = self.text('patch-note-accounting.yml')
        self.assertGreaterEqual(accounting.count('continue-on-error: true'), 2)
        self.assertIn('diagnostic only', accounting)

    def test_historical_r8_workflow_is_not_executable(self):
        self.assertFalse((WORKFLOWS / 'swrlz-server-r8-patch-build.yml').exists())
        self.assertTrue((ROOT / 'swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
