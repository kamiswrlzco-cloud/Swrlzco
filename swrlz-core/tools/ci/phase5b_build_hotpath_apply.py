#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one marker, found {count}')
    path.write_text(text.replace(old, new, 1), encoding='utf-8')


router = ROOT / '.github/workflows/swrlz-apk-router.yml'
validation = ROOT / '.github/workflows/swrlz-ci-tooling-validation.yml'
helper = ROOT / 'swrlz-core/tools/ci/build_swrlz_component.sh'
helper_test = ROOT / 'swrlz-core/tools/ci/test_build_swrlz_component.py'
contract_test = ROOT / 'swrlz-core/tools/ci/test_workflow_phase5_contract.py'

# Gradle cache setup: move to current v6.3.0 implementation and measure restore/setup cost.
replace_once(
    router,
    """      - name: Set up Gradle wrapper cache
        id: setup-gradle
        uses: gradle/actions/setup-gradle@0723195856401067f7a2779048b490ace7a47d7c # v5

      - name: Set up Android SDK tooling
        id: setup-android
        uses: android-actions/setup-android@40fd30fb8d7440372e1316f5d1809ec01dcd3699 # v4
        with:
          packages: ''
""",
    """      - name: Start Gradle wrapper/cache timer
        run: echo \"SWRLZ_GRADLE_SETUP_STARTED_MS=$(date +%s%3N)\" >> \"$GITHUB_ENV\"

      - name: Set up Gradle wrapper cache
        id: setup-gradle
        uses: gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb # v6.3.0
        with:
          cache-cleanup: on-success

      - name: Record Gradle wrapper/cache timing
        id: gradle-setup-timing
        run: |
          set -euo pipefail
          END_MS=\"$(date +%s%3N)\"
          ELAPSED_MS=$((END_MS - SWRLZ_GRADLE_SETUP_STARTED_MS))
          echo \"gradle_setup_ms=$ELAPSED_MS\" >> \"$GITHUB_OUTPUT\"
          echo \"Gradle wrapper/cache setup: ${ELAPSED_MS} ms\" >> \"$GITHUB_STEP_SUMMARY\"

      - name: Start Android SDK tooling timer
        run: echo \"SWRLZ_ANDROID_SDK_STARTED_MS=$(date +%s%3N)\" >> \"$GITHUB_ENV\"

      - name: Inspect preinstalled Android SDK
        id: android-sdk-preflight
        run: |
          set -euo pipefail
          SDK_DIR=\"${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}\"
          FALLBACK_REQUIRED=false
          if [[ -z \"$SDK_DIR\" || ! -d \"$SDK_DIR\" ]]; then
            FALLBACK_REQUIRED=true
          else
            APKSIGNER=\"$(find \"$SDK_DIR/build-tools\" -mindepth 2 -maxdepth 2 -type f -name apksigner -print 2>/dev/null | sort -V | tail -n 1 || true)\"
            ZIPALIGN=\"$(find \"$SDK_DIR/build-tools\" -mindepth 2 -maxdepth 2 -type f -name zipalign -print 2>/dev/null | sort -V | tail -n 1 || true)\"
            [[ -n \"$APKSIGNER\" && -x \"$APKSIGNER\" && -n \"$ZIPALIGN\" && -x \"$ZIPALIGN\" ]] || FALLBACK_REQUIRED=true
          fi
          echo \"fallback_required=$FALLBACK_REQUIRED\" >> \"$GITHUB_OUTPUT\"
          if [[ \"$FALLBACK_REQUIRED\" == 'false' ]]; then
            echo 'Android SDK fast path: using tools already present on the pinned Ubuntu 24.04 runner.'
          else
            echo '::notice::Pinned runner Android SDK is incomplete; invoking the setup-android fallback.'
          fi

      - name: Set up Android SDK tooling fallback
        if: steps.android-sdk-preflight.outputs.fallback_required == 'true'
        uses: android-actions/setup-android@40fd30fb8d7440372e1316f5d1809ec01dcd3699 # v4
        with:
          packages: 'platform-tools build-tools;35.0.0'

      - name: Validate Android SDK tooling
        id: android-sdk
        run: |
          set -euo pipefail
          SDK_DIR=\"${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}\"
          [[ -n \"$SDK_DIR\" && -d \"$SDK_DIR\" ]] || {
            echo 'Android SDK root is unavailable after preflight/fallback.' >&2
            exit 1
          }
          APKSIGNER=\"$(find \"$SDK_DIR/build-tools\" -mindepth 2 -maxdepth 2 -type f -name apksigner -print 2>/dev/null | sort -V | tail -n 1 || true)\"
          ZIPALIGN=\"$(find \"$SDK_DIR/build-tools\" -mindepth 2 -maxdepth 2 -type f -name zipalign -print 2>/dev/null | sort -V | tail -n 1 || true)\"
          [[ -n \"$APKSIGNER\" && -x \"$APKSIGNER\" ]] || { echo 'apksigner not found in Android build-tools.' >&2; exit 1; }
          [[ -n \"$ZIPALIGN\" && -x \"$ZIPALIGN\" ]] || { echo 'zipalign not found in Android build-tools.' >&2; exit 1; }
          END_MS=\"$(date +%s%3N)\"
          ELAPSED_MS=$((END_MS - SWRLZ_ANDROID_SDK_STARTED_MS))
          {
            echo \"sdk_dir=$SDK_DIR\"
            echo \"apksigner=$APKSIGNER\"
            echo \"zipalign=$ZIPALIGN\"
            echo \"android_sdk_setup_ms=$ELAPSED_MS\"
          } >> \"$GITHUB_OUTPUT\"
          {
            echo \"Android SDK tooling: ${ELAPSED_MS} ms\"
            echo \"Android SDK root: \\`$SDK_DIR\\`\"
            echo \"Android SDK fallback used: \\`${{ steps.android-sdk-preflight.outputs.fallback_required }}\\`\"
          } >> \"$GITHUB_STEP_SUMMARY\"
""",
    'router Gradle/Android setup block',
)

