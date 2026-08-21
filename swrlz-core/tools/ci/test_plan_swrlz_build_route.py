#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import plan_swrlz_build_route as route


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def commit_all(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


class BuildRouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "ci@example.invalid")
        git(self.repo, "config", "user.name", "SWRLZ CI")
        (self.repo / "swrlz-core/requests").mkdir(parents=True)
        (self.repo / "swrlz-core/requests/000_CURRENT.request").write_text(
            "enabled=false\n", encoding="utf-8"
        )
        self.base = commit_all(self.repo, "base")

    def tearDown(self):
        self.tmp.cleanup()

    def _write_transport(self, component: str, revision: int) -> Path:
        lane_name = component.lower()
        lane = self.repo / f"swrlz-core/sources/{lane_name}"
        lane.mkdir(parents=True, exist_ok=True)
        stem = f"{component}_CFv2.1.27_SWRLZ_CANDIDATE_R{revision}"
        path = lane / f"{stem}.transport.json"
        path.write_text(
            json.dumps({"schema": 2, "transport": "chunked-git-blobs-v2", "component": component}),
            encoding="utf-8",
        )
        return path

    def test_push_preserves_exact_transport_identity(self):
        transport = self._write_transport("SERVER", 140)
        head = commit_all(self.repo, "server source")
        plan = route.plan_route(
            self.repo,
            event_name="push",
            before_sha=self.base,
            after_sha=head,
        )
        self.assertTrue(plan["has_work"])
        self.assertEqual(
            plan["matrix"]["include"],
            [{"component": "SERVER", "source_identity": transport.relative_to(self.repo).as_posix()}],
        )

    def test_metadata_only_change_maps_to_existing_transport(self):
        transport = self._write_transport("CLIENT", 100)
        commit_all(self.repo, "identity")
        metadata = transport.with_name(transport.name.removesuffix(".transport.json") + "_METADATA.zip")
        metadata.write_bytes(b"metadata")
        before = git(self.repo, "rev-parse", "HEAD")
        head = commit_all(self.repo, "metadata")
        plan = route.plan_route(
            self.repo,
            event_name="push",
            before_sha=before,
            after_sha=head,
        )
        self.assertEqual(
            plan["matrix"]["include"][0]["source_identity"],
            transport.relative_to(self.repo).as_posix(),
        )

    def test_multiple_changed_identities_fail_closed(self):
        self._write_transport("SERVER", 140)
        self._write_transport("SERVER", 141)
        head = commit_all(self.repo, "two server sources")
        with self.assertRaises(route.RoutePlanningError):
            route.plan_route(
                self.repo,
                event_name="push",
                before_sha=self.base,
                after_sha=head,
            )

    def test_multi_commit_push_fetches_missing_before_boundary(self):
        with tempfile.TemporaryDirectory() as origin_tmp, tempfile.TemporaryDirectory() as clone_tmp:
            origin = Path(origin_tmp) / "origin.git"
            subprocess.run(
                ["git", "init", "--bare", str(origin)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            git(self.repo, "branch", "-M", "main")
            git(self.repo, "remote", "add", "origin", f"file://{origin}")
            git(self.repo, "push", "-u", "origin", "main")
            before = git(self.repo, "rev-parse", "HEAD")

            transport = self._write_transport("CLIENT", 101)
            commit_all(self.repo, "client source")
            (self.repo / "unrelated.txt").write_text("second commit\n", encoding="utf-8")
            after = commit_all(self.repo, "second commit in push")
            git(self.repo, "push", "origin", "main")

            shallow = Path(clone_tmp) / "shallow"
            subprocess.run(
                ["git", "clone", "--depth", "1", "--branch", "main", f"file://{origin}", str(shallow)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            missing = subprocess.run(
                ["git", "cat-file", "-e", f"{before}^{{commit}}"],
                cwd=shallow,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.assertNotEqual(missing.returncode, 0)

            plan = route.plan_route(
                shallow,
                event_name="push",
                before_sha=before,
                after_sha=after,
            )
            self.assertEqual(
                plan["matrix"]["include"],
                [{"component": "CLIENT", "source_identity": transport.relative_to(self.repo).as_posix()}],
            )
            self.assertEqual(
                subprocess.run(
                    ["git", "cat-file", "-e", f"{before}^{{commit}}"],
                    cwd=shallow,
                    check=False,
                ).returncode,
                0,
            )

    def test_manual_explicit_identity_is_forwarded(self):
        plan = route.plan_route(
            self.repo,
            event_name="workflow_dispatch",
            manual_component="CLIENT",
            manual_source_identity="CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100.zip",
            manual_variant="debug",
        )
        self.assertEqual(
            plan["matrix"]["include"],
            [{"component": "CLIENT", "source_identity": "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100.zip"}],
        )

    def test_manual_both_uses_compatible_full_lane_fallback(self):
        plan = route.plan_route(
            self.repo,
            event_name="workflow_dispatch",
            manual_component="BOTH",
        )
        self.assertEqual(
            plan["matrix"]["include"],
            [
                {"component": "CLIENT", "source_identity": ""},
                {"component": "SERVER", "source_identity": ""},
            ],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
