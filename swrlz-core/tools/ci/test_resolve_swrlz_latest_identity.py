#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import inspect
import io
import json
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile
from pathlib import Path

import resolve_swrlz_latest_identity as latest


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def metadata_bundle(component: str, stem: str, source_bytes: bytes, version_code: int) -> bytes:
    source_name = stem + ".zip"
    sha = hashlib.sha256(source_bytes).hexdigest()
    revision = stem.rsplit("_", 1)[-1]
    manifest = {
        "component": component,
        "sourceZip": {
            "filename": source_name,
            "sha256": sha,
            "sizeBytes": len(source_bytes),
        },
        "versionCode": version_code,
        "revision": revision,
        "verified": True,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f"{stem}.sha256", f"{sha} *{source_name}\n")
        archive.writestr(f"{stem}.manifest.json", json.dumps(manifest))
    return output.getvalue()


class LatestIdentityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "ci@example.invalid")
        git(self.repo, "config", "user.name", "SWRLZ CI")
        (self.repo / "swrlz-core/sources/client").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def add_transport(self, revision: int, version_code: int, *, verified: bool = True) -> str:
        lane = self.repo / "swrlz-core/sources/client"
        stem = f"CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R{revision}"
        source_bytes = (f"source-{revision}" * 20).encode()
        source_sha = hashlib.sha256(source_bytes).hexdigest()
        metadata = metadata_bundle("CLIENT", stem, source_bytes, version_code)
        metadata_path = lane / f"{stem}_METADATA.zip"
        metadata_path.write_bytes(metadata)
        chunk_dir = lane / ".transport" / stem
        chunk_dir.mkdir(parents=True, exist_ok=True)
        chunk = chunk_dir / f"{stem}.zip.part0001"
        chunk.write_bytes(source_bytes)
        payload = {
            "schema": 2,
            "transport": "chunked-git-blobs-v2",
            "component": "CLIENT",
            "source_zip": stem + ".zip",
            "source_sha256": source_sha,
            "source_size_bytes": len(source_bytes),
            "chunks": [{
                "index": 1,
                "path": chunk.relative_to(self.repo).as_posix(),
                "size_bytes": len(source_bytes),
                "sha256": source_sha,
            }],
            "metadata_bundle_path": metadata_path.relative_to(self.repo).as_posix(),
            "metadata_bundle_sha256": hashlib.sha256(metadata).hexdigest(),
            "verified": verified,
        }
        identity = lane / f"{stem}.transport.json"
        identity.write_text(json.dumps(payload), encoding="utf-8")
        return identity.relative_to(self.repo).as_posix()

    def commit(self):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-m", "fixture")

    def test_existence_probe_uses_tree_metadata_not_blob_materialization(self):
        source = inspect.getsource(latest._exists)
        self.assertIn("ls-tree", source)
        self.assertNotIn('["git", "cat-file"', source)

    def test_highest_verified_version_code_wins(self):
        self.add_transport(151, 274)
        expected = self.add_transport(152, 275)
        self.commit()
        self.assertEqual(
            latest.resolve_latest_identity(self.repo, "CLIENT", ref="HEAD"),
            expected,
        )

    def test_newest_valid_identity_short_circuits_historical_validation(self):
        self.add_transport(150, 273)
        self.add_transport(151, 274)
        expected = self.add_transport(152, 275)
        self.commit()
        with mock.patch.object(
            latest, "_transport_candidate", wraps=latest._transport_candidate
        ) as probe:
            resolved = latest.resolve_latest_identity(self.repo, "CLIENT", ref="HEAD")
        self.assertEqual(resolved, expected)
        self.assertEqual(probe.call_count, 1)

    def test_broken_newer_transport_is_quarantined(self):
        expected = self.add_transport(152, 275)
        self.add_transport(153, 276, verified=False)
        self.commit()
        self.assertEqual(
            latest.resolve_latest_identity(self.repo, "CLIENT", ref="HEAD"),
            expected,
        )

    def test_direct_source_can_win_without_hydrating_other_payloads(self):
        self.add_transport(152, 275)
        lane = self.repo / "swrlz-core/sources/client"
        stem = "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R154"
        source = lane / f"{stem}.zip"
        source_bytes = b"direct-latest-source"
        source.write_bytes(source_bytes)
        (lane / f"{stem}_METADATA.zip").write_bytes(
            metadata_bundle("CLIENT", stem, source_bytes, 277)
        )
        self.commit()
        self.assertEqual(
            latest.resolve_latest_identity(self.repo, "CLIENT", ref="HEAD"),
            source.relative_to(self.repo).as_posix(),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