replace_once(
    router,
    """          SWRLZ_VERIFIED_SOURCE_SHA256: ${{ steps.resolve.outputs.source_sha256 }}
          SWRLZ_SOURCE_HYDRATION_MS: ${{ steps.hydration.outputs.source_hydration_ms }}
          SWRLZ_BUILD_WORK_DIR: ${{ runner.temp }}/swrlz-build/router
""",
    """          SWRLZ_VERIFIED_SOURCE_SHA256: ${{ steps.resolve.outputs.source_sha256 }}
          SWRLZ_SOURCE_HYDRATION_MS: ${{ steps.hydration.outputs.source_hydration_ms }}
          SWRLZ_GRADLE_SETUP_MS: ${{ steps.gradle-setup-timing.outputs.gradle_setup_ms }}
          SWRLZ_ANDROID_SDK_SETUP_MS: ${{ steps.android-sdk.outputs.android_sdk_setup_ms }}
          SWRLZ_BUILD_WORK_DIR: ${{ runner.temp }}/swrlz-build/router
""",
    'router build timing env',
)

replace_once(
    router,
    """          SWRLZ_DEV_KEYSTORE_PASSWORD: ${{ secrets.SWRLZ_DEV_KEYSTORE_PASSWORD }}
          SWRLZ_DEV_KEY_ALIAS: ${{ secrets.SWRLZ_DEV_KEY_ALIAS }}
        run: |
""",
    """          SWRLZ_DEV_KEYSTORE_PASSWORD: ${{ secrets.SWRLZ_DEV_KEYSTORE_PASSWORD }}
          SWRLZ_DEV_KEY_ALIAS: ${{ secrets.SWRLZ_DEV_KEY_ALIAS }}
          APKSIGNER: ${{ steps.android-sdk.outputs.apksigner }}
          ZIPALIGN: ${{ steps.android-sdk.outputs.zipalign }}
        run: |
""",
    'router signing tool env',
)

