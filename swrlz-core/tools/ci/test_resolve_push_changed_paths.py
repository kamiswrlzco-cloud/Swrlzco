#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from resolve_push_changed_paths import (
    ChangedRangeError,
    commit_is_available,
    resolve_push_changed_paths,
)


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=repo, text=True, stderr=subprocess.PIPE
    ).strip()


class PushChangedPathTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        self.seed = self.root / "seed"
        self.shallow = self.root / "shallow"

        subprocess.run(
            ["git", "init", "--bare", "--initial-branch=main", str(self.remote)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(["git", "init", "-b", "main", str(self.seed)], check=True, stdout=subprocess.DEVNULL)
        git(self.seed, "config", "user.name", "SWRLZ CI Test")
        git(self.seed, "config", "user.email", "ci-test@swrlz.invalid")

        (self.seed / "base.txt").write_text("base\n", encoding="utf-8")
        git(self.seed, "add", "base.txt")
        git(self.seed, "commit", "-m", "base")
        self.before = git(self.seed, "rev-parse", "HEAD")

        source = self.seed / "swrlz-core/sources/server/source.transport.json"
        source.parent.mkdir(parents=True)
        source.write_text("{}\n", encoding="utf-8")
        git(self.seed, "add", source.relative_to(self.seed).as_posix())
        git(self.seed, "commit", "-m", "source")

        receipt = self.seed / "swrlz-core/docs/checkpoints/receipt.md"
        receipt.parent.mkdir(parents=True)
        receipt.write_text("receipt\n", encoding="utf-8")
        git(self.seed, "add", receipt.relative_to(self.seed).as_posix())
        git(self.seed, "commit", "-m", "receipt")
        self.after = git(self.seed, "rev-parse", "HEAD")

        git(self.seed, "remote", "add", "origin", self.remote.as_uri())
        git(self.seed, "push", "-u", "origin", "main")
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--depth=2",
                "--branch",
                "main",
                self.remote.as_uri(),
                str(self.shallow),
            ],
            check=True,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_depth_two_checkout_fetches_missing_base_for_two_commit_push(self):
        self.assertFalse(commit_is_available(self.shallow, self.before))

        paths, fetched = resolve_push_changed_paths(self.shallow, self.before, self.after)

        self.assertEqual(fetched, [self.before])
        self.assertTrue(commit_is_available(self.shallow, self.before))
        self.assertEqual(git(self.shallow, "rev-parse", "HEAD"), self.after)
        self.assertEqual(
            paths,
            [
                "swrlz-core/docs/checkpoints/receipt.md",
                "swrlz-core/sources/server/source.transport.json",
            ],
        )

    def test_one_commit_range_uses_available_history_without_fetch(self):
        parent = git(self.shallow, "rev-parse", "HEAD^")

        paths, fetched = resolve_push_changed_paths(self.shallow, parent, self.after)

        self.assertEqual(fetched, [])
        self.assertEqual(paths, ["swrlz-core/docs/checkpoints/receipt.md"])

    def test_zero_before_uses_after_commit_only(self):
        paths, fetched = resolve_push_changed_paths(self.shallow, "0" * 40, self.after)

        self.assertEqual(fetched, [])
        self.assertEqual(paths, ["swrlz-core/docs/checkpoints/receipt.md"])

    def test_invalid_boundary_fails_closed(self):
        with self.assertRaisesRegex(ChangedRangeError, "full hexadecimal Git object ID"):
            resolve_push_changed_paths(self.shallow, "not-a-sha", self.after)

    def test_unavailable_boundary_fails_closed(self):
        with self.assertRaisesRegex(ChangedRangeError, "could not be fetched"):
            resolve_push_changed_paths(self.shallow, "f" * 40, self.after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
