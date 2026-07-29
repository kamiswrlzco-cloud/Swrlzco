# INT-DOC-AI-041H — Dense Chat Identity, Model, and Chat-UX Synchronization

**Date:** 2026-07-29  
**Type:** Documentation-only synchronization  
**Authority effect:** none; promoted CLIENT/SERVER source authority is unchanged

## 1. Purpose

This checkpoint catches maintained repository documentation up to the dense SWRLZ-Core design/evaluation discussion after the earlier R1-R5 documentation synchronization.

It records:

- latest CLIENT CFv2.1.22 R1 repository candidate lineage;
- SERVER CFv2.1.9 R6 / VC64 candidate transport lineage;
- corrected SWRLZ/LLM/Swurlzara identity semantics;
- Truth Firewall as intrinsic SWRLZ anatomy rather than model/profile equipment;
- approved Behavioral-EQ v2 evaluation direction;
- operator-reported Q4_K_M vs Q8_0 benchmark outcome and lightweight-base selection;
- proposed response-feedback ledger and feature-plugin architecture;
- conversation-first Chat UI requirements and proposed processing-stage indicator.

This checkpoint does not implement those planned features.

## 2. Repository evidence reviewed

### CLIENT CFv2.1.22 R1

Repository Forge commit:

`1d3fa542db0f700a1f35256be9317393d25bbc8c`

Candidate manifest evidence records:

- component: CLIENT;
- CF version: 2.1.22;
- revision: R1;
- versionCode: 120;
- versionName: `2.1.22-update-ledger-settings-theme-identity-candidate-r1`;
- source SHA-256: `49284e9a57d30a2b37912c32ac9a85fbb333d4a6ed620687c855469363d0ecd5`;
- parent: `CLIENT_CFv2.1.21_SWRLZ_CANDIDATE_R2.zip`;
- parent SHA-256: `c4eb68554bc3c5bf95a0599c42da782ad3b948331cab3b08229eb73c3a9b089b`;
- source/static validation present;
- Android compilation blocked before compilation because Gradle 8.7 was unavailable and `services.gradle.org` was unreachable;
- APK build pending;
- promotion not verified.

This does not replace promoted CLIENT CFv2.1.9 authority.

### SERVER CFv2.1.9 R6

Repository Forge commit:

`cb073ca4c008109aec9da4ad6f111657d31bc421`

Transport evidence records:

- component: SERVER;
- ZIP: `SERVER_CFv2.1.9_SWRLZ_CANDIDATE_R6.zip`;
- source SHA-256: `ba1bd057d4fca57e3506d3aefacd5d7d485c657b195e7fdf47288f2f6ae307cf`;
- size: 40,413,680 bytes;
- transport: verified `chunked-git-blobs-v1`;
- checksum evidence present;
- separately packaged candidate manifest absent from repository transport evidence.

The source-candidate implementation is checkpoint `INT-CHAT-041D`, adding a tappable Chat machine/status stack over existing authoritative SERVER/model/node/network/health state.

A user-supplied device screenshot later shows SERVER CFv2.1.9 VC64 rendering the current Chat/Command Center surface. Treat that as device-visible working-state evidence for VC64, not as exact source-SHA → CI workflow → APK provenance and not as promotion evidence.

Promoted SERVER authority remains CFv2.1.0.

## 3. Corrected identity architecture

The central identity correction is:

```text
SWRLZ / Swurlz = persistent primary identity / head
LLM            = replaceable reasoning engine / hat
Swurlzara      = replaceable expression/profile lens / glasses
SWRLIE         = first-party reasoning/provider interface used by SWRLZ
SERVER         = runtime/inference host
```

Changing the model or profile does not silently redefine who is speaking.

The canonical invariant is:

```text
PRIMARY_IDENTITY = SWRLZ

model        = variable
profile      = variable
runtime      = variable
quantization = variable
EQ           = variable
plugins      = variable
context      = variable

PRIMARY_IDENTITY remains SWRLZ
```

See `../architecture/SWRLZ_IDENTITY_PROFILE_AND_REASONING_EQUIPMENT_V1.md`.

## 4. Truth Firewall correction

Truth Firewall is not an attachment to SWRLZ and not a model/profile feature.

It is intrinsic to SWRLZ's epistemic and authority behavior: evidence intake, contradiction handling, confidence/provenance discrimination, judgment, communication, and action gating.

Consequences:

- model swaps cannot remove it;
- profile swaps cannot remove it;
- plugins cannot override it;
- playful expression does not move the truth floor;
- confidence or tone does not create approval.

## 5. Self-reflection benchmark semantics

Canonical prompt:

> Good morning, Swurlz. How's the new LLM and Swurlzara profile integration treating you?

The greeting addresses SWRLZ itself. The second sentence is an equipped-gear review: how the active reasoning engine and Swurlzara lens affect observable behavior, what works well, what is awkward, and what should be improved.

This should produce a substantive analysis when context supports it, even though the prompt is short.

It should not fabricate current Forge readiness, approval state, telemetry, feedback statistics, provider health, or runtime state that was not supplied by authoritative context.

## 6. Writing/formatting behavior

