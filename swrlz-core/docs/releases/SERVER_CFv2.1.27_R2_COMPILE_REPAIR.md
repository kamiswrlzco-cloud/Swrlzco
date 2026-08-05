# SERVER CFv2.1.27 R2 — Operations Compose Compile Repair

**Checkpoint:** `INT-FIX-075A`

**Candidate:** `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2`

**Version code:** `130`

**Version name:** `2.1.27-swrlz-llm-studio-compile-repair-r2`

R2 is the direct SERVER-only repair successor to immutable §wyrlz LLM Studio R1.

## Repair

- Removes the invalid explicit `androidx.compose.foundation.layout.weight` import from `ServerOperationsScreen.kt`.
- Preserves both valid contextual `Modifier.weight(1f)` calls.
- Makes the established SERVER compiler-regression precheck mandatory in the paired INT-AI-074A verifier.
- Preserves the paired INT-AI-074A CLIENT source without publishing or changing the repository CLIENT lane, plus all LLM runtime/Studio behavior and contracts, Room schema 16, trust/admin gates, Truth Firewall, offline-first behavior, and compatibility identifiers.

## Source identity

- Source ZIP: `SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2.zip`
- Source SHA-256: `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86`
- Metadata ZIP SHA-256: `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647`
- Parent R1 SHA-256: `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`
- Source-publication commit: `ece8bda4ae572fe585e662484c8469e84ad923ef`

## Evidence boundary

R1 workflow run `30950003262` verified the parent and proved the compile failure. R2 is source/static/package verified. Android compilation, APK production, installation, device acceptance, promotion, release, and deployment remain pending until separately evidenced.
