# Current CLIENT / SERVER Candidate Lineage — 2026-08-02

This file tracks the newest repository-transported source candidates independently from promoted authority. `../CURRENT_AUTHORITY.md` remains the promotion authority until an explicit promotion checkpoint changes it.

## Current repository candidates

| Component | Logical candidate | VC | Source SHA-256 | Metadata SHA-256 | Checkpoint | Forge commit | Repository identity |
|---|---|---:|---|---|---|---|---|
| CLIENT | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | `6f246527543d28c010a67a019879ec4280706a6011a66f119c9a2fa366341391` | INT-FIX-060C | `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b` | `sources/client/CLIENT_CFv2.1.26_SWRLZ_CANDIDATE_R8.zip` |
| SERVER | CFv2.1.26 R21 | 104 | `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c` | `7f7f0e1baf8ff80837797aa132fd86587e31cc990d870796feb0cb28968e54f2` | INT-FIX-060P | `dbfeed2e8edd95d06bf7e6a775b3afd237a47989` | `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R21.transport.json` |

The SERVER transport uses the repository's chunked transport identity. The lane-root `.transport.json` is the repository source identity; chunks and metadata are evidence members, not independent source candidates.

## Prepared local successors — not repository candidates

| Component | Candidate | VC | Source SHA-256 | Metadata SHA-256 | Checkpoint | State |
|---|---|---:|---|---|---|---|
| SERVER | CFv2.1.26 R22 | 105 | `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52` | `2ffdcde47c3cad22258ace69932021ae06623905459279b3f0f0c76285d26681` | INT-DOC-060P-REPAIR | documentation-only successor; no Forge transport established |
| SERVER | CFv2.1.26 R23 | 106 | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | `670211b8d50b7d53673ee3840c5432ab626027c9d7ee6cc3c8ed6ae6f3b95fb0` | INT-STABILITY-063A | source-only stability successor; Forge/build/device evidence pending |

Prepared local source does not replace a repository candidate. The current SERVER pointer remains R21 until Forge establishes the exact R23 transport identity.

## Active direct-successor progression

### CLIENT

| Candidate | VC | Source SHA-256 | Parent / relationship | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R6 | 129 | `09d221ffff66feb56971525d039904a0e7cd135dfc89e65d3a13c5be2e0f3136` | accepted baseline | real source/metadata resolver fixture PASS |
| CFv2.1.26 R7 | 130 | `ab453b8cc213e65ad10d99e5d9cf3bdb4cc77974b72dfb5f73ca8eaa9a63ac2e` | direct successor of R6 | workflow compile failure |
| CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | direct successor of R7 | source verification PASS; owner-reported Android build success |

### SERVER

