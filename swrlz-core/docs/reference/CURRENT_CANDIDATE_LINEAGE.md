# Current CLIENT / SERVER Candidate Lineage — 2026-08-05

This file tracks repository-transported or publication-ready candidates independently from promoted authority. `../CURRENT_AUTHORITY.md` remains the promotion authority until an explicit promotion checkpoint changes it.

## Current non-promoted candidate pointers

| Component | Display role | Logical candidate | VC | Source SHA-256 | Metadata bundle SHA-256 | Checkpoint | Evidence boundary |
|---|---|---|---:|---|---|---|---|
| CLIENT | §wyrlix | CFv2.1.27 R8 | 134 | `dcc68cd54c213c81cd3b9fc4d0b7789ba377719cc074ad052fc9a9d57abb1f64` | `73a3e732293376db2482c208cbe58e7b515053f4cc49ca8f38bef3906923036e` | INT-FORGE-082A | source-only successor; APK build pending; not promoted |
| SERVER | §wyrver | CFv2.1.27 R10 | 133 | `4c4358fc4995986c05e29f78621f8cb949eda77ee58a938d8a80f1189e18f770` | `4a31abefc4d43fc9c9164d2d130d3c9706a05fcfd823c2c5c868b32c808cfbdf` | INT-FORGE-082A | source-only successor; APK build pending; not promoted |

The exact repository identity may be a lane-root ZIP or canonical transport descriptor depending on Forge transport. Repository transport establishes package identity only and does not prove Android compilation, installation, device acceptance, promotion, release, or deployment.

## INT-FORGE-082A relationship

### CLIENT / §wyrlix

- canonical candidate: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R8`
- direct parent: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R7.zip`
- evidence workflow: `31069235859`
- repairs stale source selection by requiring explicit component/source dispatch;
- permits an exact repository duplicate to be built without creating a duplicate source commit;
- prevents CLIENT monitoring from accepting an unrelated SERVER artifact;
- preserves CLIENT local/control authority and all existing trust, Truth Firewall, offline-first, lineage, and compatibility boundaries.

### SERVER / §wyrver

- canonical candidate: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R10`
- direct parent: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R9.zip`
- evidence workflow: `31069235859`
- adds duplicate-aware mixed-lane upload/build orchestration;
- keeps CLIENT and SERVER lanes independent when one source is already present;
- binds workflow monitoring and artifact extraction to the expected component and candidate stem;
- preserves `server-root`, SERVER authority, local/remote distinctions, approval gates, protocol discipline, and compatibility identifiers.

## Immediate prior lineage

| Component | Candidate | VC | Checkpoint | Source SHA-256 | Evidence state |
|---|---|---:|---|---|---|
| CLIENT | CFv2.1.27 R7 | 133 | INT-FORGE-081A | `a25af33abfe9ef6879b5f6ce8bdc0c1d79526382b68e1d21ea314a000d1d0a45` | source-only Dragon Master Workshop and parser-repair successor |
| CLIENT | CFv2.1.27 R5 | 132 | INT-FORGE-079A | `4b6ea04aec69f1cbd3bdd7c8b0914348f0af418d1fb2530aef08f95f8e44943b` | workflow `31069235859` resolved this stale source and CLIENT compilation failed |
| SERVER | CFv2.1.27 R9 | 132 | INT-FORGE-081A | `a16d4df443d08f8fbab8cbc2a9d42e1b46957c9317903c4387fce9178b6041c0` | source-only Dragon Master Workshop and parser-repair successor |
| SERVER | CFv2.1.27 R7 | 131 | INT-FORGE-079A | `99e4d70bbe8b50b61a0576cc27c5b3effa31148777fb95e41f0e9accde0530bf` | source-only adaptive Forge Project Conveyor foundation |

## Preserved earlier verified repository candidates

The following remain historical evidence and are not rewritten or promoted by this pointer update:

- CLIENT `CFv2.1.26 R8` / VC131 / INT-FIX-060C / SHA `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` — owner-reported Android build success; not promoted.
- SERVER `CFv2.1.27 R2` / VC130 / INT-FIX-075A / SHA `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` — exact-SHA Android debug build succeeded in workflow `30965115165`; device/runtime acceptance pending; not promoted.
- SERVER R1 remains immutable failed-build lineage from workflow `30950003262`.
- Earlier CLIENT and SERVER candidate history remains preserved through Git history and package-internal lineage records.

## Patch-accounting boundary

- Package-internal `CHANGELOG.md`, `ReleaseNotes.md`, checkpoint evidence, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` must identify the exact candidate/checkpoint/SHA.
- Repository `CLIENT_PATCH_NOTES.md`, `SERVER_PATCH_NOTES.md`, this file, and `CURRENT_AUTHORITY.md` must identify the same non-promoted candidate pointers.
- A candidate pointer update does not promote, release, install, or deploy software.
- Android build success does not prove device acceptance.
- Unknown evidence remains unknown.
