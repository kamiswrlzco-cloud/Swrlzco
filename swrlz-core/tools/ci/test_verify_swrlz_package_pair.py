#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import verify_swrlz_package_pair as verifier


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(root: Path, component: str = "SERVER", revision: int = 7):
    source = root / f"{component}_CFv2.1.26_SWRLZ_CANDIDATE_R{revision}.zip"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("settings.gradle.kts", "rootProject.name='fixture'\n")
    digest = sha(source)
    manifest = {
        "schema": 1,
        "component": component,
        "zip": source.name,
        "sha256": digest,
        "size_bytes": source.stat().st_size,
        "versionCode": 90,
        "revision": f"R{revision}",
        "verified": True,
    }
    checksum = root / f"{source.stem}.sha256"
    manifest_path = root / f"{source.stem}.manifest.json"
    checksum.write_text(f"{digest}  {source.name}\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    metadata = root / f"{source.stem}_METADATA.zip"
    with zipfile.ZipFile(metadata, "w") as archive:
        archive.write(checksum, checksum.name)
        archive.write(manifest_path, manifest_path.name)
    return source, checksum, manifest_path, metadata


class VerifyTests(unittest.TestCase):
    def test_metadata_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            source, _, _, metadata = fixture(Path(temp))
            self.assertTrue(verifier.verify(source, metadata, None, None)["verified"])

    def test_legacy_sidecars(self):
        with tempfile.TemporaryDirectory() as temp:
            source, checksum, manifest, _ = fixture(Path(temp))
            self.assertEqual(verifier.verify(source, None, checksum, manifest)["format"], "legacy-sidecars")

    def test_modified_source_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            source, _, _, metadata = fixture(Path(temp))
            source.write_bytes(source.read_bytes() + b"changed")
            with self.assertRaises(ValueError):
                verifier.verify(source, metadata, None, None)

    def test_nested_metadata_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, checksum, manifest, metadata = fixture(root)
            with zipfile.ZipFile(metadata, "w") as archive:
                archive.write(checksum, "nested/" + checksum.name)
                archive.write(manifest, manifest.name)
            with self.assertRaises(ValueError):
                verifier.verify(source, metadata, None, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
