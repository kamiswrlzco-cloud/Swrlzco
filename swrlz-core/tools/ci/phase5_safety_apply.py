#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path('.').resolve()


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


write('swrlz-core/tools/ci/verify_swrlz_package_pair.py', r'''#!/usr/bin/env python3
"""Verify one SWRLZ source ZIP against metadata and safe archive topology."""
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
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:/")
MAX_ARCHIVE_ENTRIES = 100_000
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 2 * 1024 * 1024 * 1024
MAX_SINGLE_ENTRY_BYTES = 512 * 1024 * 1024


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
    expected_root = stem(zip_path.name, ".zip")
    with zipfile.ZipFile(zip_path) as archive:
        infos = archive.infolist()
        if not infos:
            raise ValueError("Source archive is empty")
        if len(infos) > MAX_ARCHIVE_ENTRIES:
            raise ValueError("Source archive has too many entries")

        roots: set[str] = set()
        file_names: set[str] = set()
        total_uncompressed = 0

        for info in infos:
            raw = info.filename
            if "\x00" in raw:
                raise ValueError("Source archive contains NUL in path")
            normalized = raw.replace("\\", "/")
            if normalized.startswith("/") or WINDOWS_ABSOLUTE_RE.match(normalized):
                raise ValueError(f"Source archive contains absolute path: {raw}")
            cleaned = normalized[:-1] if normalized.endswith("/") else normalized
            if not cleaned:
                raise ValueError("Source archive contains empty path")
            path = PurePosixPath(cleaned)
            if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
                raise ValueError(f"Source archive contains unsafe path: {raw}")
            roots.add(path.parts[0])

            mode = (info.external_attr >> 16) & 0xFFFF
            file_type = stat.S_IFMT(mode)
            if file_type == stat.S_IFLNK:
                raise ValueError(f"Source archive contains symlink: {raw}")
            if file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
                raise ValueError(f"Source archive contains unsupported file type: {raw}")

            if info.file_size > MAX_SINGLE_ENTRY_BYTES:
                raise ValueError(f"Source archive entry exceeds safety limit: {raw}")
            total_uncompressed += info.file_size
            if total_uncompressed > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                raise ValueError("Source archive exceeds uncompressed safety limit")

            if not info.is_dir():
                file_names.add(cleaned)

        if roots != {expected_root}:
            raise ValueError(
                f"Source archive must have exactly canonical root {expected_root!r}; found {sorted(roots)}"
            )

        wrappers = {
            name[: -len("/gradlew")]
            for name in file_names
            if name.endswith("/gradlew")
        }
        project_roots = {
            root
            for root in wrappers
            if f"{root}/settings.gradle" in file_names or f"{root}/settings.gradle.kts" in file_names
        }
        if len(project_roots) != 1:
            raise ValueError(
                f"Source archive must contain exactly one Android Gradle project root; found {sorted(project_roots)}"
            )

    return {
        "archive_root": expected_root,
        "android_project_root": next(iter(project_roots)),
        "archive_entry_count": len(infos),
        "archive_uncompressed_bytes": total_uncompressed,
        "archive_topology_verified": True,
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
''')

write('swrlz-core/tools/ci/test_verify_swrlz_package_pair.py', r'''#!/usr/bin/env python3
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
''')

