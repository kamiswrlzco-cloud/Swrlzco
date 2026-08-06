# Current Authority — 2026-08-05

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

The promoted rows below are intentionally unchanged. A newer candidate, successful build, downloaded APK, installed APK, device screenshot, route proof, admin-registry assignment, or defect report does not promote a candidate by itself.

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Android applicationId: `sh.swrlz.core`
- versionCode: `107`
- versionName: `2.1.9-package-pair-repair-v1`
- Checkpoint: `INT-THEME-035D`
- Status: package pair and repository CLIENT debug build verified; device acceptance pending

### SERVER

- File: `sources/server/SERVER_CFv2.1.0_SWRLZ.zip`
- SHA-256: `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940`
- Android applicationId: `sh.swrlz.nodehost`
- versionCode: `50`
- versionName: `2.1.0-forge-parity-portable-repository-v1`

## Current candidate pointer — not promoted authority

The current source-only candidate lineage is maintained in `reference/CURRENT_CANDIDATE_LINEAGE.md`.

| Component | Display role | Candidate | VC | Source SHA-256 | Metadata bundle SHA-256 | Checkpoint | Status boundary |
|---|---|---|---:|---|---|---|---|
| CLIENT | §wyrlix | CFv2.1.27 R8 | 134 | `dcc68cd54c213c81cd3b9fc4d0b7789ba377719cc074ad052fc9a9d57abb1f64` | `73a3e732293376db2482c208cbe58e7b515053f4cc49ca8f38bef3906923036e` | INT-FORGE-082A | source-only successor; APK build pending; not promoted |
| SERVER | §wyrver | CFv2.1.27 R10 | 133 | `4c4358fc4995986c05e29f78621f8cb949eda77ee58a938d8a80f1189e18f770` | `4a31abefc4d43fc9c9164d2d130d3c9706a05fcfd823c2c5c868b32c808cfbdf` | INT-FORGE-082A | source-only successor; APK build pending; not promoted |

These pointers account for the prepared exact source/metadata pairs. They do not claim that the archives have been promoted, installed, released, or deployed.

## INT-FORGE-082A interpretation

### CLIENT / §wyrlix

- canonical candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R8`
- direct parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R7`
- workflow evidence: `31069235859`
- purpose: stale-source selection repair, duplicate-aware dispatch, mixed-lane continuation, and component-accurate artifact monitoring;
- build truth: no CLIENT R8 Android build success has been established yet.

The failed manual CLIENT run resolved the older repository CLIENT R5 and failed in Kotlin compilation. That failure remains attached to R5 and does not prove failure of R8.

### SERVER / §wyrver

- canonical candidate: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R10`
- direct parent: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R9`
- workflow evidence: `31069235859`
- purpose: duplicate-aware mixed-lane upload/build orchestration and exact component/candidate artifact binding;
- build truth: no SERVER R10 Android build success has been established yet.

The SERVER artifact obtained from the earlier dual-lane route remains separate workflow evidence and must not be presented as a CLIENT result.

## Preserved earlier candidate evidence

- CLIENT CFv2.1.26 R8 / VC131 / INT-FIX-060C / SHA `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` remains earlier owner-reported build-success lineage; not promoted.
- SERVER CFv2.1.27 R2 / VC130 / INT-FIX-075A / SHA `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` remains exact-SHA Android debug build-success lineage from workflow `30965115165`; device/runtime acceptance pending; not promoted.
- SERVER R1 remains immutable failed-build lineage from workflow `30950003262`.
- Earlier CLIENT and SERVER candidate history remains preserved in Git history and package-internal lineage records.

## Patch Note Accounting boundary

Patch Note Accounting run `31068508343` displayed failure because the current repository accounting surfaces did not consistently identify the latest candidate, checkpoint, and SHA values. This reconciliation updates the repository-side accounting surfaces for INT-FORGE-082A.

Package-internal documentation remains immutable inside each source archive. If a transported archive's own `CHANGELOG.md`, `ReleaseNotes.md`, or `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` omits its exact candidate/checkpoint/SHA, repository documentation alone cannot rewrite that archive or convert package-internal debt into a pass.

## SERVER runtime authority boundary

The permanent SERVER-owned internal principal remains:

- principal ID: `server-root`
- principal type: `SERVER_INTERNAL`
- authority: `ROOT_CONTROL_PLANE`
- externally assignable: `false`
- source of proof: process identity plus SERVER installation identity

`server-root` remains authoritative over registry and policy enforcement, but destructive or consequential operations remain policy- or user-approval-gated. A promoted node-admin remains a bounded client principal and never becomes server-root.

## Candidate documentation entry points

- `reference/CURRENT_CANDIDATE_LINEAGE.md` — current and historical candidate identities;
- `patch-notes/CLIENT_PATCH_NOTES.md` — CLIENT / §wyrlix candidate history;
- `patch-notes/SERVER_PATCH_NOTES.md` — SERVER / §wyrver candidate history;
- `contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory documentation accounting.

## Validation boundary

- Promoted authority changes only through an explicit promotion checkpoint.
- Repository source transport does not prove Android compilation.
- Android build success does not prove installation or device acceptance.
- Installation does not prove trust elevation, promotion, release, or deployment.
- Runtime `server-root` authority does not promote a source package.
- Node-admin assignment does not grant `server-root` identity.
- Remote route evidence does not grant mission, approval, Forge, release, or deployment authority.
- Patch notes are navigation/accounting evidence and cannot strengthen an unsupported claim.
- Unknown evidence remains unknown.
