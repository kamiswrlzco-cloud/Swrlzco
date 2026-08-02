# SWRLZ-Core Continuity Handoff — 2026-08-02

Status: current-thread migration handoff  
Repository: `kamiswrlzco-cloud/Swrlzco`  
Operating rule: integrate; do not overwrite

## Start here

Use this handoff with the three-deep-analysis declaration pack. Canonical source ZIPs, SHA-256 receipts, metadata manifests, implementation files, accepted contracts, and GitHub evidence outrank narrative summaries.

## Non-negotiable project behavior

- Work one bounded checkpoint at a time.
- Separate facts, requirements, assumptions, recommendations, operator reports, and evidence.
- Preserve offline-first behavior, SWRLZ identity, trust, Truth Firewall, lineage, local-versus-remote distinctions, and protocol discipline.
- Do not infer promotion from packaging, repository transport, build success, installation, or device screenshots.
- Different source bytes require a new candidate identity.
- Update package-internal and repository patch notes for every source candidate.
- Before every stop, state approval waiting, what it authorizes, what it does not authorize, expected result, and exact approval phrase.

## Current authority and candidate matrix

| Lane | Identity | VC | Source SHA-256 | Repository/transport state |
|---|---|---:|---|---|
| Promoted CLIENT | CFv2.1.9 | 107 | `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac` | promoted authority unchanged |
| Promoted SERVER | CFv2.1.0 | 50 | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` | promoted authority unchanged |
| Current repository CLIENT candidate | CFv2.1.26 R8 | 131 | `5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912` | Forge commit `d2e54ff07759cbc74d15a88a987dd0dc1ffc6f4b`; owner-reported build success |
| Current repository SERVER candidate | CFv2.1.26 R21 | 104 | `9b1695b46513229ec1937c5f070b1cada9be4af2abaf78f8b8d417460ee80d0c` | Forge commit `dbfeed2e8edd95d06bf7e6a775b3afd237a47989`; Android build succeeded |
| Prepared documentation-only SERVER successor | CFv2.1.26 R22 | 105 | `3f730f70da5e5dbedc4cd97cfda94c5ff098c0eaa697786e2f632488d8d5ed52` | local artifact; not repository-transported |
| Prepared stability SERVER successor | CFv2.1.26 R23 | 106 | `39c1708021c76a0bf5346fa16dffe70cb6a0923b89d0a6083c22c323e973fd17` | source-only; Forge/build/device proof pending |

R23 metadata SHA-256: `670211b8d50b7d53673ee3840c5432ab626027c9d7ee6cc3c8ed6ae6f3b95fb0`.

## Completed CI/documentation foundation

INT-CI-064H was implemented through commits `c34c721`, `303f3c3`, `268fe3a`, `28317b8`, and `7ec19b9`. Resolver and changed-source mapping tests later passed 22/22 with zero skips.

Patch Note Accounting was introduced through commits `96e70898`, `187af6c8`, `694e1264`, and `eb4d0482`. It intentionally remains separate from Android builds: source may build while documentation accounting fails.

## Native MCP/tunnel progression

### R14-R16

R14 established native MCP before tunnel startup and no-OAuth loopback behavior. R15 ported the Termux-proven MCP contract, persistent SSE, complete tool catalog, exact tunnel CLI shape, and Android CA handling. R16 corrected IPv4 loopback binding consistency.

### R17-R19

R17 added rotating redacted tunnel diagnostics and capture. R18 fixed Android `Process.pid()` compilation. R19 replaced internal loopback `HttpURLConnection`, retained encrypted credentials, and proved native MCP, tunnel launch, CA bundle, and local readiness on-device.

### R20-R21

R20 added a fixed-destination Android-resolved CONNECT bridge for `api.openai.com:443` and separated local readiness from control-plane/ChatGPT route evidence. R21 replaced the final MCP-to-NODE_HOST `HttpURLConnection` hop with bounded raw IPv4 loopback HTTP and treated authenticated non-preflight `tools/call` as direct route evidence independent of downstream success.

## Current stability checkpoint — INT-STABILITY-063A

### Trigger evidence

The R21 diagnostic contains five independent SERVER/tunnel sessions in approximately 31 seconds; the first four end without orderly shutdown records. The operator separately reported repeated startup crashes while multiple LLMs were loaded/probed, plus a later full background-process loss.

### Source findings

- Automatic fleet startup was invoked from Application, foreground Service, and Chat composition.
- Fleet startup integrity-verified and native-load-probed every enabled compatible model.
- Selected residency was restored after probing without consistently respecting the normal startup residency policy.
- Heavy model work overlapped NODE_HOST, MCP, tunnel, CA, egress, database, and notification startup.

### R23 implementation

- `NodeHostService` is the sole automatic model-runtime startup owner.
- Normal startup indexes models without fleet-wide native loading.
- **PROBE ALL ENABLED** is explicit operator action.
- Automatic preload is selected-model-only, respects `keepModelLoaded`, and requires memory admission.
- Heavy model startup waits for tunnel startup to settle.
- Unclean service sessions trigger model safe mode on the next launch.
- Periodic memory watchdog and Android trim/low-memory handling can unload the resident model according to policy.
- A rotating redacted SERVER Stability Ledger and **CAPTURE STABILITY LOG** button record lifecycle, memory, and model-stage evidence without prompts, messages, credentials, proofs, model content, or tunnel payloads.

### Verification

- Focused stability verifier: 32/32 PASS.
- Pure Kotlin policy harness: PASS.
- Kotlin parser screen: zero syntax-class diagnostics.
- SERVER compiler-regression precheck: PASS.
- Source manifest: 928/928 PASS.
- Source/package verification: PASS.
- Android compile and device survival: not yet established.

## Preserved architecture

SWRLZ remains the persistent identity and authority. LLMs are replaceable reasoning equipment; Swurlzara is an expression/profile lens; Truth Firewall is intrinsic SWRLZ anatomy. R23 does not change MCP tools, NODE_HOST routes, control-plane TLS, tunnel binary, encrypted credential storage, proof/trust gates, mission/approval authority, or model bytes.

## Repository documentation synchronization

Repository documentation should identify CLIENT R8 and SERVER R21 as the current repository candidates because they have actual Forge commits. R22 and R23 must remain prepared/local successors until Forge establishes exact transport commits. Promoted authority remains unchanged.

## Immediate next actions

1. Upload R23 source and metadata through Forge.
2. Record exact Forge commit and workflow results.
3. Build and install only under separate authorization/operator action.
4. Test repeated cold starts with multiple models present.
5. Test background survival beyond one hour.
6. Capture and review `SWRLZ_SERVER_STABILITY_106.ndjson`.
7. Synchronize repository candidate pointers from R21 to R23 only after transport evidence exists.

## Approval boundary at handoff

Approval waiting: R23 Forge transport/build/device evidence.  
What approval would authorize: upload/transport documentation follow-up or a bounded repair based on R23 evidence.  
What approval would not authorize: promotion, release, deployment, trust elevation, live credential disclosure, or unrelated source changes.  
Expected result: one stable SERVER startup, retained foreground operation, and evidence-backed background survival.  
Exact approval phrase: none until the next evidence result is available.
