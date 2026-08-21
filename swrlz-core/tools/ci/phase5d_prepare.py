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
replace_once(
    router,
    """      - name: Set up Java 17\n        id: setup-java\n        uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5\n        with:\n          distribution: temurin\n          java-version: '17'\n          check-latest: false\n""",
    """      - name: Start Java 17 tooling timer\n        run: echo \"SWRLZ_JAVA_SETUP_STARTED_MS=$(date +%s%3N)\" >> \"$GITHUB_ENV\"\n\n      - name: Validate preinstalled Java 17\n        id: java\n        run: |\n          set -euo pipefail\n          JDK_DIR=\"${JAVA_HOME_17_X64:-}\"\n          [[ -n \"$JDK_DIR\" && -x \"$JDK_DIR/bin/java\" && -x \"$JDK_DIR/bin/javac\" && -x \"$JDK_DIR/bin/keytool\" ]] || {\n            echo 'Pinned Ubuntu 24.04 runner does not expose a complete JAVA_HOME_17_X64 toolchain.' >&2\n            exit 1\n          }\n          SPEC=\"$(\"$JDK_DIR/bin/java\" -XshowSettings:properties -version 2>&1 | awk -F'= ' '/java.specification.version/{print $2; exit}')\"\n          [[ \"$SPEC\" == '17' ]] || {\n            echo \"Expected Java 17, found specification version: ${SPEC:-unknown}\" >&2\n            exit 1\n          }\n          echo \"JAVA_HOME=$JDK_DIR\" >> \"$GITHUB_ENV\"\n          echo \"$JDK_DIR/bin\" >> \"$GITHUB_PATH\"\n          END_MS=\"$(date +%s%3N)\"\n          ELAPSED_MS=$((END_MS - SWRLZ_JAVA_SETUP_STARTED_MS))\n          echo \"java_setup_ms=$ELAPSED_MS\" >> \"$GITHUB_OUTPUT\"\n          echo \"Java 17 tooling: ${ELAPSED_MS} ms · preinstalled pinned-runner fast path\" >> \"$GITHUB_STEP_SUMMARY\"\n""",
    'router Java fast path',
)
replace_once(
    router,
    """      - name: Set up Android SDK tooling fallback\n        if: steps.android-sdk-preflight.outputs.fallback_required == 'true'\n        uses: android-actions/setup-android@40fd30fb8d7440372e1316f5d1809ec01dcd3699 # v4\n""",
    """      - name: Set up Android SDK tooling fallback\n        id: setup-android\n        if: steps.android-sdk-preflight.outputs.fallback_required == 'true'\n        uses: android-actions/setup-android@40fd30fb8d7440372e1316f5d1809ec01dcd3699 # v4\n""",
    'router Android fallback id',
)
replace_once(
    router,
    """          SWRLZ_SOURCE_HYDRATION_MS: ${{ steps.hydration.outputs.source_hydration_ms }}\n          SWRLZ_GRADLE_SETUP_MS: ${{ steps.gradle-setup-timing.outputs.gradle_setup_ms }}\n""",
    """          SWRLZ_SOURCE_HYDRATION_MS: ${{ steps.hydration.outputs.source_hydration_ms }}\n          SWRLZ_JAVA_SETUP_MS: ${{ steps.java.outputs.java_setup_ms }}\n          SWRLZ_GRADLE_SETUP_MS: ${{ steps.gradle-setup-timing.outputs.gradle_setup_ms }}\n""",
    'router Java timing env',
)
replace_once(
    router,
    """            echo \"- Source hydration: `${{ steps.hydration.outputs.source_hydration_ms }} ms`\"\n            echo \"- Gradle wrapper/cache setup: \\`${{ steps.gradle-setup-timing.outputs.gradle_setup_ms }} ms\\`\"\n""",
    """            echo \"- Source hydration: `${{ steps.hydration.outputs.source_hydration_ms }} ms`\"\n            echo \"- Java 17 tooling: \\`${{ steps.java.outputs.java_setup_ms }} ms\\`\"\n            echo \"- Gradle wrapper/cache setup: \\`${{ steps.gradle-setup-timing.outputs.gradle_setup_ms }} ms\\`\"\n""",
    'router Java provenance summary',
)
replace_once(
    router,
    """          JAVA_OUTCOME: ${{ steps.setup-java.outcome }}\n""",
    """          JAVA_OUTCOME: ${{ steps.java.outcome }}\n""",
    'router Java failure outcome',
)
replace_once(
    router,
    """          ref: ${{ github.ref_name }}\n          fetch-depth: 1\n          filter: blob:none\n          sparse-checkout: |\n            swrlz-core/releases\n""",
    """          ref: ${{ github.ref_name }}\n          fetch-depth: 2\n          filter: blob:none\n          sparse-checkout: |\n            swrlz-core/releases\n""",
    'release checkout depth',
)
replace_once(
    router,
    """          git commit -m \"build(${COMPONENT,,}): add ${CANONICAL_STEM} APK artifacts\"\n          git push origin \"HEAD:${GITHUB_REF_NAME}\"\n""",
    """          git commit -m \"build(${COMPONENT,,}): add ${CANONICAL_STEM} APK artifacts\"\n\n          # A source or sibling-component release commit may land while this job is\n          # packaging. Rebase the release-only commit onto the newest branch tip and\n          # retry a bounded number of times instead of failing a valid APK publication\n          # on a harmless non-fast-forward race.\n          for attempt in 1 2 3; do\n            git fetch --no-tags origin \"$GITHUB_REF_NAME\"\n            if ! git rebase \"origin/$GITHUB_REF_NAME\"; then\n              git rebase --abort >/dev/null 2>&1 || true\n              echo 'Release-only commit conflicted while rebasing; refusing to overwrite newer repository state.' >&2\n              exit 1\n            fi\n            if git push origin \"HEAD:${GITHUB_REF_NAME}\"; then\n              exit 0\n            fi\n            if [[ \"$attempt\" -eq 3 ]]; then\n              echo 'Release publication remained non-fast-forward after 3 attempts.' >&2\n              exit 1\n            fi\n            sleep $((attempt * 2))\n          done\n""",
    'release bounded rebase retry',
)

