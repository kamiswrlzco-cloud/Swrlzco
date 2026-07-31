# SERVER Patch Notes

Maintained SERVER update ledger for the active `kamiswrlzco-cloud/Swrlzco` repository.

## Evidence policy

Patch notes preserve source-candidate progression without silently promoting it. Current promoted SERVER authority remains governed by `../CURRENT_AUTHORITY.md`; candidate transport, static validation, build evidence, device evidence, promotion, release, deployment, and installation are distinct evidence classes.

Every accepted SERVER implementation checkpoint should add an entry here at packaging/documentation time. Different source bytes must retain distinct candidate identity and lineage.

## 2026-07-31 — latest repository transport: SERVER CFv2.1.25 R1

- Repository path identity: `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1`.
- Whole-source SHA-256 declared by verified chunk transport: `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`.
- Forge upload commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`.
- Transport: `chunked-git-blobs-v1`, 10 chunks, 40,710,681 bytes reconstructed whole ZIP.
- Repository transport includes checksum evidence but no separately packaged candidate manifest.
- This entry therefore records source-transport identity only. It does not infer Android compilation, APK output, device acceptance, promotion, release, deployment, installation, or the internal checkpoint contents of CFv2.1.25.

## 2026-07-31 — SERVER CFv2.1.24 R1 — INT-FORGE-054A-R2

- versionCode: `82`.
- versionName: `2.1.24-forge-conveyor-lineage-candidate-r1`.
- Source SHA-256: `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`.
- Parent: SERVER CFv2.1.23 R1, SHA `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6`.
- Adds the shared Forge build-conveyor baseline: ASK/CLIENT/SERVER/BOTH/FILES target modes; authoritative latest-source selection using component/version/manifest/SHA/lineage; configurable SAF root/source/artifact/log/model/mod/evidence directories; user-initiated verify/upload/build/watch flow through existing GitHub transport; successful-artifact and failed-workflow-log auto-download defaults; persistent Build Ledger state; and machine-readable patch/checkpoint lineage.
- SERVER keeps its broader runtime/inference/model/evidence authority; shared Forge behavior is mirrored to CLIENT without collapsing role boundaries.
- No automatic APK installation, protocol-version change, Truth Firewall authority change, model/GGUF/SWRLZMOD content change, release, deployment, or installation is claimed by the source checkpoint.

## SERVER CFv2.1.23 R1 — INT-PERF-052A

- versionCode: `81`.
- versionName: `2.1.23-casual-short-fast-path-candidate-r1`.
- Source SHA-256: `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6`.
- Adds conservative `CASUAL_SHORT_FAST` routing for acknowledgements, user personal-state updates, and light social follow-ups while preserving USER/SWRLZ perspective.
- Rejects questions, technical/control/source/code requests, long/multi-line turns, and uncertain prompts to the normal route.
- Preserves 050B greeting and 050D status fast paths plus model/context/sampling/thread/residency configuration.

## SERVER CFv2.1.22 R1 — INT-CHAT-051A

- Source SHA-256: `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d`.
- Collapses oversized Chat header/status controls into a compact SWRLZ/status orb while retaining thread/title/history/new/Command Center/model/EQ/status access when expanded.
- Adds direct Chat model switching with SERVER-authoritative verification/compatibility probing and recovery ordering.
- Startup restores/scans persisted GGUF/SWRLZMOD locations without silently activating newly discovered modules.

## SERVER CFv2.1.21 R1 — INT-PERF-050D

- Source SHA-256: `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791`.
- Adds narrow `STATUS_FAST_V1` routing for active model, active EQ/profile, active modules, SERVER version, and node identity.
- Uses only required authoritative state and falls back to normal reasoning for explanatory, multi-intent, or change requests.

## SERVER CFv2.1.20 R1 — INT-PERF-050B

- Source SHA-256: `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915`.
- Adds a greeting-only fast path with tiny directive/output budget while preserving normal Chat/disclosure/model configuration for semantic requests.
- Device evidence later showed the pure greeting route cutting latency dramatically relative to the earlier full-prompt path; this does not imply the normal reasoning path shares the same latency.

## SERVER CFv2.1.19 R2 — INT-CHAT-045C

- Source SHA-256: `b15916669dd6b0ca601c86093092ed2b76a22c45823e773f4f5fa29e0c9f0fa9`.
- Startup GGUF/SWRLZMOD discovery/import from persisted SAF folders; explicit model and EQ-profile selection; immutable per-response runtime/model/profile/module evidence; and user-triggered Chat History evidence ZIP export.
- No silent module activation, training, weight modification, or broad storage permission is implied.

## SERVER CFv2.1.18 R1 — INT-CHAT-045B

- Source SHA-256: `360bf097...` in prior checkpoint evidence; exact full SHA remains in the accepted source/evidence package.
- Adds smart response landing/new-response jump behavior, per-response/thread reactions, optional stars/comments, Room relational evidence, safe response-construction details, and per-thread JSON/Markdown evidence.
- Hidden prompts/private chain-of-thought/credentials/internal wiring remain excluded.

## SERVER CFv2.1.17 R1 — INT-CHAT-045A

- Source SHA-256: `e3881840dc5134c9a88052b03a8959c9d9e70bf0d4447a87490de4bc0b21aaf3`.
- Adds persistent Room chat threads/messages/history metadata plus persisted SAF model/module directories and verified discovery/import.
- History is saved but not automatically injected into inference at this checkpoint.

## SERVER CFv2.1.16 R1 — INT-FIX-041F-C2C

- Name-cue invariance, CASUAL/STATUS/ARCHITECTURE/DEBUG classification, relevance gating, compact Mirror behavior, and protections against profile/workspace reification.
- Unknown terms do not become runtime status facts.

## SERVER CFv2.1.15 R1 — INT-FIX-041F-C2B

- Positive-only behavior compiler with bounded foundation/shard/directive budgets and telemetry; tone influences style without inventing pseudo-QA history.

## SERVER CFv2.1.14 R1 — INT-FIX-041F-C2A

- Repairs the bounded C2 SERVER Kotlin blockers while preserving provider cleanup and behavior-shard architecture.

## SERVER CFv2.1.13 R1 — INT-AI-041F-C2

- Removes active Gemini runtime/key/planner/UI dependence from the current architecture path while preserving intentionally dormant compatibility.
- Adds Model Rack V2 behavior-shard parity/import validation/compiler/routing direction.

## SERVER CFv2.1.10 R1 — INT-AI-041F-A-R8

- Modular Model Rack + Expression EQ SERVER half with exact optimized-GGUF identity, per-model profiles, Speed/Depth/EQ controls, declarative prompt/EQ module import, rollback, and paired-LAN control plane.
- LoRA activation remains recognized but fail-closed in this lineage.

## Earlier maintained lineage

SERVER CFv2.1.9 R1-R8 and earlier source histories remain preserved in repository documentation/source lineage. They cover the SWRLIE local inference foundation, SERVER Chat/Settings, startup/model recovery, Model Vault/safe switching, self-knowledge/runtime grounding, status-stack/Command Center progression, and later modular-model work. Historical records are retained rather than rewritten.

## Approved but not yet implementation-evidenced here — INT-FILE-059A

`INT-FILE-059A` is approved for a shared CLIENT/SERVER Forge File Lab + Archive Cartographer foundation: read-only inventory/search/hash/map/preview/selective extraction, staged text editing and archive-entry replacement with explicit commit/new checksum/parent lineage, binary split/exact recombination, logical size-bounded shard archives with manifests/provenance, configurable SAF work/output/shard directories, and deterministic analyzer APIs for later SWRLZ evidence retrieval.

This approval is not itself proof that a specific SERVER source package implements 059A. Implementation/package evidence must be linked separately before this section is promoted to an implemented candidate entry.

## Documentation rule going forward

A SERVER source update is not documentation-complete until its checkpoint/version/parent/change summary/evidence boundary is represented in this file and linked into the repository engineering/documentation indexes.
