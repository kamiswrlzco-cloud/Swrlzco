# SWRLZ Core

This is the active SWRLZ project root inside `kamiswrlzco-cloud/Swrlzco`.

## Current promoted source authority

| Role | Package | SHA-256 | Status |
|---|---|---|---|
| CLIENT | `CLIENT_CFv2.1.9_SWRLZ.zip` | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` | INT-THEME-035D package-pair/identity repair; CI debug build verified; device acceptance remains evidence-gated |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` | Promoted baseline retained; later SERVER work remains candidate/evidence lineage until separately promoted |

The older `.reference` source trees described by Documentation Rebuild v2 are historical evidence only. Later candidates and repository transports do not outrank the promoted rows without a separate promotion checkpoint.

Current candidate lineage is maintained in [`docs/reference/CURRENT_CANDIDATE_LINEAGE.md`](docs/reference/CURRENT_CANDIDATE_LINEAGE.md).

## Current candidate pointer — 2026-07-31

Current Forge repository transport at commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`:

| Role | Candidate | VC | Source SHA-256 | Checkpoint |
|---|---|---:|---|---|
| CLIENT | CFv2.1.27 R1 | 125 | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | INT-AI-060A truth/reasoning/expression separation |
| SERVER | CFv2.1.25 R1 | 83 | `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` | INT-AI-060A truth/reasoning/expression separation |

INT-FILE-059A previously packaged different source bytes under the same external CLIENT CFv2.1.27 R1 / SERVER CFv2.1.25 R1 identifiers. The collision is preserved by SHA-256/versionName/checkpoint provenance in the current-candidate ledger. Future candidates must advance version and/or revision rather than silently reuse the identity.

The shared Forge parent is CLIENT CFv2.1.26 R1 / VC124 / SHA `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` and SERVER CFv2.1.24 R1 / VC82 / SHA `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` under INT-FORGE-054A-R2.

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
    │   ├── patch-notes/
    │   ├── checkpoints/
    │   └── reference/
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

Forge path fields remain configurable so this layout can move without another repository-target rewrite.

INT-FORGE-054A-R2 establishes the shared CLIENT/SERVER Forge conveyor direction while preserving CLIENT-only Missions/legacy Dev Mode and SERVER-only inference/model/evidence authority.

## APK Router / Source Package Integrity policy

Repository CI accepts either:

- a lane-root CLIENT/SERVER source `.zip`; or
- a lane-root `*.transport.json` describing verified chunked source transport.

For build attempts, CI resolves a canonical source identity, reconstructs verified chunk transports in runner temporary storage, computes the whole ZIP SHA-256, and validates supplied checksum/manifest evidence when present. Contradictory supplied evidence fails closed.

INT-CI-061A repairs the 2026-07-31 nested-transport-evidence failure in Source Package Integrity by mapping changed transport members back to their lane-root transport identity instead of fabricating sibling ZIPs. APK Router now hardens lane-root source routing and supports manual CLIENT / SERVER / BOTH selection with ambiguity guards.

A GitHub-hosted runner queue/wait state is external scheduling evidence and is not treated as a workflow-code failure by itself.

The CI repairs do **not** change promoted source authority and do not by themselves prove an APK build. See `docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md`.

## Patch-note policy

Every future CLIENT/SERVER source update must synchronize its patch-history surfaces in the same bounded checkpoint. The active contract is [`docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`](docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md).

Repository ledgers:

- [`docs/patch-notes/CLIENT_PATCH_NOTES.md`](docs/patch-notes/CLIENT_PATCH_NOTES.md)
- [`docs/patch-notes/SERVER_PATCH_NOTES.md`](docs/patch-notes/SERVER_PATCH_NOTES.md)

Patch notes are navigation/lineage evidence; source ZIPs, exact checksums, accepted manifests/contracts, and validated build/device/promotion evidence retain precedence.
