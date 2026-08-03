# Current Authority — 2026-08-03

## Official repository

- Repository: `kamiswrlzco-cloud/Swrlzco`
- Active project root: `/swrlz-core`
- Default branch: `main`

## Current promoted source packages

The promoted rows below are intentionally unchanged. A newer candidate, successful build, downloaded APK, installed APK, device screenshot, route proof, admin-registry assignment, or defect report does not promote a candidate by itself.

### CLIENT

- File: `sources/client/CLIENT_CFv2.1.9_SWRLZ.zip`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Android applicationId: `sh.swurlz.core`
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

The current repository-transported Forge candidate lineage is maintained in `reference/CURRENT_CANDIDATE_LINEAGE.md`.

| Component | Candidate | VC | Source SHA-256 | Metadata SHA-256 | Repository transport | Status boundary |
|---|---|---:|---|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391` | commit `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | owner-reported Android build success; not promoted |
| SERVER | CFv2.1.26 R30 | 113 | `d07e814ab986491c2035854310630fe2638d5693ce9bd463ed665c82eeb19414` | `9d91109df048f87eada46f4737ca701ed7397ef4a7e0ff6ff38428e4889689da` | commit `2d21cd6ae0516dbfea8f69f144e8313f93822fef` | INT-CONTROL-069A; repository transported; not promoted |

R30 replaces the prior non-promoted SERVER candidate pointer because its exact chunked Forge transport is established. It does not change promoted SERVER authority.

## Prepared SERVER successor — no repository pointer change yet

- Candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R31`
- Logical identity: `CFv2.1.26 R31`
- versionCode: `114`
- versionName: `2.1.26-persistent-admin-registry-r31`
- checkpoint: `INT-CONTROL-069B`
- source SHA-256: `2ff51a057917d8280bab5e1142a964925b767e87e879e74a64dfce887ef2f5a2`
- metadata SHA-256: `ae57111b8f00b3c5cc13327d39b6e84f2381ff39d40316565d75a47257dc5685`
- direct parent: R30
- Forge transport/build/device evidence: pending
- promotion: not promoted

R31 does not replace the R30 repository pointer until Forge establishes its exact transport identity.

## SERVER runtime authority boundary

R31 defines a permanent SERVER-owned internal principal:

- principal ID: `server-root`
- principal type: `SERVER_INTERNAL`
- authority: `ROOT_CONTROL_PLANE`
- externally assignable: `false`
- source of proof: process identity plus SERVER installation identity

`server-root` is authoritative over the SERVER registry and policy engine. It may read/write registry state, evaluate policy, assign or revoke trust/admin state, dispatch authorized routes, append audit evidence, create/resolve approvals, and complete correlation records.

This internal authority is not a public client role and cannot be claimed through a client header, request payload, node label, or advertised capability. All server-root writes are audited. Destructive or consequential operations remain policy- or user-approval-gated.

## Node-admin registry boundary

R31 adds a user-facing node action to **Promote device to admin** and its corresponding revocation action. The resulting `SWRLZ_ADMIN_OPERATOR` role is durable registry state, not self-asserted client metadata.

Promotion requires server-owned evaluation of:

- active registration and supported protocol;
- confirmed identity;
- bound proof with retained proof hash;
- non-archived installation lineage;
- policy/trust eligibility;
- explicit user confirmation;
- bounded granted capabilities;
- immutable audit linkage to `server-root`.

A promoted admin node remains a client principal. It does not become `server-root`, cannot grant itself authority, cannot fabricate target capabilities, and cannot bypass approval policy for destructive execution.

## Current evidence interpretation

- CLIENT R8 remains the current repository CLIENT candidate.
- SERVER R30 is the current repository SERVER candidate by exact Forge transport identity.
- R30 implements proof/trust/capability/approval validation plus correlated node request/result routing.
- R31 prepares persistent admin promotion/revocation and the internal server-root principal while preserving R30 control-plane boundaries.
- R31 source/static verification does not prove Android compilation, installation, persistence across an actual app upgrade, device acceptance, promotion, release, or deployment.

## Candidate documentation entry points

- `reference/CURRENT_CANDIDATE_LINEAGE.md` — current and prepared candidate identities;
- `patch-notes/CLIENT_PATCH_NOTES.md` — CLIENT candidate history;
- `patch-notes/SERVER_PATCH_NOTES.md` — SERVER candidate and control-plane history;
- `contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory documentation accounting;
- package-internal `SWRLZ_SERVER_UPDATE_DELIVERY_PROTOCOL.md` — two-package handoff and standing log-repair workflow;
- package-internal `SWRLZ_ADMIN_NODE_CONTROL_PLANE_HANDOFF_v1.0.0_2026-08-03.docx` — authorized admin-node design and acceptance contract.

## Historical evidence boundary

Earlier candidate and evidence lineages remain preserved in repository history and the applicable documents under `docs/checkpoints/`, `docs/rebuild-v2/`, `docs/handoffs/`, `docs/reference/`, and `docs/patch-notes/`. Exact source SHA-256 and checkpoint provenance decide identity. Historical records are not rewritten into false current parentage.

## Validation boundary

- Promoted authority changes only through an explicit promotion checkpoint.
- Repository source transport does not prove Android compilation.
- Android build success does not prove installation or device acceptance.
- Installation does not prove trust elevation, promotion, release, or deployment.
- Runtime server-root authority does not promote a source package.
- Node-admin assignment does not grant server-root identity.
- Remote route evidence does not grant mission, approval, Forge, release, or deployment authority.
- Patch notes are navigation/accounting evidence and cannot strengthen an unsupported claim.
- Unknown evidence remains unknown.
