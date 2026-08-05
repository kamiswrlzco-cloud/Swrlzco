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

## Unaccounted repository candidate evidence

Repository head `3d37cf5eadd6eea5a5cba8e796d3a02002fde634` contains a later CLIENT
CFv2.1.27 R1 Forge transport with source SHA-256
`2c43d60454d16defda959e482bd03b40ce29a1898d71a966fa67ef30333aabe5`.
Patch Note Accounting run `30969188766` proves that its package `ReleaseNotes.md` and
the repository current-lineage/authority surfaces are not synchronized to that exact
identity. Therefore the documentation-complete candidate pointer below is not silently
advanced by this CI checkpoint. Repairing or accepting that CLIENT lineage requires a
separate bounded documentation/source-authority decision.

## Current candidate pointer — not promoted authority

The current repository-transported Forge candidate lineage is maintained in `reference/CURRENT_CANDIDATE_LINEAGE.md`.

| Component | Candidate | VC | Source SHA-256 | Metadata SHA-256 | Repository transport | Status boundary |
|---|---|---:|---|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391` | commit `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | owner-reported Android build success; not promoted |
| SERVER | CFv2.1.27 R2 | 130 | `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` | `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647` | commit `ece8bda4ae572fe585e662484c8469e84ad923ef` | exact-SHA Android debug build succeeded in run `30965115165`; device/runtime pending; not promoted |

R2 replaces R1 only as the non-promoted repository SERVER candidate pointer. R1 remains immutable failed-build lineage. Neither repository transport nor the successful exact-SHA debug build changes promoted SERVER authority.

## Current SERVER candidate interpretation

- Candidate: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2`
- Logical identity: `CFv2.1.27 R2`
- versionCode: `130`
- versionName: `2.1.27-swrlz-llm-studio-compile-repair-r2`
- checkpoint: `INT-FIX-075A`
- source SHA-256: `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`
- metadata SHA-256: `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`
- direct parent: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R1` / SHA-256 `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`
- repository identity: `sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2.transport.json`
- repository transport: commit `ece8bda4ae572fe585e662484c8469e84ad923ef`
- promotion: not promoted

R1 introduced the first-party §wyrlz LLM system layer, role-scoped knowledge/training, CLIENT context bridge, and dedicated SERVER LLM Studio. APK Router run `30950003262` selected and verified exact R1, then failed at `:app:compileDebugKotlin` on the explicit internal Compose `foundation.layout.weight` import in `ServerOperationsScreen.kt`.

R2 removes only that invalid import, preserves both contextual `Modifier.weight(1f)` calls, and makes the existing SERVER compiler-regression precheck mandatory in the paired LLM verifier. It preserves the paired INT-AI-074A CLIENT source without publishing or changing the repository CLIENT lane, plus the LLM behavior/contracts, Room schema 16, package/protocol/database identifiers, `server-root`, proof-bound admin authority, identity, trust, Truth Firewall, offline-first behavior, local/remote distinctions, and protocol discipline.

## Build and workflow evidence boundary

- R1 transport commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` established exact source SHA-256 `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`.
- APK Router run `30950003262` verified that exact R1 source and failed at Kotlin compilation on the explicit internal Compose weight import. It produced no APK and did not build CLIENT.
- APK Router run `30965115165` resolved exact R2 SHA-256 `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`, verified metadata SHA-256 `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`, passed package verification, and completed `:app:assembleDebug` successfully.
- Run `30965115165` produced artifact `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2_debug_APK` / artifact ID `8914536222`; contained APK SHA-256 `c9932345cc8f07d110bffa364d4b30d111cf149d78fed789153a63cde9f3d726`.
- Source Package Integrity run `30965115656` and Patch Note Accounting run `30965115160` failed before source selection/audit because their `fetch-depth: 2` checkout omitted push `before` commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` from this two-commit push. Their `bad object` failures are CI changed-range defects, not contradictory package or build evidence.
- INT-CI-076A implements a shared fail-closed changed-range resolver that retains
  shallow checkout and fetches only a missing exact event-base commit. Its direct
  depth-2 multi-commit regression and historical 83-path replay pass locally;
  post-publication workflow evidence remains pending at this documentation freeze.
- Patch Note Accounting run `30969188766` for later CLIENT Forge commit `3d37cf5e...`
  passed changed-range resolution and failed in the subsequent audit on separate
  CLIENT package/repository patch-history omissions. INT-CI-076A does not suppress or
  repair that evidence.

## SERVER runtime authority boundary

The permanent SERVER-owned internal principal remains:

- principal ID: `server-root`
- principal type: `SERVER_INTERNAL`
- authority: `ROOT_CONTROL_PLANE`
- externally assignable: `false`
- source of proof: process identity plus SERVER installation identity

`server-root` remains authoritative over registry and policy enforcement, but destructive or consequential operations remain policy- or user-approval-gated. A promoted node-admin remains a bounded client principal and never becomes server-root.

## Current evidence interpretation

- CLIENT R8 remains the current repository CLIENT candidate.
- SERVER R2 is the current repository SERVER candidate by exact chunked transport identity.
- R1 remains preserved as the failed-build §wyrlz LLM Studio parent.
- R2 is a bounded compile-repair successor; it does not alter the §wyrlz LLM contract or CLIENT.
- Exact APK Router run `30965115165` establishes R2 Android debug build success. It does not establish installation, device/runtime acceptance, promotion, release, or deployment.

## Candidate documentation entry points

- `reference/CURRENT_CANDIDATE_LINEAGE.md` — current and historical candidate identities;
- `patch-notes/CLIENT_PATCH_NOTES.md` — CLIENT candidate history;
- `patch-notes/SERVER_PATCH_NOTES.md` — SERVER candidate and implementation history;
- `contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` — mandatory documentation accounting;
- package-internal `SWRLZ_SERVER_UPDATE_DELIVERY_PROTOCOL.md` — two-package handoff and standing log-repair workflow;
- package-internal `SWRLZ_SERVER_INTERFACE_FORGE_MEMORY_HANDOFF_v1.0.docx` — controlling interface/Forge/memory/permission requirements.

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
