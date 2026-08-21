#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from prepare_swrlz_sparse_checkout import LANES, build_sparse_paths, sparse_checkout_patterns
from resolve_swrlz_latest_identity import resolve_latest_identity

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


def _label(size: int) -> str:
    return f'{size / (1024 * 1024):.2f} MiB' if size > 0 else 'unknown size'


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
        requested_identity = str(raw.get('source_identity') or '').strip()
        source_identity = requested_identity
        checkout_mode = 'exact-candidate'
        if not source_identity:
            source_identity = resolve_latest_identity(repo_root, component, ref=ref)
            checkout_mode = 'exact-latest-candidate'

        paths, actual = build_sparse_paths(repo_root, component, source_identity, ref=ref)
        size, chunk_count, source_kind = _source_stats(repo_root, ref, actual)

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

        row = dict(raw)
        row.update(
            {
                'source_identity': actual.as_posix(),
                'requested_source_identity': requested_identity,
                'checkout_patterns': sparse_checkout_patterns(paths),
                'accounting_checkout_patterns': sparse_checkout_patterns(accounting_paths),
                'checkout_mode': checkout_mode,
                'actual_source_identity': actual.as_posix(),
                'source_size_bytes': size,
                'source_size_label': _label(size),
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
