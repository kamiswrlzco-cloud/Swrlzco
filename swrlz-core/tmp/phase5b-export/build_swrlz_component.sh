#!/usr/bin/env bash
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
GRADLE_SETUP_MS="${SWRLZ_GRADLE_SETUP_MS:-0}"
ANDROID_SDK_SETUP_MS="${SWRLZ_ANDROID_SDK_SETUP_MS:-0}"

case "$COMPONENT" in CLIENT|SERVER) ;; *) usage ;; esac
case "$VARIANT" in
  debug) GRADLE_TASK=':app:assembleDebug' ;;
  release) GRADLE_TASK=':app:assembleRelease' ;;
  *) usage ;;
esac
for timing_name in SOURCE_HYDRATION_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS; do
  timing_value="${!timing_name}"
  [[ "$timing_value" =~ ^[0-9]+$ ]] || {
    echo "$timing_name must be a non-negative integer." >&2
    exit 65
  }
done

SOURCE_ZIP="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$SOURCE_ZIP")"
WORK_DIR="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$WORK_DIR")"
ARTIFACT_DIR="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$ARTIFACT_DIR")"
[[ -f "$SOURCE_ZIP" ]] || { echo "Source ZIP not found: $SOURCE_ZIP" >&2; exit 66; }

BUILD_STARTED_MS="$(now_ms)"
rm -rf "$WORK_DIR" "$ARTIFACT_DIR"
mkdir -p "$WORK_DIR/extracted" "$ARTIFACT_DIR"
EXTRACT_STARTED_MS="$(now_ms)"
unzip -q "$SOURCE_ZIP" -d "$WORK_DIR/extracted"
# Source packages are already topology-validated before this helper runs. Repair
# traversal on directories first, then only touch regular files that are actually
# unreadable instead of chmod-ing every source/resource file on every build.
find "$WORK_DIR/extracted" -type d -exec chmod u+rwx,go+rx {} +
find "$WORK_DIR/extracted" -type f ! -readable -exec chmod u+rw,go+r {} +
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
  --no-watch-fs
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
  export COMPONENT CANONICAL_STEM VARIANT EXTRACT_DURATION_MS GRADLE_DURATION_MS SOURCE_HYDRATION_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS
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
    "gradle_setup_ms": int(os.environ["GRADLE_SETUP_MS"]),
    "android_sdk_setup_ms": int(os.environ["ANDROID_SDK_SETUP_MS"]),
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
    "gradle_setup_ms": int(os.environ["GRADLE_SETUP_MS"]),
    "android_sdk_setup_ms": int(os.environ["ANDROID_SDK_SETUP_MS"]),
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

EXPECTED_APK_DIR="$PROJECT_ROOT/app/build/outputs/apk/$VARIANT"
APKS=()
if [[ -d "$EXPECTED_APK_DIR" ]]; then
  mapfile -t APKS < <(
    find "$EXPECTED_APK_DIR" -maxdepth 1 -type f -name '*.apk' \
      ! -name '*aligned*.apk' ! -name '*stable-signed*.apk' -print 2>/dev/null | sort -u
  )
fi
if [[ "${#APKS[@]}" -eq 0 ]]; then
  echo '::notice::Expected app APK directory was empty; using compatibility-wide APK discovery.'
  mapfile -t APKS < <(
    find "$PROJECT_ROOT" -type f -path '*/build/outputs/apk/*' -name '*.apk' \
      ! -name '*aligned*.apk' ! -name '*stable-signed*.apk' -print 2>/dev/null | sort -u
  )
fi
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
  echo "- Gradle filesystem watching: disabled (ephemeral extracted workspace)"
  echo "- Gradle clean task: omitted (fresh isolated extraction workspace)"
  echo "- Source hydration duration: ${SOURCE_HYDRATION_MS} ms"
  echo "- Gradle wrapper/cache setup duration: ${GRADLE_SETUP_MS} ms"
  echo "- Android SDK tooling duration: ${ANDROID_SDK_SETUP_MS} ms"
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
    echo "gradle_setup_ms=$GRADLE_SETUP_MS"
    echo "android_sdk_setup_ms=$ANDROID_SDK_SETUP_MS"
    echo "extract_ms=$EXTRACT_DURATION_MS"
    echo "gradle_ms=$GRADLE_DURATION_MS"
    echo "build_helper_total_ms=$TOTAL_DURATION_MS"
  } >> "$GITHUB_OUTPUT"
fi
