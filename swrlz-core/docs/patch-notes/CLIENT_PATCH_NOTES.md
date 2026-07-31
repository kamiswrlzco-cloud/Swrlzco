# CLIENT Patch Notes

**Scope:** modern CLIENT source-candidate lineage after the 2026-07-29 documentation baseline.  
**Authority:** candidate/history index only. Promoted authority remains defined by `../CURRENT_AUTHORITY.md`.

Patch notes do not imply build, device acceptance, promotion, release, deployment, or installation unless separate evidence is named.

## CFv2.1.27 R1 — INT-AI-060A — current repository transport

- versionCode: `125`
- versionName: `2.1.27-truth-reasoning-expression-separation-candidate-r1`
- source SHA-256: `28074d8f2e97bec734b460e944399972920a32309ba21222a6a240642c35b433`
- Forge transport commit: `ac6e58c642d6ad58cc2f806cdb93794d0a4bf4af`
- repository transport identity: `CLIENT_CFv2.1.27_SWRLZ_CANDIDATE_R1.transport.json`

Changes:
- mirrors the shared Truth Core boundary used by SERVER-facing reasoning requests;
- keeps truth/authority standards outside personality/profile controls;
- preserves profile use as expression shaping rather than fact authority;
- removes profile-owned reasoning/provider/context semantics from active runtime shaping while retaining compatibility where required.

Validation recorded by packaged checkpoint evidence: CLIENT static `47/47`, package/manifest integrity PASS. Gradle/Android compilation was not established in the packaging environment because the Gradle distribution could not be reached.

### Identity collision notice

This candidate reused the external `CFv2.1.27 R1` identity previously used by INT-FILE-059A for different source bytes. The two sources remain distinct by SHA-256 and lineage. Future candidates must advance version and/or revision rather than reuse the identity.

## CFv2.1.27 R1 — INT-FILE-059A — packaged candidate, superseded external identity

- versionCode: `125`
- versionName: `2.1.27-file-lab-cartographer-candidate-r1`
- source SHA-256: `9bc88da752d0d310a1ddfc6c9357ce93f8115567f7a6c6eeee35f0ec77f66603`
- repository transport: not asserted by this synchronization

Changes:
- mirrors the shared Forge File Lab / Archive Cartographer foundation;
- read-only file/ZIP inventory, map/search/preview and SHA-256;
- selective extraction;
- staged text revision with new-output lineage while preserving originals;
- binary split/recombine and logical size-bounded ZIP sharding;
- SAF working/output/shard directories;
- deterministic analyzer/map export interfaces.

Validation recorded by packaged checkpoint evidence: static `41/41`, ZIP CRC/integrity and deterministic repack PASS, shared parity/protocol checks PASS. No APK/device/release/install claim.

## CFv2.1.26 R1 — INT-FORGE-054A-R2

- versionCode: `124`
- versionName: `2.1.26-forge-parity-chat-settings-candidate-r1`
- source SHA-256: `7b0202c01ea2ffbf7c7a3cb50f1e635c1eb6658299abb63de78b2b78502589eb`

Changes:
- mirrors the baseline Forge conveyor used by SERVER while preserving CLIENT-only Missions and legacy Dev Mode;
- adds shared source/manifest/SHA/lineage selection, configurable SAF lanes, Build Ledger, success artifact auto-download and failure-log auto-download controls;
- catches CLIENT Chat/Settings controls up to the shared baseline without copying SERVER-only inference authority;
- adds machine-readable patch/checkpoint lineage support.

Static verifier recorded `75/75` PASS. No APK build was claimed by the source-only packaging checkpoint.

## CFv2.1.25 R1 — INT-AI-041F-C2 provider cleanup / Model Rack parity

Changes:
- removes Gemini from active CLIENT planner/key/runtime/UI paths;
- hides public GPT/OpenAI controls while dormant backend compatibility remains;
- preserves local-first/provider-neutral routing and Model Rack behavior-shard transport direction.

The exact source SHA is preserved in its packaged checkpoint evidence; this backfill does not reassert a partial hash.

## CFv2.1.24 R1 — Model Rack Transport V2

- versionCode: `122`
- source SHA-256: `6bfa4a4b1d7d31c9f3ef3469d869c4fa35d50c4568ec2ba155ee6848cdd9fa55`

Changes:
- introduces bounded chunked model/module transport with retries;
- supports Model Rack transfer without changing SERVER model authority;
- preserves CLIENT request/preference/capability role rather than making CLIENT the model authority.

## CFv2.1.23 R1 — INT-AI-041F-A-R8

Changes:
- adds CLIENT Model Rack controls for model quality/reasoning/EQ configuration;
- adds declarative `.swrlzmod` import foundation;
- prompt/EQ behavior is live, LoRA is recognized fail-closed, knowledge/tool module types remain reserved in that checkpoint.

The exact source SHA is preserved in its packaged checkpoint evidence; this backfill does not reassert a partial hash.

## CFv2.1.22 R1 — INT-UX-039Q

- versionCode: `120`
- source SHA-256: `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`
- Forge transport commit: `1d3fa542db0f700a1f35256be9317393d25bbc8c`

Changes recorded by repository documentation:
- Update Ledger / Settings / Theme-identity candidate progression;
- checksum + candidate-manifest evidence and static validation;
- Android compilation remained pending in that checkpoint because the required Gradle distribution was unavailable.

---

## CLIENT-specific preservation rule

Shared SERVER/CLIENT Forge, Chat and Settings foundations should remain behaviorally compatible where the capability is shared. CLIENT-only Missions, legacy Dev Mode, and legitimate CLIENT-side controls remain CLIENT-specific. SERVER-only inference/model/evidence authority must not be cloned into CLIENT merely for visual parity.

## Accounting rule from 2026-07-31 onward

Every CLIENT candidate must update this file plus the component package's `ReleaseNotes.md`, `CHANGELOG.md`, and `SWRLZ_PATCH_LINEAGE_INDEX_V1.json` when those surfaces exist. See `../contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`.