helper = ROOT / 'swrlz-core/tools/ci/build_swrlz_component.sh'
replace_once(
    helper,
    """SOURCE_HYDRATION_MS=\"${SWRLZ_SOURCE_HYDRATION_MS:-0}\"\nGRADLE_SETUP_MS=\"${SWRLZ_GRADLE_SETUP_MS:-0}\"\nANDROID_SDK_SETUP_MS=\"${SWRLZ_ANDROID_SDK_SETUP_MS:-0}\"\n""",
    """SOURCE_HYDRATION_MS=\"${SWRLZ_SOURCE_HYDRATION_MS:-0}\"\nJAVA_SETUP_MS=\"${SWRLZ_JAVA_SETUP_MS:-0}\"\nGRADLE_SETUP_MS=\"${SWRLZ_GRADLE_SETUP_MS:-0}\"\nANDROID_SDK_SETUP_MS=\"${SWRLZ_ANDROID_SDK_SETUP_MS:-0}\"\n""",
    'helper Java timing input',
)
replace_once(
    helper,
    """for timing_name in SOURCE_HYDRATION_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS; do\n""",
    """for timing_name in SOURCE_HYDRATION_MS JAVA_SETUP_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS; do\n""",
    'helper Java timing validation',
)
replace_once(
    helper,
    """  export COMPONENT CANONICAL_STEM VARIANT EXTRACT_DURATION_MS GRADLE_DURATION_MS SOURCE_HYDRATION_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS\n""",
    """  export COMPONENT CANONICAL_STEM VARIANT EXTRACT_DURATION_MS GRADLE_DURATION_MS SOURCE_HYDRATION_MS JAVA_SETUP_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS\n""",
    'helper Java timing export',
)
replace_once(
    helper,
    """    \"source_hydration_ms\": int(os.environ[\"SOURCE_HYDRATION_MS\"]),\n    \"gradle_setup_ms\": int(os.environ[\"GRADLE_SETUP_MS\"]),\n""",
    """    \"source_hydration_ms\": int(os.environ[\"SOURCE_HYDRATION_MS\"]),\n    \"java_setup_ms\": int(os.environ[\"JAVA_SETUP_MS\"]),\n    \"gradle_setup_ms\": int(os.environ[\"GRADLE_SETUP_MS\"]),\n""",
    'helper timing JSON Java field',
)
replace_once(
    helper,
    """  export COMPONENT CANONICAL_STEM VARIANT GRADLE_RC SOURCE_HYDRATION_MS EXTRACT_DURATION_MS GRADLE_DURATION_MS TOTAL_DURATION_MS ARTIFACT_DIR\n""",
    """  export COMPONENT CANONICAL_STEM VARIANT GRADLE_RC SOURCE_HYDRATION_MS JAVA_SETUP_MS GRADLE_SETUP_MS ANDROID_SDK_SETUP_MS EXTRACT_DURATION_MS GRADLE_DURATION_MS TOTAL_DURATION_MS ARTIFACT_DIR\n""",
    'helper failure timing export',
)
# The failure payload uses the same setup-field sequence as the primary timing payload.
text = helper.read_text(encoding='utf-8')
old = '    "source_hydration_ms": int(os.environ["SOURCE_HYDRATION_MS"]),\n    "gradle_setup_ms": int(os.environ["GRADLE_SETUP_MS"]),\n'
new = '    "source_hydration_ms": int(os.environ["SOURCE_HYDRATION_MS"]),\n    "java_setup_ms": int(os.environ["JAVA_SETUP_MS"]),\n    "gradle_setup_ms": int(os.environ["GRADLE_SETUP_MS"]),\n'
if text.count(old) != 1:
    raise SystemExit(f'helper failure JSON Java field: expected one remaining marker, found {text.count(old)}')
