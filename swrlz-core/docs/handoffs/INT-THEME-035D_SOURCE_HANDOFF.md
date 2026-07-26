# INT-THEME-035D — CLIENT Source Handoff

Source: `CLIENT_CFv2.1.9_SWRLZ.zip`
SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
Bytes: `36,527,185`
ZIP entries: `688`
Android identity: versionCode `107`, versionName `2.1.9-package-pair-repair-v1`

Parent:

- `CLIENT_CFv2.1.8_SWRLZ.zip`
- `d344e683cc76756020b1a02e118b2417c03d6552eeb032dd5dd91058c0f7f055`
- merge commit `bc80d7a4d28d656f640ac1a511b9ae340e8b45ee`

Failed predecessor evidence:

- Source Package Integrity run `30222384992`
- APK Router run `30222384996`
- cause: sidecar manifest schema mismatch before compilation
- APK produced: no

Repair:

- preserves all CFv2.1.8 theme/application behavior;
- advances package/application identity;
- adds canonical `zip`, `sha256`, `size_bytes`, and `verified: true` manifest fields;
- preserves failed CFv2.1.8 evidence rather than replacing it.

Verification:

- behavior diff limited to identity/documentation: PASS
- deterministic ZIP bytes: PASS
- ZIP CRC/root/path safety: PASS
- checksum/manifest identity: PASS
- repository verifier: PASS locally
- Source Package Integrity run `30223152048`: PASS
- APK Router run `30223152052`: PASS
- CLIENT debug APK SHA-256:
  `0f7312dd346c6eb587b0ec44ab28b9dd30e9371799c26dbbe657fdc354fba419`
- CI artifact ZIP SHA-256:
  `e4e5c65c134f11ab1dac77d368e0f2cc8e09c393917e9ed2e22b9a6282be20c4`
- CI signing mode: `runner/default-source-signing`
- device acceptance: pending

Detailed CI evidence:

- `../evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md`

Excluded:

- SERVER, protocol, trust, Truth Firewall, permissions, missions, Forge authority,
  local/remote distinctions, accessibility automation, release, deployment, and installation.
