# Current CLIENT / SERVER Candidate Lineage — 2026-08-04

This file tracks repository-transported candidates independently from promoted authority. `../CURRENT_AUTHORITY.md` remains the promotion authority until an explicit promotion checkpoint changes it.

## Current repository candidates

| Component | Logical candidate | VC | Source SHA-256 | Metadata SHA-256 | Checkpoint | Forge commit | Repository identity |
|---|---|---:|---|---|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391` | INT-FIX-060C | `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | `sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8.zip` |
| SERVER | CFv2.1.27 R2 | 130 | `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` | `65034a407090c80d252361c449f0cc471ad57a7fde3742b9622958a96465a647` | INT-FIX-075A | `ece8bda4ae572fe585e662484c8469e84ad923ef` | `sources/server/SERVER_CFv2.1.27_SWRLZ_CANDIDATE_R2.transport.json` |

The SERVER transport uses chunked Git blobs. The lane-root `.transport.json` is the repository source identity; chunks, metadata, and bounded accounting receipts are evidence members, not independent source candidates.

R2 is the current non-promoted repository SERVER candidate. Repository transport establishes exact package identity only; it does not prove Android compilation, installation, device acceptance, promotion, release, or deployment.

## R1 failure and R2 repair relationship

R1 is the §wyrlz LLM Studio successor to R45. Forge commit `193fe26155c26c07f77fec9bda212c84d8e7b5f9` transported exact R1 source SHA-256 `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc`. APK Router run `30950003262` verified that package and failed at `:app:compileDebugKotlin` on the explicit internal Compose `foundation.layout.weight` import.

R2 is the direct SERVER-only repair successor:

- removes that invalid import while preserving both contextual `Modifier.weight(1f)` calls;
- makes the established SERVER compiler-regression precheck mandatory in the paired LLM verifier;
- preserves the paired INT-AI-074A CLIENT source without publishing or changing the repository CLIENT lane, plus the LLM runtime/Studio/contracts, Room schema 16, identity, trust, Truth Firewall, offline-first behavior, and compatibility identifiers;
- is exact-SHA Android debug build successful in APK Router run `30965115165`; installation and device/runtime acceptance remain pending.

## Active direct-successor progression

### CLIENT

| Candidate | VC | Source SHA-256 | Relationship | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R6 | 129 | `09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136` | accepted baseline | resolver fixture PASS |
| CFv2.1.26 R7 | 130 | `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e` | direct successor of R6 | workflow compile failure |
| CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | direct successor of R7 | source verification and owner-reported build success |

### SERVER

