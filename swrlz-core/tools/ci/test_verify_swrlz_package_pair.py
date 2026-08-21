#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

import verify_swrlz_package_pair as verifier


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_archive(source: Path, *, extra=None):
    root = source.stem
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr(f"{root}/settings.gradle.kts", "rootProject.name='fixture'\n")
        archive.writestr(f"{root}/gradlew", "#!/usr/bin/env bash\nexit 0\n")
        archive.writestr(f"{root}/app/build.gradle.kts", "plugins {}\n")
        for name, value in extra or []:
            archive.writestr(name, value)


def fixture(root: Path, component: str = "SERVER", revision: int = 7):
    source = root / f"{component}_CFv2.1.26_SWRLZ_CANDIDATE_R{revision}.zip"
    source_archive(source)
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
    def test_metadata_bundle_and_topology(self):
        with tempfile.TemporaryDirectory() as temp:
            source, _, _, metadata = fixture(Path(temp))
            result = verifier.verify(source, metadata, None, None)
            self.assertTrue(result["verified"])
            self.assertTrue(result["archive_topology_verified"])
            self.assertEqual(result["archive_root"], source.stem)

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

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R1.zip"
            source_archive(source, extra=[(f"{source.stem}/../escape.txt", "no")])
            with self.assertRaisesRegex(ValueError, "unsafe path"):
                verifier.validate_archive_topology(source)

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R1.zip"
            source_archive(source)
            with zipfile.ZipFile(source, "a") as archive:
                info = zipfile.ZipInfo(f"{source.stem}/danger-link")
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, "../../outside")
            with self.assertRaisesRegex(ValueError, "symlink"):
                verifier.validate_archive_topology(source)

    def test_multiple_gradle_roots_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R1.zip"
            source_archive(source, extra=[
                (f"{source.stem}/nested/settings.gradle.kts", "rootProject.name='nested'"),
                (f"{source.stem}/nested/gradlew", "#!/bin/sh\n"),
            ])
            with self.assertRaisesRegex(ValueError, "exactly one Android Gradle project root"):
                verifier.validate_archive_topology(source)

    def test_wrong_top_level_root_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R1.zip"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("WRONG/settings.gradle.kts", "rootProject.name='wrong'")
                archive.writestr("WRONG/gradlew", "#!/bin/sh\n")
            with self.assertRaisesRegex(ValueError, "canonical root"):
                verifier.validate_archive_topology(source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
