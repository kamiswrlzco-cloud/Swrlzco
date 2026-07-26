# CLIENT CFv2.1.8 — Theme Chrome + Runtime Visual Repair

Status: source implementation preserved; repository package-pair verification failed; superseded by INT-THEME-035D
Checkpoint: `INT-THEME-035C`
Parent: `CLIENT_CFv2.1.7_SWRLZ.zip`
Parent SHA-256: `bc5b941e9b0c86e28581d8f6019b6c54722243279ef666aa3c35c4f97745fe76`

CLIENT now carries the selected ThemePack through its full visual shell instead of stopping at palette changes. Each built-in theme resolves its own background identity, Kapanion, motif, panel geometry, border ornament, progress calibration, and motion personality.

This source candidate:

- replaces the old default Android launcher identity with Glitch Dragon Glass artwork;
- removes the empty-circle startup fallback by completing legacy/default identity mappings;
- clips all animated progress artwork to one calibrated inner track;
- stages Jester Core Ignition instead of stacking full-screen frames;
- places the selected Kapanion in the header, voice core, companion rail, assistant messages, and preview;
- keeps Jester art exclusive to Jester and preserves distinct art for other families;
- retains truthful progress, reduced motion, accessibility semantics, independent CLIENT preference, and all authority/protocol boundaries.

No SERVER source changed. After PR #1 merged at
`bc80d7a4d28d656f640ac1a511b9ae340e8b45ee`, Source Package Integrity run
`30222384992` and APK Router run `30222384996` both stopped before compilation
because this package's sidecar manifest lacked the canonical `zip`, `size_bytes`,
and `verified: true` fields. The ZIP and SHA remained matched. No APK was produced.
INT-THEME-035D / CLIENT CFv2.1.9 is the preserved-behavior package-pair successor.
