# SERVER Patch Notes

**Scope:** SERVER source-candidate lineage, repository transport history, and prepared direct successors.  
**Authority:** Candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply Android compilation, installation, device acceptance, promotion, release, or deployment unless separate evidence is named.

## Current repository candidate — 2026-08-03

### CFv2.1.26 R34 — SWYRLZ-SERVER-UI-HANDOFF-001-B

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R34`
- versionCode: `117`
- versionName: `2.1.26-chat-interface-cleanup-r34`
- source SHA-256: `9cafb443adfcf8dc250eefc7e8894c50190418f9604de7e151356a0e6a12f9cb`
- metadata SHA-256: `34cf10cdcdea4c2beeb5c39b91067743dab74019f3d5eafa0d7962a2551569e3`
- checkpoint: `SWYRLZ-SERVER-UI-HANDOFF-001-B`
- direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R33.zip`
- Forge transport commit: `c92e124656fd1d9b0c2b039d29c8b508a54de309`
- repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R34.transport.json`
- promotion: not promoted

Changes:

- replaces the generic Chat header with the active thread title at upper left and an evidence-derived LLM state at upper right;
- adds functional New Chat, Chat History, Pinned Chats, and Bookmarked Chats navigation;
- replaces the full-width Send control with a compact translucent composer containing the dragon action and send icon;
- makes the dragon menu open upward with Commands, Pinned Responses, and Bookmarked Responses;
- places GitHub Actions first among Forge operational dialogs and expands it by default;
- reports approved local-link unavailability on mobile data while preserving truthful loopback availability;
- begins the visible `Swyrlz` / `Swyrler` display transition while preserving compatibility-sensitive internal identifiers;
- preserves R33 Core semantics, R32 capability-bearing mission routing, R31 persistent admin registry and `server-root`, tunnel isolation/lifecycle, identity, trust, Truth Firewall, offline-first behavior, and protocol discipline.

Repository transport proves exact R34 package identity. The supplied APK Router run was canceled during GitHub checkout before component routing or Android compilation; no R34 build result is inferred from that run.

## Recent direct-successor progression

| Candidate | VC | Checkpoint | Source SHA-256 | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R30 | 113 | INT-CONTROL-069A | `d07e814ab986491c2035854310630fe2638d5693ce9bd463ed665c82eeb19414` | authorized operator/correlation control plane; Forge transported |
| CFv2.1.26 R31 | 114 | INT-CONTROL-069B | `2ff51a057917d8280bab5e1142a964925b767e87e879e74a64dfce887ef2f5a2` | persistent admin registry and internal server-root; Forge transported |
| CFv2.1.26 R32 | 115 | INT-CONTROL-069C | `c7a947803d2b29d3bef9f0ca4622c24b5cfd90357fc504635e77aa77944d6a15` | capability-bearing messages and mission route; Forge transported |
| CFv2.1.26 R33 | 116 | SWRLZ-SERVER-UI-HANDOFF-001-A | `5a725d0d827b871e8f7b44d954fbe140c1d5dc857afe9be447deac9f809a020c` | truthful Core status/layout checkpoint; Forge transported |
| CFv2.1.26 R34 | 117 | SWYRLZ-SERVER-UI-HANDOFF-001-B | `9cafb443adfcf8dc250eefc7e8894c50190418f9604de7e151356a0e6a12f9cb` | current repository candidate; Chat interface cleanup and visible terminology transition |

## Preserved historical accounting snapshot

The detailed R30/R31 and earlier lineage below is retained as historical accounting context. The canonical current pointer above supersedes the earlier snapshot’s former “current” labels without rewriting its historical evidence.

### CFv2.1.26 R30 — INT-CONTROL-069A

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R30`
- versionCode: `113`
- versionName: `2.1.26-authorized-control-plane-r30`
- source SHA-256: `d07e814ab986491c2035854310630fe2638d5693ce9bd463ed665c82eeb19414`
- metadata SHA-256: `9d91109df048f87eada46f4737ca701ed7397ef4a7e0ff6ff38428e4889689da`
- checkpoint: `INT-CONTROL-069A`
- direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R29.zip`
- Forge transport commit: `2d21cd6ae0516dbfea8f69f144e8313f93822fef`
- repository identity: `sources/server/SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R30.transport.json`
- promotion: not promoted

R30 introduced proof-bound, trust-scoped `SWRLZ_ADMIN_OPERATOR` authorization, durable message/correlation/conversation tracking, result-return routing, redacted audit events, and Room migration `8 -> 9` while preserving target capability truth and approval gates.

### CFv2.1.26 R31 — INT-CONTROL-069B

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R31`
- versionCode: `114`
- versionName: `2.1.26-persistent-admin-registry-r31`
- source SHA-256: `2ff51a057917d8280bab5e1142a964925b767e87e879e74a64dfce887ef2f5a2`
- metadata SHA-256: `ae57111b8f00b3c5cc13327d39b6e84f2381ff39d40316565d75a47257dc5685`
- checkpoint: `INT-CONTROL-069B`

