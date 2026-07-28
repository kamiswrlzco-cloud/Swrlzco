# INT-FORGE-039F + INT-FORGE-039N — Documentation Impact Set

Date: 2026-07-28

## Gate rule

This impact set separates repository CI implementation, CLIENT runtime candidate state, and current source authority. Historical evidence remains historical.

## Maintained documentation reviewed for impact

| Document | Impact | Action |
|---|---|---|
| `docs/CURRENT_AUTHORITY.md` | Authority boundary | **NO CHANGE** — no candidate is promoted by this checkpoint |
| `docs/reference/source-of-truth.md` | Authority hierarchy | **NO CHANGE** — promoted authority still requires matching SHA-256 evidence |
| `AGENTS.md` | Automated-agent build/authority guidance | **UPDATE** — distinguish ZIP-only build eligibility from promoted package evidence |
| `docs/DOCUMENTATION_INDEX.md` | Maintained documentation navigation | **UPDATE** — index this checkpoint and transport architecture state |
| `docs/architecture/conversational-artifact-forge-and-file-organization-v1.md` | Forge/file architecture | **UPDATE** — record 039F/039N repository CI implementation and optional-sidecar semantics |
| `docs/reference/feature-registry.md` | Feature status registry | **UPDATE** — mark repository chunk transport/ZIP-only CI as IMPLEMENTED while CLIENT runtime remains candidate |
| `docs/reference/module-map.md` | BUILD/TEST module mapping | **UPDATE** — add APK Router/resolver/verifier/tests as current repository BUILD/TEST modules |
| `docs/reference/status-matrix.md` | Major system status | **UPDATE** — add repository CI transport/build-input status |
| `docs/reference/documentation-manifest.md` | Package/evidence accounting | **UPDATE** — clarify build eligibility vs source-authority evidence |
| `docs/engineering/Engineering_Log.md` | Engineering chronology/evidence | **UPDATE** — record applied commit chain and validation boundary |
| `docs/checkpoints/INT-DOC-FILE-039M_ENGINEERING_SYNC.md` | Earlier documentation checkpoint | **NO CHANGE** — remains historical evidence of the state when written |
| `docs/releases/*` | Promoted/release evidence | **NO CHANGE** — no release or promotion occurred |
| `docs/evidence/INT-THEME-035D_CI_BUILD_EVIDENCE.md` | Historical build evidence | **NO CHANGE** — prior CLIENT build evidence remains historical |
| `docs/handoffs/*` historical handoffs | Historical lineage | **NO CHANGE** — do not rewrite prior handoff truth |

## Implementation/evidence documents added by this checkpoint

- `docs/checkpoints/INT-FORGE-039F-039N_CI_APPLICATION.md`
- `docs/checkpoints/INT-FORGE-039F-039N_DOCUMENTATION_IMPACT_SET.md`

## Boundary

The repository APK Router now supports direct ZIP input and verified chunk transport, and permits missing checksum/manifest evidence for build attempts. That does not weaken promotion rules: supplied contradictory evidence blocks, and current source authority remains separately governed by `CURRENT_AUTHORITY.md` and `reference/source-of-truth.md`.
