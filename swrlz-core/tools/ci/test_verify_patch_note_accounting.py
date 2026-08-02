#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import verify_patch_note_accounting as audit


def manifest(component: str = "CLIENT", revision: str = "R9", vc: int = 132, sha: str = "a" * 64) -> dict:
    return {
        "component": component,
        "checkpoint": "INT-TEST-001",
        "version": "CFv2.1.26",
        "revision": revision,
        "versionCode": vc,
        "versionName": "2.1.26-test-candidate",
        "sourceZip": {
            "filename": f"{component}_CFv2.1.26_SWRLZ_CANDIDATE_{revision}.zip",
            "sha256": sha,
        },
        "parent": {"sha256": "b" * 64},
    }


def write_package(path: Path, data: dict, stale_release: bool = False, stale_lineage: bool = False) -> None:
    candidate = data["sourceZip"]["filename"][:-4]
    short = f"{data['version']} {data['revision']}"
    current = f"# {candidate} / VC{data['versionCode']} — {data['checkpoint']}\n"
    release = "# old parent\n" if stale_release else current
    lineage = {
        "component": data["component"],
        "candidate": "OLD" if stale_lineage else candidate,
        "version": data["version"],
        "versionCode": data["versionCode"],
        "versionName": data["versionName"],
        "parent": {"sha256": data["parent"]["sha256"]},
    }
    with zipfile.ZipFile(path, "w") as z:
        root = candidate + "/"
        z.writestr(root + "CHANGELOG.md", current)
        z.writestr(root + "ReleaseNotes.md", release)
        z.writestr(root + "SWRLZ_PATCH_LINEAGE_INDEX_V1.json", json.dumps(lineage))


class PatchAccountingTests(unittest.TestCase):
    def test_current_internal_surfaces_pass(self):
        data = manifest()
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "candidate.zip"
            write_package(package, data)
            result = audit.AuditResult("CLIENT", "x", audit._candidate_stem(data), data["sourceZip"]["sha256"])
            with zipfile.ZipFile(package) as z:
                audit._check_internal_text(result, z, "CHANGELOG.md", data)
                audit._check_internal_text(result, z, "ReleaseNotes.md", data)
                audit._check_internal_lineage(result, z, data)
            self.assertEqual(result.status, "PASS")
            self.assertEqual(result.errors, [])

    def test_stale_non_grandfathered_surfaces_fail(self):
        data = manifest()
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "candidate.zip"
            write_package(package, data, stale_release=True, stale_lineage=True)
            result = audit.AuditResult("CLIENT", "x", audit._candidate_stem(data), data["sourceZip"]["sha256"])
            with zipfile.ZipFile(package) as z:
                audit._check_internal_text(result, z, "ReleaseNotes.md", data)
                audit._check_internal_lineage(result, z, data)
            self.assertEqual(result.status, "FAIL")
            self.assertEqual(len(result.errors), 2)

    def test_exact_grandfathered_sha_records_debt(self):
        sha = next(iter(audit.GRANDFATHERED_DEBT))
        data = manifest(sha=sha)
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp) / "candidate.zip"
            write_package(package, data, stale_release=True, stale_lineage=True)
            result = audit.AuditResult("CLIENT", "x", audit._candidate_stem(data), sha)
            with zipfile.ZipFile(package) as z:
                audit._check_internal_text(result, z, "ReleaseNotes.md", data)
                audit._check_internal_lineage(result, z, data)
            self.assertEqual(result.status, "DEBT_RECORDED")
            self.assertEqual(result.errors, [])
            self.assertEqual(len(result.warnings), 2)

    def test_repository_doc_requires_sha_candidate_and_checkpoint(self):
        data = manifest()
        with tempfile.TemporaryDirectory() as temp:
            doc = Path(temp) / "notes.md"
            doc.write_text("nothing useful\n", encoding="utf-8")
            result = audit.AuditResult("CLIENT", "x", audit._candidate_stem(data), data["sourceZip"]["sha256"])
            audit._require_doc_tokens(result, doc, data, require_checkpoint=True)
            self.assertEqual(result.status, "FAIL")
            self.assertIn("source SHA-256", result.errors[0])
            self.assertIn("checkpoint", result.errors[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
