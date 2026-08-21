#!/usr/bin/env python3
from pathlib import Path

helper = Path('swrlz-core/tools/ci/build_swrlz_component.sh')
text = helper.read_text(encoding='utf-8')
marker = '''case "${CONFIGURATION_CACHE_REQUESTED,,}" in
  true) CONFIGURATION_CACHE_ENABLED=true ;;
  false|'') CONFIGURATION_CACHE_ENABLED=false ;;
  *) echo 'SWRLZ_GRADLE_CONFIGURATION_CACHE must be true or false.' >&2; exit 65 ;;
esac

case "$COMPONENT" in CLIENT|SERVER) ;; *) usage ;; esac
'''
replacement = '''case "${CONFIGURATION_CACHE_REQUESTED,,}" in
  true) CONFIGURATION_CACHE_ENABLED=true ;;
  false|'') CONFIGURATION_CACHE_ENABLED=false ;;
  *) echo 'SWRLZ_GRADLE_CONFIGURATION_CACHE must be true or false.' >&2; exit 65 ;;
esac
PREPARE_ONLY="${SWRLZ_PREPARE_ONLY:-false}"
REUSE_EXTRACTED_WORKSPACE="${SWRLZ_REUSE_EXTRACTED_WORKSPACE:-false}"
PREPARED_EXTRACT_MS="${SWRLZ_PREPARED_EXTRACT_MS:-0}"
for boolean_name in PREPARE_ONLY REUSE_EXTRACTED_WORKSPACE; do
  boolean_value="${!boolean_name}"
  case "${boolean_value,,}" in
    true|false) ;;
    *) echo "$boolean_name must be true or false." >&2; exit 65 ;;
  esac
done
PREPARE_ONLY="${PREPARE_ONLY,,}"
REUSE_EXTRACTED_WORKSPACE="${REUSE_EXTRACTED_WORKSPACE,,}"
[[ "$PREPARED_EXTRACT_MS" =~ ^[0-9]+$ ]] || {
  echo 'SWRLZ_PREPARED_EXTRACT_MS must be a non-negative integer.' >&2
  exit 65
}
if [[ "$PREPARE_ONLY" == 'true' && "$REUSE_EXTRACTED_WORKSPACE" == 'true' ]]; then
  echo 'Prepare-only and reuse-extracted modes are mutually exclusive.' >&2
  exit 65
fi

case "$COMPONENT" in CLIENT|SERVER) ;; *) usage ;; esac
'''
if text.count(marker) != 1:
    raise SystemExit('helper configuration marker missing or ambiguous')
text = text.replace(marker, replacement)

old_extract = '''BUILD_STARTED_MS="$(now_ms)"
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
'''
new_extract = '''BUILD_STARTED_MS="$(now_ms)"
if [[ "$REUSE_EXTRACTED_WORKSPACE" == 'true' ]]; then
  rm -rf "$ARTIFACT_DIR"
  mkdir -p "$ARTIFACT_DIR"
  [[ -d "$WORK_DIR/extracted" ]] || {
    echo "Prepared extracted workspace not found: $WORK_DIR/extracted" >&2
    exit 66
  }
  EXTRACT_DURATION_MS="$PREPARED_EXTRACT_MS"
else
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
fi

mapfile -t PROJECT_ROOTS < <(
'''
if text.count(old_extract) != 1:
    raise SystemExit('helper extraction block missing or ambiguous')
text = text.replace(old_extract, new_extract)

local_marker = '''if [[ -n "$SDK_DIR" ]]; then
  printf 'sdk.dir=%s\\n' "$SDK_DIR" > "$PROJECT_ROOT/local.properties"
fi

GRADLE_ARGS=(
'''
local_replacement = '''if [[ -n "$SDK_DIR" ]]; then
  printf 'sdk.dir=%s\\n' "$SDK_DIR" > "$PROJECT_ROOT/local.properties"
fi

if [[ "$PREPARE_ONLY" == 'true' ]]; then
  if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
    {
      echo "project_root=$PROJECT_ROOT"
      echo "work_dir=$WORK_DIR"
      echo "extract_ms=$EXTRACT_DURATION_MS"
    } >> "$GITHUB_OUTPUT"
  fi
  exit 0
fi

GRADLE_ARGS=(
'''
if text.count(local_marker) != 1:
    raise SystemExit('helper local.properties marker missing or ambiguous')
