# CLIENT Source

Current source package:

- `CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- applicationId: `sh.swurlz.core`
- versionCode: `107`
- versionName: `2.1.9-package-pair-repair-v1`
- checkpoint: `INT-THEME-035D`

CFv2.1.9 preserves CFv2.1.8 theme behavior and repairs its canonical manifest contract.
CFv2.1.8 remains in this lane as failed package-pair lineage, and CFv2.1.7 remains the
preceding implementation rollback baseline.

Validation boundary: exact ZIP/SHA/manifest identity, deterministic packaging, path safety,
and the repository package-pair verifier pass locally. Repository CI compilation, APK
assembly, and device acceptance are not yet asserted.
