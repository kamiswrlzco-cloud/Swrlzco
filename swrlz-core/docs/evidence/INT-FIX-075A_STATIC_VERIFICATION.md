# INT-FIX-075A Static and Package Verification

**Candidate:** `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2`

**Source SHA-256:** `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`

**Metadata SHA-256:** `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`

## Results

| Check | Result |
|---|---|
| SERVER compiler-regression precheck | PASS |
| Paired INT-AI-074A static gate | 113/113 PASS |
| INT-FIX-075A repair gate | 28/28 PASS |
| Kotlin/KTS ordinary-string scan | 397 files / 0 violations / PASS |
| R1→R2 inventory | 7 added / 12 modified / 0 removed |
| Shared CLIENT/SERVER LLM contract | byte-identical |
| Room schema | 16 unchanged |
| Internal source manifest | 1,191/1,191 PASS |
| Source ZIP CRC/path safety | PASS |
| Immutable source/metadata package pair | 26/26 PASS |
| Repository CI unit suite | 30 PASS / 1 absent-fixture skip |
| Repository chunk reconstruction/package verification | PASS |
| Repository patch-note accounting for exact R2 identity | PASS |

## Compiler-evidence lineage

R1 transport commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` carried exact parent SHA-256 `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`. APK Router run `30950003262` verified that source and failed at `:app:compileDebugKotlin` on the explicit internal Compose weight import. R2 removes that import and preserves contextual weight usage.

R2 source-publication commit `ece8bda4ae572fe585e662484c8469e84ad923ef` carries the exact 68-part chunk transport, metadata ZIP, and synchronized documentation. Automatic post-publication workflow results remain separate evidence.

## Non-claims

These results are source/static/package evidence. They are not Android compilation, APK, installation, device, integration, promotion, release, or deployment evidence. Automatic post-publication workflows must be recorded by exact run and resolved source SHA before the evidence state advances.