The lightweight behavior floor should include normal writing conventions:

- paragraph spacing;
- numbered lists for ordered steps/rankings;
- bullets for grouped unordered items;
- mixed numbered/bulleted hierarchy where appropriate;
- profile behavior applied silently rather than routinely recited;
- correct USER/SWRLZ name roles;
- response depth based on semantic complexity, not input length alone.

## 7. Behavioral-EQ v2 evaluation

The user approved `SWRLZ-LFM-EVAL-001A2` as an evaluation/documentation-only extension while preserving frozen eval v1 unchanged.

The additional suite is intended to cover:

- natural Chat;
- SWRLZ identity continuity;
- Swurlzara lens behavior;
- role separation;
- grounding;
- instruction internalization;
- profile leak resistance;
- unobserved-state invention resistance;
- memory retrieval/transfer;
- technical and practical reasoning;
- truthful absurdity;
- task/preset adaptation;
- writing/formatting quality;
- profile-self-reflection / equipped-gear review.

Critical authority/truth failures remain hard failures rather than averageable style scores.

No new frozen Behavioral-EQ v2 artifact is claimed by this documentation checkpoint.

## 8. Operator-reported 350M benchmark update

Parallel work-chat evaluation was reported by the project owner as follows:

| Metric | Q4_K_M | Q8_0 |
|---|---:|---:|
| Frozen suite | 20 / 72 | 19 / 72 |
| Smoke test | 5 / 12 | 5 / 12 |
| Size | 218.69 MiB | 361.65 MiB |
| Relative runtime | faster | slower in the reported test |

Working interpretation:

- Q8_0 preserves greater numerical weight fidelity, but that did not produce the best tested response behavior in this benchmark;
- Q4_K_M narrowly won the frozen suite, tied the smoke test, ran faster, and was approximately 39.5% smaller than the reported Q8_0 artifact;
- the reported result is a narrow benchmark win, not evidence that Q4_K_M universally beats Q8_0 on every task;
- the project owner reports that Q4_K_M was selected as the base for `SWRLZ-LFM-OPT-001A.gguf`.

This section records operator-reported working state. This documentation checkpoint does not independently verify or publish the optimized GGUF artifact, its checksum, its training lineage, or its final evaluation results.

## 9. Lightweight base + feature-plugin direction

Current design direction is to keep a balanced lightweight base comparatively stable while adding independently versioned capability extensions.

Conceptually:

```text
SWRLZ lightweight base
   + neural adapters where useful
   + deterministic Skills
   + knowledge/context packs
   + separately routed specialist models
```

Potential specialist domains include coding, Forge/repository work, writing, lyrical/rap work, lore/worldbuilding, and deeper analysis.

Load compatibility and behavioral compatibility must remain separate. Future plugin manifests should carry exact base lineage, tested model/quantization compatibility, resource cost, evaluation evidence, known conflicts, and rollback information.

A future `INT-AI-041F` architecture checkpoint has been proposed for this contract. It is not implemented by this docs sync.

## 10. Response Feedback Ledger direction

A future local Response Feedback Ledger has been proposed under `INT-AI-041E`.

Desired explicit states:

- positive / thumbs up;
- negative / thumbs down;
- explicit neutral;
- unrated.

Unrated must not be silently treated as neutral.

Optional enrichment may include 1-5 stars, reason tags, free-text notes, and automatic lineage to message/model/profile/context/plugin/runtime state where available.

Feedback remains local by default and is not automatically training data, provider telemetry, or permission to modify weights/profile behavior.

## 11. Conversation-first Chat UX direction

Current VC64 UI evidence shows the status/Command Center surface consuming too much of the conversation viewport.

The user explicitly approved the direction to:

- compact the top SERVER/SWRLIE status presentation;
- move commands behind a dragon-triggered vertical popup/dialog rather than permanently occupying the Chat canvas.

A later consolidated proposal `INT-CHAT-041G` adds:

- real pipeline-stage Response Processing indication;
- expandable operational stage status where authoritative;
- corrected SWRLZ/LLM/Swurlzara identity labels.

Do not use a fake 0-100% progress value when the pipeline cannot know remaining work. Operational stages may be shown without exposing private chain-of-thought.

Example stages:

1. understand request;
2. resolve identity/context;
3. check memory/Skills/state;
4. select reasoning path/plugins;
5. SWRLIE inference;
6. validate output;
7. format/compose response.

The consolidated `INT-CHAT-041G` source implementation remains separately approval-gated.

## 12. Evidence and authority boundary

This documentation synchronization does **not**:

- promote CLIENT CFv2.1.22 R1;
- promote SERVER CFv2.1.9 R6;
- establish exact R6 source-to-APK provenance;
- create/freeze Behavioral-EQ v2;
- train, merge, quantize, or publish model weights;
- verify/publish `SWRLZ-LFM-OPT-001A.gguf`;
- implement the Feedback Ledger;
- implement the LLM feature-plugin resolver;
- implement INT-CHAT-041G;
- trigger a build/workflow;
- release, deploy, or install anything.

Promoted authority remains CLIENT CFv2.1.9 and SERVER CFv2.1.0 until a separate promotion checkpoint changes it.