write('swrlz-core/tools/ci/build_swrlz_component.sh', r'''#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: build_swrlz_component.sh CLIENT|SERVER SOURCE_ZIP CANONICAL_STEM debug|release WORK_DIR ARTIFACT_DIR" >&2
  exit 64
}

now_ms() {
  date +%s%3N
}

[[ $# -eq 6 ]] || usage
COMPONENT="${1^^}"
SOURCE_ZIP="$2"
CANONICAL_STEM="$3"
VARIANT="${4,,}"
WORK_DIR="$5"
ARTIFACT_DIR="$6"
SOURCE_HYDRATION_MS="${SWRLZ_SOURCE_HYDRATION_MS:-0}"

case "$COMPONENT" in CLIENT|SERVER) ;; *) usage ;; esac
case "$VARIANT" in
  debug) GRADLE_TASK=':app:assembleDebug' ;;
  release) GRADLE_TASK=':app:assembleRelease' ;;
  *) usage ;;
esac
[[ "$SOURCE_HYDRATION_MS" =~ ^[0-9]+$ ]] || {
  echo 'SWRLZ_SOURCE_HYDRATION_MS must be a non-negative integer.' >&2
  exit 65
}

SOURCE_ZIP="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$SOURCE_ZIP")"
WORK_DIR="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$WORK_DIR")"
ARTIFACT_DIR="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$ARTIFACT_DIR")"
[[ -f "$SOURCE_ZIP" ]] || { echo "Source ZIP not found: $SOURCE_ZIP" >&2; exit 66; }

BUILD_STARTED_MS="$(now_ms)"
rm -rf "$WORK_DIR" "$ARTIFACT_DIR"
mkdir -p "$WORK_DIR/extracted" "$ARTIFACT_DIR"
EXTRACT_STARTED_MS="$(now_ms)"
unzip -q "$SOURCE_ZIP" -d "$WORK_DIR/extracted"
chmod -R u+rwX,go+rX "$WORK_DIR/extracted"
EXTRACT_FINISHED_MS="$(now_ms)"
EXTRACT_DURATION_MS=$((EXTRACT_FINISHED_MS - EXTRACT_STARTED_MS))

mapfile -t PROJECT_ROOTS < <(
  while IFS= read -r wrapper; do
    root="$(dirname "$wrapper")"
    if [[ -f "$root/settings.gradle" || -f "$root/settings.gradle.kts" ]]; then
      printf '%s\n' "$root"
    fi
  done < <(find "$WORK_DIR/extracted" -type f -name gradlew -not -path '*/.gradle/*' -print | sort)
)
mapfile -t PROJECT_ROOTS < <(printf '%s\n' "${PROJECT_ROOTS[@]:-}" | sed '/^$/d' | sort -u)
[[ "${#PROJECT_ROOTS[@]}" -eq 1 ]] || {
  echo "Expected exactly one Android Gradle project root; found ${#PROJECT_ROOTS[@]}:" >&2
  printf ' - %s\n' "${PROJECT_ROOTS[@]:-none}" >&2
  exit 65
}
PROJECT_ROOT="${PROJECT_ROOTS[0]}"
chmod +x "$PROJECT_ROOT/gradlew"

SDK_DIR="${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}"
if [[ -n "$SDK_DIR" ]]; then
  printf 'sdk.dir=%s\n' "$SDK_DIR" > "$PROJECT_ROOT/local.properties"
fi

GRADLE_ARGS=(
  --no-daemon
  --stacktrace
  --build-cache
  --parallel
)

BUILD_LOG="$ARTIFACT_DIR/BUILD_LOG.txt"
GRADLE_STARTED_MS="$(now_ms)"
set +e
(
  cd "$PROJECT_ROOT"
  ./gradlew "${GRADLE_ARGS[@]}" "$GRADLE_TASK"
) 2>&1 | tee "$BUILD_LOG"
GRADLE_RC=${PIPESTATUS[0]}
set -e
GRADLE_FINISHED_MS="$(now_ms)"
GRADLE_DURATION_MS=$((GRADLE_FINISHED_MS - GRADLE_STARTED_MS))

write_timing() {
  local status="$1"
  local gradle_rc="$2"
  local total_ms="$3"
  local timing_json="$ARTIFACT_DIR/CI_TIMING.json"
  export COMPONENT CANONICAL_STEM VARIANT EXTRACT_DURATION_MS GRADLE_DURATION_MS SOURCE_HYDRATION_MS
  export SWRLZ_TIMING_STATUS="$status" SWRLZ_TIMING_GRADLE_RC="$gradle_rc" SWRLZ_TIMING_TOTAL_MS="$total_ms" SWRLZ_TIMING_JSON="$timing_json"
  python3 - <<'PY'
import json, os
from pathlib import Path
payload = {
    "schema": 2,
    "component": os.environ["COMPONENT"],
    "candidate": os.environ["CANONICAL_STEM"],
    "variant": os.environ["VARIANT"],
    "status": os.environ["SWRLZ_TIMING_STATUS"],
    "source_hydration_ms": int(os.environ["SOURCE_HYDRATION_MS"]),
    "extract_ms": int(os.environ["EXTRACT_DURATION_MS"]),
    "gradle_ms": int(os.environ["GRADLE_DURATION_MS"]),
    "gradle_exit_code": int(os.environ["SWRLZ_TIMING_GRADLE_RC"]),
    "build_helper_total_ms": int(os.environ["SWRLZ_TIMING_TOTAL_MS"]),
}
Path(os.environ["SWRLZ_TIMING_JSON"]).write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
PY
  sha256sum "$timing_json" > "$timing_json.sha256"
}

if [[ "$GRADLE_RC" -ne 0 ]]; then
  BUILD_FINISHED_MS="$(now_ms)"
  TOTAL_DURATION_MS=$((BUILD_FINISHED_MS - BUILD_STARTED_MS))
  write_timing failed "$GRADLE_RC" "$TOTAL_DURATION_MS"
  export COMPONENT CANONICAL_STEM VARIANT GRADLE_RC SOURCE_HYDRATION_MS EXTRACT_DURATION_MS GRADLE_DURATION_MS TOTAL_DURATION_MS ARTIFACT_DIR
  python3 - <<'PY'
import json, os
from pathlib import Path
payload = {
    "schema": 1,
    "component": os.environ["COMPONENT"],
    "candidate": os.environ["CANONICAL_STEM"],
    "variant": os.environ["VARIANT"],
    "gradle_exit_code": int(os.environ["GRADLE_RC"]),
    "source_hydration_ms": int(os.environ["SOURCE_HYDRATION_MS"]),
    "extract_ms": int(os.environ["EXTRACT_DURATION_MS"]),
    "gradle_ms": int(os.environ["GRADLE_DURATION_MS"]),
    "total_ms": int(os.environ["TOTAL_DURATION_MS"]),
}
target = Path(os.environ["ARTIFACT_DIR"]) / "BUILD_FAILURE.json"
target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY
  sha256sum "$ARTIFACT_DIR/BUILD_FAILURE.json" > "$ARTIFACT_DIR/BUILD_FAILURE.json.sha256"
  exit "$GRADLE_RC"
fi

mapfile -t APKS < <(
  find "$PROJECT_ROOT" -type f -path '*/build/outputs/apk/*' -name '*.apk' \
    ! -name '*aligned*.apk' ! -name '*stable-signed*.apk' -print 2>/dev/null | sort -u
)
[[ "${#APKS[@]}" -gt 0 ]] || { echo "Build completed without a discoverable APK." >&2; exit 65; }

EXPECTED="app-${VARIANT}.apk"
if [[ "${#APKS[@]}" -gt 1 ]]; then
  mapfile -t MATCHES < <(printf '%s\n' "${APKS[@]}" | awk -v expected="$EXPECTED" 'BEGIN{IGNORECASE=1} {n=split($0,a,"/"); if(a[n]==expected) print $0}')
  [[ "${#MATCHES[@]}" -eq 1 ]] || {
    echo "Expected one canonical APK; found ${#APKS[@]} candidates:" >&2
    printf ' - %s\n' "${APKS[@]}" >&2
    exit 65
  }
  APKS=("${MATCHES[0]}")
fi

FINAL_APK="$ARTIFACT_DIR/${CANONICAL_STEM}_${VARIANT^^}.apk"
install -m 0644 "${APKS[0]}" "$FINAL_APK"
sha256sum "$FINAL_APK" > "$FINAL_APK.sha256"

SOURCE_SHA="${SWRLZ_VERIFIED_SOURCE_SHA256:-}"
SOURCE_SHA_ORIGIN='resolver-verified'
if [[ -n "$SOURCE_SHA" ]]; then
  [[ "$SOURCE_SHA" =~ ^[0-9a-fA-F]{64}$ ]] || {
    echo 'SWRLZ_VERIFIED_SOURCE_SHA256 is not a valid SHA-256 digest.' >&2
    exit 65
  }
  SOURCE_SHA="${SOURCE_SHA,,}"
else
  SOURCE_SHA="$(sha256sum "$SOURCE_ZIP" | awk '{print $1}')"
  SOURCE_SHA_ORIGIN='builder-fallback-hash'
fi

BUILD_FINISHED_MS="$(now_ms)"
TOTAL_DURATION_MS=$((BUILD_FINISHED_MS - BUILD_STARTED_MS))
write_timing succeeded 0 "$TOTAL_DURATION_MS"

PROVENANCE="$ARTIFACT_DIR/BUILD_PROVENANCE_REPORT.md"
{
  echo '# SWRLZ APK Router Build Provenance'
  echo
  echo "- Status: succeeded"
  echo "- Component: $COMPONENT"
  echo "- Canonical source identity: $CANONICAL_STEM"
  echo "- Selected source path: $SOURCE_ZIP"
  echo "- Selected source SHA-256: $SOURCE_SHA"
  echo "- Selected source SHA origin: $SOURCE_SHA_ORIGIN"
  echo "- Build variant: $VARIANT"
  echo "- Gradle task: $GRADLE_TASK"
  echo "- Gradle build cache: enabled"
  echo "- Gradle parallel execution: enabled"
  echo "- Gradle clean task: omitted (fresh isolated extraction workspace)"
  echo "- Source hydration duration: ${SOURCE_HYDRATION_MS} ms"
  echo "- Source extraction duration: ${EXTRACT_DURATION_MS} ms"
  echo "- Gradle duration: ${GRADLE_DURATION_MS} ms"
  echo "- Build helper total duration: ${TOTAL_DURATION_MS} ms"
  echo "- Project root: $PROJECT_ROOT"
  echo "- Final APK: $(basename "$FINAL_APK")"
  echo "- Final APK SHA-256: $(sha256sum "$FINAL_APK" | awk '{print $1}')"
  echo "- Repository: ${GITHUB_REPOSITORY:-local}"
  echo "- Source commit: ${GITHUB_SHA:-local}"
  echo "- Workflow: ${GITHUB_WORKFLOW:-local}"
  echo "- Workflow run: ${GITHUB_RUN_ID:-local}"
  echo "- Generated UTC: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
} > "$PROVENANCE"
sha256sum "$PROVENANCE" > "$PROVENANCE.sha256"

if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  {
    echo "project_root=$PROJECT_ROOT"
    echo "artifact_dir=$ARTIFACT_DIR"
    echo "final_apk=$FINAL_APK"
    echo "gradle_task=$GRADLE_TASK"
    echo "source_hydration_ms=$SOURCE_HYDRATION_MS"
    echo "extract_ms=$EXTRACT_DURATION_MS"
    echo "gradle_ms=$GRADLE_DURATION_MS"
    echo "build_helper_total_ms=$TOTAL_DURATION_MS"
  } >> "$GITHUB_OUTPUT"
fi
''')