helper.write_text(text.replace(old, new, 1), encoding='utf-8')
replace_once(
    helper,
    """  echo \"- Source hydration duration: ${SOURCE_HYDRATION_MS} ms\"\n  echo \"- Gradle wrapper/cache setup duration: ${GRADLE_SETUP_MS} ms\"\n""",
    """  echo \"- Source hydration duration: ${SOURCE_HYDRATION_MS} ms\"\n  echo \"- Java 17 tooling duration: ${JAVA_SETUP_MS} ms\"\n  echo \"- Gradle wrapper/cache setup duration: ${GRADLE_SETUP_MS} ms\"\n""",
    'helper provenance Java timing',
)
replace_once(
    helper,
    """    echo \"source_hydration_ms=$SOURCE_HYDRATION_MS\"\n    echo \"gradle_setup_ms=$GRADLE_SETUP_MS\"\n""",
    """    echo \"source_hydration_ms=$SOURCE_HYDRATION_MS\"\n    echo \"java_setup_ms=$JAVA_SETUP_MS\"\n    echo \"gradle_setup_ms=$GRADLE_SETUP_MS\"\n""",
    'helper output Java timing',
)

helper_test = ROOT / 'swrlz-core/tools/ci/test_build_swrlz_component.py'
replace_once(
    helper_test,
    """        env['SWRLZ_SOURCE_HYDRATION_MS'] = str(hydration)\n        env['SWRLZ_GRADLE_SETUP_MS'] = '45'\n""",
    """        env['SWRLZ_SOURCE_HYDRATION_MS'] = str(hydration)\n        env['SWRLZ_JAVA_SETUP_MS'] = '23'\n        env['SWRLZ_GRADLE_SETUP_MS'] = '45'\n""",
    'helper test Java input',
)
text = helper_test.read_text(encoding='utf-8')
old = "            self.assertEqual(timing['source_hydration_ms'], 123)\n            self.assertEqual(timing['gradle_setup_ms'], 45)\n"
new = "            self.assertEqual(timing['source_hydration_ms'], 123)\n            self.assertEqual(timing['java_setup_ms'], 23)\n            self.assertEqual(timing['gradle_setup_ms'], 45)\n"
if text.count(old) != 1:
    raise SystemExit('helper success timing assertion marker mismatch')
text = text.replace(old, new, 1)
old = "            self.assertEqual(timing['source_hydration_ms'], 321)\n            self.assertEqual(timing['gradle_setup_ms'], 45)\n"
new = "            self.assertEqual(timing['source_hydration_ms'], 321)\n            self.assertEqual(timing['java_setup_ms'], 23)\n            self.assertEqual(timing['gradle_setup_ms'], 45)\n"
if text.count(old) != 1:
    raise SystemExit('helper failure timing assertion marker mismatch')
text = text.replace(old, new, 1)
old = "            self.assertEqual(failure['gradle_setup_ms'], 45)\n"
new = "            self.assertEqual(failure['java_setup_ms'], 23)\n            self.assertEqual(failure['gradle_setup_ms'], 45)\n"
if text.count(old) != 1:
    raise SystemExit('helper failure JSON assertion marker mismatch')
