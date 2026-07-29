# INT-DOC-AI-040B-R1-R5 — SWRLIE Runtime Candidate Documentation Sync

**Checkpoint class:** documentation synchronization only  
**Date:** 2026-07-29  
**Repository:** `kamiswrlzco-cloud/Swrlzco`  
**Project root:** `swrlz-core/`

## Purpose

Synchronize maintained repository documentation with the SERVER CFv2.1.9 SWRLIE candidate lineage that was uploaded through SWRLZ Forge after the 2026-07-28 distributed-intelligence/update-architecture documentation sync.

This checkpoint records source-candidate evidence and architecture consequences. It does **not** promote any SERVER candidate and does not change `CURRENT_AUTHORITY.md`.

## Repository evidence reviewed

Five SERVER CFv2.1.9 candidate revisions are present in repository transport lineage after the prior documentation sync:

| Rev | Checkpoint | VC | Version name | Source SHA-256 | Forge commit |
|---|---|---:|---|---|---|
| R1 | `INT-AI-040B` / `INT-AI-040B-Q4_0` | 59 | `2.1.9-swrlie-350m-local-inference-candidate-r1` | `988eb4bb108bdc0b762e20bb65c25baab014f9bab424dd7d1d5eea01b0b296f9` | `55654e3bca3b80445bb0873d545966a8a7131a29` |
| R2 | `INT-AI-040B-R2` | 60 | `2.1.9-swrlie-server-chat-settings-ia-candidate-r2` | `fe2b547ede3b16521c8a2f41cedbe00e408232d2efbb6124404bc64a7eaa1fd6` | `2ea339f972178e71819225def7f7a0d33c48636e` |
| R3 | `INT-AI-040B-R3` | 61 | `2.1.9-swrlie-startup-chat-ledger-candidate-r3` | `8012a32decc24260ed3978ead0520fa26277fea7712f71a26faadd37772bc955` | `54c64be91e0fdc0bf229a1389518707eec150356` |
| R4 | `INT-AI-040B-R4` | 62 | `2.1.9-swrlie-multimodel-context-profile-candidate-r4` | `9adaec91086f0c994194acd08865fa3797c125a87e1f885d45269d707c9b8112` | `e4955c8e0e81773fdb3583d7da5654ca20e0cbc1` |
| R5 | `INT-AI-040B-R5` | 63 | `2.1.9-swrlie-self-knowledge-candidate-r5` | `88179c35705e845ae9ad8e53ca44408b49471d7728c3a12acba1d9e219bba355` | `f158d75cba7553b7eb8a4f6d0c5ac3307f8b9be7` |

The R1 and R2 Forge uploads include candidate-manifest evidence in their transport evidence sets. The R3-R5 repository Forge uploads prove the transport/checksum identity of the candidate ZIPs; their separately packaged candidate manifests were not added by those Forge commits and therefore are not treated as repository-resident manifest evidence by this documentation checkpoint.

## Candidate progression

### R1 — local SWRLIE foundation

R1 establishes the first model-independent local neural reasoning slot on SERVER:

- SWRLZ-owned `LocalInferenceEngine` contract;
- deterministic `NoModelEngine` fallback;
- llama.cpp Android adapter boundary;
- external exact LFM2.5-350M Q4_0 bootstrap target;
- manual SERVER-private Model Vault import/verification/registration;
- Provider Mesh integration through the existing local route;
- operational inference telemetry without prompt/response capture;
- model weights remain outside source/APK.

R1 source/static evidence does not equal Android build/device evidence.

### R2 — SERVER Chat + Settings IA

R2 keeps the R1 model boundary and adds:

- first-class SERVER Chat;
- SWRLIE/local-first provider routing surface;
- Command Center composer insertion;
- nested `Chat & Commands` and `Nodes & Connections` settings domains;
- Android Back hierarchy across nested settings and Chat mode;
- Groups moved under Nodes rather than a standalone user tab.

### R3 — startup, adaptive Chat, Update Ledger, approval-tone guard

R3 adds:

- local Model Vault verification/recovery at SERVER startup;
- automatic load of an already-present verified bootstrap model;
- immediate load attempt after successful manual import;
- keyboard/IME-aware SERVER Chat layout;
- response follow/detach + `LATEST` recovery;
- single Enter newline + rapid double-Enter send;
- selectable/copyable Chat message text;
- floating dragon retained as the Android Chat bubble/interface entry point;
- horseshoe Update Ledger UI backed by packaged update history;
- explicit law that tone, mood, urgency, humor, affect, or excitement never imply approval/disapproval.

R3 does not add internet model bootstrap.

### R4 — multi-GGUF, adaptive context, inference controls, code-native Swurlzara

R4 changes the bootstrap target from an exclusive allow-list into a verified baseline while allowing compatible user-provided GGUF candidates to be staged and probed.

R4 source scope includes:

- multi-GGUF Model Vault staging and metadata/fingerprint recording;
- deep native load/inference probe before selected/known-good state is committed;
- previous/last-known-good rollback policy;
- ECO/BALANCED/QUALITY/CUSTOM inference presets;
- AUTO/2K/4K/8K/16K/32K context targets;
- output/temperature/top-K/top-P/CPU-thread/keep-loaded/memory-pressure controls where supported;
- device/model/runtime-aware context selection with a 32,768-token R4 runtime hard ceiling;
- pre-native prompt-budget guard reserving output/safety capacity and refusing silent user-prompt truncation;
- code-native bounded Swurlzara profile compilation instead of repeatedly injecting a full canonical profile manuscript;
- personality controls remain subordinate to SWRLZ Truth Firewall, approval, trust, provenance, file/node/mission/Forge authority.

R4 does not claim universal compatibility for every GGUF architecture.

### R5 — local self-knowledge and live runtime grounding

R5 adds a local-only self-knowledge layer before local SWRLIE inference:

- installed SERVER version/versionCode grounding;
- explicit USER / SWRLZ / SWRLIE / Swurlzara role map;
- shared Update Ledger repository used by both visible UI and Chat retrieval;
- prompt-relevant patch/version history retrieval, bounded to at most two entries;
- current Model Vault/model/runtime/context/preset/Swurlzara/keep-loaded/warning state retrieval;
- bounded self-knowledge bundle before local inference;
- explicit rule that unknown self-state remains unknown rather than being filled by model narrative;
- local runtime/device/model state is not silently disclosed to GPT/Gemini/Council/Compare paths.

R5 explicitly does **not** implement the future SWRLZ Skills framework, web access, model training, device file organization, GitHub writes, build promotion, release, deployment, or installation.

## Architecture consequences now documented

The R1-R5 lineage strengthens these architecture rules:

1. **SWRLZ is the control plane.** Models reason; they do not own approvals, Truth Firewall, tools, files, nodes, missions, Forge, provenance, or execution authority.
2. **SWRLIE is provider identity, not a model identity.** Underlying model, quantization, runtime, and execution node remain explicit and replaceable.
3. **Swurlzara is identity/expression, not authority.** Profile/personality controls can shape behavior but cannot change trust or authorization state.
4. **Self-knowledge is local authoritative context.** Current version/runtime/model/patch state should be retrieved from SWRLZ state and supplied to the model rather than memorized inside weights.
5. **Skills, memory, and self-knowledge remain distinct.** Skills are reusable SWRLZ capabilities; memory preserves relevant history/learned context; self-knowledge reports current authoritative state.
6. **Heavier models extend capability rather than redefine baseline behavior.** The smallest certified model should establish the behavioral floor; larger models must preserve it and add depth/context/specialization.
7. **Efficiency is first-class.** Model quality must be evaluated against latency, RAM, storage, context cost, and energy rather than model size alone.

## Evidence boundary

This documentation sync records repository source-candidate lineage and design implications only.

It does not claim:

- current SERVER authority changed from CFv2.1.0;
- Android compile/build evidence for R1-R5 merely because Forge transport exists;
- device/integration acceptance;
- model training/fine-tuning/LoRA completion;
- web research enablement;
- SWRLZ Skills implementation;
- file organizer implementation;
- promotion, release, deployment, or installation.

`docs/CURRENT_AUTHORITY.md` remains authoritative for promoted CLIENT/SERVER source identity until a separate evidence-complete promotion checkpoint changes it.
