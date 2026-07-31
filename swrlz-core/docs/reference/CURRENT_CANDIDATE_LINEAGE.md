# Current CLIENT / SERVER Candidate Lineage — 2026-07-31

This file tracks the newest source-candidate/evidence lineage independently from promoted authority. `../CURRENT_AUTHORITY.md` remains the promotion authority until an explicit promotion checkpoint changes it.

## Current repository transport

Repository Forge commit `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af` uploaded the current source transports:

| Component | Logical candidate | VC | Source SHA-256 | Checkpoint / content identity | Repository transport |
|---|---|---:|---|---|---|
| CLIENT | CFv2.1.27 R1 | 125 | `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433` | INT-AI-060A truth/reasoning/expression separation | `sources/client/CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1.transport.json` |
| SERVER | CFv2.1.25 R1 | 83 | `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798` | INT-AI-060A truth/reasoning/expression separation | `sources/server/SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1.transport.json` |

The SERVER `-1` transport filename is repository transport identity. Do not infer semantic equivalence from the suffix alone; source SHA-256 and checkpoint lineage remain decisive.

## Immediately preceding packaged candidates

INT-FILE-059A produced different source bytes using the same external component version/revision identifiers:

| Component | External candidate identity | VC | Source SHA-256 | versionName | Repository transport claim |
|---|---|---:|---|---|---|
| CLIENT | CFv2.1.27 R1 | 125 | `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603` | `2.1.27-file-lab-cartographer-candidate-r1` | none asserted here |
| SERVER | CFv2.1.25 R1 | 83 | `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed` | `2.1.25-file-lab-cartographer-candidate-r1` | none asserted here |

This is an **external identity collision**. The 059A and 060A packages must remain separate by exact SHA-256, versionName and checkpoint provenance. The next candidate must advance version and/or revision; it must not silently overwrite either history.

## Shared Forge baseline parent

INT-FORGE-054A-R2 established the shared Forge conveyor / CLIENT parity parent lineage:

| Component | Candidate | VC | Source SHA-256 | versionName |
|---|---|---:|---|---|
| CLIENT | CFv2.1.26 R1 | 124 | `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb` | `2.1.26-forge-parity-chat-settings-candidate-r1` |
| SERVER | CFv2.1.24 R1 | 82 | `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00` | `2.1.24-forge-conveyor-lineage-candidate-r1` |

The SERVER parent transport is evidenced by Forge commit `737a86f81238cc189d9ae84330e5c1fd7e5ceb01`.

## Candidate feature progression since the 041H documentation baseline

SERVER progression includes persistence/evidence assets, greeting/status/casual fast paths, compact Chat/status controls, Forge conveyor/lineage, File Lab/Cartographer packaging, and truth/reasoning/expression separation. CLIENT progression includes Model Rack/module transport, provider cleanup, Forge parity/Chat/Settings catch-up, File Lab/Cartographer packaging, and truth/reasoning/expression separation.

Detailed component notes are maintained in:

- `../patch-notes/SERVER_PATCH_NOTES.md`
- `../patch-notes/CLIENT_PATCH_NOTES.md`

## Evidence boundary

- Repository transport/checksum proves repository source identity, not Android compilation or APK success.
- Packaged static validation proves only the validation actually recorded by that checkpoint.
- Device screenshots/operator reports are working-state evidence only to the degree explicitly stated.
- Candidate lineage does not change promoted authority.
- Downloaded, built, installed, promoted, released and deployed are distinct states.
