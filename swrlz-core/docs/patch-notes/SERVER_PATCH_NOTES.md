# SERVER Patch Notes

**Scope:** modern SERVER source-candidate lineage after the 2026-07-29 documentation baseline.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, device acceptance, promotion, release, deployment, or installation unless separate evidence is named.

## CFv2.1.25 R1 — INT-AI-060A — current repository transport

- versionCode: `83`
- versionName: `2.1.25-truth-reasoning-expression-separation-candidate-r1`
- source SHA-256: `5aa743e47c0e5474120e907f5dc2440b9333aa40245c9832e2b4e700a0a27798`
- Forge transport commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`
- repository transport identity at that commit: `SERVER_CFv2.1.25_SWRLZ_CANDIDATE_R1-1.transport.json`

Changes:
- separates non-profile Truth Core invariants from expression/profile shaping;
- centralizes truthfulness, sovereignty, speaker grounding, authority/evidence precedence, uncertainty honesty, and action-result honesty;
- prevents expression creativity from mutating reasoning sampling temperature;
- moves reasoning-depth behavior to explicit reasoning/output budgeting rather than profile density;
- keeps legacy EQ compatibility fields from silently becoming runtime truth authority.

Validation recorded by packaged checkpoint evidence: SERVER static `56/56`, compiler-regression PASS, standalone `SwrlzTruthCoreV1` Kotlin compilation PASS, package/manifest integrity PASS. Gradle/Android compilation was not established because the Gradle distribution could not be reached in the packaging environment.

### Identity collision notice

This candidate reused the external `CFv2.1.25 R1` identity previously used by INT-FILE-059A for different source bytes. The two sources must never be conflated. The current repository transport above is identified by SHA-256 and Forge commit. Future candidates must advance version and/or revision.

## CFv2.1.25 R1 — INT-FILE-059A — packaged candidate, superseded external identity

- versionCode: `83`
- versionName: `2.1.25-file-lab-cartographer-candidate-r1`
- source SHA-256: `78d7a2efa540fe0b7d9676233cde1a67b606155beb04198f4fd564b9570173ed`
- repository transport: not asserted by this synchronization

Changes:
- shared Forge File Lab / Archive Cartographer foundation;
- read-only file and ZIP inventory, hashing, structural mapping, search and preview;
- selective extraction;
- staged text revision with new-output lineage, preserving original inputs;
- byte-exact binary split/recombine and logical size-bounded ZIP sharding;
- SAF working/output/shard directory support;
- deterministic analyzer/map export surfaces for later evidence retrieval.

Validation recorded by packaged checkpoint evidence: static `41/41`, ZIP CRC/integrity and deterministic repack PASS, parity/protocol checks PASS. No APK/device/release/install claim.

## CFv2.1.24 R1 — INT-FORGE-054A-R2

- versionCode: `82`
- versionName: `2.1.24-forge-conveyor-lineage-candidate-r1`
- source SHA-256: `e5baafa58e0b71d87f7a1042db5c7c8b287d3978aca9445ad1d35661469abe00`
- Forge transport commit: `737a86f81238cc189d9ae84330e5c1fd7e5ceb01`

Changes:
- shared Forge build-conveyor baseline with CLIENT parity;
- `ASK / CLIENT / SERVER / BOTH / FILES` target model in the application candidate;
- authoritative latest-source/manifest/SHA/lineage selection;
- configurable SAF project/source/artifact/log/model/mod lanes;
- artifact auto-download and failure-log auto-download defaults;
- persistent Build Ledger and machine-readable patch/checkpoint lineage.

Static verifier recorded `68/68` PASS. No APK build was claimed by the source-only packaging checkpoint.

## CFv2.1.23 R1 — INT-PERF-052A

- versionCode: `81`
- versionName: `2.1.23-casual-short-fast-path-candidate-r1`
- source SHA-256: `c7c639996f7c0094492315c98e7b5334a63c33a76017e0522e7341092d5cbfe6`
- Forge transport commit: `faf6a249d08c976354c9437eb7073ea0fbe98fb0`

Changes:
- adds bounded `CASUAL_SHORT_FAST` routing after greeting/status fast paths;
- distinguishes acknowledgement, personal-state, and light-social updates;
- preserves USER `I/me/my` perspective and fails back to normal routing for semantic/explanatory/action requests.

## CFv2.1.22 R1 — INT-CHAT-051A

- versionCode: `80`
- versionName: `2.1.22-chat-control-orb-asset-auto-ready-candidate-r1`
- source SHA-256: `f697350829cce9aca6c8b6e6694c977b71a2710bf94126108b8ad2217079263d`
- Forge transport commit: `7b508ba7f218b94eaaaf5514484f58fd48761326`

Changes:
- compacts Chat controls into SWRLZ/status orb behavior;
- retains expanded thread/history/Command Center/model/EQ controls;
- strengthens persisted GGUF/SWRLZMOD discovery and selected-model restoration;
- preserves explicit module activation and recovery ordering.

## CFv2.1.21 R1 — INT-PERF-050D

- versionCode: `79`
- versionName: `2.1.21-status-fast-path-candidate-r1`
- source SHA-256: `756b88ce2fb6d6cf8f552968d6380cdd17227f4755b8d5f932f9873984510791`

Changes:
- adds narrow `STATUS_FAST_V1` for authoritative active model/EQ/modules/SERVER/node state;
- skips broad profile/module injection for eligible deterministic status questions;
- explanatory, multi-intent, and change requests remain on normal reasoning routes.

## CFv2.1.20 R1 — INT-PERF-050B

- versionCode: `78`
- versionName: `2.1.20-casual-greeting-fast-path-candidate-r1`
- source SHA-256: `642cde0c06f132fb71f367c970bc3c6fe8a7d566d481b8dd370542f69da44915`
- Forge transport commit: `fca443bbc8555d7de236d39c0034557fcd1e5b93`

Changes:
- introduces a greeting-only fast path with bounded directive/output;
- keeps semantic/model/status requests on normal routes;
- preserves model configuration and Truth Firewall boundaries.

Device evidence later showed a pure greeting around 1.98 seconds on the tested device/model/runtime; that observation is device-specific, not a universal benchmark.

## CFv2.1.19 R2 — INT-CHAT-045C-R2

- versionCode: `77`
- versionName: `2.1.19-chat-asset-eq-evidence-candidate-r2`
- source SHA-256: `b15916669dd6b0ca601c86093092ed2b76a22c45823e773f4f5fa29e0c9f0fa9`

Changes:
- startup scanning/import for persisted GGUF and SWRLZMOD assets;
- Chat model/EQ selectors and full Settings lab;
- built-in and LAB EQ profiles with immutable built-ins/lineage-aware custom edits;
- per-response evidence records exact model/profile/EQ/module/runtime/timing lineage;
- Chat History evidence export via SAF.

## CFv2.1.18 R1 — INT-CHAT-045B

Changes:
- smart Chat landing/follow behavior;
- message reactions, stars/comments and thread ratings;
- relational Room evidence;
- safe socket-panel details inspector;
- per-thread app-private conversation evidence/export foundation.

The exact source SHA is preserved in its packaged checkpoint evidence; this backfill does not reassert a partial hash.

## CFv2.1.17 R1 — INT-CHAT-045A

- versionCode: `74`
- source SHA-256: `e3881840dc5134c9a88052b03a8959c9d9e70bf0d4447a87490de4bc0b21aaf3`

Changes:
- Room thread/message persistence and history metadata;
- persisted SAF directories for SWRLZMOD/GGUF assets;
- exact preferred model restoration foundation;
- conversation history storage without yet injecting full history into inference.

---

## Accounting rule from 2026-07-31 onward

Every SERVER candidate must update this file plus the component package's `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` when those surfaces exist. See `../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`.
