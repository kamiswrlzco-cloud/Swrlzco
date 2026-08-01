#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from resolve_changed_source_identities import IdentityMappingError, map_changed_path, map_changed_paths


class ChangedSourceIdentityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for lane in ("client", "server"):
            (self.root / f"swrlz-core/sources/{lane}").mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_nested_transport_evidence_maps_to_root_transport_identity(self):
        lane = self.root / "swrlz-core/sources/client"
        bundle = "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1"
        identity = lane / f"{bundle}.transport.json"
        identity.write_text("{}", encoding="utf-8")
        changed = f"swrlz-core/sources/client/.transport/{bundle}/evidence/{bundle}.sha256"
        self.assertEqual(
            map_changed_path(self.root, changed),
            ("CLIENT", f"swrlz-core/sources/client/{bundle}.transport.json"),
        )

    def test_nested_transport_chunk_maps_to_root_transport_identity(self):
        lane = self.root / "swrlz-core/sources/server"
        bundle = "SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1"
        (lane / f"{bundle}.transport.json").write_text("{}", encoding="utf-8")
        changed = f"swrlz-core/sources/server/.transport/{bundle}/{bundle}.zip.part0001"
        self.assertEqual(
            map_changed_path(self.root, changed),
            ("SERVER", f"swrlz-core/sources/server/{bundle}.transport.json"),
        )

    def test_root_direct_zip_maps_to_itself(self):
        changed = "swrlz-core/sources/client/CLIENT_CFv9.0.0_SWRLZ.zip"
        self.assertEqual(map_changed_path(self.root, changed), ("CLIENT", changed))

    def test_metadata_zip_maps_to_existing_direct_zip(self):
        lane = self.root / "swrlz-core/sources/client"
        stem = "CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R6"
        (lane / f"{stem}.zip").write_bytes(b"zip")
        changed = f"swrlz-core/sources/client/{stem}_METADATA.zip"
        self.assertEqual(
            map_changed_path(self.root, changed),
            ("CLIENT", f"swrlz-core/sources/client/{stem}.zip"),
        )

    def test_metadata_zip_maps_to_existing_chunked_transport(self):
        lane = self.root / "swrlz-core/sources/server"
        stem = "SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R9"
        (lane / f"{stem}.transport.json").write_text("{}", encoding="utf-8")
        changed = f"swrlz-core/sources/server/{stem}_METADATA.zip"
        self.assertEqual(
            map_changed_path(self.root, changed),
            ("SERVER", f"swrlz-core/sources/server/{stem}.transport.json"),
        )

    def test_source_and_metadata_zip_deduplicate_to_one_identity(self):
        lane = self.root / "swrlz-core/sources/client"
        stem = "CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R6"
        (lane / f"{stem}.zip").write_bytes(b"zip")
        changed = [
            f"swrlz-core/sources/client/{stem}.zip",
            f"swrlz-core/sources/client/{stem}_METADATA.zip",
        ]
        self.assertEqual(
            map_changed_paths(self.root, changed),
            [("CLIENT", f"swrlz-core/sources/client/{stem}.zip")],
        )

    def test_metadata_zip_direct_and_chunked_ambiguity_fails_closed(self):
        lane = self.root / "swrlz-core/sources/client"
        stem = "CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R6"
        (lane / f"{stem}.zip").write_bytes(b"zip")
        (lane / f"{stem}.transport.json").write_text("{}", encoding="utf-8")
        changed = f"swrlz-core/sources/client/{stem}_METADATA.zip"
        with self.assertRaisesRegex(IdentityMappingError, "ambiguous"):
            map_changed_path(self.root, changed)

    def test_orphan_metadata_zip_fails_closed(self):
        changed = "swrlz-core/sources/client/CLIENT_CFv9.0.0_SWRLZ_METADATA.zip"
        with self.assertRaisesRegex(IdentityMappingError, "no source identity"):
            map_changed_path(self.root, changed)

    def test_root_checksum_maps_to_existing_direct_zip(self):
        lane = self.root / "swrlz-core/sources/client"
        (lane / "CLIENT_CFv9.0.0_SWRLZ.zip").write_bytes(b"zip")
        changed = "swrlz-core/sources/client/CLIENT_CFv9.0.0_SWRLZ.sha256"
        self.assertEqual(
            map_changed_path(self.root, changed),
            ("CLIENT", "swrlz-core/sources/client/CLIENT_CFv9.0.0_SWRLZ.zip"),
        )

    def test_root_manifest_maps_to_existing_transport(self):
        lane = self.root / "swrlz-core/sources/server"
        (lane / "SERVER_CFv9.0.0_SWRLZ.transport.json").write_text("{}", encoding="utf-8")
        changed = "swrlz-core/sources/server/SERVER_CFv9.0.0_SWRLZ.manifest.json"
        self.assertEqual(
            map_changed_path(self.root, changed),
            ("SERVER", "swrlz-core/sources/server/SERVER_CFv9.0.0_SWRLZ.transport.json"),
        )

    def test_root_sidecar_direct_and_chunked_ambiguity_fails_closed(self):
        lane = self.root / "swrlz-core/sources/server"
        stem = "SERVER_CFv9.0.0_SWRLZ"
        (lane / f"{stem}.zip").write_bytes(b"zip")
        (lane / f"{stem}.transport.json").write_text("{}", encoding="utf-8")
        changed = f"swrlz-core/sources/server/{stem}.sha256"
        with self.assertRaisesRegex(IdentityMappingError, "ambiguous"):
            map_changed_path(self.root, changed)

    def test_missing_transport_identity_fails_closed(self):
        changed = "swrlz-core/sources/client/.transport/missing/evidence/missing.sha256"
        with self.assertRaisesRegex(IdentityMappingError, "no lane-root transport identity"):
            map_changed_path(self.root, changed)

    def test_deduplicates_many_members_of_same_transport(self):
        lane = self.root / "swrlz-core/sources/client"
        bundle = "CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1"
        (lane / f"{bundle}.transport.json").write_text("{}", encoding="utf-8")
        changed = [
            f"swrlz-core/sources/client/{bundle}.transport.json",
            f"swrlz-core/sources/client/.transport/{bundle}/{bundle}.zip.part0001",
            f"swrlz-core/sources/client/.transport/{bundle}/evidence/{bundle}.sha256",
        ]
        self.assertEqual(
            map_changed_paths(self.root, changed),
            [("CLIENT", f"swrlz-core/sources/client/{bundle}.transport.json")],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