replace_once(
    router,
    """          APKSIGNER=\"$(find \"${ANDROID_HOME:-$HOME}\" -type f -name apksigner -print 2>/dev/null | sort -V | tail -n 1 || true)\"
          ZIPALIGN=\"$(find \"${ANDROID_HOME:-$HOME}\" -type f -name zipalign -print 2>/dev/null | sort -V | tail -n 1 || true)\"
          [[ -n \"$APKSIGNER\" && -n \"$ZIPALIGN\" ]] || {
            echo 'apksigner/zipalign not found.' >&2
            exit 1
          }
""",
    """          [[ -n \"$APKSIGNER\" && -x \"$APKSIGNER\" && -n \"$ZIPALIGN\" && -x \"$ZIPALIGN\" ]] || {
            echo 'Validated apksigner/zipalign paths are unavailable.' >&2
            exit 1
          }
""",
    'router duplicate SDK scan',
)

replace_once(
    router,
    """            echo \"- Source hydration: `${{ steps.hydration.outputs.source_hydration_ms }} ms`\"
            echo \"- Source extraction: \\`${{ steps.build.outputs.extract_ms }} ms\\`\"
            echo \"- Gradle execution: \\`${{ steps.build.outputs.gradle_ms }} ms\\`\"
""",
    """            echo \"- Source hydration: `${{ steps.hydration.outputs.source_hydration_ms }} ms`\"
            echo \"- Gradle wrapper/cache setup: \\`${{ steps.gradle-setup-timing.outputs.gradle_setup_ms }} ms\\`\"
            echo \"- Android SDK tooling: \\`${{ steps.android-sdk.outputs.android_sdk_setup_ms }} ms\\`\"
            echo \"- Source extraction: \\`${{ steps.build.outputs.extract_ms }} ms\\`\"
            echo \"- Gradle execution: \\`${{ steps.build.outputs.gradle_ms }} ms\\`\"
""",
    'router timing summary',
)

# Build helper: account for tool setup, make ephemeral-workspace intent explicit, and avoid broad APK search on the common path.
replace_once(
    helper,
    """SOURCE_HYDRATION_MS=\"${SWRLZ_SOURCE_HYDRATION_MS:-0}\"

case \"$COMPONENT\" in CLIENT|SERVER) ;; *) usage ;; esac
""",
    """SOURCE_HYDRATION_MS=\"${SWRLZ_SOURCE_HYDRATION_MS:-0}\"
GRADLE_SETUP_MS=\"${SWRLZ_GRADLE_SETUP_MS:-0}\"
ANDROID_SDK_SETUP_MS=\"${SWRLZ_ANDROID_SDK_SETUP_MS:-0}\"

case \"$COMPONENT\" in CLIENT|SERVER) ;; *) usage ;; esac
""",
    'helper setup timing vars',
)

replace_once(
    helper,
    """[[ \"$SOURCE_HYDRATION_MS\" =~ ^[0-9]+$ ]] || {
  echo 'SWRLZ_SOURCE_HYDRATION_MS must be a non-negative integer.' >&2
  exit 65
}
""",
    """for timing_name in SOURCE_HYDRATION_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS; do
  timing_value=\"${!timing_name}\"
  [[ \"$timing_value\" =~ ^[0-9]+$ ]] || {
    echo \"$timing_name must be a non-negative integer.\" >&2
    exit 65
  }
done
""",
    'helper timing validation',
)

replace_once(
    helper,
    """unzip -q \"$SOURCE_ZIP\" -d \"$WORK_DIR/extracted\"
chmod -R u+rwX,go+rX \"$WORK_DIR/extracted\"
EXTRACT_FINISHED_MS=\"$(now_ms)\"
""",
    """unzip -q \"$SOURCE_ZIP\" -d \"$WORK_DIR/extracted\"
# Source packages are already topology-validated before this helper runs. Repair
# traversal on directories first, then only touch regular files that are actually
# unreadable instead of chmod-ing every source/resource file on every build.
find \"$WORK_DIR/extracted\" -type d -exec chmod u+rwx,go+rx {} +
find \"$WORK_DIR/extracted\" -type f ! -readable -exec chmod u+rw,go+r {} +
EXTRACT_FINISHED_MS=\"$(now_ms)\"
""",
    'helper permission normalization',
)

