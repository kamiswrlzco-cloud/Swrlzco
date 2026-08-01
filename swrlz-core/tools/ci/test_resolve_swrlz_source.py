#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import resolve_swrlz_source as resolver


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_direct(repo: Path, component: str, revision: int, version_code: int):
    lane = repo / resolver.COMPONENT_LANES[component]
    lane.mkdir(parents=True, exist_ok=True)
    source = lane / f"{component}_CFv2.1.26_SWRLZ_CANDIDATE_R{revision}.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("settings.gradle.kts", "rootProject.name='fixture'\n")
    digest = sha(source)
    manifest = {
        "schema": 1,
        "component": component,
        "zip": source.name,
        "sha256": digest,
        "size_bytes": source.stat().st_size,
        "versionCode": version_code,
        "revision": f"R{revision}",
        "verified": True,
    }
    checksum_name = f"{source.stem}.sha256"
    manifest_name = f"{source.stem}.manifest.json"
    metadata = lane / f"{source.stem}_METADATA.zip"
    with zipfile.ZipFile(metadata, "w") as archive:
        archive.writestr(checksum_name, f"{digest}  {source.name}\n")
        archive.writestr(manifest_name, json.dumps(manifest))
    return source, metadata


def make_chunked_v2(repo: Path, component: str, revision: int, version_code: int):
    source, metadata = make_direct(repo, component, revision, version_code)
    lane = source.parent
    data = source.read_bytes()
    source.unlink()
    transport_dir = lane / ".transport" / source.stem
    transport_dir.mkdir(parents=True)
    chunks = []
    for index, start in enumerate(range(0, len(data), 32), 1):
        part = data[start : start + 32]
        path = transport_dir / f"{source.name}.part{index:04d}"
        path.write_bytes(part)
        chunks.append({
            "index": index,
            "path": path.relative_to(repo).as_posix(),
            "size_bytes": len(part),
            "sha256": hashlib.sha256(part).hexdigest(),
        })
    transport = lane / f"{source.stem}.transport.json"
    transport.write_text(json.dumps({
        "schema": 2,
        "transport": "chunked-git-blobs-v2",
        "component": component,
        "source_zip": source.name,
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "source_size_bytes": len(data),
        "chunks": chunks,
        "metadata_bundle": metadata.name,
        "metadata_bundle_path": metadata.relative_to(repo).as_posix(),
        "metadata_bundle_sha256": sha(metadata),
        "verified": True,
    }), encoding="utf-8")
    return transport, metadata


class ResolverTests(unittest.TestCase):
    def test_direct_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            make_direct(repo, "CLIENT", 5, 128)
            result = resolver.resolve(repo, "CLIENT", work_dir=repo / "work")
            self.assertEqual(result["source_kind"], "direct-bundle")
            self.assertEqual(result["revision"], "R5")

    def test_chunked_v2_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            make_chunked_v2(repo, "SERVER", 7, 90)
            result = resolver.resolve(repo, "SERVER", work_dir=repo / "work")
            self.assertEqual(result["source_kind"], "chunked-v2")
            self.assertTrue(Path(result["selected_source"]).is_file())

    def test_evidence_ranking(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            make_direct(repo, "SERVER", 6, 89)
            make_direct(repo, "SERVER", 7, 90)
            result = resolver.resolve(repo, "SERVER", work_dir=repo / "work")
            self.assertEqual(result["revision"], "R7")

    def test_unsupported_historical_transport_is_quarantined(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            source, _ = make_direct(repo, "SERVER", 7, 90)
            bad = source.parent / "SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1.transport.json"
            bad.write_text('{"schema":99,"transport":"future"}', encoding="utf-8")
            candidates = resolver.discover(repo, "SERVER", repo / "work", strict_paths=set())
            self.assertEqual(len(candidates), 1)

    def test_unsupported_current_transport_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            lane = repo / resolver.COMPONENT_LANES["SERVER"]
            lane.mkdir(parents=True)
            bad = lane / "SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R8.transport.json"
            bad.write_text('{"schema":99,"transport":"future","component":"SERVER"}', encoding="utf-8")
            with self.assertRaises(Exception):
                resolver.discover(repo, "SERVER", repo / "work", strict_paths={bad})


if __name__ == "__main__":
    unittest.main(verbosity=2)
