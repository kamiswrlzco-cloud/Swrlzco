#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import prepare_swrlz_sparse_checkout as sparse


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def commit_all(repo: Path, message: str = "fixture") -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


class SparseCheckoutPlannerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "ci@example.invalid")
        git(self.repo, "config", "user.name", "SWRLZ CI")
        (self.repo / "swrlz-core/tools/ci").mkdir(parents=True)
        (self.repo / "swrlz-core/tools/ci/placeholder.txt").write_text("ci", encoding="utf-8")
        (self.repo / "swrlz-core/requests").mkdir(parents=True)
        (self.repo / "swrlz-core/requests/000_CURRENT.request").write_text("enabled=false\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_direct_source_plan_excludes_historical_siblings(self):
        lane = self.repo / "swrlz-core/sources/client"
        lane.mkdir(parents=True)
        selected = lane / "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100.zip"
        selected.write_bytes(b"selected")
        metadata = lane / "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100_METADATA.zip"
        metadata.write_bytes(b"metadata")
        historical = lane / "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R99.zip"
        historical.write_bytes(b"historical")
        ref = commit_all(self.repo)

        paths, actual = sparse.build_sparse_paths(
            self.repo,
            "CLIENT",
            selected.relative_to(self.repo).as_posix(),
            ref=ref,
        )
        self.assertEqual(actual, selected.relative_to(self.repo))
        self.assertIn(selected.relative_to(self.repo), paths)
        self.assertIn(metadata.relative_to(self.repo), paths)
        self.assertNotIn(historical.relative_to(self.repo), paths)

    def test_sparse_checkout_application_materializes_only_selected_direct_payload(self):
        lane = self.repo / "swrlz-core/sources/client"
        lane.mkdir(parents=True)
        selected = lane / "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100.zip"
        selected.write_bytes(b"selected")
        metadata = lane / "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100_METADATA.zip"
        metadata.write_bytes(b"metadata")
        historical = lane / "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R99.zip"
        historical.write_bytes(b"historical")
        ref = commit_all(self.repo)

        paths, _ = sparse.build_sparse_paths(
            self.repo,
            "CLIENT",
            selected.relative_to(self.repo).as_posix(),
            ref=ref,
        )
        git(self.repo, "sparse-checkout", "init", "--cone")
        sparse.apply_sparse_checkout(self.repo, paths)

        self.assertTrue(selected.is_file())
        self.assertTrue(metadata.is_file())
        self.assertFalse(historical.exists())
        self.assertTrue((self.repo / "swrlz-core/tools/ci/placeholder.txt").is_file())

    def test_logical_zip_resolves_to_exact_chunked_transport_payload(self):
        lane = self.repo / "swrlz-core/sources/server"
        lane.mkdir(parents=True)
        stem = "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R140"
        chunk_dir = lane / ".transport" / stem
        chunk_dir.mkdir(parents=True)
        chunks = []
        for index, data in enumerate((b"one", b"two"), 1):
            path = chunk_dir / f"{stem}.zip.part{index:04d}"
            path.write_bytes(data)
            chunks.append({"index": index, "path": path.relative_to(self.repo).as_posix()})
        metadata = lane / f"{stem}_METADATA.zip"
        metadata.write_bytes(b"metadata")
        transport = lane / f"{stem}.transport.json"
        transport.write_text(
            json.dumps(
                {
                    "schema": 2,
                    "transport": "chunked-git-blobs-v2",
                    "component": "SERVER",
                    "source_zip": f"{stem}.zip",
                    "metadata_bundle_path": metadata.relative_to(self.repo).as_posix(),
                    "chunks": chunks,
                    "verified": True,
                }
            ),
            encoding="utf-8",
        )
        historical_dir = lane / ".transport" / "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R139"
        historical_dir.mkdir(parents=True)
        historical = historical_dir / "old.part0001"
        historical.write_bytes(b"old")
        ref = commit_all(self.repo)

        logical = f"swrlz-core/sources/server/{stem}.zip"
        paths, actual = sparse.build_sparse_paths(self.repo, "SERVER", logical, ref=ref)
        self.assertEqual(actual, transport.relative_to(self.repo))
        self.assertIn(metadata.relative_to(self.repo), paths)
        for chunk in chunks:
            self.assertIn(Path(chunk["path"]), paths)
        self.assertNotIn(historical.relative_to(self.repo), paths)

    def test_transport_path_escape_is_rejected(self):
        lane = self.repo / "swrlz-core/sources/server"
        lane.mkdir(parents=True)
        stem = "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R140"
        metadata = lane / f"{stem}_METADATA.zip"
        metadata.write_bytes(b"metadata")
        transport = lane / f"{stem}.transport.json"
        transport.write_text(
            json.dumps(
                {
                    "schema": 2,
                    "transport": "chunked-git-blobs-v2",
                    "component": "SERVER",
                    "source_zip": f"{stem}.zip",
                    "metadata_bundle_path": metadata.relative_to(self.repo).as_posix(),
                    "chunks": [{"index": 1, "path": "../escape.bin"}],
                    "verified": True,
                }
            ),
            encoding="utf-8",
        )
        ref = commit_all(self.repo)
        with self.assertRaises(sparse.SparseCheckoutError):
            sparse.build_sparse_paths(
                self.repo,
                "SERVER",
                transport.relative_to(self.repo).as_posix(),
                ref=ref,
            )

    def test_transport_component_mismatch_is_rejected(self):
        lane = self.repo / "swrlz-core/sources/client"
        lane.mkdir(parents=True)
        stem = "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R100"
        chunk = lane / ".transport" / stem / "part0001"
        chunk.parent.mkdir(parents=True)
        chunk.write_bytes(b"x")
        metadata = lane / f"{stem}_METADATA.zip"
        metadata.write_bytes(b"metadata")
        transport = lane / f"{stem}.transport.json"
        transport.write_text(
            json.dumps(
                {
                    "schema": 2,
                    "transport": "chunked-git-blobs-v2",
                    "component": "SERVER",
                    "source_zip": f"{stem}.zip",
                    "metadata_bundle_path": metadata.relative_to(self.repo).as_posix(),
                    "chunks": [{"index": 1, "path": chunk.relative_to(self.repo).as_posix()}],
                    "verified": True,
                }
            ),
            encoding="utf-8",
        )
        ref = commit_all(self.repo)
        with self.assertRaises(sparse.SparseCheckoutError):
            sparse.build_sparse_paths(
                self.repo,
                "CLIENT",
                transport.relative_to(self.repo).as_posix(),
                ref=ref,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