R31 defined the non-spoofable internal `server-root` principal, persistent node-admin state, Room migration `9 -> 10`, proof/trust-gated admin promotion and revocation, and redacted audit evidence.

## Preserved earlier active lineage

| Candidate | VC | Checkpoint | Source SHA-256 | Milestone |
|---|---:|---|---|---|
| CFv2.1.26 R9 | 92 | INT-FORGE-064G | `b7657be3d59d54099f44fdbbca6d6dc4b79d6387074c52cf69d1f7e374f6509f` | verified source/metadata baseline |
| CFv2.1.26 R10 | 93 | INT-MSG-060A | `02434e16eb3985d20537570ab8025bb061c7ae04cb13a8d3197e2b27d2152665` | first messaging compile failure |
| CFv2.1.26 R11 | 94 | INT-FIX-060C | `7110f94c989128150ae3b8f5059bade4c8e24c455fe1ba34726369644061fa82` | messaging compile repair |
| CFv2.1.26 R12 | 95 | INT-TUNNEL-060D | `c0c125b56c9be2a04748e2f712c4dca4ff0fbc05273059d35e3cda132a46441f` | pinned tunnel runtime |
| CFv2.1.26 R13 | 96 | INT-FIX-060F | `12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693` | tunnel operations repair |
| CFv2.1.26 R14 | 97 | INT-FIX-060H | `d11bd43ec028f44aa374b218edc53237e5763e087a6278762448a5c4bef7cea0` | native MCP-before-tunnel route |
| CFv2.1.26 R15 | 98 | INT-FIX-060J | `b69a264f225c6f03b840158f3b1896fe6e185364eb4f30e3d0bbadf6b3fc9638` | MCP compatibility port |
| CFv2.1.26 R16 | 99 | INT-FIX-060K | `8706ceccfba63a88128e1245f944fcdda1dcd4afc86546e693a9696ee1cbe8d7` | explicit IPv4 loopback binding |
| CFv2.1.26 R17 | 100 | INT-TUNNEL-DIAGNOSTICS-001E | `c45f5fd5aa8c5bac60061db7c9d5cee98517739f33206efda83a7b7598e952bf` | redacted tunnel diagnostics |
| CFv2.1.26 R18 | 101 | INT-FIX-060L | `0bf66150022ba2f35943accfb55ee03f135b936c2e441c1e0fa6cb70696ae404` | Process PID compile repair |
| CFv2.1.26 R19 | 102 | INT-FIX-060M | `356f501da34946896829d82342068318d0327ce5bf6cdf96f8649a0703e52efb` | local route readiness and credential retention |
| CFv2.1.26 R20 | 103 | INT-FIX-060N | `b18aa2cbf9940a63e8c67ea98dc37f549bf95322301efba60ffa3fde271f8f28` | Android-resolved control-plane egress |
| CFv2.1.26 R21 | 104 | INT-FIX-060P | `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c` | raw NODE_HOST loopback transport |
| CFv2.1.26 R22 | 105 | INT-DOC-060P-REPAIR | `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52` | package-internal accounting repair |
| CFv2.1.26 R23 | 106 | INT-STABILITY-063A | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | model/startup stability |
| CFv2.1.26 R24 | 107 | INT-STABILITY-065A | `20af0c617c5b8f96708fffc27d73ac6d81e473af4401aafcb170d0ec0057293f` | launch crash-loop breaker |
| CFv2.1.26 R25 | 108 | INT-STABILITY-066A | `5f195ae4c3e8f73cba974f81f8591f93c706fe546e0ed9b9af046df810602101` | isolated tunnel-process firewall |
| CFv2.1.26 R26 | 109 | update-delivery protocol | `1088e51b8c559733b73a18abac7961bb51b14b58596725058f2a10b25e7f1b2c` | embedded two-package handoff |
| CFv2.1.26 R27 | 110 | INT-STABILITY-068A | `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1` | generation-safe tunnel lifecycle |
| CFv2.1.26 R28 | 111 | INT-DOC-068B | `2187eaf0dd1f071ced561d823f169a52f185c6986f158652572a367fc62b31d0` | accounting/handoff successor |
| CFv2.1.26 R29 | 112 | INT-FIX-068C | `12517439d2bf4da501a2e0efa260d38a41ab00a8ca6a7e4586a9693737f01fc8` | Binder `Unit` compile repair |

## Pinned tunnel-runtime evidence

- SHA-256: `2e4c628f46624330ccb58d3511e33218db32bc2bcd68ac02a5fb46371686b508`
- size: `18,546,850` bytes
- runtime: tunnel-client `v0.0.10`, arm64-v8a

## Mandatory accounting rule

Every later SERVER source candidate must update package-internal `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file, `../reference/CURRENT_CANDIDATE_LINEAGE.md`, and the non-promoted candidate section of `../CURRENT_AUTHORITY.md`. The Patch Note Accounting workflow remains independent from source integrity and Android builds.
