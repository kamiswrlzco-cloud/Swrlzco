# SWRLZ Core

This is the active SWRLZ project root inside `kamiswrlzco-cloud/Swrlzco`.

## Current promoted source authority

| Role | Package | SHA-256 | Status |
|---|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` | INT-THEME-035D package-pair/identity repair; CI debug build verified; device acceptance remains evidence-gated |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` | Promoted baseline retained; later SERVER candidates remain separately evidence-gated |

Later source candidates do not change this table without an explicit promotion checkpoint. See [`docs/CURRENT_AUTHORITY.md`](docs/CURRENT_AUTHORITY.md).

## Latest repository transport identities — candidate only

Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` currently carries verified chunk-transport identity for:

| Role | Repository candidate identity | Whole-source SHA-256 | Transport evidence |
|---|---|---|---|
| CLIENT | `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1` | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | 15,127,739 bytes / 4 chunks / checksum evidence / no separately packaged candidate manifest in that transaction |
| SERVER | `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1` | `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` | 40,710,681 bytes / 10 chunks / checksum evidence / no separately packaged candidate manifest in that transaction |

These rows prove repository transport identity only. They do not by themselves prove Android compilation, APK output, device acceptance, promotion, release, deployment, or installation.

The preceding accepted source-only Forge-parity lineage is CLIENT CFv2.1.26 R1 / VC124 / SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` and SERVER CFv2.1.24 R1 / VC82 / SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` under `INT-FORGE-054A-R2`.

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
    │   ├── client/PATCH_NOTES.md
    │   └── server/PATCH_NOTES.md
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
- Generic documentation/inbox path: choose the intended destination, such as `swrlz-core/docs/inbox` or `swrlz-core/requests/inbox`

The Forge path fields remain configurable so this layout can move again without requiring another repository-target rewrite.

`INT-FORGE-054A-R2` establishes the shared CLIENT/SERVER Forge-conveyor direction: CLIENT/SERVER/BOTH/ASK targeting, authoritative newest-source resolution, configurable SAF storage lanes, persistent Build Ledger provenance, and default-on successful-artifact/failed-log download policy while preserving CLIENT-only and SERVER-only roles.

## APK Router source-input policy

Repository CI accepts either:

- a lane-root CLIENT/SERVER source `.zip`; or
- a lane-root `*.transport.json` describing verified chunked source transport.

For a build attempt, the source ZIP is the required source identity. CI computes the whole ZIP SHA-256. A matching checksum or package manifest is optional build evidence; when supplied it must validate exactly and contradictory evidence blocks the build.

For chunked transport, CI verifies each declared chunk and reconstructs the exact original ZIP in runner temporary storage before compilation. Transport chunks and nested transport evidence are not independent source authority or independent build routes.

`INT-CI-DOC-060A` prepares a repair that prevents Source Package Integrity from interpreting nested `.transport/.../evidence/*.sha256` as a direct source sidecar and hardens APK Router to route only from lane-root source identities/evidence. The repair is staged on `checkpoint/int-ci-doc-060a-router-docs` until explicit merge approval.

This build-input flexibility does **not** change the promoted-source-authority table above. Promotion remains a separate evidence-gated checkpoint.

## Patch-note policy

Maintained component patch notes are:

- [`docs/client/PATCH_NOTES.md`](docs/client/PATCH_NOTES.md)
- [`docs/server/PATCH_NOTES.md`](docs/server/PATCH_NOTES.md)

Every accepted source-update checkpoint must synchronize the affected ledger; shared CLIENT/SERVER updates synchronize both. Already packaged ZIPs remain immutable. Patch notes are lineage/navigation evidence and do not outrank canonical source packages, checksums, contracts/manifests, or stronger validation/promotion evidence.

## Approved future file-analysis scope

`INT-FILE-059A` is approved for a shared CLIENT/SERVER Forge File Lab + Archive Cartographer foundation. Approval is recorded as scope only; this README does not claim a current CLIENT/SERVER source package implements it.
