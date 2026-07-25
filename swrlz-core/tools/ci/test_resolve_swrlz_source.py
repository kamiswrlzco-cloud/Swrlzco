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
        for spec in COMPONENTS.values():
            (self.root / spec.lane).mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_pair(self, component, zip_name, data, checksum_name=None):
        lane = self.root / COMPONENTS[component].lane
        source = lane / zip_name
        source.write_bytes(data)
        checksum = lane / (checksum_name or (zip_name[:-4] + ".sha256"))
        checksum.write_text(f"{digest(data)}  {zip_name}\n", encoding="utf-8")
        return source

    def commit(self, message):
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def test_component_lanes_match_new_repository(self):
        self.assertEqual(COMPONENTS["CLIENT"].lane, "swrlz-core/sources/client")
        self.assertEqual(COMPONENTS["SERVER"].lane, "swrlz-core/sources/server")

    def test_copy_suffix_is_transport_only(self):
        parsed = parse_transport_name("CLIENT_CFv2.1.2_SWRLZ (9).zip", ".zip")
        self.assertEqual(parsed.logical_stem, "CLIENT_CFv2.1.2_SWRLZ")
        self.assertEqual(parsed.duplicate_suffix, 9)

    def test_explicit_client_source_resolves(self):
        source = self.write_pair("CLIENT", "CLIENT_CFv2.1.2_SWRLZ.zip", b"client")
        result = resolve_source(self.root, "CLIENT", str(source.relative_to(self.root)))
        self.assertEqual(result["selected_source"], str(source.relative_to(self.root)))
        self.assertEqual(result["source_sha256"], digest(b"client"))

    def test_current_push_selects_changed_server(self):
        source = self.write_pair("SERVER", "SERVER_CFv2.1.0_SWRLZ.zip", b"server-v1")
        first = self.commit("initial")
        source.write_bytes(b"server-v2")
        source.with_suffix(".sha256").write_text(f"{digest(b'server-v2')}  {source.name}\n")
        second = self.commit("update")
        event = self.root / "event.json"
        event.write_text(json.dumps({"before": first, "after": second}), encoding="utf-8")
        with patch.dict(os.environ, {
            "GITHUB_EVENT_NAME": "push",
            "GITHUB_EVENT_PATH": str(event),
            "GITHUB_SHA": second,
        }, clear=False):
            result = resolve_source(self.root, "SERVER")
        self.assertEqual(result["selection_reason"], "current-push")

    def test_missing_checksum_fails_closed(self):
        lane = self.root / COMPONENTS["CLIENT"].lane
        (lane / "CLIENT_CFv9.9.9_SWRLZ.zip").write_bytes(b"x")
        with self.assertRaisesRegex(ResolutionError, "No matching checksum"):
            resolve_source(self.root, "CLIENT")

    def test_checksum_mismatch_fails_closed(self):
        source = self.write_pair("SERVER", "SERVER_CFv1.0.0_SWRLZ.zip", b"actual")
        source.with_suffix(".sha256").write_text(f"{digest(b'wrong')}  {source.name}\n")
        with self.assertRaisesRegex(ResolutionError, "checksum mismatch"):
            resolve_source(self.root, "SERVER")

if __name__ == "__main__":
    unittest.main(verbosity=2)
