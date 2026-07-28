# SWRLZ Core

This is the active SWRLZ project root inside `kamiswrlzco-cloud/Swrlzco`.

## Current source authority

| Role | Package | SHA-256 | Status |
|---|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` | INT-THEME-035D package-pair/identity repair; CI debug build verified; device acceptance remains evidence-gated |
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

## APK Router source-input policy

Repository CI accepts either:

- a lane-root CLIENT/SERVER source `.zip`; or
- a lane-root `*.transport.json` describing verified chunked source transport.

For a build attempt, the source ZIP is the required source identity. CI computes the whole ZIP SHA-256. A matching checksum or package manifest is optional build evidence; when supplied it must validate exactly and contradictory evidence blocks the build.

For chunked transport, CI verifies each declared chunk and reconstructs the exact original ZIP in runner temporary storage before compilation. Transport chunks are not independent source authority.

This build-input flexibility does **not** change the current-source-authority table above. Promotion remains a separate evidence-gated checkpoint. See `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md`.
