# INT-THEME-035C — CLIENT Source Handoff

Source: `CLIENT_CFv2.1.8_SWRLZ.zip`
SHA-256: `d344e683cc76756020b1a02e118b2417c03d6552eeb032dd5dd91058c0f7f055`
Bytes: `36,529,261`
ZIP entries: `684`
Android identity: versionCode `106`, versionName `2.1.8-theme-chrome-runtime-repair-v1`

Parent:

- `CLIENT_CFv2.1.7_SWRLZ.zip`
- `bc5b941e9b0c86e28581d8f6019b6c54722243279ef666aa3c35c4f97745fe76`

Implemented:

- repaired default Glitch Dragon Glass launcher/application identity;
- distinct launcher identity for all 13 selectable CLIENT themes, including Teal’s own derived launcher;
- selected ThemePack background, Kapanion, voice core, motifs, panel chrome, and motion across the CLIENT shell;
- bounded and clipped layered progress with calibrated per-pack geometry;
- staged Jester Core Ignition;
- reduced-motion and accessibility-safe decorative presentation;
- deterministic CLIENT derivative tooling and 103-entry runtime asset catalog;
- checkpoint, architecture, release, engineering, contract, and source-lineage documentation.

Preserved:

- SERVER;
- protocol, trust, Truth Firewall, identity proof, permissions, missions, Forge authority, local/remote distinctions, accessibility automation, and offline-first behavior.

Verification:

- source-only integrity: pass;
- immutable ZIP/SHA-256 pairing: pass;
- repository promotion: PR #1 merged at `bc80d7a4d28d656f640ac1a511b9ae340e8b45ee`;
- Source Package Integrity run `30222384992`: failed manifest-schema verification;
- APK Router run `30222384996`: resolver passed, then the same manifest-schema verification failed;
- Android compilation: skipped;
- APK artifact: not produced;
- device/release/deployment: not run or claimed.

This failed package pair remains immutable lineage. CLIENT CFv2.1.9 under
INT-THEME-035D preserves the implementation and repairs the canonical manifest contract.