helper.write_text(text.replace(local_marker, local_replacement), encoding='utf-8')

router = Path('.github/workflows/swrlz-apk-router.yml')
text = router.read_text(encoding='utf-8')
gradle_marker = '''      - name: Start Gradle wrapper/cache timer
        run: echo "SWRLZ_GRADLE_SETUP_STARTED_MS=$(date +%s%3N)" >> "$GITHUB_ENV"
'''
prepare_step = '''      - name: Prepare verified Gradle workspace
        id: prepare-workspace
        env:
          COMPONENT: ${{ matrix.component }}
          SOURCE_ZIP: ${{ steps.resolve.outputs.selected_source }}
          CANONICAL_STEM: ${{ steps.resolve.outputs.canonical_stem }}
          VARIANT: ${{ needs.prepare.outputs.build_variant }}
          SWRLZ_PREPARE_ONLY: 'true'
          SWRLZ_BUILD_WORK_DIR: ${{ github.workspace }}/swrlz-gradle-workspace/router
          SWRLZ_PREP_ARTIFACT_ROOT: ${{ runner.temp }}/swrlz-artifacts/router-prepare
        run: |
          set -euo pipefail
          bash "$SWRLZ_CI_ROOT/build_swrlz_component.sh" \\
            "$COMPONENT" "$SOURCE_ZIP" "$CANONICAL_STEM" "$VARIANT" \\
            "$SWRLZ_BUILD_WORK_DIR/$COMPONENT" \\
            "$SWRLZ_PREP_ARTIFACT_ROOT/$COMPONENT"

      - name: Start Gradle wrapper/cache timer
        run: echo "SWRLZ_GRADLE_SETUP_STARTED_MS=$(date +%s%3N)" >> "$GITHUB_ENV"
'''
if text.count(gradle_marker) != 1:
    raise SystemExit('router Gradle timer marker missing or ambiguous')
text = text.replace(gradle_marker, prepare_step)
old_build_env = '''          SWRLZ_GRADLE_CONFIGURATION_CACHE: ${{ secrets.SWRLZ_GRADLE_CACHE_ENCRYPTION_KEY != '' && 'true' || 'false' }}
          SWRLZ_BUILD_WORK_DIR: ${{ runner.temp }}/swrlz-build/router
          SWRLZ_ARTIFACT_ROOT: ${{ runner.temp }}/swrlz-artifacts/router
'''
new_build_env = '''          SWRLZ_GRADLE_CONFIGURATION_CACHE: ${{ secrets.SWRLZ_GRADLE_CACHE_ENCRYPTION_KEY != '' && 'true' || 'false' }}
          SWRLZ_REUSE_EXTRACTED_WORKSPACE: 'true'
          SWRLZ_PREPARED_EXTRACT_MS: ${{ steps.prepare-workspace.outputs.extract_ms }}
          SWRLZ_BUILD_WORK_DIR: ${{ github.workspace }}/swrlz-gradle-workspace/router
          SWRLZ_ARTIFACT_ROOT: ${{ runner.temp }}/swrlz-artifacts/router
'''
if text.count(old_build_env) != 1:
    raise SystemExit('router build env marker missing or ambiguous')
router.write_text(text.replace(old_build_env, new_build_env), encoding='utf-8')

validation = Path('.github/workflows/swrlz-ci-tooling-validation.yml')
text = validation.read_text(encoding='utf-8')
smoke_marker = '''      - name: Smoke test Gradle wrapper cache action
        uses: gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb # v6.3.0
        with:
          cache-cleanup: on-success
          cache-provider: basic
'''
smoke_replacement = '''      - name: Create Gradle cache smoke fixture
        run: |
          set -euo pipefail
          mkdir -p "$GITHUB_WORKSPACE/swrlz-gradle-smoke"
          printf "rootProject.name='swrlz-cache-smoke'\\n" > "$GITHUB_WORKSPACE/swrlz-gradle-smoke/settings.gradle"
          printf "plugins { id 'base' }\\n" > "$GITHUB_WORKSPACE/swrlz-gradle-smoke/build.gradle"

      - name: Smoke test Gradle wrapper cache action
        uses: gradle/actions/setup-gradle@9c971963bec38e04b3d30dcc455b5382be2fdbfb # v6.3.0
        with:
          cache-cleanup: on-success
          cache-provider: basic
          cache-read-only: true
'''
if text.count(smoke_marker) != 1:
    raise SystemExit('tooling Gradle smoke marker missing or ambiguous')