| Candidate | VC | Checkpoint | Source SHA-256 | Relationship / evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R9 | 92 | INT-FORGE-064G | `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f` | accepted verified baseline |
| CFv2.1.26 R10 | 93 | INT-MSG-060A | `02434e16eb3985d20537570ab8025bb061c7ae04cb13a8d3197e2b27d2152665` | direct successor; compile failure |
| CFv2.1.26 R11 | 94 | INT-FIX-060C | `7110f94c989128150ae3b8f5059bade4c8e24c455fe1ba34726369644061fa82` | messaging compile repair |
| CFv2.1.26 R12 | 95 | INT-TUNNEL-060D | `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f` | pinned tunnel runtime |
| CFv2.1.26 R13 | 96 | INT-FIX-060F | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | tunnel operations repair |
| CFv2.1.26 R14 | 97 | INT-FIX-060H | `d11bd43ec028f44aa374b218edc53237e5763e087a6278762448a5c4bef7cea0` | native MCP-before-tunnel route |
| CFv2.1.26 R15 | 98 | INT-FIX-060J | `b69a264f225c6f03b840158f3b1896fe6e185364eb4f30e3d0bbadf6b3fc9638` | MCP compatibility port |
| CFv2.1.26 R16 | 99 | INT-FIX-060K | `8706ceccfba63a88128e1245f944fcdda1dcd4afc86546e693a9696ee1cbe8d7` | explicit IPv4 binding |
| CFv2.1.26 R17 | 100 | INT-TUNNEL-DIAGNOSTICS-001E | `c45f5fd5aa8c5bac60061db7c9d5cee98517739f33206efda83a7b7598e952bf` | redacted diagnostics |
| CFv2.1.26 R18 | 101 | INT-FIX-060L | `0bf66150022ba2f35943accfb55ee03f135b936c2e441c1e0fa6cb70696ae404` | PID compile repair |
| CFv2.1.26 R19 | 102 | INT-FIX-060M | `356f501da34946896829d82342068318d0327ce5bf6cdf96f8649a0703e52efb` | route readiness and credential retention |
| CFv2.1.26 R20 | 103 | INT-FIX-060N | `b18aa2cbf9940a63e8c67ea98dc37f549bf95322301efba60ffa3fde271f8f28` | Android-resolved control-plane egress |
| CFv2.1.26 R21 | 104 | INT-FIX-060P | `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c` | raw NODE_HOST loopback route |
| CFv2.1.26 R22 | 105 | INT-DOC-060P-REPAIR | `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52` | package-internal accounting repair |
| CFv2.1.26 R23 | 106 | INT-STABILITY-063A | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | model/startup stability; Forge transported |
| CFv2.1.26 R24 | 107 | INT-STABILITY-065A | `20af0c617c5b8f96708fffc27d73ac6d81e473af4401aafcb170d0ec0057293f` | launch crash-loop breaker; Forge transported |
| CFv2.1.26 R25 | 108 | INT-STABILITY-066A | `5f195ae4c3e8f73cba974f81f8591f93c706fe546e0ed9b9af046df810602101` | isolated tunnel process |
| CFv2.1.26 R26 | 109 | update-delivery protocol | `1088e51b8c559733b73a18abac7961bb51b14b58596725058f2a10b25e7f1b2c` | two-package handoff; Forge transported |
| CFv2.1.26 R27 | 110 | INT-STABILITY-068A | `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1` | generation-safe tunnel lifecycle; Forge transported |
| CFv2.1.26 R28 | 111 | INT-DOC-068B | `2187eaf0dd1f071ced561d823f169a52f185c6986f158652572a367fc62b31d0` | accounting/handoff successor; Forge transported |
| CFv2.1.26 R29 | 112 | INT-FIX-068C | `12517439d2bf4da501a2e0efa260d38a41ab00a8ca6a7e4586a9693737f01fc8` | Binder callback compile repair; Forge transported and owner-reported build success |
| CFv2.1.26 R30 | 113 | INT-CONTROL-069A | `d07e814ab986491c2035854310630fe2638d5693ce9bd463ed665c82eeb19414` | authorized operator and correlated result control plane |
| CFv2.1.26 R31 | 114 | INT-CONTROL-069B | `2ff51a057917d8280bab5e1142a964925b767e87e879e74a64dfce887ef2f5a2` | persistent admin registry/server-root |
| CFv2.1.26 R32 | 115 | INT-CONTROL-069C | `c7a947803d2b29d3bef9f0ca4622c24b5cfd90357fc504635e77aa77944d6a15` | capability-bearing messages and mission route |
| CFv2.1.26 R33 | 116 | SWRLZ-SERVER-UI-HANDOFF-001-A | `5a725d0d827b871e8f7b44d954fbe140c1d5dc857afe9be447deac9f809a020c` | truthful Core status semantics and layout |
| CFv2.1.26 R34 | 117 | SWYRLZ-SERVER-UI-HANDOFF-001-B | `9cafb443adfcf8dc250eefc7e8894c50190418f9604de7e151356a0e6a12f9cb` | preserved prior repository candidate; Chat interface cleanup |
| CFv2.1.26 R35 | 118 | INT-WORKFLOW-RESET-070A | `fbd98d5879354769e43cfd7dc0a49c7d85c43d0399fd255bab2a43cc3a54bc86` | clean candidate identity successor; preserved R34 behavior |
| CFv2.1.26 R36 | 119 | INT-SERVER-CONTINUITY-071A | `d2e3b4c89ca1efaeb6ea310ce918e50c9a9c799ee19122b6b31e5abb217bac22` | credential-vault/Forge-order/IME foundation |
| CFv2.1.26 R37 | 120 | INT-SERVER-CONTINUITY-071B | `fd0e7cf2837cbf16abf1267dcb8749895570fed839c511f785bd286d5bf83eed` | canonical conversation ledger and node synchronization |
| CFv2.1.26 R38 | 121 | INT-SERVER-CONTINUITY-071C | `76a180bdcbf3b0d6d6ff40a01c7ebbc86d32736ea783cfd68ef8feb0210aa200` | capability-gated conversation observatory |
| CFv2.1.26 R39 | 122 | INT-SERVER-CONTINUITY-071D | `dc19b731e7e06a6046998df3fb64240f38900e15814b97f24c08447f915459df` | group conversations and explicit AI participation |
| CFv2.1.26 R40 | 123 | INT-SERVER-CONTINUITY-071E | `c6e5b71dd3bcd71453b4c12d868783d6a22f4bcb3283b602729523e8e4b956b1` | resumable verified transfer intake |
| CFv2.1.26 R41 | 124 | INT-SERVER-CONTINUITY-071F | `e05a2a804eebbc4f5cb414c50871ddfeadd94ea20196488ad1ab342307523a58` | protected local File Analysis Forge |
| CFv2.1.26 R42 | 125 | INT-SERVER-CONTINUITY-071G | `10108e93d4a535b550e338d8f8bbc140eb98be64ef9039cfcb0def4fb387a1f1` | verified Auto Forge intake and artifact delivery; source-only |
| CFv2.1.26 R43 | 126 | INT-SERVER-TUNNEL-072A | `ef41bc4052644e0de966a283a38e63cc7c07211cc87103758e8b9e8556ea7236` | shared 23-tool MCP catalog and route-grounded plugin presence |
| CFv2.1.26 R44 | 127 | INT-SERVER-BUILD-REPAIR-072B | `503fbc1f784621771da43761b842929196cb229060027d254233ccacdbd3a3ce` | malformed ordinary Kotlin string compile repair |
| CFv2.1.26 R45 | 128 | INT-SERVER-RUNTIME-ACCEPTANCE-073A | `4665ea6d613e2b070597e360ef281392747cdacd1ae670f41355f91ea2c5d226` | Operations/Runtime Acceptance Center; source-only |
| CFv2.1.27 R1 | 129 | INT-AI-074A | `f14a42f8d809fe4a4c23fc86c2bb193bbf3b51d7f6dc5d023205a875916f41dc` | §wyrlz LLM Studio parent; exact transport; compile failed in run `30950003262` |
| CFv2.1.27 R2 | 130 | INT-FIX-075A | `ec1627ad77e27752c8d29f665faa9f223a3c35bc74af0246bed198586cf3aa86` | current repository candidate; bounded compile repair; exact-SHA Android debug build succeeded in run `30965115165` |

## Authority and package-accounting boundary

- `server-root` remains an internal SERVER principal, not a client node and not externally assignable.
- A node may hold bounded `SWRLZ_ADMIN_OPERATOR` registry state without becoming server-root.
- Target capabilities remain implementation- and policy-bound; trust does not fabricate capabilities.
- R2 package-internal `CHANGELOG.md`, `ReleaseNotes.md`, checkpoint record, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` identify R2/VC130/INT-FIX-075A.
- Repository documentation must also name the exact transported source SHA, candidate, and checkpoint.
- Candidate pointer changes do not promote, release, or deploy software.
