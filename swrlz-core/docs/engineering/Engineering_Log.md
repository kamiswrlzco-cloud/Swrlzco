# CLIENT Engineering Log

## 2026-07-26 — INT-THEME-035C

Verified canonical parent `CLIENT_CFv2.1.7_SWRLZ.zip` at SHA-256 `bc5b941e9b0c86e28581d8f6019b6c54722243279ef666aa3c35c4f97745fe76`.

Advanced the CLIENT-only source successor to CFv2.1.8 / versionCode 106. The implementation replaces the default legacy launcher, completes per-theme identity/chrome mappings, introduces reusable full-shell ThemePack backdrop/Kapanion/panel renderers, contains progress artwork inside one calibrated track, and stages the Jester ignition sequence. Existing distinct Kapanion assets were reused; no Jester art was copied into other families and no AI-generated replacement art was required.

The authority diff remains presentation-only. SERVER, protocol, network, trust, identity proof, permission, mission, Forge transaction, accessibility automation, local/remote, and offline-first sources are unchanged.

Source-only integrity evidence is recorded in `docs/checkpoints/INT-THEME-035C_CLIENT_THEME_CHROME_RUNTIME_REPAIR.md`. Gradle, tests, APK, device acceptance, workflow execution, release, and deployment are not run or claimed.

## 2026-07-26 — INT-THEME-035B

Workflow run `30216145763` resolved and verified `CLIENT_CFv2.1.6_SWRLZ.zip`, and resolver unit tests passed 6/6. Kotlin compilation then failed at `ThemedProgress.kt:175` and `:190` because nested Compose `Box` scopes could not implicitly resolve the enclosing `BoxWithConstraints.maxWidth`.

Advanced the source successor to CLIENT CFv2.1.7 / versionCode 105 and captured the outer width as `availableWidth` before both nested scopes. The two fill images now use `Modifier.width(availableWidth)`. No build was run in this checkpoint; static repair/package verification only.

## 2026-07-26 — INT-THEME-035A

Parent `CLIENT_CFv2.1.5_SWRLZ.zip` was verified at SHA-256 `c7ed3942c9a14a110ea3a085316011b3522153e757d09614050aa15d20f9ac58` and retained as rollback.

Implemented the source-only declarative ThemePack checkpoint as CLIENT CFv2.1.6 / versionCode 104:

- shared contract and validation;
- stable legacy migration plus seven new built-ins;
- deterministic 101-resource runtime visual catalog;
- independent local CLIENT selection and staged preview;
- launcher/Kapanion/bubble/notification identity;
- Jester startup reference and safe fallbacks;
- truthful layered progress and reduced-motion behavior;
- architecture, contract, checkpoint, implementation, and release documentation.

Static XML/JSON, asset integrity, shared-contract, alias, changed-source lexical, and authority-scope checks passed. Gradle, APK, device, GitHub, commit, push, release, and deployment actions were not run.

Repository documentation publication is pending a separately authorized source promotion.
