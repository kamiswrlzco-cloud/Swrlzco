# INT-FORGE-039F + INT-FORGE-039N — Documentation Impact Set

Date: 2026-07-28

## Gate rule

This impact set separates repository CI implementation, CLIENT runtime candidate state, and current source authority. Historical evidence remains historical.

## Maintained documentation reviewed for impact

| Document | Impact | Action |
|---|---|---|
| `README.md` repository root | Repository landing page | **NO CHANGE** — no root-level authority/layout statement required revision |
| `swrlz-core/README.md` | Active project overview and Forge routing | **UPDATE** — add current APK Router direct-ZIP/chunked input policy without changing authority table |
| `swrlz-core/AGENTS.md` | Automated-agent build/authority guidance | **UPDATE** — distinguish ZIP-only build eligibility from promoted package evidence |
| `docs/README.md` | Documentation entry point | **UPDATE** — point to current transport architecture/checkpoint while preserving historical index |
| `docs/CURRENT_AUTHORITY.md` | Authority boundary | **NO CHANGE** — no candidate is promoted by this checkpoint |
| `docs/reference/source-of-truth.md` | Authority hierarchy | **NO CHANGE** — promoted authority still requires matching SHA-256 evidence |
| `docs/DOCUMENTATION_INDEX.md` | Maintained documentation navigation | **UPDATE** — index this checkpoint and transport architecture state |
| `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Forge/file architecture | **UPDATE** — record 039F/039N repository CI implementation and optional-sidecar semantics |
| `docs/architecture/system-overview.md` | Broad runtime architecture | **NO CHANGE** — this checkpoint changes build/transport tooling rather than runtime system planes |
| `docs/architecture/client-architecture.md` | CLIENT architecture | **NO CHANGE** — CLIENT CFv2.1.20 remains candidate/build-pending; no promoted runtime architecture claim |
| `docs/architecture/client-theme-chrome-runtime-v1.md` | CLIENT presentation architecture | **NO CHANGE** — unrelated to source transport/build-input policy |
| `docs/architecture/repository-migration-foundation.md` | Repository layout foundation | **NO CHANGE** — CLIENT/SERVER source lane locations remain unchanged |
| `docs/client/CLIENT_IMPLEMENTATION_ANALYSIS.md` | Promoted/current implementation analysis | **NO CHANGE** — no CLIENT source promotion |
| `docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` | Promoted/current implementation analysis | **NO CHANGE** — no SERVER source promotion |
| `docs/missions/action-resolution.md` | Mission semantics | **NO CHANGE** — mission behavior/authority unchanged |
| `docs/reference/evidence-classification.md` | Evidence terminology | **NO CHANGE** — existing separation of evidence classes remains applicable |
| `docs/reference/feature-registry.md` | Feature status registry | **UPDATE** — mark repository chunk transport/ZIP-only CI as IMPLEMENTED while CLIENT runtime remains candidate |
| `docs/reference/module-map.md` | BUILD/TEST module mapping | **UPDATE** — add APK Router/resolver/verifier/tests as current repository BUILD/TEST modules |
| `docs/reference/status-matrix.md` | Major system status | **UPDATE** — add repository CI transport/build-input status |
| `docs/reference/documentation-manifest.md` | Package/evidence accounting | **UPDATE** — clarify build eligibility vs source-authority evidence |
| `docs/wordmesh/WORDMESH_IMPLEMENTATION_GAP_ANALYSIS.md` | WordMesh gap analysis | **NO CHANGE** — no WordMesh behavior/specification changed |
| `docs/releases/compatibility-matrix.md` | Release compatibility | **NO CHANGE** — no release/promoted compatibility state changed |
| `docs/releases/CLIENT_CFv2.1.9_PACKAGE_PAIR_REPAIR.md` | Historical/promoted CLIENT release evidence | **NO CHANGE** |
| `docs/releases/CLIENT_CFv2.1.8_THEME_CHROME_RUNTIME_REPAIR.md` | Historical CLIENT release evidence | **NO CHANGE** |
| `docs/engineering/Engineering_Log.md` | Engineering chronology/evidence | **UPDATE** — record applied commit chain and validation boundary |
| `docs/checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md` | Earlier documentation checkpoint | **NO CHANGE** — remains historical evidence of the state when written |
| `docs/checkpoints/INT-THEME-035D_CLIENT_PACKAGE_PAIR_REPAIR.md` | Historical checkpoint | **NO CHANGE** |
| `docs/checkpoints/INT-THEME-035C_CLIENT_THEME_CHROME_RUNTIME_REPAIR.md` | Historical checkpoint | **NO CHANGE** |
| `docs/evidence/INT-THEME-035C_PROGRESS_GEOMETRY_PREVIEW.jpg` | Historical/static evidence | **NO CHANGE** |
| `docs/evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md` | Historical build evidence | **NO CHANGE** — prior CLIENT build evidence remains historical |
| `docs/handoffs/*` historical handoffs | Historical lineage | **NO CHANGE** — do not rewrite prior handoff truth |
| `docs/rebuild-v2/*` | Historical rebuild records | **NO CHANGE** — historical evidence preserved as historical |

## Implementation/evidence documents added by this checkpoint

- `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md`
- `docs/checkpoints/INT-FORGE-039F-039N_DOCUMENTATION_IMPACT_SET.md`

## Boundary

The repository APK Router now supports direct ZIP input and verified chunk transport, and permits missing checksum/manifest evidence for build attempts. That does not weaken promotion rules: supplied contradictory evidence blocks, and current source authority remains separately governed by `CURRENT_AUTHORITY.md` and `reference/source-of-truth.md`.
