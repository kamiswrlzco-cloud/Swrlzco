#!/usr/bin/env python3
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
        env['SWRLZ_JAVA_SETUP_MS'] = '23'
        env['SWRLZ_GRADLE_SETUP_MS'] = '45'
        env['SWRLZ_ANDROID_SDK_SETUP_MS'] = '67'
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
            source = make_source(Path(temp), """#!/usr/bin/env bash\nset -e\nmkdir -p app/build/outputs/apk/debug\nprintf apk > app/build/outputs/apk/debug/app-debug.apk\n""")
            result, artifact = self.run_helper(source, hydration=123)
            self.assertEqual(result.returncode, 0, result.stdout)
            timing = json.loads((artifact / 'CI_TIMING.json').read_text())
            self.assertEqual(timing['status'], 'succeeded')
            self.assertEqual(timing['source_hydration_ms'], 123)
            self.assertEqual(timing['java_setup_ms'], 23)
            self.assertEqual(timing['gradle_setup_ms'], 45)
            self.assertEqual(timing['android_sdk_setup_ms'], 67)
            self.assertFalse(timing['configuration_cache_enabled'])
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
            self.assertEqual(timing['java_setup_ms'], 23)
            self.assertEqual(timing['gradle_setup_ms'], 45)
            self.assertEqual(timing['android_sdk_setup_ms'], 67)
            self.assertFalse(timing['configuration_cache_enabled'])
            failure = json.loads((artifact / 'BUILD_FAILURE.json').read_text())
            self.assertEqual(failure['java_setup_ms'], 23)
            self.assertEqual(failure['gradle_setup_ms'], 45)
            self.assertEqual(failure['android_sdk_setup_ms'], 67)
            self.assertFalse(failure['configuration_cache_enabled'])
            self.assertTrue((artifact / 'BUILD_FAILURE.json').is_file())


    def test_ephemeral_gradle_flags_are_present(self):
        text = HELPER.read_text(encoding='utf-8')
        self.assertIn('--no-watch-fs', text)
        self.assertIn('--build-cache', text)
        self.assertIn('--configuration-cache', text)
        self.assertIn('SWRLZ_GRADLE_CONFIGURATION_CACHE', text)

    def test_multiple_android_roots_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            source = make_source(Path(temp), '#!/usr/bin/env bash\nexit 0\n', second_project=True)
            result, _ = self.run_helper(source, hydration=0)
            self.assertEqual(result.returncode, 65)
            self.assertIn('exactly one Android Gradle project root', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