replace_once(
    helper,
    """GRADLE_ARGS=(
  --no-daemon
  --stacktrace
  --build-cache
  --parallel
)
""",
    """GRADLE_ARGS=(
  --no-daemon
  --stacktrace
  --build-cache
  --parallel
  --no-watch-fs
)
""",
    'helper Gradle args',
)

replace_once(
    helper,
    """  export COMPONENT CANONICAL_STEM VARIANT EXTRACT_DURATION_MS GRADLE_DURATION_MS SOURCE_HYDRATION_MS
""",
    """  export COMPONENT CANONICAL_STEM VARIANT EXTRACT_DURATION_MS GRADLE_DURATION_MS SOURCE_HYDRATION_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS
""",
    'helper timing export',
)

replace_once(
    helper,
    """    \"source_hydration_ms\": int(os.environ[\"SOURCE_HYDRATION_MS\"]),
    \"extract_ms\": int(os.environ[\"EXTRACT_DURATION_MS\"]),
""",
    """    \"source_hydration_ms\": int(os.environ[\"SOURCE_HYDRATION_MS\"]),
    \"gradle_setup_ms\": int(os.environ[\"GRADLE_SETUP_MS\"]),
    \"android_sdk_setup_ms\": int(os.environ[\"ANDROID_SDK_SETUP_MS\"]),
    \"extract_ms\": int(os.environ[\"EXTRACT_DURATION_MS\"]),
""",
    'helper timing JSON setup fields',
)

# BUILD_FAILURE has its own timing payload; add setup fields there too.
text = helper.read_text(encoding='utf-8')
needle = '    "source_hydration_ms": int(os.environ["SOURCE_HYDRATION_MS"]),\n    "extract_ms": int(os.environ["EXTRACT_DURATION_MS"]),\n'
if text.count(needle) != 1:
    raise SystemExit(f'helper failure timing fields: expected one remaining marker, found {text.count(needle)}')
helper.write_text(text.replace(needle, '    "source_hydration_ms": int(os.environ["SOURCE_HYDRATION_MS"]),\n    "gradle_setup_ms": int(os.environ["GRADLE_SETUP_MS"]),\n    "android_sdk_setup_ms": int(os.environ["ANDROID_SDK_SETUP_MS"]),\n    "extract_ms": int(os.environ["EXTRACT_DURATION_MS"]),\n', 1), encoding='utf-8')

replace_once(
    helper,
    """mapfile -t APKS < <(
  find \"$PROJECT_ROOT\" -type f -path '*/build/outputs/apk/*' -name '*.apk' \\
    ! -name '*aligned*.apk' ! -name '*stable-signed*.apk' -print 2>/dev/null | sort -u
)
[[ \"${#APKS[@]}\" -gt 0 ]] || { echo \"Build completed without a discoverable APK.\" >&2; exit 65; }
""",
    """EXPECTED_APK_DIR=\"$PROJECT_ROOT/app/build/outputs/apk/$VARIANT\"
APKS=()
if [[ -d \"$EXPECTED_APK_DIR\" ]]; then
  mapfile -t APKS < <(
    find \"$EXPECTED_APK_DIR\" -maxdepth 1 -type f -name '*.apk' \\
      ! -name '*aligned*.apk' ! -name '*stable-signed*.apk' -print 2>/dev/null | sort -u
  )
fi
if [[ \"${#APKS[@]}\" -eq 0 ]]; then
  echo '::notice::Expected app APK directory was empty; using compatibility-wide APK discovery.'
  mapfile -t APKS < <(
    find \"$PROJECT_ROOT\" -type f -path '*/build/outputs/apk/*' -name '*.apk' \\
      ! -name '*aligned*.apk' ! -name '*stable-signed*.apk' -print 2>/dev/null | sort -u
  )
fi
[[ \"${#APKS[@]}\" -gt 0 ]] || { echo \"Build completed without a discoverable APK.\" >&2; exit 65; }
""",
    'helper APK discovery',
)

