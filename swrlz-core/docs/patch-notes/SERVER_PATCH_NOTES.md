# SERVER Patch Notes

**Scope:** SERVER source-candidate lineage, repository transport history, and prepared direct successors.  
**Authority:** Candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply Android compilation, installation, device acceptance, promotion, release, or deployment unless separate evidence is named.

## Current repository candidate — 2026-08-03

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

Changes:

- introduced proof-bound, trust-scoped `SWRLZ_ADMIN_OPERATOR` authorization for `client-swurlz`;
- validated caller role, caller capability, target policy, requested capability, approval mode, and trust state before dispatch;
- added durable message/correlation/conversation tracking and result-return routing;
- added redacted control-plane audit events and Room migration `8 -> 9`;
- preserved target-node capability truth, approval gates, identity, trust, Truth Firewall, offline-first behavior, NODE_HOST, MCP, model, and tunnel boundaries.

Repository transport proves exact R30 package identity. It does not by itself prove Android build success, installation, device acceptance, promotion, release, or deployment.

## Prepared direct successor — not yet repository transported

### CFv2.1.26 R31 — INT-CONTROL-069B

- canonical candidate: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R31`
- versionCode: `114`
- versionName: `2.1.26-persistent-admin-registry-r31`
- source SHA-256: `2ff51a057917d8280bab5e1142a964925b767e87e879e74a64dfce887ef2f5a2`
- metadata SHA-256: `ae57111b8f00b3c5cc13327d39b6e84f2381ff39d40316565d75a47257dc5685`
- checkpoint: `INT-CONTROL-069B`
- direct parent: `SERVER_CFv2.1.26_SWRLZ_CANDIDATE_R30.zip`
- Forge transport: pending
- promotion: not promoted

Changes:

- defines the non-spoofable internal principal `server-root`, type `SERVER_INTERNAL`, authority `ROOT_CONTROL_PLANE`, and `externallyAssignable=false`;
- preserves approval policy for destructive or consequential operations even when enforced by server-root;
- adds persistent registry fields for node admin role, state, granted capabilities, grant time, and granting principal;
- adds Room migration `9 -> 10` and indexed admin role/state fields;
- adds Nodes-screen actions **Promote device to admin** and **Remove admin status**, each with confirmation and redacted audit evidence;
- requires active registration, protocol 2, confirmed identity, bound proof, nonblank proof hash, non-archived lineage, and server-owned policy approval before durable admin promotion;
- prevents client self-promotion and preserves explicit revocation or suspended reapproval state;
- permits active registry admins to use only their granted capabilities; trust never fabricates target capability;
- embeds `SWRLZ_ADMIN_NODE_CONTROL_PLANE_HANDOFF_v1.0.0_2026-08-03.docx` and the checkpoint evidence inside the source package.

Source verification recorded for R31: focused verifier `30/30`, core Kotlin policy compile with bounded stubs PASS, changed-Kotlin bracket screen `6/6`, Room migration SQL harness PASS, internal source manifest `1013/1013`, source/metadata ZIP CRC and path safety PASS. Android project compilation was attempted but Gradle 8.9 could not be downloaded in the offline environment; no APK build is claimed.

## Recent direct-successor progression

| Candidate | VC | Checkpoint | Source SHA-256 | Evidence state |
|---|---:|---|---|---|
| CFv2.1.26 R23 | 106 | INT-STABILITY-063A | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | model/startup stability; Forge transported |
| CFv2.1.26 R24 | 107 | INT-STABILITY-065A | `20af0c617c5b8f96708fffc27d73ac6d81e473af4401aafcb170d0ec0057293f` | launch crash-loop breaker; Forge transported |
| CFv2.1.26 R25 | 108 | INT-STABILITY-066A | `5f195ae4c3e8f73cba974f81f8591f93c706fe546e0ed9b9af046df810602101` | isolated tunnel-process firewall; local source identity retained |
| CFv2.1.26 R26 | 109 | update-delivery protocol | `1088e51b8c559733b73a18abac7961bb51b14b58596725058f2a10b25e7f1b2c` | embedded two-package handoff; Forge transported |
| CFv2.1.26 R27 | 110 | INT-STABILITY-068A | `0549e79d5d89b6833b234dfa56a3bc219b5dbe681e9cc4f48d7e02d3e00a2eb1` | generation-safe tunnel lifecycle; Forge transported |
| CFv2.1.26 R28 | 111 | INT-DOC-068B | `2187eaf0dd1f071ced561d823f169a52f185c6986f158652572a367fc62b31d0` | accounting/handoff successor; Forge transported |
| CFv2.1.26 R29 | 112 | INT-FIX-068C | `12517439d2bf4da501a2e0efa260d38a41ab00a8ca6a7e4586a9693737f01fc8` | Binder `Unit` compile repair; Forge transported and owner-reported successful build |
| CFv2.1.26 R30 | 113 | INT-CONTROL-069A | `d07e814ab986491c2035854310630fe2638d5693ce9bd463ed665c82eeb19414` | current repository candidate; authorized operator/correlation control plane |
| CFv2.1.26 R31 | 114 | INT-CONTROL-069B | `2ff51a057917d8280bab5e1142a964925b767e87e879e74a64dfce887ef2f5a2` | prepared persistent admin registry/server-root successor |

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

## Pinned tunnel-runtime evidence

- SHA-256: `2e4c628f46624330ccb58d3511e33218db32bc2bcd68ac02a5fb46371686b508`
- size: `18,546,850` bytes
- runtime: tunnel-client `v0.0.10`, arm64-v8a

## Authority and accounting boundaries

- The internal `server-root` principal is SERVER runtime authority, not a promoted source-package declaration.
- A node marked admin remains a client principal and cannot claim `server-root`.
- Connected state, node label, or client-supplied role text never grants trust or admin authority.
- Promotion to node admin is a consequential registry write and must be server-owned, audited, proof-gated, and user-confirmed.
- Destructive execution remains policy/approval-gated.
- Repository transport proves package identity only.
- Android build success does not prove installation, device acceptance, promotion, release, or deployment.
- Promoted authority changes only through an explicit promotion checkpoint.

## Mandatory accounting rule

Every later SERVER source candidate must update package-internal `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`, plus this repository file, `../reference/CURRENT_CANDIDATE_LINEAGE.md`, and the non-promoted candidate section of `../CURRENT_AUTHORITY.md`. The Patch Note Accounting workflow is independent from source integrity and Android builds; one gate can pass while another fails.
