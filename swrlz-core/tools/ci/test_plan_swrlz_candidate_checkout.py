#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import plan_swrlz_candidate_checkout as checkout


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=repo, text=True).strip()


class CandidateCheckoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, 'init')
        git(self.repo, 'config', 'user.email', 'ci@example.invalid')
        git(self.repo, 'config', 'user.name', 'SWRLZ CI')
        (self.repo / 'swrlz-core/tools/ci').mkdir(parents=True)
        (self.repo / 'swrlz-core/requests').mkdir(parents=True)
        (self.repo / 'swrlz-core/docs/patch-notes').mkdir(parents=True)
        (self.repo / 'swrlz-core/docs/reference').mkdir(parents=True)
        (self.repo / 'swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md').write_text('notes\n')
        (self.repo / 'swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md').write_text('lineage\n')
        (self.repo / 'swrlz-core/docs/CURRENT_AUTHORITY.md').write_text('authority\n')

        lane = self.repo / 'swrlz-core/sources/server'
        transport_dir = lane / '.transport/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152'
        transport_dir.mkdir(parents=True)
        chunk = transport_dir / 'SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152.zip.part0001'
        chunk.write_bytes(b'x' * 32)
        metadata = lane / 'SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152_METADATA.zip'
        metadata.write_bytes(b'meta')
        self.identity = lane / 'SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152.transport.json'
        self.identity.write_text(json.dumps({
            'schema': 2,
            'transport': 'chunked-git-blobs-v2',
            'component': 'SERVER',
            'source_zip': 'SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152.zip',
            'source_size_bytes': 52582335,
            'verified': True,
            'metadata_bundle_path': metadata.relative_to(self.repo).as_posix(),
            'chunks': [{
                'index': 1,
                'path': chunk.relative_to(self.repo).as_posix(),
                'size_bytes': 32,
                'sha256': '0' * 64,
            }],
        }), encoding='utf-8')
        git(self.repo, 'add', '-A')
        git(self.repo, 'commit', '-m', 'fixture')

    def tearDown(self):
        self.tmp.cleanup()

    def test_exact_transport_is_planned_before_build_checkout(self):
        matrix = {'include': [{
            'component': 'SERVER',
            'source_identity': self.identity.relative_to(self.repo).as_posix(),
        }]}
        result = checkout.enrich_matrix(self.repo, matrix, ref='HEAD')['include'][0]
        self.assertEqual(result['checkout_mode'], 'exact-candidate')
        self.assertEqual(result['source_size_bytes'], 52582335)
        self.assertEqual(result['source_chunk_count'], 1)
        self.assertIn('/swrlz-core/sources/server/.transport/', result['checkout_patterns'])
        self.assertIn('/swrlz-core/sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152_METADATA.zip', result['checkout_patterns'])
        self.assertNotIn('/swrlz-core/docs/', result['checkout_patterns'])
        self.assertIn('/swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md', result['accounting_checkout_patterns'])

    def test_fallback_remains_lane_scoped(self):
        matrix = {'include': [{'component': 'CLIENT', 'source_identity': ''}]}
        result = checkout.enrich_matrix(self.repo, matrix, ref='HEAD')['include'][0]
        self.assertEqual(result['checkout_mode'], 'full-lane-fallback')
        self.assertIn('/swrlz-core/sources/client/', result['checkout_patterns'])
        self.assertNotIn('/swrlz-core/sources/server/', result['checkout_patterns'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
