#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import resolve_swrlz_source as resolver


CLIENT_R6_IDENTITY = "swrlz-core/sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R6.zip"
CLIENT_R6_SHA256 = "09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136"
CLIENT_R6_METADATA_SHA256 = "39021fb0efc77de30369417655326f695d276029873a78c3d3d3326982733eb6"


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
    def test_resolve_source_compatibility_wrapper_delegates(self):
        repo = Path("/tmp/repo")
        work = Path("/tmp/work")
        sentinel = {"verified": True}
        with mock.patch.object(resolver, "resolve", return_value=sentinel) as delegated:
            self.assertIs(resolver.resolve_source(repo, "CLIENT", None, work), sentinel)
        delegated.assert_called_once_with(repo, "CLIENT", "", work)

    def test_resolve_source_preserves_explicit_identity(self):
        repo = Path("/tmp/repo")
        work = Path("/tmp/work")
        explicit = "swrlz-core/sources/client/example.zip"
        with mock.patch.object(resolver, "resolve", return_value={}) as delegated:
            resolver.resolve_source(repo, "CLIENT", explicit, work)
        delegated.assert_called_once_with(repo, "CLIENT", explicit, work)

    def test_direct_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            make_direct(repo, "CLIENT", 5, 128)
            result = resolver.resolve(repo, "CLIENT", work_dir=repo / "work")
            self.assertEqual(result["source_kind"], "direct-bundle")
            self.assertEqual(result["revision"], "R5")

    def test_compatibility_wrapper_verifies_direct_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            source, _ = make_direct(repo, "CLIENT", 6, 129)
            identity = source.relative_to(repo).as_posix()
            result = resolver.resolve_source(repo, "CLIENT", identity, repo / "work")
            self.assertEqual(result["canonical_filename"], source.name)
            self.assertEqual(result["version_code"], 129)
            self.assertEqual(result["revision"], "R6")
            self.assertEqual(result["selection_reason"], "explicit-source")
            self.assertTrue(result["verified"])

    def test_direct_bundle_accepts_lane_root_filename_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            source, _ = make_direct(repo, "SERVER", 6, 129)
            result = resolver.resolve(repo, "SERVER", source.name, repo / "work")
            self.assertEqual(result["canonical_filename"], source.name)
            self.assertEqual(result["source_kind"], "direct-bundle")
            self.assertEqual(result["selection_reason"], "explicit-source")

    def test_chunked_v2_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            make_chunked_v2(repo, "SERVER", 7, 90)
            result = resolver.resolve(repo, "SERVER", work_dir=repo / "work")
            self.assertEqual(result["source_kind"], "chunked-v2")
            self.assertTrue(Path(result["selected_source"]).is_file())

    def test_discovery_defers_chunk_reassembly_until_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            work = repo / "work"
            make_chunked_v2(repo, "SERVER", 7, 90)
            make_chunked_v2(repo, "SERVER", 8, 91)
            candidates = resolver.discover(repo, "SERVER", work)
            self.assertEqual(len(candidates), 2)
            sources = work / "sources"
            self.assertFalse(sources.exists(), "discovery should not materialize historical source ZIPs")

    def test_verified_latest_falls_back_after_lazy_payload_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            older, _ = make_chunked_v2(repo, "SERVER", 7, 90)
            newer, _ = make_chunked_v2(repo, "SERVER", 8, 91)
            payload = json.loads(newer.read_text(encoding="utf-8"))
            first_chunk = repo / payload["chunks"][0]["path"]
            first_chunk.write_bytes(first_chunk.read_bytes() + b"corrupt")
            result = resolver.resolve(repo, "SERVER", work_dir=repo / "work")
            self.assertEqual(result["revision"], "R7")
            self.assertEqual(result["uploaded_filename"], older.name)
            self.assertTrue(Path(result["selected_source"]).is_file())

    def test_chunked_v2_accepts_explicit_logical_zip_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            transport, _ = make_chunked_v2(repo, "SERVER", 8, 91)
            source_name = transport.name.removesuffix(".transport.json") + ".zip"
            result = resolver.resolve(repo, "SERVER", source_name, repo / "work")
            self.assertEqual(result["source_kind"], "chunked-v2")
            self.assertEqual(result["canonical_filename"], source_name)
            self.assertEqual(result["uploaded_filename"], transport.name)
            self.assertEqual(result["selection_reason"], "explicit-source")
            self.assertTrue(Path(result["selected_source"]).is_file())

    def test_explicit_logical_zip_keeps_matching_chunked_transport_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            transport, _ = make_chunked_v2(repo, "SERVER", 9, 92)
            payload = json.loads(transport.read_text(encoding="utf-8"))
            first_chunk = repo / payload["chunks"][0]["path"]
            first_chunk.write_bytes(first_chunk.read_bytes() + b"corrupt")
            source_name = transport.name.removesuffix(".transport.json") + ".zip"
            with self.assertRaises(resolver.ResolutionError):
                resolver.resolve(repo, "SERVER", source_name, repo / "work")

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

    def test_repository_client_r6_source_and_metadata_verify_when_present(self):
        repo = Path(__file__).resolve().parents[3]
        source = repo / CLIENT_R6_IDENTITY
        metadata = source.with_name(f"{source.stem}_METADATA.zip")
        if not source.is_file() or not metadata.is_file():
            self.skipTest("Repository CLIENT R6 source/metadata fixture is not present")
        with tempfile.TemporaryDirectory() as temp:
            result = resolver.resolve_source(
                repo,
                "CLIENT",
                CLIENT_R6_IDENTITY,
                Path(temp),
            )
        self.assertEqual(result["source_sha256"], CLIENT_R6_SHA256)
        self.assertEqual(result["metadata_bundle_sha256"], CLIENT_R6_METADATA_SHA256)
        self.assertEqual(result["version_code"], 129)
        self.assertEqual(result["revision"], "R6")
        self.assertEqual(result["selection_reason"], "explicit-source")
        self.assertTrue(result["verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
