#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import plan_swrlz_integrity_route as integrity


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


class IntegrityRouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "ci@example.invalid")
        git(self.repo, "config", "user.name", "SWRLZ CI")
        (self.repo / "README.md").write_text("base\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", "base")
        self.before = git(self.repo, "rev-parse", "HEAD")

    def tearDown(self):
        self.tmp.cleanup()

    def commit_path(self, path: str, text: str = "changed\n") -> str:
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", "change")
        return git(self.repo, "rev-parse", "HEAD")

    def test_tooling_only_change_verifies_both_components(self):
        after = self.commit_path("swrlz-core/tools/ci/verify_swrlz_package_pair.py")
        base_matrix = {"include": [{"component": "CLIENT", "source_identity": ""}]}
        plan = integrity.expand_integrity_route(
            self.repo,
            base_matrix,
            False,
            event_name="push",
            before_sha=self.before,
            after_sha=after,
        )
        self.assertTrue(plan["has_work"])
        self.assertEqual(plan["reason"], "integrity-tooling-self-check")
        self.assertEqual(
            plan["matrix"]["include"],
            [
                {"component": "CLIENT", "source_identity": ""},
                {"component": "SERVER", "source_identity": ""},
            ],
        )

    def test_tooling_change_preserves_explicit_changed_source(self):
        tool = self.repo / "swrlz-core/tools/ci/plan_swrlz_candidate_checkout.py"
        source = self.repo / "swrlz-core/sources/client/CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R200.transport.json"
        tool.parent.mkdir(parents=True, exist_ok=True)
        source.parent.mkdir(parents=True, exist_ok=True)
        tool.write_text("tool\n")
        source.write_text("{}\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", "combined")
        after = git(self.repo, "rev-parse", "HEAD")
        identity = source.relative_to(self.repo).as_posix()
        matrix = {"include": [{"component": "CLIENT", "source_identity": identity}]}
        plan = integrity.expand_integrity_route(
            self.repo,
            matrix,
            True,
            event_name="push",
            before_sha=self.before,
            after_sha=after,
        )
        self.assertEqual(plan["matrix"]["include"][0]["source_identity"], identity)
        self.assertEqual(plan["matrix"]["include"][1], {"component": "SERVER", "source_identity": ""})

    def test_non_tooling_change_keeps_no_work(self):
        after = self.commit_path("docs/note.md")
        matrix = {"include": [{"component": "CLIENT", "source_identity": ""}]}
        plan = integrity.expand_integrity_route(
            self.repo,
            matrix,
            False,
            event_name="push",
            before_sha=self.before,
            after_sha=after,
        )
        self.assertFalse(plan["has_work"])
        self.assertEqual(plan["matrix"], matrix)


if __name__ == "__main__":
    unittest.main(verbosity=2)
