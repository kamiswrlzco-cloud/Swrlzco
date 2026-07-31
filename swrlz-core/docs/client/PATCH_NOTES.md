# CLIENT Patch Notes

Maintained CLIENT update ledger for the active `kamiswrlzco-cloud/Swrlzco` repository.

## Evidence policy

Patch notes record implementation/candidate history without silently promoting it. Authority remains governed by `../CURRENT_AUTHORITY.md`, canonical source ZIP/SHA evidence, accepted contracts, and accepted build/device evidence. A repository transport upload proves only the transported candidate identity unless stronger evidence is explicitly linked.

Every accepted CLIENT implementation checkpoint should add an entry here at packaging/documentation time. Different source bytes must retain distinct candidate identity and lineage.

## 2026-07-31 — latest repository transport: CLIENT CFv2.1.27 R1

- Repository path identity: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1`.
- Whole-source SHA-256 declared by verified chunk transport: `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`.
- Forge upload commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`.
- Transport: `chunked-git-blobs-v1`, 4 chunks, 15,127,739 bytes reconstructed whole ZIP.
- Repository transport includes checksum evidence but no separately packaged candidate manifest.
- This entry therefore records source-transport identity only. It does not infer Android compilation, APK output, device acceptance, promotion, release, deployment, installation, or the internal checkpoint contents of CFv2.1.27.

## 2026-07-31 — CLIENT CFv2.1.26 R1 — INT-FORGE-054A-R2

- versionCode: `124`.
- versionName: `2.1.26-forge-parity-chat-settings-candidate-r1`.
- Source SHA-256: `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`.
- Parent: CLIENT CFv2.1.25 R1, SHA `6ce26560dab4113d06bb1360c260dcc087fc2fa8b583f1583ada2bfe3688f5b2`.
- Mirrors the shared Forge build-conveyor baseline from SERVER while preserving CLIENT-specific Missions, legacy Dev Mode, CLIENT-side execution roles, and the SERVER authority split.
- Adds ASK/CLIENT/SERVER/BOTH/FILES Forge target modes; authoritative latest-source selection using component/version/manifest/SHA/lineage; configurable SAF root/source/artifact/log/model/mod/evidence directories; successful-artifact and failed-workflow-log auto-download defaults; persistent Build Ledger state; local CLIENT Chat history continuity; paired-SERVER model selection; and machine-readable patch/checkpoint lineage.
- No automatic APK installation, protocol-version change, Truth Firewall authority change, model/GGUF/SWRLZMOD content change, release, deployment, or installation is claimed by the source checkpoint.

## CLIENT CFv2.1.25 R1 — behavior-shard/provider cleanup lineage

- versionCode: `123`.
- versionName: `2.1.25-behavior-shard-v1-candidate-r1`.
- Source SHA-256: `6ce26560dab4113d06bb1360c260dcc087fc2fa8b583f1583ada2bfe3688f5b2`.
- Removes active Gemini planner/key/runtime/UI dependence and hides public GPT/OpenAI controls while preserving dormant compatibility where intentionally retained.
- Aligns CLIENT with the behavior-shard/provider-cleanup direction while keeping SWRLZ identity, Truth Firewall, offline-first policy, and SERVER-owned reasoning/model authority intact.

## CLIENT CFv2.1.24 R1 — INT-FORGE-042B

- versionCode: `122`.
- Source SHA-256: `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55`.
- Forge Transport V2: 4 MiB protected-source chunks, bounded transient per-blob retries, authentication/repository reprobe, verified resume, and richer diagnostics.
- Repairs the missing `@Composable` on `ChatSettingsChoiceGroup` that blocked the preceding build attempt.

## CLIENT CFv2.1.23 R1 — INT-AI-041F-A-R8

- Modular Model Rack + Expression EQ candidate.
- Adds SERVER GGUF selection, speed/reasoning-depth/context/output controls, nine EQ controls, module/profile/model state, rollback, and registered paired-LAN control routing while SERVER remains authoritative.
- Exact optimized-model recognition and immutable Truth Firewall/permission/approval/provenance/trust/mission/Forge/execution boundaries remain explicit.
- No GGUF bytes or promotion are implied by this CLIENT candidate.

## CLIENT CFv2.1.22 R1 — INT-UX-039Q

- versionCode: `120`.
- versionName: `2.1.22-update-ledger-settings-theme-identity-candidate-r1`.
- Source SHA-256: `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`.
- Adds local evidence-aware Update Ledger, version-specific update queries, nested Settings hierarchy, application-level Back behavior, and primary/complementary SWRLZ-owned theme identity treatment.
- Repository candidate evidence records static/source validation; Android compilation was blocked before compilation in the recorded attempt.

## Earlier maintained lineage

Earlier CLIENT source packages and patch reports remain preserved in source lineage and repository documentation. Notable sequence includes adaptive Chat, hierarchical Command Center grammar, Forge chunk transport, Forge rescue/bootstrap work, theme progress/ignition work, and the CFv2.1.9 promoted package-pair repair. These records are not deleted or rewritten by this ledger.

## Approved but not yet implementation-evidenced here — INT-FILE-059A

`INT-FILE-059A` is approved for a shared CLIENT/SERVER Forge File Lab + Archive Cartographer foundation: read-only inventory/search/hash/map/preview/selective extraction, staged text editing and archive-entry replacement with explicit commit/new checksum/parent lineage, binary split/exact recombination, logical size-bounded shard archives with manifests/provenance, configurable SAF work/output/shard directories, and deterministic analyzer APIs for later SWRLZ evidence retrieval.

This approval is not itself proof that a specific CLIENT source package implements 059A. Implementation/package evidence must be linked separately before this section is promoted to an implemented candidate entry.

## Documentation rule going forward

A CLIENT source update is not documentation-complete until its checkpoint/version/parent/change summary/evidence boundary is represented in this file and linked into the repository engineering/documentation indexes.