| Candidate | VC | Source SHA-256 | Parent / relationship | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R9 | 92 | `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f` | accepted baseline | verified source/metadata baseline |
| CFv2.1.26 R10 | 93 | `02434e16eb3985d20537570ab8025bb061c7ae04cb13a8d3197e2b27d2152665` | direct successor of R9 | workflow compile failure |
| CFv2.1.26 R11 | 94 | `7110f94c989128150ae3b8f5059bade4c8e24c455fe1ba34726369644061fa82` | direct successor of R10 | source verification; owner-reported Android build success |
| CFv2.1.26 R12 | 95 | `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f` | direct successor of R11 | pinned tunnel source; device ANR evidence |
| CFv2.1.26 R13 | 96 | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | direct successor of R12 | Forge transport established; ANR/runtime operations repair |
| CFv2.1.26 R14 | 97 | `d11bd43ec028f44aa374b218edc53237e5763e087a6278762448a5c4bef7cea0` | direct successor of R13 | native MCP-before-tunnel/no-OAuth bridge |
| CFv2.1.26 R15 | 98 | `b69a264f225c6f03b840158f3b1896fe6e185364eb4f30e3d0bbadf6b3fc9638` | direct successor of R14 | Termux-proven MCP compatibility port |
| CFv2.1.26 R16 | 99 | `8706ceccfba63a88128e1245f944fcdda1dcd4afc86546e693a9696ee1cbe8d7` | direct successor of R15 | explicit IPv4 loopback binding |
| CFv2.1.26 R17 | 100 | `c45f5fd5aa8c5bac60061db7c9d5cee98517739f33206efda83a7b7598e952bf` | direct successor of R16 | redacted tunnel diagnostics; first compile failed |
| CFv2.1.26 R18 | 101 | `0bf66150022ba2f35943accfb55ee03f135b936c2e441c1e0fa6cb70696ae404` | direct successor of R17 | PID compile repair |
| CFv2.1.26 R19 | 102 | `356f501da34946896829d82342068318d0327ce5bf6cdf96f8649a0703e52efb` | direct successor of R18 | local MCP/tunnel/CA READY proof; credential retention |
| CFv2.1.26 R20 | 103 | `b18aa2cbf9940a63e8c67ea98dc37f549bf95322301efba60ffa3fde271f8f28` | direct successor of R19 | Android-resolved control-plane egress and truthful readiness |
| CFv2.1.26 R21 | 104 | `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c` | direct successor of R20 | current repository candidate; Android build succeeded; remote MCP invocation evidence |
| CFv2.1.26 R22 | 105 | `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52` | documentation-only direct successor of R21 | package-internal accounting repair; local only |
| CFv2.1.26 R23 | 106 | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | direct successor of R22 | source-only model-startup/background-stability repair; transport/build/device pending |

## Capability progression in the active line

- CLIENT R7 and SERVER R10 introduced proof-bound protocol-2 registration and generic messaging.
- CLIENT R8 and SERVER R11 repaired the first Android/Kotlin compile failures without changing protocol or authority boundaries.
- SERVER R12 packaged and pinned the approved tunnel-client ARM64 runtime.
- SERVER R13 repaired Tunnel Settings ANR and added operational/Forge/model-rack improvements.
- SERVER R14-R16 established native MCP-before-tunnel startup, Termux-proven MCP compatibility, and explicit IPv4 binding.
- SERVER R17-R19 added redacted diagnostics, repaired PID compilation, replaced internal loopback `HttpURLConnection`, retained encrypted credentials, and reached local tunnel readiness.
- SERVER R20-R21 added Android-resolved control-plane egress, truthful remote-state separation, raw NODE_HOST loopback transport, and direct route evidence.
- SERVER R23 removes redundant automatic fleet model loading and adds startup/background memory protection and a stability ledger.

## Build and device evidence boundary

- CLIENT R8: project owner reported successful Android build through Forge; device acceptance and promotion remain separate.
- SERVER R21: supplied workflow evidence established Android build success. Device/plugin evidence showed ChatGPT reaching native MCP and exposed the final MCP-to-NODE_HOST cleartext transport defect repaired in R21 source.
- SERVER R23: source/static verification only. No Android compile, Forge transport, installation, background-survival proof, or promotion is asserted.

## Package-internal patch-history boundary

- CLIENT R8 remains grandfathered by exact SHA for historical package-local documentation debt.
- SERVER R21's immutable package notes lack the exact canonical candidate/checkpoint/VC identity required by the live accounting verifier. Repository docs now identify R21 correctly, but accounting can become fully current only after a synchronized successor such as R23 is transported.
- R23 package-internal `CHANGELOG.md`, `ReleaseNotes.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` are synchronized to R23/VC106/INT-STABILITY-063A.

## Divergent historical lineage

Earlier INT-AI-060A and INT-FILE-059A candidates reused external labels for different source bytes. Exact SHA-256 and checkpoint provenance decide identity; those lineages are not current parents.

## Patch-note accounting enforcement

`../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md` remains active. The Patch Note Accounting workflow is intentionally separate from Source Package Integrity and APK Router so documentation debt remains visible without falsifying source integrity or Android-build evidence.

## Evidence boundary

- Repository transport/checksum proves repository source identity, not Android compilation.
- Android build success does not prove installation or device acceptance.
- Installation does not elevate trust or promote a candidate.
- Source/static validation does not prove runtime survival.
- Candidate lineage does not change promoted authority.