replace_once(
    helper,
    """  echo \"- Gradle build cache: enabled\"
  echo \"- Gradle parallel execution: enabled\"
  echo \"- Gradle clean task: omitted (fresh isolated extraction workspace)\"
  echo \"- Source hydration duration: ${SOURCE_HYDRATION_MS} ms\"
""",
    """  echo \"- Gradle build cache: enabled\"
  echo \"- Gradle parallel execution: enabled\"
  echo \"- Gradle filesystem watching: disabled (ephemeral extracted workspace)\"
  echo \"- Gradle clean task: omitted (fresh isolated extraction workspace)\"
  echo \"- Source hydration duration: ${SOURCE_HYDRATION_MS} ms\"
  echo \"- Gradle wrapper/cache setup duration: ${GRADLE_SETUP_MS} ms\"
  echo \"- Android SDK tooling duration: ${ANDROID_SDK_SETUP_MS} ms\"
""",
    'helper provenance setup timing',
)

replace_once(
    helper,
    """    echo \"source_hydration_ms=$SOURCE_HYDRATION_MS\"
    echo \"extract_ms=$EXTRACT_DURATION_MS\"
""",
    """    echo \"source_hydration_ms=$SOURCE_HYDRATION_MS\"
    echo \"gradle_setup_ms=$GRADLE_SETUP_MS\"
    echo \"android_sdk_setup_ms=$ANDROID_SDK_SETUP_MS\"
    echo \"extract_ms=$EXTRACT_DURATION_MS\"
""",
    'helper GitHub outputs setup timing',
)

# Build-helper tests carry tool setup timing through success and failure evidence.
replace_once(
    helper_test,
    """        env['SWRLZ_SOURCE_HYDRATION_MS'] = str(hydration)
        env['GITHUB_OUTPUT'] = str(output)
""",
    """        env['SWRLZ_SOURCE_HYDRATION_MS'] = str(hydration)
        env['SWRLZ_GRADLE_SETUP_MS'] = '45'
        env['SWRLZ_ANDROID_SDK_SETUP_MS'] = '67'
        env['GITHUB_OUTPUT'] = str(output)
""",
    'helper test timing env',
)

replace_once(
    helper_test,
    """            self.assertEqual(timing['source_hydration_ms'], 123)
            self.assertEqual(timing['gradle_exit_code'], 0)
""",
    """            self.assertEqual(timing['source_hydration_ms'], 123)
            self.assertEqual(timing['gradle_setup_ms'], 45)
            self.assertEqual(timing['android_sdk_setup_ms'], 67)
            self.assertEqual(timing['gradle_exit_code'], 0)
""",
    'helper success timing assertions',
)

replace_once(
    helper_test,
    """            self.assertEqual(timing['source_hydration_ms'], 321)
            self.assertTrue((artifact / 'BUILD_FAILURE.json').is_file())
""",
    """            self.assertEqual(timing['source_hydration_ms'], 321)
            self.assertEqual(timing['gradle_setup_ms'], 45)
            self.assertEqual(timing['android_sdk_setup_ms'], 67)
            failure = json.loads((artifact / 'BUILD_FAILURE.json').read_text())
            self.assertEqual(failure['gradle_setup_ms'], 45)
            self.assertEqual(failure['android_sdk_setup_ms'], 67)
            self.assertTrue((artifact / 'BUILD_FAILURE.json').is_file())
""",
    'helper failure timing assertions',
)

