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
# APK router
# -----------------------------------------------------------------------------
router_path = '.github/workflows/swrlz-apk-router.yml'
router = read(router_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')

router = replace_section(
    router,
    '      - name: Sparse partial checkout for route resolution\n',
    '      - name: Resolve manual, source-path, or request route\n',
    f'''      - name: Sparse partial checkout for route resolution
        uses: {CHECKOUT}
        with:
          fetch-depth: 2
          filter: blob:none
          persist-credentials: false
          sparse-checkout: |
            swrlz-core/tools/ci
            swrlz-core/requests

''',
    'router prepare checkout',
)

router = replace_section(
    router,
    '      - name: Candidate-targeted partial checkout\n',
    '      - name: Resolve canonical source and checksum\n',
    f'''      - name: Checkout candidate routing seed
        uses: {CHECKOUT}
        with:
          fetch-depth: 1
          filter: blob:none
          persist-credentials: false
          sparse-checkout: |
            swrlz-core/tools/ci
            swrlz-core/requests

      - name: Expand candidate-targeted sparse checkout
        env:
          COMPONENT: ${{{{ matrix.component }}}}
          SOURCE_IDENTITY: ${{{{ matrix.source_identity }}}}
        run: |
          set -euo pipefail
          LANE="$(printf '%s' "$COMPONENT" | tr '[:upper:]' '[:lower:]')"
          if [[ -n "$SOURCE_IDENTITY" ]]; then
            python3 "$SWRLZ_CI_ROOT/prepare_swrlz_sparse_checkout.py" \\
              --component "$COMPONENT" \\
              --source-identity "$SOURCE_IDENTITY" \\
              --ref HEAD
          else
            git sparse-checkout set \\
              swrlz-core/tools/ci \\
              swrlz-core/requests \\
              "swrlz-core/sources/$LANE"
            echo "SWRLZ checkout mode: compatible full-lane fallback for $COMPONENT"
          fi

''',
    'router targeted checkout',
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
    router = replace_section(
        router,
        accounting_marker,
        '      - name: Define immutable artifact identity\n',
        '',
        'router accounting removal',
    )

router = router.replace(
    '      - name: Record source, accounting, timing, and signing provenance',
    '      - name: Record source, timing, and signing provenance',
)
router = router.replace('          ACCOUNTING_JSON: ${{ steps.accounting.outputs.result }}\n', '')
router = router.replace('          cp "$ACCOUNTING_JSON" "$ARTIFACT_DIR/PATCH_ACCOUNTING.json"\n', '')
router = router.replace(
    '          sha256sum "$ARTIFACT_DIR/PATCH_ACCOUNTING.json" > "$ARTIFACT_DIR/PATCH_ACCOUNTING.json.sha256"\n',
    '',
)
router = router.replace('            echo "- Patch/lineage accounting: `diagnostic only — non-blocking`"\n', '')
router = router.replace('            echo "- Patch/lineage accounting: `PASS before Gradle`"\n', '')

for name, step_id in (
    ('Set up Java 17', 'setup-java'),
    ('Set up Gradle wrapper cache', 'setup-gradle'),
    ('Set up Android SDK tooling', 'setup-android'),
):
    marker = f'      - name: {name}\n'
    if f'{marker}        id: {step_id}\n' not in router:
        router = replace_once(router, marker, marker + f'        id: {step_id}\n', f'router {step_id}')

publication_start = '      - name: Attest canonical stable APK provenance\n'
publish_job = '\n  publish-release:\n'
publication_tail = f'''      - name: Upload canonical stable APK and provenance artifact
        uses: {UPLOAD}
        with:
          name: ${{{{ steps.artifact-meta.outputs.artifact_name }}}}
          path: ${{{{ steps.build.outputs.artifact_dir }}}}/
          if-no-files-found: error
          retention-days: 30
          compression-level: 0

      - name: Attest canonical stable APK provenance
        id: attest
        continue-on-error: true
        uses: {ATTEST}
        with:
          subject-path: '${{{{ steps.build.outputs.artifact_dir }}}}/*_stable-signed.apk'

      - name: Collect failed-build diagnostics
        if: failure()
        id: failure-diagnostics
        env:
          COMPONENT: ${{{{ matrix.component }}}}
          SOURCE_IDENTITY: ${{{{ matrix.source_identity }}}}
          SOURCE_SHA256: ${{{{ steps.resolve.outputs.source_sha256 }}}}
          CANONICAL_STEM: ${{{{ steps.resolve.outputs.canonical_stem }}}}
          RESOLVE_OUTCOME: ${{{{ steps.resolve.outcome }}}}
          PACKAGE_VERIFY_OUTCOME: ${{{{ steps.package-verify.outcome }}}}
          JAVA_OUTCOME: ${{{{ steps.setup-java.outcome }}}}
          GRADLE_SETUP_OUTCOME: ${{{{ steps.setup-gradle.outcome }}}}
          ANDROID_SETUP_OUTCOME: ${{{{ steps.setup-android.outcome }}}}
          BUILD_OUTCOME: ${{{{ steps.build.outcome }}}}
          SIGNING_OUTCOME: ${{{{ steps.signing.outcome }}}}
        run: |
          set -uo pipefail
          DIAG="$RUNNER_TEMP/swrlz-failure/$COMPONENT"
          mkdir -p "$DIAG"

          BUILD_DIR="$RUNNER_TEMP/swrlz-artifacts/router/$COMPONENT"
          if [[ -d "$BUILD_DIR" ]]; then
            cp -a "$BUILD_DIR"/. "$DIAG"/ 2>/dev/null || true
          fi

          RESOLVER_DIR="$RUNNER_TEMP/swrlz-source-resolver/$COMPONENT"
          if [[ -d "$RESOLVER_DIR" ]]; then
            while IFS= read -r file; do
              cp "$file" "$DIAG/resolver_$(basename "$file")" 2>/dev/null || true
            done < <(find "$RESOLVER_DIR" -maxdepth 3 -type f \\
              \( -name '*.json' -o -name '*.txt' -o -name '*.log' \) -print 2>/dev/null | sort)
          fi

          export DIAG COMPONENT SOURCE_IDENTITY SOURCE_SHA256 CANONICAL_STEM \\
            RESOLVE_OUTCOME PACKAGE_VERIFY_OUTCOME JAVA_OUTCOME GRADLE_SETUP_OUTCOME \\
            ANDROID_SETUP_OUTCOME BUILD_OUTCOME SIGNING_OUTCOME
          python3 - <<'PYFAIL'
          import json, os
          from pathlib import Path

          outcomes = {{
              'source_resolution': os.environ.get('RESOLVE_OUTCOME', ''),
              'package_verification': os.environ.get('PACKAGE_VERIFY_OUTCOME', ''),
              'java_setup': os.environ.get('JAVA_OUTCOME', ''),
              'gradle_setup': os.environ.get('GRADLE_SETUP_OUTCOME', ''),
              'android_setup': os.environ.get('ANDROID_SETUP_OUTCOME', ''),
              'gradle_build': os.environ.get('BUILD_OUTCOME', ''),
              'stable_signing': os.environ.get('SIGNING_OUTCOME', ''),
          }}
          failed_stage = next((stage for stage, outcome in outcomes.items() if outcome == 'failure'), 'unknown')
          payload = {{
              'schema': 1,
              'component': os.environ.get('COMPONENT', ''),
              'source_identity': os.environ.get('SOURCE_IDENTITY', ''),
              'source_sha256': os.environ.get('SOURCE_SHA256', ''),
              'canonical_stem': os.environ.get('CANONICAL_STEM', ''),
              'failed_stage': failed_stage,
              'step_outcomes': outcomes,
              'repository': os.environ.get('GITHUB_REPOSITORY', ''),
              'commit': os.environ.get('GITHUB_SHA', ''),
              'run_id': os.environ.get('GITHUB_RUN_ID', ''),
              'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT', ''),
              'workflow': os.environ.get('GITHUB_WORKFLOW', ''),
          }}
          target = Path(os.environ['DIAG']) / 'FORGE_FAILURE_CONTEXT.json'
          target.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\\n', encoding='utf-8')
          PYFAIL
          sha256sum "$DIAG/FORGE_FAILURE_CONTEXT.json" > "$DIAG/FORGE_FAILURE_CONTEXT.json.sha256"
          echo "diagnostic_dir=$DIAG" >> "$GITHUB_OUTPUT"

      - name: Upload failed-build diagnostic bundle
        if: failure() && steps.failure-diagnostics.outputs.diagnostic_dir != ''
        uses: {UPLOAD}
        with:
          name: ${{{{ matrix.component }}}}_FORGE_FAILURE_${{{{ github.run_id }}}}_${{{{ github.run_attempt }}}}
          path: ${{{{ steps.failure-diagnostics.outputs.diagnostic_dir }}}}/
          if-no-files-found: error
          retention-days: 14
          compression-level: 6
'''
router = replace_section(router, publication_start, publish_job, publication_tail, 'router publication tail')
write(router_path, router)


# -----------------------------------------------------------------------------
# Patch accounting: diagnostic-only, standardized checkout, pinned runner.
# -----------------------------------------------------------------------------
accounting_path = '.github/workflows/patch-note-accounting.yml'
accounting = read(accounting_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
accounting = replace_section(
    accounting,
    '      - name: Candidate-targeted checkout with exact accounting docs\n',
    '      - name: Audit selected package and repository accounting\n',
    f'''      - name: Checkout accounting routing seed
        uses: {CHECKOUT}
        with:
          fetch-depth: 1
          filter: blob:none
          persist-credentials: false
          sparse-checkout: |
            swrlz-core/tools/ci
            swrlz-core/requests

      - name: Expand exact accounting checkout
        env:
          COMPONENT: ${{{{ matrix.component }}}}
          SOURCE_IDENTITY: ${{{{ matrix.source_identity }}}}
        run: |
          set -euo pipefail
          [[ -n "$SOURCE_IDENTITY" ]] || {{
            echo 'Targeted accounting requires an exact source identity.' >&2
            exit 64
          }}
          python3 "$SWRLZ_CI_ROOT/prepare_swrlz_sparse_checkout.py" \\
            --component "$COMPONENT" \\
            --source-identity "$SOURCE_IDENTITY" \\
            --ref HEAD \\
            --extra-path "swrlz-core/docs/patch-notes/${{COMPONENT}}_PATCH_NOTES.md" \\
            --extra-path swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md \\
            --extra-path swrlz-core/docs/CURRENT_AUTHORITY.md

''',
    'accounting targeted checkout',
)

accounting = replace_section(
    accounting,
    '      - name: Audit selected package and repository accounting\n',
    '\n  audit-fallback:\n',
    '''      - name: Audit selected package and repository accounting
        env:
          COMPONENT: ${{ matrix.component }}
          SOURCE_IDENTITY: ${{ matrix.source_identity }}
        run: |
          set -uo pipefail
          identities="$RUNNER_TEMP/swrlz-patch-accounting-identities.tsv"
          result="$RUNNER_TEMP/swrlz-patch-accounting.json"
          printf '%s\\t%s\\n' "$COMPONENT" "$SOURCE_IDENTITY" > "$identities"
          rc=0
          python3 "$SWRLZ_CI_ROOT/verify_patch_note_accounting.py" \\
            --repo-root . \\
            --identity-file "$identities" \\
            --json-output "$result" || rc=$?
          if [[ ! -s "$result" ]]; then
            printf '{"schema":1,"status":"WARN","blocking":false,"exit_code":%d}\\n' "$rc" > "$result"
          fi
          if [[ "$rc" -ne 0 ]]; then
            echo "::warning::Patch-note accounting diagnostic failed with exit $rc; source/build authority is unaffected."
          fi
          {
            echo "## $COMPONENT patch note accounting (diagnostic only)"
            echo
            echo '```json'
            cat "$result"
            echo '```'
          } >> "$GITHUB_STEP_SUMMARY"
''',
    'accounting targeted audit',
)

fallback_marker = '      - name: Audit current repository accounting\n'
fallback_pos = accounting.find(fallback_marker)
if fallback_pos < 0:
    raise RuntimeError('accounting fallback marker missing')
accounting = accounting[:fallback_pos] + '''      - name: Audit current repository accounting
        run: |
          set -uo pipefail
          identities="$RUNNER_TEMP/swrlz-patch-accounting-identities.tsv"
          result="$RUNNER_TEMP/swrlz-patch-accounting.json"
          : > "$identities"
          rc=0
          python3 "$SWRLZ_CI_ROOT/verify_patch_note_accounting.py" \\
            --repo-root . \\
            --identity-file "$identities" \\
            --json-output "$result" || rc=$?
          if [[ ! -s "$result" ]]; then
            printf '{"schema":1,"status":"WARN","blocking":false,"exit_code":%d}\\n' "$rc" > "$result"
          fi
          if [[ "$rc" -ne 0 ]]; then
            echo "::warning::Current-candidate accounting diagnostic failed with exit $rc; source/build authority is unaffected."
          fi
          {
            echo '## SWRLZ Patch Note Accounting (diagnostic only)'
            echo
            echo '```json'
            cat "$result"
            echo '```'
          } >> "$GITHUB_STEP_SUMMARY"
'''
write(accounting_path, accounting)


# -----------------------------------------------------------------------------
# Source package integrity: standardized checkout and pinned runner.
# -----------------------------------------------------------------------------
integrity_path = '.github/workflows/source-package-integrity.yml'
integrity = read(integrity_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
integrity = replace_section(
    integrity,
    '      - name: Candidate-targeted partial checkout\n',
    '      - name: Resolve selected source\n',
    f'''      - name: Checkout integrity routing seed
        uses: {CHECKOUT}
        with:
          fetch-depth: 1
          filter: blob:none
          persist-credentials: false
          sparse-checkout: |
            swrlz-core/tools/ci
            swrlz-core/requests

      - name: Expand candidate-targeted integrity checkout
        env:
          COMPONENT: ${{{{ matrix.component }}}}
          SOURCE_IDENTITY: ${{{{ matrix.source_identity }}}}
        run: |
          set -euo pipefail
          [[ -n "$SOURCE_IDENTITY" ]] || {{
            echo 'Source integrity requires an exact source identity.' >&2
            exit 64
          }}
          python3 "$SWRLZ_CI_ROOT/prepare_swrlz_sparse_checkout.py" \\
            --component "$COMPONENT" \\
            --source-identity "$SOURCE_IDENTITY" \\
            --ref HEAD

''',
    'integrity targeted checkout',
)
write(integrity_path, integrity)


# -----------------------------------------------------------------------------
# Deletion-aware routing.
# -----------------------------------------------------------------------------
planner_path = 'swrlz-core/tools/ci/plan_swrlz_build_route.py'
planner = read(planner_path)
if 'Deleted or renamed-away historical files are archival maintenance' not in planner:
    needle = '        changed = _changed_paths(repo_root, before_sha, after_sha)\n        for path in changed:\n'
    replacement = '''        changed = _changed_paths(repo_root, before_sha, after_sha)
        for path in changed:
            # Deleted or renamed-away historical files are archival maintenance,
            # not build requests. A rename's new path still exists and routes normally.
            if not _path_exists(repo_root, after_sha, Path(path)):
                continue
'''
    planner = replace_once(planner, needle, replacement, 'planner deletion guard')
write(planner_path, planner)

planner_test_path = 'swrlz-core/tools/ci/test_plan_swrlz_build_route.py'
planner_test = read(planner_test_path)
if 'test_deleted_source_identity_does_not_trigger_fallback_build' not in planner_test:
    insertion = '''    def test_deleted_source_identity_does_not_trigger_fallback_build(self):
        transport = self._write_transport("SERVER", 142)
        before = commit_all(self.repo, "server identity to archive")
        transport.unlink()
        head = commit_all(self.repo, "archive old server identity")
        plan = route.plan_route(
            self.repo,
            event_name="push",
            before_sha=before,
            after_sha=head,
        )
        self.assertFalse(plan["has_work"])
        self.assertEqual(
            plan["matrix"]["include"],
            [{"component": "CLIENT", "source_identity": ""}],
        )

'''
    marker = '    def test_manual_explicit_identity_is_forwarded(self):\n'
    planner_test = replace_once(planner_test, marker, insertion + marker, 'planner deletion test')
write(planner_test_path, planner_test)


# -----------------------------------------------------------------------------
# Package verifier: archive path/topology safety.
# -----------------------------------------------------------------------------
verifier_path = 'swrlz-core/tools/ci/verify_swrlz_package_pair.py'
verifier = r'''#!/usr/bin/env python3
"""Verify one SWRLZ source ZIP against metadata and safe Android archive topology."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

SHA_RE = re.compile(r"(?i)(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
REVISION_RE = re.compile(r"(?i)_CANDIDATE_R(\d+)$")
MAX_ARCHIVE_ENTRIES = 200_000
ABSOLUTE_MAX_UNCOMPRESSED = 2 * 1024 * 1024 * 1024
MIN_UNCOMPRESSED_BUDGET = 512 * 1024 * 1024
MAX_EXPANSION_MULTIPLIER = 100


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stem(name: str, suffix: str) -> str:
    if not name.lower().endswith(suffix.lower()):
        raise ValueError(f"Expected {suffix}: {name}")
    return name[: -len(suffix)].rstrip()


def manifest_source(payload: dict) -> tuple[str, str, int]:
    source = payload.get("sourceZip") if isinstance(payload.get("sourceZip"), dict) else {}
    name = str(source.get("filename") or payload.get("zip") or "")
    digest = str(source.get("sha256") or payload.get("sha256") or "").lower()
    size = source.get("sizeBytes", source.get("size_bytes", payload.get("sizeBytes", payload.get("size_bytes", -1))))
    return name, digest, int(size)


def validate_archive_topology(zip_path: Path) -> dict:
    archive_size = max(1, zip_path.stat().st_size)
    budget = min(
        ABSOLUTE_MAX_UNCOMPRESSED,
        max(MIN_UNCOMPRESSED_BUDGET, archive_size * MAX_EXPANSION_MULTIPLIER),
    )
    with zipfile.ZipFile(zip_path) as archive:
        entries = archive.infolist()
        if not entries:
            raise ValueError("Source ZIP is empty")
        if len(entries) > MAX_ARCHIVE_ENTRIES:
            raise ValueError("Source ZIP contains too many entries")
        names: set[str] = set()
        roots: set[str] = set()
        total_uncompressed = 0
        for item in entries:
            raw = item.filename
            if not raw or "\\" in raw or "\x00" in raw:
                raise ValueError(f"Unsafe archive path: {raw!r}")
            path = PurePosixPath(raw)
            if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
                raise ValueError(f"Unsafe archive path: {raw!r}")
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError(f"Source ZIP may not contain symlinks: {raw}")
            total_uncompressed += int(item.file_size)
            if total_uncompressed > budget:
                raise ValueError(
                    f"Source ZIP declared expansion exceeds safety budget ({total_uncompressed} > {budget})"
                )
            normalized = path.as_posix().rstrip("/")
            if not normalized:
                continue
            names.add(normalized)
            roots.add(path.parts[0])
        if len(roots) != 1:
            raise ValueError(f"Source ZIP must have exactly one top-level candidate root: {sorted(roots)}")
        root = next(iter(roots))
        expected_root = stem(zip_path.name, ".zip")
        if root.casefold() != expected_root.casefold():
            raise ValueError(f"Source ZIP root {root!r} does not match canonical candidate {expected_root!r}")
        project_roots: list[str] = []
        for name in sorted(names):
            path = PurePosixPath(name)
            if path.name != "gradlew":
                continue
            parent = path.parent.as_posix()
            if f"{parent}/settings.gradle" in names or f"{parent}/settings.gradle.kts" in names:
                project_roots.append(parent)
        project_roots = sorted(set(project_roots))
        if len(project_roots) != 1:
            raise ValueError(
                f"Source ZIP must contain exactly one Android Gradle wrapper root; found {project_roots}"
            )
    return {
        "archive_root": root,
        "android_project_root": project_roots[0],
        "archive_entries": len(entries),
        "archive_uncompressed_bytes": total_uncompressed,
        "archive_uncompressed_budget_bytes": budget,
    }


def validate(zip_path: Path, checksum_text: str, payload: dict) -> dict:
    actual_sha = sha256(zip_path)
    actual_size = zip_path.stat().st_size
    match = SHA_RE.search(checksum_text)
    if not match or match.group(1).lower() != actual_sha:
        raise ValueError("Source checksum mismatch")
    target = checksum_text[match.end():].strip().lstrip("*").strip()
    if target and stem(target, ".zip").casefold() != stem(zip_path.name, ".zip").casefold():
        raise ValueError("Checksum target filename mismatch")
    name, manifest_sha, manifest_size = manifest_source(payload)
    if stem(name, ".zip").casefold() != stem(zip_path.name, ".zip").casefold():
        raise ValueError("Manifest source filename mismatch")
    if manifest_sha != actual_sha or manifest_size != actual_size:
        raise ValueError("Manifest source identity mismatch")
    if int(payload.get("versionCode", payload.get("version_code", -1))) <= 0:
        raise ValueError("Manifest versionCode missing or invalid")
    component = str(payload.get("component") or "").upper()
    expected_component = "CLIENT" if zip_path.name.upper().startswith("CLIENT_") else "SERVER" if zip_path.name.upper().startswith("SERVER_") else ""
    if expected_component and component and component != expected_component:
        raise ValueError("Manifest component mismatch")
    revision_match = REVISION_RE.search(stem(zip_path.name, ".zip"))
    if revision_match and str(payload.get("revision") or "").upper() != f"R{revision_match.group(1)}":
        raise ValueError("Manifest revision mismatch")
    if "verified" in payload and payload.get("verified") is not True:
        raise ValueError("Manifest verified flag is false")
    topology = validate_archive_topology(zip_path)
    return {
        "source": str(zip_path),
        "source_sha256": actual_sha,
        "size_bytes": actual_size,
        "verified": True,
        **topology,
    }


def verify(zip_path: Path, metadata: Path | None, checksum: Path | None, manifest: Path | None) -> dict:
    if not zip_path.is_file():
        raise ValueError("Source ZIP is missing")
    if metadata:
        expected_stem = stem(zip_path.name, ".zip")
        checksum_name = f"{expected_stem}.sha256"
        manifest_name = f"{expected_stem}.manifest.json"
        if metadata.stat().st_size > 4 * 1024 * 1024:
            raise ValueError("Metadata ZIP exceeds 4 MiB")
        with zipfile.ZipFile(metadata) as archive:
            files = [item for item in archive.infolist() if not item.is_dir()]
            if len(files) != 2:
                raise ValueError("Metadata ZIP must contain exactly checksum and manifest")
            names = {}
            for item in files:
                normalized = item.filename.replace("\\", "/")
                if "/" in normalized or item.file_size > 1024 * 1024:
                    raise ValueError("Metadata ZIP contains nested or oversized entry")
                names[normalized.casefold()] = item
            if checksum_name.casefold() not in names or manifest_name.casefold() not in names:
                raise ValueError("Metadata ZIP entry names do not match source")
            checksum_text = archive.read(names[checksum_name.casefold()]).decode("utf-8")
            payload = json.loads(archive.read(names[manifest_name.casefold()]).decode("utf-8"))
        result = validate(zip_path, checksum_text, payload)
        result.update({"format": "metadata-bundle-v1", "metadata_bundle": str(metadata), "metadata_bundle_sha256": sha256(metadata)})
        return result
    if not checksum or not manifest:
        raise ValueError("Metadata ZIP or complete legacy sidecars are required")
    result = validate(zip_path, checksum.read_text(encoding="utf-8"), json.loads(manifest.read_text(encoding="utf-8")))
    result.update({"format": "legacy-sidecars", "checksum": str(checksum), "manifest": str(manifest)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--checksum", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.zip_path, args.metadata, args.checksum, args.manifest)
    except (ValueError, OSError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"SWRLZ package verification failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''
write(verifier_path, verifier)

verifier_test_path = 'swrlz-core/tools/ci/test_verify_swrlz_package_pair.py'
verifier_test = r'''#!/usr/bin/env python3
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


def write_android_source(archive: zipfile.ZipFile, root: str) -> None:
    archive.writestr(f"{root}/settings.gradle.kts", "rootProject.name='fixture'\n")
    archive.writestr(f"{root}/gradlew", "#!/bin/sh\n")
    archive.writestr(f"{root}/app/build.gradle.kts", "plugins {{ }}\n")


def fixture(root: Path, component: str = "SERVER", revision: int = 7):
    source = root / f"{component}_CFv2.1.26_SWRLZ_CANDIDATE_R{revision}.zip"
    with zipfile.ZipFile(source, "w") as archive:
        write_android_source(archive, source.stem)
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


def refresh_evidence(source: Path, checksum: Path, manifest: Path) -> None:
    digest = sha(source)
    checksum.write_text(f"{digest}  {source.name}\n", encoding="utf-8")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["sha256"] = digest
    payload["size_bytes"] = source.stat().st_size
    manifest.write_text(json.dumps(payload), encoding="utf-8")


class VerifyTests(unittest.TestCase):
    def test_metadata_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            source, _, _, metadata = fixture(Path(temp))
            result = verifier.verify(source, metadata, None, None)
            self.assertTrue(result["verified"])
            self.assertEqual(result["archive_root"], source.stem)
            self.assertEqual(result["android_project_root"], source.stem)

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
            source, checksum, manifest, _ = fixture(root)
            with zipfile.ZipFile(source, "w") as archive:
                write_android_source(archive, source.stem)
                archive.writestr("../escape.txt", "nope")
            refresh_evidence(source, checksum, manifest)
            with self.assertRaisesRegex(ValueError, "Unsafe archive path"):
                verifier.verify(source, None, checksum, manifest)

    def test_symlink_entry_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, checksum, manifest, _ = fixture(root)
            with zipfile.ZipFile(source, "w") as archive:
                write_android_source(archive, source.stem)
                link = zipfile.ZipInfo(f"{source.stem}/link")
                link.create_system = 3
                link.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(link, "target")
            refresh_evidence(source, checksum, manifest)
            with self.assertRaisesRegex(ValueError, "symlinks"):
                verifier.verify(source, None, checksum, manifest)

    def test_multiple_android_roots_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, checksum, manifest, _ = fixture(root)
            with zipfile.ZipFile(source, "w") as archive:
                write_android_source(archive, source.stem)
                archive.writestr(f"{source.stem}/nested/settings.gradle.kts", "rootProject.name='nested'\n")
                archive.writestr(f"{source.stem}/nested/gradlew", "#!/bin/sh\n")
            refresh_evidence(source, checksum, manifest)
            with self.assertRaisesRegex(ValueError, "exactly one Android Gradle wrapper root"):
                verifier.verify(source, None, checksum, manifest)

    def test_mismatched_top_level_root_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, checksum, manifest, _ = fixture(root)
            with zipfile.ZipFile(source, "w") as archive:
                write_android_source(archive, "WRONG_ROOT")
            refresh_evidence(source, checksum, manifest)
            with self.assertRaisesRegex(ValueError, "does not match canonical candidate"):
                verifier.verify(source, None, checksum, manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''
write(verifier_test_path, verifier_test)


# -----------------------------------------------------------------------------
# Archive historical R8 workflow so it remains evidence, not executable control.
# -----------------------------------------------------------------------------
old_r8 = ROOT / '.github/workflows/swrlz-server-r8-patch-build.yml'
archived_r8 = ROOT / 'swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml'
if old_r8.is_file():
    archived_r8.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(old_r8), str(archived_r8))
elif not archived_r8.is_file():
    raise RuntimeError('historical SERVER R8 workflow missing')

readme_path = '.github/workflows/README.md'
readme = read(readme_path)
readme = readme.replace(
    '- `swrlz-server-r8-patch-build.yml` — preserved explicit historical SERVER R8 patch-build lane.\n',
    '',
)
if '## Historical workflow evidence' not in readme:
    readme += '''

## Historical workflow evidence

Historical executable definitions are archived outside `/.github/workflows/` so they
remain byte-reviewable lineage evidence without remaining runnable controls. The
former SERVER R8 derived-build lane is preserved at:

`swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml`
'''
write(readme_path, readme)


# -----------------------------------------------------------------------------
# Static workflow contract and tooling validation updates.
# -----------------------------------------------------------------------------
contract_test_path = 'swrlz-core/tools/ci/test_workflow_phase5_contract.py'
contract_test = r'''#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS = ROOT / ".github/workflows"


class Phase5WorkflowContractTests(unittest.TestCase):
    def test_active_workflows_pin_ubuntu_2404(self):
        for path in sorted(WORKFLOWS.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("runs-on: ubuntu-latest", text, path.name)

    def test_router_has_failure_bundle_and_no_accounting_execution(self):
        text = (WORKFLOWS / "swrlz-apk-router.yml").read_text(encoding="utf-8")
        self.assertNotIn("verify_patch_note_accounting.py", text)
        self.assertIn("FORGE_FAILURE_CONTEXT.json", text)
        self.assertIn("_FORGE_FAILURE_", text)

    def test_success_artifact_upload_precedes_best_effort_attestation(self):
        text = (WORKFLOWS / "swrlz-apk-router.yml").read_text(encoding="utf-8")
        upload = text.index("Upload canonical stable APK and provenance artifact")
        attest = text.index("Attest canonical stable APK provenance")
        self.assertLess(upload, attest)
        self.assertIn("continue-on-error: true", text[attest:attest + 500])

    def test_historical_r8_lane_is_not_executable(self):
        self.assertFalse((WORKFLOWS / "swrlz-server-r8-patch-build.yml").exists())
        self.assertTrue((ROOT / "swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml").is_file())

    def test_accounting_workflow_declares_diagnostic_semantics(self):
        text = (WORKFLOWS / "patch-note-accounting.yml").read_text(encoding="utf-8")
        self.assertIn("source/build authority is unaffected", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''
write(contract_test_path, contract_test)

validation_path = '.github/workflows/swrlz-ci-tooling-validation.yml'
validation = read(validation_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
if '            .github/workflows\n' not in validation:
    validation = replace_once(
        validation,
        '            swrlz-core/requests\n',
        '            swrlz-core/requests\n            .github/workflows\n            swrlz-core/history/workflows\n',
        'validation sparse paths',
    )
if 'test_workflow_phase5_contract.py' not in validation:
    validation = replace_once(
        validation,
        '            test_verify_patch_note_accounting.py\n',
        '            test_verify_patch_note_accounting.py \\\n            test_workflow_phase5_contract.py\n',
        'validation compile test',
    )
    validation = replace_once(
        validation,
        '          python3 test_verify_patch_note_accounting.py\n',
        '          python3 test_verify_patch_note_accounting.py\n          python3 test_workflow_phase5_contract.py\n',
        'validation run test',
    )
validation = validation.replace('SWRLZ Phase 4 action stack OK', 'SWRLZ Phase 5 action stack OK')
validation = validation.replace('swrlz-phase4-action-smoke-', 'swrlz-phase5-action-smoke-')
write(validation_path, validation)

print('Phase 5 patch applied to working tree.')
