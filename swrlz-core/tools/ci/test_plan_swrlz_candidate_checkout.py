#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import plan_swrlz_candidate_checkout as checkout


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=repo, text=True).strip()


def metadata_bundle(stem: str, source_bytes: bytes) -> bytes:
    source_name = stem + '.zip'
    sha = hashlib.sha256(source_bytes).hexdigest()
    manifest = {
        'component': 'SERVER',
        'sourceZip': {
            'filename': source_name,
            'sha256': sha,
            'sizeBytes': len(source_bytes),
        },
        'versionCode': 275,
        'revision': 'R152',
        'verified': True,
    }
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(f'{stem}.sha256', f'{sha} *{source_name}\n')
        archive.writestr(f'{stem}.manifest.json', json.dumps(manifest))
    return output.getvalue()


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
        stem = 'SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152'
        transport_dir = lane / '.transport' / stem
        transport_dir.mkdir(parents=True)
        source_bytes = b'x' * 32
        source_sha = hashlib.sha256(source_bytes).hexdigest()
        chunk = transport_dir / f'{stem}.zip.part0001'
        chunk.write_bytes(source_bytes)
        metadata = lane / f'{stem}_METADATA.zip'
        metadata_bytes = metadata_bundle(stem, source_bytes)
        metadata.write_bytes(metadata_bytes)
        self.identity = lane / f'{stem}.transport.json'
        self.identity.write_text(json.dumps({
            'schema': 2,
            'transport': 'chunked-git-blobs-v2',
            'component': 'SERVER',
            'source_zip': f'{stem}.zip',
            'source_sha256': source_sha,
            'source_size_bytes': len(source_bytes),
            'verified': True,
            'metadata_bundle_path': metadata.relative_to(self.repo).as_posix(),
            'metadata_bundle_sha256': hashlib.sha256(metadata_bytes).hexdigest(),
            'chunks': [{
                'index': 1,
                'path': chunk.relative_to(self.repo).as_posix(),
                'size_bytes': len(source_bytes),
                'sha256': source_sha,
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
        self.assertEqual(result['source_size_bytes'], 32)
        self.assertEqual(result['source_chunk_count'], 1)
        self.assertIn('/swrlz-core/sources/server/.transport/', result['checkout_patterns'])
        self.assertIn('/swrlz-core/sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R152_METADATA.zip', result['checkout_patterns'])
        self.assertNotIn('/swrlz-core/docs/', result['checkout_patterns'])
        self.assertIn('/swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md', result['accounting_checkout_patterns'])

    def test_blank_identity_resolves_latest_exact_candidate(self):
        matrix = {'include': [{'component': 'SERVER', 'source_identity': ''}]}
        result = checkout.enrich_matrix(self.repo, matrix, ref='HEAD')['include'][0]
        self.assertEqual(result['checkout_mode'], 'exact-latest-candidate')
        self.assertEqual(result['source_identity'], self.identity.relative_to(self.repo).as_posix())
        self.assertEqual(result['requested_source_identity'], '')
        self.assertIn('/swrlz-core/sources/server/.transport/', result['checkout_patterns'])
        self.assertNotIn('/swrlz-core/sources/server/', result['checkout_patterns'].splitlines())


if __name__ == '__main__':
    unittest.main(verbosity=2)