write('swrlz-core/tools/ci/test_build_swrlz_component.py', r'''#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPER = HERE / 'build_swrlz_component.sh'


def make_source(root: Path, gradlew: str, *, second_project: bool = False) -> Path:
    source = root / 'SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R999.zip'
    top = source.stem
    with zipfile.ZipFile(source, 'w') as archive:
        archive.writestr(f'{top}/settings.gradle.kts', "rootProject.name='fixture'\n")
        archive.writestr(f'{top}/gradlew', gradlew)
        if second_project:
            archive.writestr(f'{top}/nested/settings.gradle.kts', "rootProject.name='nested'\n")
            archive.writestr(f'{top}/nested/gradlew', '#!/usr/bin/env bash\nexit 0\n')
    return source


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BuildHelperTests(unittest.TestCase):
    def run_helper(self, source: Path, *, hydration: int):
        root = source.parent
        work = root / 'work'
        artifact = root / 'artifact'
        output = root / 'github-output.txt'
        env = os.environ.copy()
        env['SWRLZ_VERIFIED_SOURCE_SHA256'] = digest(source)
        env['SWRLZ_SOURCE_HYDRATION_MS'] = str(hydration)
        env['GITHUB_OUTPUT'] = str(output)
        result = subprocess.run(
            ['bash', str(HELPER), 'SERVER', str(source), source.stem, 'debug', str(work), str(artifact)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            check=False,
        )
        return result, artifact

    def test_success_records_hydration_and_apk(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_source(Path(temp), '''#!/usr/bin/env bash\nset -e\nmkdir -p app/build/outputs/apk/debug\nprintf apk > app/build/outputs/apk/debug/app-debug.apk\n''')
            result, artifact = self.run_helper(source, hydration=123)
            self.assertEqual(result.returncode, 0, result.stdout)
            timing = json.loads((artifact / 'CI_TIMING.json').read_text())
            self.assertEqual(timing['status'], 'succeeded')
            self.assertEqual(timing['source_hydration_ms'], 123)
            self.assertEqual(timing['gradle_exit_code'], 0)
            self.assertTrue(any(artifact.glob('*_DEBUG.apk')))

    def test_gradle_failure_preserves_log_and_timing(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_source(Path(temp), '#!/usr/bin/env bash\necho synthetic-gradle-failure\nexit 7\n')
            result, artifact = self.run_helper(source, hydration=321)
            self.assertEqual(result.returncode, 7, result.stdout)
            self.assertIn('synthetic-gradle-failure', (artifact / 'BUILD_LOG.txt').read_text())
            timing = json.loads((artifact / 'CI_TIMING.json').read_text())
            self.assertEqual(timing['status'], 'failed')
            self.assertEqual(timing['gradle_exit_code'], 7)
            self.assertEqual(timing['source_hydration_ms'], 321)
            self.assertTrue((artifact / 'BUILD_FAILURE.json').is_file())

    def test_multiple_android_roots_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_source(Path(temp), '#!/usr/bin/env bash\nexit 0\n', second_project=True)
            result, _ = self.run_helper(source, hydration=0)
            self.assertEqual(result.returncode, 65)
            self.assertIn('exactly one Android Gradle project root', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
''')

write('swrlz-core/tools/ci/test_workflow_phase5_contract.py', r'''#!/usr/bin/env python3
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / '.github/workflows'


class Phase5WorkflowContractTests(unittest.TestCase):
    def text(self, name: str) -> str:
        return (WORKFLOWS / name).read_text(encoding='utf-8')

    def test_active_workflows_use_pinned_runner_and_no_embedded_token_remote(self):
        for name in (
            'swrlz-apk-router.yml',
            'source-package-integrity.yml',
            'patch-note-accounting.yml',
            'swrlz-ci-tooling-validation.yml',
        ):
            text = self.text(name)
            self.assertNotIn('ubuntu-latest', text, name)
            self.assertNotIn('x-access-token:', text, name)

    def test_router_has_one_pass_hydration_and_no_accounting_gate(self):
        router = self.text('swrlz-apk-router.yml')
        self.assertIn('matrix.checkout_patterns', router)
        self.assertIn('Plan one-pass candidate hydration', router)
        self.assertIn('source_hydration_ms', router)
        self.assertNotIn('Check patch-note and lineage accounting', router)
        self.assertIn('FORGE_FAILURE_CONTEXT.json', router)

    def test_success_artifact_upload_precedes_best_effort_attestation(self):
        router = self.text('swrlz-apk-router.yml')
        upload = router.index('Upload canonical stable APK and provenance artifact')
        attest = router.index('Attest canonical stable APK provenance')
        self.assertLess(upload, attest)
        attest_tail = router[attest:]
        self.assertIn('continue-on-error: true', attest_tail)

    def test_integrity_uses_preplanned_exact_checkout(self):
        integrity = self.text('source-package-integrity.yml')
        self.assertIn('matrix.checkout_patterns', integrity)
        self.assertIn('Plan one-pass candidate hydration', integrity)

    def test_accounting_is_diagnostic_only(self):
        accounting = self.text('patch-note-accounting.yml')
        self.assertGreaterEqual(accounting.count('continue-on-error: true'), 2)
        self.assertIn('diagnostic only', accounting)

    def test_historical_r8_workflow_is_not_executable(self):
        self.assertFalse((WORKFLOWS / 'swrlz-server-r8-patch-build.yml').exists())
        self.assertTrue((ROOT / 'swrlz-core/history/workflows/swrlz-server-r8-patch-build.yml').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
''')

validation_path = '.github/workflows/swrlz-ci-tooling-validation.yml'
validation = read(validation_path).replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04')
validation = replace_once(
    validation,
    '            plan_swrlz_build_route.py \\\n            prepare_swrlz_sparse_checkout.py \\\n',
    '            plan_swrlz_build_route.py \\\n            plan_swrlz_candidate_checkout.py \\\n            prepare_swrlz_sparse_checkout.py \\\n',
    'validation compile candidate planner',
)
validation = replace_once(
    validation,
    '            test_plan_swrlz_build_route.py \\\n            test_prepare_swrlz_sparse_checkout.py \\\n',
    '            test_plan_swrlz_build_route.py \\\n            test_plan_swrlz_candidate_checkout.py \\\n            test_prepare_swrlz_sparse_checkout.py \\\n',
    'validation compile planner test',
)
validation = replace_once(
    validation,
    '            test_verify_swrlz_package_pair.py \\\n            test_verify_patch_note_accounting.py\n',
    '            test_verify_swrlz_package_pair.py \\\n            test_verify_patch_note_accounting.py \\\n            test_build_swrlz_component.py \\\n            test_workflow_phase5_contract.py\n',
    'validation compile phase5 tests',
)
validation = replace_once(
    validation,
    '          python3 test_plan_swrlz_build_route.py\n          python3 test_prepare_swrlz_sparse_checkout.py\n',
    '          python3 test_plan_swrlz_build_route.py\n          python3 test_plan_swrlz_candidate_checkout.py\n          python3 test_prepare_swrlz_sparse_checkout.py\n',
    'validation run candidate planner test',
)
validation = replace_once(
    validation,
    '          python3 test_verify_patch_note_accounting.py\n',
    '          python3 test_verify_patch_note_accounting.py\n          python3 test_build_swrlz_component.py\n          python3 test_workflow_phase5_contract.py\n',
    'validation run phase5 tests',
)
write(validation_path, validation)

print('Phase 5 archive/build-safety/failure-diagnostics patch applied.')
