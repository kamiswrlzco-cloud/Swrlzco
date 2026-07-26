# SWRLZ Core

This is the active SWRLZ project root inside `kamiswrlzco-cloud/Swrlzco`.

## Current source authority

| Role | Package | SHA-256 | Status |
|---|---|---|---|
| CLIENT | `CLIENT_CFv2.1.8_SWRLZ.zip` | `d344e683cc76756020b1a02e118b2417c03d6552eeb032dd5dd91058c0f7f055` | INT-THEME-035C source-only ThemePack chrome/runtime repair; compile/device validation remains evidence-gated |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` | Current supplied source package; compile/device validation remains evidence-gated |

The older `.reference` source trees described by Documentation Rebuild v2 are historical
evidence only. They do not outrank the source packages above.

## Repository layout

```text
/
├── README.md
├── .github/
│   └── workflows/                 # executable GitHub Actions YAML
└── swrlz-core/
    ├── README.md
    ├── AGENTS.md
    ├── docs/
    ├── schemas/
    ├── brain/
    │   ├── core/
    │   ├── packs/
    │   └── manifests/
    ├── sources/
    │   ├── client/
    │   └── server/
    ├── requests/
    │   ├── client/
    │   ├── server/
    │   ├── brain/
    │   └── inbox/
    ├── releases/
    ├── reports/
    └── tools/
```

## Forge routing

For this repository layout, configure SWRLZ Forge to use:

- Repository: `kamiswrlzco-cloud/Swrlzco`
- CLIENT source path: `swrlz-core/sources/client`
- SERVER source path: `swrlz-core/sources/server`
- Generic documentation/inbox path: choose the intended destination, such as
  `swrlz-core/docs/inbox` or `swrlz-core/requests/inbox`

The Forge path fields remain configurable so this layout can move again without requiring
another repository-target rewrite.