validation.write_text(text.replace(smoke_marker, smoke_replacement), encoding='utf-8')

contract = Path('swrlz-core/tools/ci/test_workflow_phase5_contract.py')
text = contract.read_text(encoding='utf-8')
router_assert = "        self.assertIn('cache-provider: basic', router)\n"
router_added = (
    router_assert
    + "        self.assertIn('Prepare verified Gradle workspace', router)\n"
    + "        self.assertIn(\"SWRLZ_PREPARE_ONLY: 'true'\", router)\n"
    + "        self.assertIn(\"SWRLZ_REUSE_EXTRACTED_WORKSPACE: 'true'\", router)\n"
    + "        self.assertIn('SWRLZ_PREPARED_EXTRACT_MS', router)\n"
    + "        self.assertIn('${{ github.workspace }}/swrlz-gradle-workspace/router', router)\n"
    + "        self.assertLess(router.index('Prepare verified Gradle workspace'), router.index('Set up Gradle wrapper cache'))\n"
)
if text.count(router_assert) != 1:
    raise SystemExit('contract router cache assertion marker missing or ambiguous')
text = text.replace(router_assert, router_added)
validation_assert = "        self.assertIn('cache-provider: basic', validation)\n"
validation_added = validation_assert + "        self.assertIn('Create Gradle cache smoke fixture', validation)\n" + "        self.assertIn('cache-read-only: true', validation)\n"
if text.count(validation_assert) != 1:
    raise SystemExit('contract validation cache assertion marker missing or ambiguous')
contract.write_text(text.replace(validation_assert, validation_added), encoding='utf-8')

tests = Path('swrlz-core/tools/ci/test_build_swrlz_component.py')
text = tests.read_text(encoding='utf-8')
insertion = '''    def test_prepare_then_reuse_workspace_without_second_extraction(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = make_source(root, """#!/usr/bin/env bash\nset -e\nmkdir -p app/build/outputs/apk/debug\nprintf apk > app/build/outputs/apk/debug/app-debug.apk\n""")
            work = root / 'work'
            prep_artifact = root / 'prep-artifact'
            prep_output = root / 'prep-output.txt'
            env = os.environ.copy()
            env['SWRLZ_PREPARE_ONLY'] = 'true'
            env['GITHUB_OUTPUT'] = str(prep_output)
            prepared = subprocess.run(
                ['bash', str(HELPER), 'SERVER', str(source), source.stem, 'debug', str(work), str(prep_artifact)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, check=False,
            )
            self.assertEqual(prepared.returncode, 0, prepared.stdout)
            self.assertIn('project_root=', prep_output.read_text())
            sentinel = work / 'extracted' / 'PREPARED_SENTINEL'
            sentinel.write_text('keep', encoding='utf-8')

            artifact = root / 'artifact'
            output = root / 'reuse-output.txt'
            env = os.environ.copy()
            env['SWRLZ_VERIFIED_SOURCE_SHA256'] = digest(source)
            env['SWRLZ_SOURCE_HYDRATION_MS'] = '11'
            env['SWRLZ_JAVA_SETUP_MS'] = '22'
            env['SWRLZ_GRADLE_SETUP_MS'] = '33'
            env['SWRLZ_ANDROID_SDK_SETUP_MS'] = '44'
            env['SWRLZ_REUSE_EXTRACTED_WORKSPACE'] = 'true'
            env['SWRLZ_PREPARED_EXTRACT_MS'] = '777'
            env['GITHUB_OUTPUT'] = str(output)
            reused = subprocess.run(
                ['bash', str(HELPER), 'SERVER', str(source), source.stem, 'debug', str(work), str(artifact)],
                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, check=False,
            )
            self.assertEqual(reused.returncode, 0, reused.stdout)
            self.assertTrue(sentinel.is_file(), 'reuse mode unexpectedly re-extracted the workspace')
            timing = json.loads((artifact / 'CI_TIMING.json').read_text())
            self.assertEqual(timing['extract_ms'], 777)

'''
test_marker = '    def test_ephemeral_gradle_flags_are_present(self):\n'
if text.count(test_marker) != 1:
    raise SystemExit('build helper test insertion marker missing or ambiguous')
tests.write_text(text.replace(test_marker, insertion + test_marker), encoding='utf-8')

print('Phase 5E Gradle ordering transformation applied.')
