# INT-THEME-035D — CI Build Evidence

Evidence date: 2026-07-26
Scope: CLIENT only
Checkpoint: `INT-THEME-035D`

## Repository promotion

- Pull request: `#2` — `CLIENT CFv2.1.9: package pair repair`
- Pull request URL: `https://github.com/kamiswrlzco-cloud/Swrlzco/pull/2`
- Verified head: `1c53f08421cc18765dab357710c6b29e82826094`
- Merge commit: `77be6f4f93ff73c0f9cbd2b3c5d6f401bcb893ef`
- Main-parent tree and uploaded branch tree were compared before merge.
- Changed scope: 22 CLIENT package/documentation paths; no SERVER paths.

## Canonical source pair

- ZIP: `CLIENT_CFv2.1.9_SWRLZ.zip`
- ZIP SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- ZIP bytes: `36,527,185`
- ZIP entries: `688`
- Android versionCode: `107`
- Android versionName: `2.1.9-package-pair-repair-v1`

## Automatic workflow evidence

### Source Package Integrity

- Run: `30223152048`
- URL: `https://github.com/kamiswrlzco-cloud/Swrlzco/actions/runs/30223152048`
- Conclusion: `success`
- Job: `verify` (`89848962266`)
- Resolver: `success`
- Final ZIP checksum and optional-manifest verification: `success`

This is the exact verification step that rejected the superseded CFv2.1.8
manifest in run `30222384992`.

### APK Router

- Run: `30223152052`
- URL: `https://github.com/kamiswrlzco-cloud/Swrlzco/actions/runs/30223152052`
- Conclusion: `success`
- Resolver unit-test job: `89848962291` — `success`
- Component-route job: `89848990762` — `success`
- CLIENT build job: `89849022603` — `success`
- SERVER build job: not started
- Release-commit step: skipped

The CLIENT job passed canonical source resolution, selected-package verification,
Gradle compilation, debug-signing handling, provenance generation, and artifact
upload.

## Artifact evidence

- Artifact ID: `8637844750`
- Artifact name: `CLIENT_CFv2.1.9_SWRLZ_debug_APK`
- Artifact bytes: `55,906,214`
- Artifact ZIP SHA-256:
  `e4e5c65c134f11ab1dac77d368e0f2cc8e09c393917e9ed2e22b9a6282be20c4`
- Artifact retention expiry: `2026-08-25T22:31:55Z`
- Artifact ZIP CRC: pass

Downloaded artifact contents:

- `CLIENT_CFv2.1.9_SWRLZ_DEBUG.apk`
- `CLIENT_CFv2.1.9_SWRLZ_DEBUG.apk.sha256`
- `SOURCE_RESOLUTION.json`
- `SOURCE_RESOLUTION.json.sha256`
- `BUILD_PROVENANCE_REPORT.md`
- `BUILD_PROVENANCE_REPORT.md.sha256`
- `BUILD_LOG.txt`
- `SWRLZ_SIGNING_MODE.txt`

Independent downloaded-byte verification:

- APK bytes: `56,667,850`
- APK SHA-256:
  `0f7312dd346c6eb587b0ec44ab28b9dd30e9371799c26dbbe657fdc354fba419`
- APK ZIP structure: pass
- Source-resolution JSON SHA-256:
  `075926ad43b4906a2266da4fdd775afe5a165621535275cc32314b89b0170663`
- Provenance report SHA-256:
  `810e74fbcaa452f831de0f96ea24a307f987278cf9b02fc896afd2c77b5fd784`
- Resolved source SHA-256:
  `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Selection reason: `current-push`
- Build variant/task: `debug` / `:app:assembleDebug`
- Signing mode: `runner/default-source-signing`
- Provenance source commit:
  `77be6f4f93ff73c0f9cbd2b3c5d6f401bcb893ef`

The three included checksum receipts contain correct hash values. Their filename
fields use runner-temporary absolute paths, so portable verification was performed
by recalculating each downloaded file and comparing the receipt's first field.
Receipt path normalization is a non-blocking CI hardening item; it does not change
the verified artifact bytes or hashes above.

## Build log

- Result: `BUILD SUCCESSFUL`
- Duration: `3m 21s`
- Tasks: `42 actionable tasks` (`40 executed`, `2 up-to-date`)
- Compiler errors: none
- Non-blocking Kotlin deprecation warnings: 9
- Native strip notice: two packaged libraries could not be stripped and were
  packaged unchanged

## Boundary

This evidence proves repository package verification and CI debug APK assembly.
It does not prove installation, launcher migration on a real device, startup
animation timing, progress animation geometry at runtime, theme switching across
process restarts, performance, accessibility acceptance, release signing,
distribution, deployment, or SERVER behavior.
