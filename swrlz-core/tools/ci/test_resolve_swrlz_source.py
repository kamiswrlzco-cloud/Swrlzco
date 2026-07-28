#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from resolve_swrlz_source import COMPONENTS, ResolutionError, parse_transport_name, resolve_source


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ResolveSwrlzSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "tests@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "SWRLZ Tests"], cwd=self.root, check=True)
        for key in ("GITHUB_EVENT_NAME", "GITHUB_EVENT_PATH", "GITHUB_EVENT_BEFORE", "GITHUB_SHA"):
            os.environ.pop(key, None)
        for spec in COMPONENTS.values():
            (self.root / spec.lane).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def lane(self, component):
        return self.root / COMPONENTS[component].lane

    def write_zip(self, component, zip_name, data, checksum=False, manifest=False):
        lane = self.lane(component)
        source = lane / zip_name
        source.write_bytes(data)
        if checksum:
            source.with_suffix(".sha256").write_text(f"{digest(data)}  {zip_name}\n", encoding="utf-8")
        if manifest:
            source.with_suffix(".manifest.json").write_text(json.dumps({
                "zip": zip_name,
                "sha256": digest(data),
                "size_bytes": len(data),
                "verified": True,
            }), encoding="utf-8")
        return source

    def write_chunked(self, component, zip_name, data, chunk_size=7):
        lane = self.lane(component)
        stem = zip_name[:-4]
        transport = lane / ".transport" / stem
        transport.mkdir(parents=True)
        chunks = []
        for index, start in enumerate(range(0, len(data), chunk_size), 1):
            payload = data[start:start + chunk_size]
            path = transport / f"{zip_name}.part{index:04d}"
            path.write_bytes(payload)
            chunks.append({
                "index": index,
                "path": str(path.relative_to(self.root)),
                "size_bytes": len(payload),
                "sha256": digest(payload),
            })
        manifest = lane / f"{stem}.transport.json"
        manifest.write_text(json.dumps({
            "schema": 1,
            "transport": "chunked-git-blobs-v1",
            "component": component,
            "zip": zip_name,
            "sha256": digest(data),
            "size_bytes": len(data),
            "chunk_size_bytes": chunk_size,
            "chunks": chunks,
            "verified": True,
        }), encoding="utf-8")
        return manifest

    def commit(self, message):
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def test_component_lanes_match_repository(self):
        self.assertEqual(COMPONENTS["CLIENT"].lane, "swrlz-core/sources/client")
        self.assertEqual(COMPONENTS["SERVER"].lane, "swrlz-core/sources/server")

    def test_copy_suffix_is_transport_only(self):
        parsed = parse_transport_name("CLIENT_CFv2.1.3_SWRLZ (9).zip", ".zip")
        self.assertEqual(parsed.logical_stem, "CLIENT_CFv2.1.3_SWRLZ")
        self.assertEqual(parsed.duplicate_suffix, 9)

    def test_zip_without_sidecars_is_build_eligible(self):
        source = self.write_zip("CLIENT", "CLIENT_CFv9.9.9_SWRLZ.zip", b"zip-only")
        result = resolve_source(self.root, "CLIENT", str(source.relative_to(self.root)))
        self.assertEqual(result["checksum_file"], "")
        self.assertEqual(result["manifest_file"], "")
        self.assertEqual(result["source_sha256"], digest(b"zip-only"))

    def test_supplied_checksum_mismatch_still_fails(self):
        source = self.write_zip("SERVER", "SERVER_CFv1.0.0_SWRLZ.zip", b"actual", checksum=True)
        source.with_suffix(".sha256").write_text(f"{digest(b'wrong')}  {source.name}\n")
        with self.assertRaisesRegex(ResolutionError, "checksum mismatch"):
            resolve_source(self.root, "SERVER")

    def test_supplied_manifest_mismatch_still_fails(self):
        source = self.write_zip("CLIENT", "CLIENT_CFv1.2.3_SWRLZ.zip", b"actual", manifest=True)
        source.with_suffix(".manifest.json").write_text(json.dumps({
            "zip": source.name,
            "sha256": digest(b"wrong"),
            "verified": True,
        }))
        with self.assertRaisesRegex(ResolutionError, "manifest SHA-256 mismatch"):
            resolve_source(self.root, "CLIENT")

    def test_chunk_transport_reassembles_exact_zip(self):
        data = b"chunked-source-payload" * 100
        manifest = self.write_chunked("SERVER", "SERVER_CFv2.1.8_SWRLZ_CANDIDATE_R3.zip", data, 31)
        work = self.root / "work"
        result = resolve_source(self.root, "SERVER", str(manifest.relative_to(self.root)), work)
        selected = Path(result["selected_source"])
        self.assertEqual(selected.read_bytes(), data)
        self.assertEqual(result["source_kind"], "chunked")
        self.assertEqual(result["source_sha256"], digest(data))

    def test_corrupt_chunk_fails_closed(self):
        data = b"abcdefghijklmnopqrstuvwxyz"
        manifest = self.write_chunked("SERVER", "SERVER_CFv2.1.8_SWRLZ.zip", data, 8)
        payload = json.loads(manifest.read_text())
        first = self.root / payload["chunks"][0]["path"]
        first.write_bytes(b"BROKEN!!")
        with self.assertRaisesRegex(ResolutionError, "Chunk SHA-256 mismatch"):
            resolve_source(self.root, "SERVER", str(manifest.relative_to(self.root)), self.root / "work")

    def test_current_push_selects_final_transport_manifest(self):
        old = self.write_zip("SERVER", "SERVER_CFv2.1.7_SWRLZ.zip", b"old")
        first = self.commit("baseline")
        manifest = self.write_chunked("SERVER", "SERVER_CFv2.1.8_SWRLZ.zip", b"new-source", 4)
        second = self.commit("transport complete")
        event = self.root / "event.json"
        event.write_text(json.dumps({"before": first, "after": second}), encoding="utf-8")
        with patch.dict(os.environ, {
            "GITHUB_EVENT_NAME": "push",
            "GITHUB_EVENT_PATH": str(event),
            "GITHUB_SHA": second,
        }, clear=False):
            result = resolve_source(self.root, "SERVER", work_dir=self.root / "work")
        self.assertEqual(result["selection_reason"], "current-push")
        self.assertEqual(result["source_kind"], "chunked")


if __name__ == "__main__":
    unittest.main(verbosity=2)