helper_test.write_text(text.replace(old, new, 1), encoding='utf-8')

validation = ROOT / '.github/workflows/swrlz-ci-tooling-validation.yml'
replace_once(
    validation,
    """          fetch-depth: 2\n          filter: blob:none\n          sparse-checkout: |\n""",
    """          fetch-depth: 2\n          filter: blob:none\n          persist-credentials: false\n          sparse-checkout: |\n""",
    'validation checkout auth',
)
replace_once(
    validation,
    """      - name: Smoke test Java 17 action\n        uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5\n        with:\n          distribution: temurin\n          java-version: '17'\n          check-latest: false\n\n""",
    """      - name: Smoke test preinstalled Java 17 fast path\n        run: |\n          set -euo pipefail\n          JDK_DIR=\"${JAVA_HOME_17_X64:-}\"\n          [[ -n \"$JDK_DIR\" && -x \"$JDK_DIR/bin/java\" && -x \"$JDK_DIR/bin/javac\" && -x \"$JDK_DIR/bin/keytool\" ]]\n          SPEC=\"$(\"$JDK_DIR/bin/java\" -XshowSettings:properties -version 2>&1 | awk -F'= ' '/java.specification.version/{print $2; exit}')\"\n          [[ \"$SPEC\" == '17' ]]\n          echo \"JAVA_HOME=$JDK_DIR\" >> \"$GITHUB_ENV\"\n          echo \"$JDK_DIR/bin\" >> \"$GITHUB_PATH\"\n          printf 'Java 17 fast path: %s\\n' \"$JDK_DIR\"\n\n""",
    'validation Java fast path',
)

contract = ROOT / 'swrlz-core/tools/ci/test_workflow_phase5_contract.py'
replace_once(
    contract,
    """        self.assertIn('Inspect preinstalled Android SDK', router)\n        self.assertIn(\"if: steps.android-sdk-preflight.outputs.fallback_required == 'true'\", router)\n""",
    """        self.assertIn('Validate preinstalled Java 17', router)\n        self.assertNotIn('actions/setup-java@', router)\n        self.assertIn('java_setup_ms', router)\n        self.assertIn('Inspect preinstalled Android SDK', router)\n        self.assertIn(\"if: steps.android-sdk-preflight.outputs.fallback_required == 'true'\", router)\n        self.assertIn('id: setup-android', router)\n""",
    'contract router Java/Android assertions',
)
replace_once(
    contract,
    """        self.assertIn('Smoke test preinstalled Android SDK fast path', validation)\n""",
    """        self.assertIn('Smoke test preinstalled Java 17 fast path', validation)\n        self.assertNotIn('actions/setup-java@', validation)\n        self.assertIn('Smoke test preinstalled Android SDK fast path', validation)\n""",
    'contract validator Java assertions',
)
replace_once(
    contract,
    """    def test_integrity_uses_preplanned_exact_checkout(self):\n        integrity = self.text('source-package-integrity.yml')\n        self.assertIn('matrix.checkout_patterns', integrity)\n        self.assertIn('Plan one-pass candidate hydration', integrity)\n""",
    """    def test_integrity_uses_preplanned_exact_checkout(self):\n        integrity = self.text('source-package-integrity.yml')\n        self.assertIn('matrix.checkout_patterns', integrity)\n        self.assertIn('Plan one-pass candidate hydration', integrity)\n        self.assertIn(\"- 'swrlz-core/tools/ci/plan_swrlz_candidate_checkout.py'\", integrity)\n        self.assertIn(\"- 'swrlz-core/tools/ci/verify_swrlz_package_pair.py'\", integrity)\n        self.assertGreaterEqual(integrity.count('persist-credentials: false'), 2)\n\n    def test_release_publication_rebases_and_retries(self):\n        router = self.text('swrlz-apk-router.yml')\n        self.assertIn('for attempt in 1 2 3; do', router)\n        self.assertIn('git rebase \"origin/$GITHUB_REF_NAME\"', router)\n        self.assertIn('Release publication remained non-fast-forward after 3 attempts.', router)\n""",
    'contract integrity/release assertions',
)

print('Phase 5D transformation prepared.')
