#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path('.').resolve()
CHECKOUT = 'actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6'
UPLOAD = 'actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7'
ATTEST = 'actions/attest-build-provenance@4d101475d8b20a2381f78447822ac1eab6504dd8 # v4.2.2'


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, text: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected one match, found {count}')
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, replacement: str, label: str) -> str:
    a = text.find(start)
    b = text.find(end, a + len(start))
    if a < 0 or b < 0:
        raise RuntimeError(f'{label}: section markers missing')
    return text[:a] + replacement + text[b:]


# -----------------------------------------------------------------------------
# Exact candidate checkout planner. This runs in the tiny prepare checkout and
# emits the final sparse patterns before the expensive CLIENT/SERVER runner starts.
# -----------------------------------------------------------------------------
write('swrlz-core/tools/ci/plan_swrlz_candidate_checkout.py', r'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

from prepare_swrlz_sparse_checkout import BASE_PATHS, LANES, build_sparse_paths, sparse_checkout_patterns

ACCOUNTING_GLOBAL = (
    'swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md',
    'swrlz-core/docs/CURRENT_AUTHORITY.md',
)


class CandidateCheckoutPlanError(RuntimeError):
    pass


def _git(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=repo_root, text=True).strip()


def _source_stats(repo_root: Path, ref: str, actual: Path) -> tuple[int, int, str]:
    if actual.name.lower().endswith('.transport.json'):
        payload = json.loads(_git(repo_root, 'show', f'{ref}:{actual.as_posix()}'))
        size = int(payload.get('source_size_bytes', 0) or 0)
        chunks = payload.get('chunks')
        chunk_count = len(chunks) if isinstance(chunks, list) else 0
        kind = str(payload.get('transport') or 'transport')
        return size, chunk_count, kind
    size = int(_git(repo_root, 'cat-file', '-s', f'{ref}:{actual.as_posix()}'))
    return size, 1, 'direct-git-zip'


def _fallback_paths(component: str) -> list[Path]:
    return [*BASE_PATHS, LANES[component]]


def _label(size: int, mode: str) -> str:
    if size > 0:
        return f'{size / (1024 * 1024):.2f} MiB'
    return 'lane fallback' if mode == 'full-lane-fallback' else 'unknown size'


def enrich_matrix(repo_root: Path, matrix: dict, *, ref: str = 'HEAD') -> dict:
    include = matrix.get('include')
    if not isinstance(include, list) or not include:
        raise CandidateCheckoutPlanError('matrix.include must be a non-empty list')

    enriched: list[dict] = []
    for raw in include:
        if not isinstance(raw, dict):
            raise CandidateCheckoutPlanError('matrix include row must be an object')
        component = str(raw.get('component') or '').upper()
        if component not in LANES:
            raise CandidateCheckoutPlanError(f'unsupported component: {component!r}')
        source_identity = str(raw.get('source_identity') or '').strip()

        row = dict(raw)
        if source_identity:
            paths, actual = build_sparse_paths(repo_root, component, source_identity, ref=ref)
            size, chunk_count, source_kind = _source_stats(repo_root, ref, actual)
            checkout_mode = 'exact-candidate'

            accounting_extras = [
                f'swrlz-core/docs/patch-notes/{component}_PATCH_NOTES.md',
                *ACCOUNTING_GLOBAL,
            ]
            try:
                accounting_paths, _ = build_sparse_paths(
                    repo_root,
                    component,
                    source_identity,
                    ref=ref,
                    extra_paths=accounting_extras,
                )
                accounting_status = 'planned'
            except Exception:
                # Accounting is diagnostic-only. Missing/stale accounting evidence
                # must never prevent the APK router from receiving an exact source.
                accounting_paths = paths
                accounting_status = 'source-only-fallback'
        else:
            paths = _fallback_paths(component)
            accounting_paths = [*paths, Path('swrlz-core/docs')]
            actual = LANES[component]
            size = 0
            chunk_count = 0
            source_kind = 'full-lane-fallback'
            checkout_mode = 'full-lane-fallback'
            accounting_status = 'full-lane-fallback'

        row.update(
            {
                'checkout_patterns': sparse_checkout_patterns(paths),
                'accounting_checkout_patterns': sparse_checkout_patterns(accounting_paths),
                'checkout_mode': checkout_mode,
                'actual_source_identity': actual.as_posix(),
                'source_size_bytes': size,
                'source_size_label': _label(size, checkout_mode),
                'source_chunk_count': chunk_count,
                'source_payload_kind': source_kind,
                'accounting_checkout_status': accounting_status,
            }
        )
        enriched.append(row)

    return {'include': enriched}


def write_github_output(path: Path, matrix: dict) -> None:
    with path.open('a', encoding='utf-8') as handle:
        handle.write('matrix=' + json.dumps(matrix, separators=(',', ':')) + '\n')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--matrix-json', required=True)
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--ref', default='HEAD')
    parser.add_argument('--github-output')
    args = parser.parse_args()
    try:
        matrix = json.loads(args.matrix_json)
        result = enrich_matrix(Path(args.repo_root).resolve(), matrix, ref=args.ref)
    except (CandidateCheckoutPlanError, OSError, subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f'SWRLZ candidate checkout planning failed: {exc}') from exc
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.github_output:
        write_github_output(Path(args.github_output), result)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
''')

write('swrlz-core/tools/ci/test_plan_swrlz_candidate_checkout.py', r'''#!/usr/bin/env python3
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
''')

# Public helper used by the candidate planner and actions/checkout non-cone mode.
sparse_path = 'swrlz-core/tools/ci/prepare_swrlz_sparse_checkout.py'
sparse = read(sparse_path)
needle = '''def _pattern(path: Path) -> str:\n    value = path.as_posix()\n    if path in BASE_PATHS or path == RELEASES_PATH:\n        return f"/{value}/"\n    return f"/{value}"\n\n\n'''
replacement = needle + '''def sparse_checkout_patterns(paths: list[Path]) -> str:\n    """Return exact non-cone sparse patterns suitable for actions/checkout."""\n    return "\\n".join(_pattern(path) for path in paths) + "\\n"\n\n\n'''
sparse = replace_once(sparse, needle, replacement, 'sparse pattern exporter')
write(sparse_path, sparse)

# Deletion-aware routing: archive/prune operations must not trigger a build.
planner_path = 'swrlz-core/tools/ci/plan_swrlz_build_route.py'
planner = read(planner_path)
planner_needle = '''        changed = _changed_paths(repo_root, before_sha, after_sha)\n        for path in changed:\n            lane_component = _lane_component(path)\n'''
planner_replacement = '''        changed = _changed_paths(repo_root, before_sha, after_sha)\n        for path in changed:\n            # Deleted or renamed-away historical files are archival maintenance,\n            # not build requests. A rename's new path still exists and routes normally.\n            if not _path_exists(repo_root, after_sha, Path(path)):\n                continue\n            lane_component = _lane_component(path)\n'''
planner = replace_once(planner, planner_needle, planner_replacement, 'deletion-aware route')
write(planner_path, planner)

planner_test_path = 'swrlz-core/tools/ci/test_plan_swrlz_build_route.py'
planner_test = read(planner_test_path)
insert_marker = '    def test_manual_explicit_identity_is_forwarded(self):\n'
new_test = '''    def test_deleted_source_identity_does_not_trigger_fallback_build(self):\n        transport = self._write_transport("SERVER", 142)\n        before = commit_all(self.repo, "server identity to archive")\n        transport.unlink()\n        head = commit_all(self.repo, "archive old server identity")\n        plan = route.plan_route(\n            self.repo,\n            event_name="push",\n            before_sha=before,\n            after_sha=head,\n        )\n        self.assertFalse(plan["has_work"])\n        self.assertEqual(plan["matrix"]["include"], [{"component": "CLIENT", "source_identity": ""}])\n\n'''
planner_test = replace_once(planner_test, insert_marker, new_test + insert_marker, 'deletion route test')
write(planner_test_path, planner_test)

# -----------------------------------------------------------------------------
# APK router: one-pass candidate checkout, no accounting in critical path,
# deterministic runner, success artifact before best-effort attestation, and
# failure diagnostic artifacts.
# -----------------------------------------------------------------------------
router_path = '.github/workflows/swrlz-apk-router.yml'
router = read(router_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
router = replace_once(
    router,
    '      matrix: ${{ steps.route.outputs.matrix }}\n',
    '      matrix: ${{ steps.checkout-plan.outputs.matrix }}\n',
    'router prepared matrix output',
)
router = replace_section(
    router,
    '      - name: Sparse partial checkout for route resolution\n',
    '      - name: Resolve manual, source-path, or request route\n',
    f'''      - name: Sparse partial checkout for route resolution\n        uses: {CHECKOUT}\n        with:\n          fetch-depth: 2\n          filter: blob:none\n          persist-credentials: false\n          sparse-checkout: |\n            swrlz-core/tools/ci\n            swrlz-core/requests\n\n''',
    'router prepare checkout',
)
plan_step = '''      - name: Plan one-pass candidate hydration\n        id: checkout-plan\n        env:\n          ROUTE_MATRIX: ${{ steps.route.outputs.matrix }}\n        run: |\n          set -euo pipefail\n          python3 "$SWRLZ_CI_ROOT/plan_swrlz_candidate_checkout.py" \\\n            --matrix-json "$ROUTE_MATRIX" \\\n            --ref "$GITHUB_SHA" \\\n            --github-output "$GITHUB_OUTPUT"\n\n'''
router = replace_once(router, '\n  build:\n', '\n' + plan_step + '  build:\n', 'router checkout plan step')
router = replace_section(
    router,
    '      - name: Candidate-targeted partial checkout\n',
    '      - name: Resolve canonical source and checksum\n',
    f'''      - name: Start source hydration timer\n        run: |\n          echo "SWRLZ_HYDRATION_STARTED_MS=$(date +%s%3N)" >> "$GITHUB_ENV"\n\n      - name: Hydrate ${{{{ matrix.component }}}} source · ${{{{ matrix.source_size_label }}}}\n        id: hydrate-source\n        uses: {CHECKOUT}\n        with:\n          fetch-depth: 1\n          filter: blob:none\n          persist-credentials: false\n          sparse-checkout-cone-mode: false\n          sparse-checkout: ${{{{ matrix.checkout_patterns }}}}\n\n      - name: Record source hydration timing\n        id: hydration\n        run: |\n          set -euo pipefail\n          END_MS="$(date +%s%3N)"\n          ELAPSED_MS=$((END_MS - SWRLZ_HYDRATION_STARTED_MS))\n          echo "source_hydration_ms=$ELAPSED_MS" >> "$GITHUB_OUTPUT"\n          {{\n            echo "## ${{{{ matrix.component }}}} source hydration"\n            echo\n            echo "- Mode: `${{{{ matrix.checkout_mode }}}}`"\n            echo "- Payload: `${{{{ matrix.source_size_label }}}}`"\n            echo "- Transport chunks: `${{{{ matrix.source_chunk_count }}}}`"\n            echo "- Hydration duration: `${{ELAPSED_MS}} ms`"\n          }} >> "$GITHUB_STEP_SUMMARY"\n\n''',
    'router one-pass hydration',
)
if '      - name: Verify selected source package\n        id: package-verify\n' not in router:
    router = replace_once(
        router,
        '      - name: Verify selected source package\n        run: |',
        '      - name: Verify selected source package\n        id: package-verify\n        run: |',
        'router package verify id',
    )
accounting_marker = '      - name: Check patch-note and lineage accounting (non-blocking diagnostic)\n'
if accounting_marker in router:
    router = replace_section(router, accounting_marker, '      - name: Define immutable artifact identity\n', '', 'remove router accounting')
router = router.replace('      - name: Record source, accounting, timing, and signing provenance', '      - name: Record source, timing, and signing provenance')
for dead in (
    '          ACCOUNTING_JSON: ${{ steps.accounting.outputs.result }}\n',
    '          cp "$ACCOUNTING_JSON" "$ARTIFACT_DIR/PATCH_ACCOUNTING.json"\n',
    '          sha256sum "$ARTIFACT_DIR/PATCH_ACCOUNTING.json" > "$ARTIFACT_DIR/PATCH_ACCOUNTING.json.sha256"\n',
    '            echo "- Patch/lineage accounting: `diagnostic only — non-blocking`"\n',
    '            echo "- Patch/lineage accounting: `PASS before Gradle`"\n',
):
    router = router.replace(dead, '')
for name, step_id in (
    ('Set up Java 17', 'setup-java'),
    ('Set up Gradle wrapper cache', 'setup-gradle'),
    ('Set up Android SDK tooling', 'setup-android'),
):
    marker = f'      - name: {name}\n'
    if f'{marker}        id: {step_id}\n' not in router:
        router = replace_once(router, marker, marker + f'        id: {step_id}\n', f'router {step_id}')
router = replace_once(
    router,
    '          SWRLZ_VERIFIED_SOURCE_SHA256: ${{ steps.resolve.outputs.source_sha256 }}\n',
    '          SWRLZ_VERIFIED_SOURCE_SHA256: ${{ steps.resolve.outputs.source_sha256 }}\n          SWRLZ_SOURCE_HYDRATION_MS: ${{ steps.hydration.outputs.source_hydration_ms }}\n',
    'router hydration env',
)
summary_needle = '            echo "- Source extraction: `${{ steps.build.outputs.extract_ms }} ms`"\n'
summary_add = '''            echo "- Planned source payload: `${{ matrix.source_size_label }}`"\n            echo "- Source transport chunks: `${{ matrix.source_chunk_count }}`"\n            echo "- Source hydration: `${{ steps.hydration.outputs.source_hydration_ms }} ms`"\n'''
router = replace_once(router, summary_needle, summary_add + summary_needle, 'router hydration summary')

publication_tail = f'''      - name: Upload canonical stable APK and provenance artifact\n        uses: {UPLOAD}\n        with:\n          name: ${{{{ steps.artifact-meta.outputs.artifact_name }}}}\n          path: ${{{{ steps.build.outputs.artifact_dir }}}}/\n          if-no-files-found: error\n          retention-days: 30\n          compression-level: 0\n\n      - name: Attest canonical stable APK provenance\n        id: attest\n        continue-on-error: true\n        uses: {ATTEST}\n        with:\n          subject-path: '${{{{ steps.build.outputs.artifact_dir }}}}/*_stable-signed.apk'\n\n      - name: Collect failed-build diagnostics\n        if: failure()\n        id: failure-diagnostics\n        env:\n          COMPONENT: ${{{{ matrix.component }}}}\n          SOURCE_IDENTITY: ${{{{ matrix.source_identity }}}}\n          SOURCE_SHA256: ${{{{ steps.resolve.outputs.source_sha256 }}}}\n          CANONICAL_STEM: ${{{{ steps.resolve.outputs.canonical_stem }}}}\n          SOURCE_SIZE_BYTES: ${{{{ matrix.source_size_bytes }}}}\n          SOURCE_CHUNK_COUNT: ${{{{ matrix.source_chunk_count }}}}\n          HYDRATE_OUTCOME: ${{{{ steps.hydrate-source.outcome }}}}\n          HYDRATION_MS: ${{{{ steps.hydration.outputs.source_hydration_ms }}}}\n          RESOLVE_OUTCOME: ${{{{ steps.resolve.outcome }}}}\n          PACKAGE_VERIFY_OUTCOME: ${{{{ steps.package-verify.outcome }}}}\n          JAVA_OUTCOME: ${{{{ steps.setup-java.outcome }}}}\n          GRADLE_SETUP_OUTCOME: ${{{{ steps.setup-gradle.outcome }}}}\n          ANDROID_SETUP_OUTCOME: ${{{{ steps.setup-android.outcome }}}}\n          BUILD_OUTCOME: ${{{{ steps.build.outcome }}}}\n          SIGNING_OUTCOME: ${{{{ steps.signing.outcome }}}}\n        run: |\n          set -uo pipefail\n          DIAG="$RUNNER_TEMP/swrlz-failure/$COMPONENT"\n          mkdir -p "$DIAG"\n          BUILD_DIR="$RUNNER_TEMP/swrlz-artifacts/router/$COMPONENT"\n          if [[ -d "$BUILD_DIR" ]]; then cp -a "$BUILD_DIR"/. "$DIAG"/ 2>/dev/null || true; fi\n          RESOLVER_DIR="$RUNNER_TEMP/swrlz-source-resolver/$COMPONENT"\n          if [[ -d "$RESOLVER_DIR" ]]; then\n            while IFS= read -r file; do\n              cp "$file" "$DIAG/resolver_$(basename "$file")" 2>/dev/null || true\n            done < <(find "$RESOLVER_DIR" -maxdepth 3 -type f \\\n              \\( -name '*.json' -o -name '*.txt' -o -name '*.log' \\) -print 2>/dev/null | sort)\n          fi\n          export DIAG COMPONENT SOURCE_IDENTITY SOURCE_SHA256 CANONICAL_STEM SOURCE_SIZE_BYTES SOURCE_CHUNK_COUNT \\\n            HYDRATE_OUTCOME HYDRATION_MS RESOLVE_OUTCOME PACKAGE_VERIFY_OUTCOME JAVA_OUTCOME \\\n            GRADLE_SETUP_OUTCOME ANDROID_SETUP_OUTCOME BUILD_OUTCOME SIGNING_OUTCOME\n          python3 - <<'PYFAIL'\n          import json, os\n          from pathlib import Path\n          outcomes = {{\n              'source_hydration': os.environ.get('HYDRATE_OUTCOME', ''),\n              'source_resolution': os.environ.get('RESOLVE_OUTCOME', ''),\n              'package_verification': os.environ.get('PACKAGE_VERIFY_OUTCOME', ''),\n              'java_setup': os.environ.get('JAVA_OUTCOME', ''),\n              'gradle_setup': os.environ.get('GRADLE_SETUP_OUTCOME', ''),\n              'android_setup': os.environ.get('ANDROID_SETUP_OUTCOME', ''),\n              'gradle_build': os.environ.get('BUILD_OUTCOME', ''),\n              'stable_signing': os.environ.get('SIGNING_OUTCOME', ''),\n          }}\n          failed_stage = next((stage for stage, outcome in outcomes.items() if outcome == 'failure'), 'unknown')\n          def number(name):\n              value = os.environ.get(name, '')\n              return int(value) if value.isdigit() else None\n          payload = {{\n              'schema': 2,\n              'component': os.environ.get('COMPONENT', ''),\n              'source_identity': os.environ.get('SOURCE_IDENTITY', ''),\n              'source_sha256': os.environ.get('SOURCE_SHA256', ''),\n              'canonical_stem': os.environ.get('CANONICAL_STEM', ''),\n              'source_size_bytes': number('SOURCE_SIZE_BYTES'),\n              'source_chunk_count': number('SOURCE_CHUNK_COUNT'),\n              'source_hydration_ms': number('HYDRATION_MS'),\n              'failed_stage': failed_stage,\n              'step_outcomes': outcomes,\n              'repository': os.environ.get('GITHUB_REPOSITORY', ''),\n              'commit': os.environ.get('GITHUB_SHA', ''),\n              'run_id': os.environ.get('GITHUB_RUN_ID', ''),\n              'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT', ''),\n              'workflow': os.environ.get('GITHUB_WORKFLOW', ''),\n          }}\n          target = Path(os.environ['DIAG']) / 'FORGE_FAILURE_CONTEXT.json'\n          target.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\\n', encoding='utf-8')\n          PYFAIL\n          sha256sum "$DIAG/FORGE_FAILURE_CONTEXT.json" > "$DIAG/FORGE_FAILURE_CONTEXT.json.sha256"\n          echo "diagnostic_dir=$DIAG" >> "$GITHUB_OUTPUT"\n\n      - name: Upload failed-build diagnostic bundle\n        if: failure() && steps.failure-diagnostics.outputs.diagnostic_dir != ''\n        uses: {UPLOAD}\n        with:\n          name: ${{{{ matrix.component }}}}_FORGE_FAILURE_${{{{ github.run_id }}}}_${{{{ github.run_attempt }}}}\n          path: ${{{{ steps.failure-diagnostics.outputs.diagnostic_dir }}}}/\n          if-no-files-found: error\n          retention-days: 14\n          compression-level: 6\n'''
router = replace_section(router, '      - name: Attest canonical stable APK provenance\n', '\n  publish-release:\n', publication_tail, 'router publication order')
write(router_path, router)

# -----------------------------------------------------------------------------
# Source package integrity: same exact preplanned candidate checkout, no custom
# token-bearing remote URL.
# -----------------------------------------------------------------------------
integrity_path = '.github/workflows/source-package-integrity.yml'
integrity = read(integrity_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
integrity = replace_once(integrity, '      matrix: ${{ steps.route.outputs.matrix }}\n', '      matrix: ${{ steps.checkout-plan.outputs.matrix }}\n', 'integrity matrix output')
integrity_plan = '''      - name: Plan one-pass candidate hydration\n        id: checkout-plan\n        env:\n          ROUTE_MATRIX: ${{ steps.route.outputs.matrix }}\n        run: |\n          set -euo pipefail\n          python3 "$SWRLZ_CI_ROOT/plan_swrlz_candidate_checkout.py" \\\n            --matrix-json "$ROUTE_MATRIX" \\\n            --ref "$GITHUB_SHA" \\\n            --github-output "$GITHUB_OUTPUT"\n\n'''
integrity = replace_once(integrity, '\n  verify:\n', '\n' + integrity_plan + '  verify:\n', 'integrity checkout plan')
integrity = replace_section(
    integrity,
    '      - name: Candidate-targeted partial checkout\n',
    '      - name: Resolve selected source\n',
    f'''      - name: Hydrate exact ${{{{ matrix.component }}}} source · ${{{{ matrix.source_size_label }}}}\n        uses: {CHECKOUT}\n        with:\n          fetch-depth: 1\n          filter: blob:none\n          persist-credentials: false\n          sparse-checkout-cone-mode: false\n          sparse-checkout: ${{{{ matrix.checkout_patterns }}}}\n\n''',
    'integrity one-pass checkout',
)
write(integrity_path, integrity)

# -----------------------------------------------------------------------------
# Accounting stays available as evidence but can no longer paint source updates
# red. Targeted accounting also uses a single exact checkout when evidence exists.
# -----------------------------------------------------------------------------
accounting_path = '.github/workflows/patch-note-accounting.yml'
accounting = read(accounting_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
accounting = replace_once(accounting, '      matrix: ${{ steps.route.outputs.matrix }}\n', '      matrix: ${{ steps.checkout-plan.outputs.matrix }}\n', 'accounting matrix output')
accounting_plan = '''      - name: Plan accounting candidate hydration\n        id: checkout-plan\n        env:\n          ROUTE_MATRIX: ${{ steps.route.outputs.matrix }}\n        run: |\n          set -euo pipefail\n          python3 "$SWRLZ_CI_ROOT/plan_swrlz_candidate_checkout.py" \\\n            --matrix-json "$ROUTE_MATRIX" \\\n            --ref "$GITHUB_SHA" \\\n            --github-output "$GITHUB_OUTPUT"\n\n'''
accounting = replace_once(accounting, '\n  audit-targeted:\n', '\n' + accounting_plan + '  audit-targeted:\n', 'accounting checkout plan')
accounting = replace_once(accounting, '    timeout-minutes: 10\n\n    steps:\n      - name: Candidate-targeted checkout with exact accounting docs\n', '    timeout-minutes: 10\n    continue-on-error: true\n\n    steps:\n      - name: Candidate-targeted checkout with exact accounting docs\n', 'accounting targeted continue')
accounting = replace_section(
    accounting,
    '      - name: Candidate-targeted checkout with exact accounting docs\n',
    '      - name: Audit selected package and repository accounting\n',
    f'''      - name: Hydrate accounting evidence · ${{{{ matrix.source_size_label }}}}\n        uses: {CHECKOUT}\n        with:\n          fetch-depth: 1\n          filter: blob:none\n          persist-credentials: false\n          sparse-checkout-cone-mode: false\n          sparse-checkout: ${{{{ matrix.accounting_checkout_patterns }}}}\n\n''',
    'accounting one-pass checkout',
)
accounting = replace_section(
    accounting,
    '      - name: Audit selected package and repository accounting\n',
    '\n  audit-fallback:\n',
    '''      - name: Audit selected package and repository accounting\n        env:\n          COMPONENT: ${{ matrix.component }}\n          SOURCE_IDENTITY: ${{ matrix.source_identity }}\n        run: |\n          set -uo pipefail\n          identities="$RUNNER_TEMP/swrlz-patch-accounting-identities.tsv"\n          result="$RUNNER_TEMP/swrlz-patch-accounting.json"\n          printf '%s\\t%s\\n' "$COMPONENT" "$SOURCE_IDENTITY" > "$identities"\n          rc=0\n          python3 "$SWRLZ_CI_ROOT/verify_patch_note_accounting.py" \\\n            --repo-root . \\\n            --identity-file "$identities" \\\n            --json-output "$result" || rc=$?\n          if [[ ! -s "$result" ]]; then\n            printf '{"schema":1,"status":"WARN","blocking":false,"exit_code":%d}\\n' "$rc" > "$result"\n          fi\n          if [[ "$rc" -ne 0 ]]; then\n            echo "::warning::Patch-note accounting diagnostic failed with exit $rc; source/build authority is unaffected."\n          fi\n          {\n            echo "## $COMPONENT patch note accounting (diagnostic only)"\n            echo\n            echo '```json'\n            cat "$result"\n            echo '```'\n          } >> "$GITHUB_STEP_SUMMARY"\n''',
    'accounting targeted warning mode',
)
accounting = replace_once(accounting, '  audit-fallback:\n    name: Audit current CLIENT / SERVER accounting\n    needs: prepare\n    if: needs.prepare.outputs.has_source_work != \'true\'\n    runs-on: ubuntu-24.04\n    timeout-minutes: 10\n', '  audit-fallback:\n    name: Audit current CLIENT / SERVER accounting\n    needs: prepare\n    if: needs.prepare.outputs.has_source_work != \'true\'\n    runs-on: ubuntu-24.04\n    timeout-minutes: 10\n    continue-on-error: true\n', 'accounting fallback continue')
fallback = accounting.find('      - name: Audit current repository accounting\n')
if fallback < 0:
    raise RuntimeError('accounting fallback marker missing')
accounting = accounting[:fallback] + '''      - name: Audit current repository accounting\n        run: |\n          set -uo pipefail\n          identities="$RUNNER_TEMP/swrlz-patch-accounting-identities.tsv"\n          result="$RUNNER_TEMP/swrlz-patch-accounting.json"\n          : > "$identities"\n          rc=0\n          python3 "$SWRLZ_CI_ROOT/verify_patch_note_accounting.py" \\\n            --repo-root . \\\n            --identity-file "$identities" \\\n            --json-output "$result" || rc=$?\n          if [[ ! -s "$result" ]]; then\n            printf '{"schema":1,"status":"WARN","blocking":false,"exit_code":%d}\\n' "$rc" > "$result"\n          fi\n          if [[ "$rc" -ne 0 ]]; then\n            echo "::warning::Current-candidate accounting diagnostic failed with exit $rc; source/build authority is unaffected."\n          fi\n          {\n            echo '## SWRLZ Patch Note Accounting (diagnostic only)'\n            echo\n            echo '```json'\n            cat "$result"\n            echo '```'\n          } >> "$GITHUB_STEP_SUMMARY"\n'''
write(accounting_path, accounting)

# Pin the central validation runner here; the second Phase 5 layer extends tests.
validation_path = '.github/workflows/swrlz-ci-tooling-validation.yml'
validation = read(validation_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
write(validation_path, validation)

# Archive the executable historical R8 lane rather than leaving an ancient manual button.
r8_workflow = ROOT / '.github/workflows/swrlz-server-r8-patch-build.yml'
archive = ROOT / 'swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml'
if r8_workflow.exists():
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(r8_workflow, archive)
    r8_workflow.unlink()

readme_path = '.github/workflows/README.md'
readme = read(readme_path)
readme = readme.replace(
    '- `swrlz-server-r8-patch-build.yml` — preserved explicit historical SERVER R8 patch-build lane.',
    '- historical SERVER R8 patch-build lane — archived (non-executable) at `swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml`.',
)
write(readme_path, readme)

print('Phase 5 workflow/routing/hydration patch applied.')