insert = """
    def test_ephemeral_gradle_flags_are_present(self):
        text = HELPER.read_text(encoding='utf-8')
        self.assertIn('--no-watch-fs', text)
        self.assertIn('--build-cache', text)
        self.assertNotIn('--configuration-cache', text)

"""
replace_once(
    helper_test,
    """    def test_multiple_android_roots_fail_closed(self):
""",
    insert + """    def test_multiple_android_roots_fail_closed(self):
""",
    'helper Gradle flag test insertion',
)

# Normal CI validator must hydrate the workflow/history files its Phase5 contract tests inspect.
replace_once(
    validation,
    """          sparse-checkout: |
            swrlz-core/tools/ci
            swrlz-core/requests
""",
    """          sparse-checkout: |
            .github/workflows
            swrlz-core/tools/ci
            swrlz-core/requests
            swrlz-core/history
""",
    'validation sparse checkout scope',
)

replace_once(
    validation,
    """      - name: Smoke test Gradle wrapper cache action
        uses: gradle/actions/setup-gradle@0723195856401067f7a2779048b490ace7a47d7c # v5

      - name: Smoke test Android SDK action
        uses: android-actions/setup-android@40fd30fb8d7440372e1316f5d1809ec01dcd3699 # v4
        with:
          packages: ''

      - name: Verify toolchain availability
        run: |
          set -euo pipefail
          java -version
          sdkmanager --version
          command -v keytool
""",
    """      - name: Smoke test Gradle wrapper cache action
        uses: gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb # v6.3.0
        with:
          cache-cleanup: on-success

      - name: Smoke test preinstalled Android SDK fast path
        run: |
          set -euo pipefail
          SDK_DIR=\"${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}\"
          [[ -n \"$SDK_DIR\" && -d \"$SDK_DIR\" ]]
          APKSIGNER=\"$(find \"$SDK_DIR/build-tools\" -mindepth 2 -maxdepth 2 -type f -name apksigner -print 2>/dev/null | sort -V | tail -n 1)\"
          ZIPALIGN=\"$(find \"$SDK_DIR/build-tools\" -mindepth 2 -maxdepth 2 -type f -name zipalign -print 2>/dev/null | sort -V | tail -n 1)\"
          [[ -x \"$APKSIGNER\" && -x \"$ZIPALIGN\" ]]
          printf 'Android fast path: %s / %s\n' \"$APKSIGNER\" \"$ZIPALIGN\"

      - name: Verify toolchain availability
        run: |
          set -euo pipefail
          java -version
          command -v keytool
""",
    'validation Gradle/Android smoke stack',
)

# Contract tests lock the new hot-path invariants in place.
replace_once(
    contract_test,
    """        self.assertIn('FORGE_FAILURE_CONTEXT.json', router)
""",
    """        self.assertIn('FORGE_FAILURE_CONTEXT.json', router)
        self.assertIn('gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb', router)
        self.assertIn('Inspect preinstalled Android SDK', router)
        self.assertIn("if: steps.android-sdk-preflight.outputs.fallback_required == 'true'", router)
        self.assertIn('android_sdk_setup_ms', router)
        self.assertIn('APKSIGNER: ${{ steps.android-sdk.outputs.apksigner }}', router)
        self.assertNotIn('find "${ANDROID_HOME:-$HOME}" -type f -name apksigner', router)
""",
    'workflow contract hotpath assertions',
)

insert_contract = """
    def test_tooling_validator_hydrates_contract_inputs_and_smokes_fast_path(self):
        validation = self.text('swrlz-ci-tooling-validation.yml')
        self.assertIn('.github/workflows', validation)
        self.assertIn('swrlz-core/history', validation)
        self.assertIn('gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb', validation)
        self.assertIn('Smoke test preinstalled Android SDK fast path', validation)

"""
replace_once(
    contract_test,
    """    def test_success_artifact_upload_precedes_best_effort_attestation(self):
""",
    insert_contract + """    def test_success_artifact_upload_precedes_best_effort_attestation(self):
""",
    'workflow validation contract insertion',
)

print('Phase 5B Gradle/Android/build hotpath patch applied.')
