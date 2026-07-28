# SWRLZ Distributed Intelligence Architecture v1.0

**Status:** Architecture / design consolidation. This document records the intended architecture and current evidence discussed through 2026-07-28. It does **not** claim that every described component is implemented.

**Project:** SWRLZ-Core

**Primary design rule:** SWRLZ remains SWRLZ regardless of which neural model, inference runtime, SERVER node, or online provider is available. Models are replaceable reasoning modules, not the identity or authority of the system.

---

## 1. Executive Summary

SWRLZ is converging on a distributed, offline-first assistant architecture with a lightweight Android CLIENT and a heavyweight SERVER. The CLIENT is the complete local expert for Android, SWRLZ itself, its interface, permissions, device state, local missions, local files, and local execution. The SERVER owns heavyweight general reasoning, local LLM inference, online research, large file and screenshot analysis, Forge/GitHub network operations, model lifecycle, and multi-node coordination.

The architecture intentionally resembles a durable multiplayer-game architecture without turning SWRLZ into a game: local input and rendering stay responsive, authoritative responsibilities are separated, data is scoped to the task, and expensive work is delegated to a SERVER. CLIENT operation is event-driven rather than continuously polling or inferring.

Three primary operating modes are defined:

1. **SWRLZ LOCAL:** CLIENT works without any SERVER. Android/SWRLZ-domain features remain available; broad/general reasoning and online research that require SERVER are unavailable.
2. **SWRLZ LAN:** CLIENT has a reachable SERVER over LAN, but the SERVER has no internet. SWRLIE/local-model reasoning is available from the model's weights and local knowledge stores, but current web research is unavailable.
3. **SWRLZ ONLINE:** CLIENT has a reachable SERVER and the SERVER has internet. Local model reasoning, online research, GitHub/Forge operations, model updates, and other explicitly permitted external work can run through SERVER.

A degraded state is also recognized when SERVER was expected but is temporarily unreachable.

SWRLZ will keep CLIENT, SERVER, and MODEL as independent versioned product lines. Large model weights should not be embedded into CLIENT/SERVER source archives or APKs. Model packages are installed separately, verified, persisted in a Model Vault, and restored/re-registered after compatible app updates or reinstalls when possible.

The first-party reasoning provider identity is **SWRLIE**. Initially SWRLIE may route to third-party open-weight base models. Over time those models act as teachers/crutches while SWRLZ-specific datasets, evaluation, fine-tuning, adapters, and distillation produce increasingly SWRLZ-native reasoning models.

---

## 2. Architecture Laws

### 2.1 SWRLZ is not the LLM

The neural model is a detachable reasoning engine. SWRLZ owns conversation state, identity, memory, Truth Firewall, permissions, capability routing, mission execution, device ownership, file authority, Forge policy, node trust, and provenance.

Removing or replacing a model must not collapse Chat or the rest of SWRLZ.

### 2.2 CLIENT domain sovereignty

CLIENT maintains authoritative local knowledge of:

- SWRLZ CLIENT runtime and interface.
- Android device state and capabilities.
- Accessibility/UI semantics and observed screen state.
- Local permissions and user-authorized storage roots.
- Local missions and execution state.
- Local command/capability catalog.
- Patch/update knowledge bundled with the CLIENT.
- Local files and artifacts the CLIENT is allowed to inspect.

CLIENT is the final executor of actions on its own Android device.

### 2.3 SERVER reasoning and network sovereignty

SERVER owns heavyweight work outside the CLIENT's bounded Android/SWRLZ domain, including:

- Local LLM/SWRLIE inference.
- Broad/general reasoning.
- Online research and search.
- Heavy screenshot/image/document analysis.
- GitHub/Forge writes and workflow/network integration.
- Model package storage, activation, verification, and updates.
- Multi-node coordination and shared state.

### 2.4 No open-web research from CLIENT

CLIENT does not perform open-ended internet search or general URL retrieval. Out-of-domain or current-information requests route to SERVER. If no SERVER is reachable, the request is explicitly unavailable rather than silently switching to a CLIENT web path.

Narrow CLIENT network operations may exist for bootstrap/recovery, SERVER communication, node discovery/enrollment, and tightly scoped self-update behavior. These are protocol operations, not open-ended research.

### 2.5 Task-scoped disclosure

CLIENT may know its entire local Android/SWRLZ world, but it sends SERVER only the context relevant to the current task and policy. SERVER does not automatically receive full device storage, full UI history, unrelated conversation data, or credentials.

### 2.6 Mutual validation

SERVER does not blindly trust CLIENT requests. CLIENT does not blindly execute SERVER proposals. Each side validates the operation against its own authority boundary, current state, protocol version, trust state, and approvals.

### 2.7 Event-driven CLIENT

CLIENT should feel fluid like a well-architected game client, but it must not run an unnecessary continuous game loop. Work is triggered by user input, accessibility changes, scheduled work, node/network events, notifications, and meaningful state changes. When nothing is happening, CLIENT should sleep.

---

## 3. Product and Authority Topology

```text
                         SWRLZ ECOSYSTEM

                          ┌───────────┐
                          │   USER    │
                          └─────┬─────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   ANDROID CLIENT    │
                    │ cockpit + local     │
                    │ domain authority    │
                    └─────────┬───────────┘
                              │ authenticated LAN / private route
                              ▼
                    ┌─────────────────────┐
                    │       SERVER        │
                    │ reasoning + network │
                    │ + Forge + nodes     │
                    └──────┬───────┬──────┘
                           │       │
                    ┌──────▼───┐ ┌─▼──────────┐
                    │ SWRLIE   │ │ GitHub/Web │
                    │ models   │ │ external   │
                    └──────────┘ └────────────┘
```

CLIENT and SERVER remain independent product lines. MODEL is a third independent product line.

```text
CLIENT CFvX.Y.Z
SERVER CFvA.B.C
SWRLIE MODEL MPvM.N.P
```

Compatibility is explicit through protocol/model-contract versions rather than assumed from matching app versions.

---

## 4. Operational Modes

| Mode | CLIENT | SERVER | SERVER Internet | General LLM Reasoning | Online Research | Android/SWRLZ Local Work |
|---|---|---|---|---|---|---|
| SWRLZ LOCAL | Available | Unavailable | N/A | Unavailable except deterministic CLIENT logic | No | Yes |
| SWRLZ LAN | Available | Available over LAN | No | Yes, from local SWRLIE/model + local knowledge | No | Yes |
| SWRLZ ONLINE | Available | Available | Yes | Yes | Yes, SERVER only | Yes |
| DEGRADED | Available | Expected but unreachable | Unknown | Temporarily unavailable | No | Yes within CLIENT domain |

### 4.1 SWRLZ LOCAL

CLIENT continues to handle Android/SWRLZ knowledge, commands, mission control, device observation, patch notes, diagnostics, authorized local file work, and local execution. Requests that require broad reasoning or current external information return a truthful SERVER-required state.

### 4.2 SWRLZ LAN

A SERVER on the local network supplies local model reasoning without requiring public internet access. The system can reason using pretrained/fine-tuned knowledge and locally stored documentation, memory, indexes, or cached reference material. Current events or fresh web facts remain unavailable unless already present in trusted local data.

### 4.3 SWRLZ ONLINE

SERVER retains local reasoning while gaining policy-controlled web research, GitHub/Forge work, model package retrieval, and other networked services. CLIENT still does not become the web-research agent.

---

## 5. CLIENT Responsibilities

CLIENT is the local cockpit and Android/SWRLZ domain expert.

### 5.1 Knowledge and perception

- Complete SWRLZ CLIENT interface semantics.
- Current CLIENT identity/version/build evidence.
- Device manufacturer/model/Android/SDK/ABI.
- Display geometry, density, orientation, navigation mode.
- Permission/capability state.
- Accessibility observations and semantic node tree.
- Screen deltas between observations.
- Local artifact and file context within authorized roots.
- Current mission, command, Forge, notification, and interaction state.

### 5.2 Interaction and execution

- Compose/render the UI.
- Accept touch, keyboard, voice, command, and notification input.
- Resolve deterministic CLIENT-domain commands.
- Build task-scoped context for SERVER when needed.
- Enforce local approvals and Truth Firewall rules.
- Execute permitted actions on the Android device.
- Observe and report the result back to SERVER when part of a SERVER-assisted operation.

### 5.3 Network behavior

Normal CLIENT network traffic should be narrow and intentional:

- Authenticated communication with SERVER.
- Discovery/enrollment and trust bootstrap.
- Constrained recovery/self-update channel where explicitly designed.

Open-ended research, GitHub repository writes, large external downloads, and heavyweight external analysis belong on SERVER.

---

## 6. SERVER Responsibilities

SERVER is the heavyweight reasoning, network, and coordination tier.

### 6.1 Reasoning

- SWRLIE provider and model routing.
- General reasoning outside CLIENT's Android/SWRLZ domain.
- Complex synthesis and specialist model invocation.
- Optional vision/image/document analysis.
- Model-independent Reasoning Gateway.

### 6.2 Network

- Online search/research with provenance.
- GitHub/Forge repository operations.
- Workflow/build coordination when authorized.
- Model-pack retrieval/update.
- External API integration only when explicitly configured.

### 6.3 Nodes and shared state

- Registered node identities.
- Trust and revocation state.
- Cross-node mission coordination.
- Shared model availability.
- Shared/remote state that is outside one CLIENT's exclusive local authority.

### 6.4 Heavy file work

CLIENT may transfer an approved file or screenshot over fast LAN. SERVER performs expensive analysis and returns findings/results. Temporary SERVER staging must be transaction-scoped and cleaned after completion according to policy.

---

## 7. Forge Delegation Model

Forge should move from direct mobile-to-GitHub heavy transfer toward CLIENT-planned, SERVER-executed repository work when SERVER is available.

### 7.1 Intended flow

```text
CLIENT
  selects artifact + acceptable parameters
  validates local source identity
  obtains required user approval
        │
        ▼ LAN
SERVER temporary staging
  hashes received bytes
  validates package / lane / protocol / policy
  independently confirms CLIENT request is legal
        │
        ▼
GitHub / workflow operation
        │
        ▼
SERVER verifies remote result + records provenance
        │
        ▼
SERVER cleans transaction staging
        │
        ▼
CLIENT receives evidence/result
```

### 7.2 CLIENT controls intent, SERVER controls execution

CLIENT may declare parameters such as:

- source identity and SHA-256;
- CLIENT vs SERVER lane;
- branch/target allowed by policy;
- sidecar evidence included;
- whether a build route is requested;
- explicit statement that promotion/release/deployment is not authorized.

SERVER verifies those claims and refuses incompatible or unauthorized operations.

### 7.3 Temporary staging

Recommended transaction structure:

```text
forge-staging/
└── <transaction-id>/
    ├── source-or-payload
    ├── evidence/
    └── transaction.json
```

Prefer encrypted temporary storage with an ephemeral transaction key. On verified completion, delete staging data and destroy the ephemeral key. Do not claim guaranteed forensic overwrite on flash storage.

### 7.4 Transfer resilience

The recent device evidence showed a CLIENT Forge transfer that streamed an 8 MiB chunk to 100%, received a repository-operation HTTP 401, and immediately re-probed the credential successfully. This supports a future adaptive transport design with smaller-chunk fallback, resumable state, and failure classification that preserves credentials when authentication remains valid.

---

## 8. Shared SWRLZ Context Contract

CLIENT Missions already demonstrates the core context architecture needed for future SWRLIE reasoning. The system should generalize that capability rather than create a parallel context implementation.

### 8.1 Existing conceptual packet

```text
SWRLZ Context
├── device
├── app
├── screenDelta
└── visibleNodes
```

Representative device fields already demonstrated include manufacturer, model, Android version, SDK, ABI, display characteristics, navigation mode, locale/timezone, capability flags, battery/charging/network state, and collection time.

Representative app fields include package identity, app version/build identity, requested/granted permissions, UI framework evidence, and patch/build metadata.

The visible-node layer provides semantic UI controls rather than relying only on screenshot coordinates.

### 8.2 Context levels

- **STANDARD:** balanced device/app facts and redacted semantic controls.
- **DETAILED:** richer permission/window/node state and geometry when needed for difficult planning.
- **LOCAL ONLY:** collect for local reasoning/preview but prohibit inclusion in external-provider requests.

### 8.3 Canonical reuse

The shared context contract should serve:

- Missions.
- CLIENT Chat.
- SERVER Chat/reasoning.
- SWRLIE inference.
- Teach/Take Over flows.
- Diagnostics.
- File/Forge reasoning.

### 8.4 Contradiction handling

Context producers may disagree. SWRLZ should mark unresolved telemetry inconsistencies instead of silently choosing one source. Model reasoning must consume evidence status, not convert ambiguity into false certainty.

---

## 9. SERVER Chat Parity

SERVER needs a first-class Chat/Command Center surface comparable to CLIENT Chat. The goal is shared conversation architecture with role-specific capabilities, not two incompatible chatbot implementations.

Shared behavior should include:

- conversation history model;
- command grammar;
- composer behavior;
- patch/update knowledge integration;
- reasoning route/status display;
- provenance and approval surfaces.

SERVER-specific capabilities can expose node status, model status, reasoning jobs, Forge operations, diagnostics, and SERVER configuration.

CLIENT and SERVER chat events should carry lineage IDs so a distributed request can be reconstructed end to end.

---

## 10. Game-Like CLIENT Architecture

SWRLZ should adopt the durability of game architecture while remaining a utility/assistant platform.

```text
SWRLZ CLIENT
├── World State
│   ├── device
│   ├── permissions
│   ├── active app
│   ├── nodes
│   ├── missions
│   ├── Forge
│   └── conversation
├── Input
│   ├── touch
│   ├── voice
│   ├── commands
│   ├── accessibility events
│   └── notifications
├── Systems
│   ├── Chat
│   ├── Missions
│   ├── Files
│   ├── Forge
│   ├── Nodes
│   └── UI Context
├── Renderer
│   └── Compose / Kapanion interface
└── Network
    └── authenticated SERVER channel
```

The key flow is:

```text
input -> state -> system -> result -> render
```

The architecture must remain event-driven. Accessibility events, user messages, node responses, scheduled jobs, and material device-state changes trigger work. Idle CLIENT should not continuously inspect or infer.

---

## 11. SWRLIE Provider and Model Independence

**SWRLIE** is the first-party reasoning provider identity owned by SWRLZ. Provider identity is separate from model identity, runtime, execution node, and model lineage.

Example:

```text
Provider:   SWRLIE
Model:      SWRLIE Fast v1
Runtime:    llama.cpp adapter (example only)
Execution:  SERVER / LOCAL
Lineage:    LFM2.5-350M -> SWRLIE specialization -> v1
Trust:      OFFICIAL SWRLZ / VERIFIED
```

A later native model can become:

```text
Provider:   SWRLIE
Model:      SWRLIE Native vN
Runtime:    replaceable runtime adapter
Origin:     SWRLIE-native lineage when technically/licensing-correct
Execution:  SERVER / LOCAL
```

### 11.1 Reasoning Gateway

Chat and other systems talk to a SWRLZ-owned Reasoning Gateway, never directly to a particular model library.

```text
Reasoning Gateway
├── NoModelEngine
├── SWRLIE Local Model Engine
├── SERVER Model Engine
├── Private Node Engine
└── Optional External Engine
```

Representative engine contract:

```text
ReasoningEngine
- id
- capabilities
- availability
- load / unload
- infer
- cancel
- health
- metrics
```

### 11.2 No-model fallback

Removing all neural models must not break Chat. Deterministic commands, status, retrieval, device knowledge, missions, patch notes, diagnostics, and other non-generative capabilities continue to work. SWRLZ reports that generative/general reasoning is unavailable when required.

### 11.3 Runtime independence

Inference runtime should also be adapter-based. llama.cpp, LiteRT, ExecuTorch, or a future NPU-specific runtime may be swapped without rewriting Chat, mission authority, or provider contracts.

---

## 12. SWRLIE Model Evolution Strategy

The long-term goal is for SWRLZ to progressively own more of its neural reasoning instead of permanently depending on a generic external model.

### Generation 0 - SWRLZ Core

No neural model required. Deterministic systems, memory, commands, missions, context, tools, Truth Firewall, Forge, and device intelligence exist independently.

### Generation 1 - Assisted SWRLZ

Use small open-weight models as temporary reasoning engines/teachers. They are crutches, not identity.

### Generation 2 - SWRLZ-specialized models

Fine-tune or adapt candidate models on SWRLZ-specific tasks:

- command/capability routing;
- Android semantic UI reasoning;
- approval-class selection;
- artifact/file classification;
- SWRLZ terminology and protocols;
- tool-use schemas;
- concise diagnostics;
- patch/update interpretation.

### Generation 3 - Distilled SWRLIE

Use stronger models and curated successful usage records to train smaller SWRLIE students that reproduce the behavior SWRLZ actually needs.

### Generation 4 - SWRLIE Native

A SWRLZ-owned reasoning line becomes the default first-party model. Other models remain optional specialists or teachers. SWRLZ remains model-independent even after its own model exists.

---

## 13. Current Model Research Candidates (Not Selected)

This section records current research candidates only. It is not an adoption decision.

### 13.1 LFM2.5-350M - fast text/tool candidate

Current Liquid AI documentation describes LFM2.5-350M as a 350M-parameter edge-oriented text model, recommends it for structured output/tool use, and reports a 32K-class context family with edge deployment support. A current official GGUF Q4_K_M file is approximately **229 MB**.

Potential SWRLIE role:

- fast intent/command routing;
- structured output;
- tool selection;
- extraction and summaries;
- lightweight conversation.

### 13.2 LFM2.5-VL-450M - visual/UI candidate

Current Liquid AI documentation describes LFM2.5-VL-450M as a 450M-class vision-language model using the LFM2.5-350M language backbone plus an 86M SigLIP2 vision encoder, with 32,768-token context and bounding-box/object-localization capability. A published 4-bit MLX variant is about **376 MB**; the exact Android-ready package size depends on the runtime and quantization selected later.

Potential SWRLIE role:

- screenshot and UI interpretation;
- document/image comprehension;
- visual validation against accessibility semantics;
- narrow Android/SWRLZ visual specialization.

### 13.3 Why complementary models are optional, not permanent

SWRLZ may initially run both, only one, or neither depending on benchmarks. If deterministic SWRLZ plus one visual/general model meets requirements, the extra model should not be shipped merely for symmetry. Usage telemetry and evaluation determine whether each module earns its storage/energy cost.

---

## 14. Model Product Line, Packaging, and Storage

### 14.1 Separate lineages

CLIENT, SERVER, and MODEL evolve independently.

An app update must not require model re-download when the installed model remains compatible.

A model update must not require a CLIENT/SERVER rebuild when the model contract remains compatible.

### 14.2 Keep weights out of normal source archives

Model weights are hundreds of MB; current SWRLZ source packages are tens of MB. Embedding model weights into source or APKs would make Forge, Git history, Android installs, and repeated builds unnecessarily expensive.

Recommended repository layout:

```text
swrlz-core/
├── sources/
│   ├── client/
│   └── server/
├── models/
│   ├── contracts/
│   ├── manifests/
│   ├── training/
│   ├── evaluation/
│   └── adapters/
└── docs/
```

Large distributable weights should live in a release/artifact channel rather than ordinary Git history. GitHub currently warns on regular Git files above 50 MiB, blocks regular Git files above 100 MiB, recommends repositories stay under 1 GB ideally and under 5 GB strongly, and supports release assets under 2 GiB each with up to 1000 assets per release.

### 14.3 Model Pack manifest

Representative fields:

```text
modelId
modelVersion
provider = SWRLIE
runtimeFormat
capabilities
contextWindow
memoryRequirement
supportedABIs / accelerators
modelContractVersion
baseLineage
license
sizeBytes
sha256
signature
releaseArtifact
```

### 14.4 Persistent Model Vault

The user-facing CLIENT may orchestrate model installation to a selected SERVER/node, but storage/execution authority belongs to that inference node.

A persistent Model Vault can preserve downloaded model packages independently from ordinary runtime caches so compatible SERVER reinstalls can re-verify/re-register a model without re-downloading it.

A SERVER-private runtime copy/cache can remain optimized for inference while the persistent vault preserves the canonical package.

---

## 15. Model Security and Trust

The goal is tamper resistance, provenance, and verifiable identity - not an impossible promise that model extraction can never occur on a fully controlled/rooted device.

### 15.1 Signed manifests

Official SWRLIE packs should be signed. SERVER verifies signature, SHA-256, size, compatibility, and lineage before activation.

### 15.2 Encrypted payload option

A SWRLZ model-pack container may encrypt model payloads at rest and use Android/host secure key storage where available. Authenticated encryption can detect payload modification before load.

### 15.3 Trust classes

- **OFFICIAL / VERIFIED:** signature and manifest valid.
- **USER PROVIDED / UNVERIFIED:** compatible custom model explicitly allowed by user policy.
- **SIGNATURE INVALID / MODIFIED:** must not masquerade as an official model.

Custom models should remain possible because model interchangeability is an architectural requirement. The Truth Firewall and execution authority do not weaken merely because a model is official.

---

## 16. Node Hosting and Remote Administration

A gaming PC or other capable machine can host SERVER/SWRLIE as a NODE_HOST.

```text
SWRLZ NODE_HOST
├── SERVER
├── SWRLIE reasoning runtime
├── Model Vault
├── Forge/network worker
├── diagnostics
└── resource governor
```

CLIENT can administer enrolled nodes through authenticated, revocable identities.

Recommended controls:

- run always / when idle / scheduled;
- CPU/GPU/RAM limits;
- model availability;
- job status;
- LAN/private-only vs online capability;
- GitHub/Forge capability state;
- explicit prohibition on unrelated personal-file access unless separately granted.

Node enrollment should require explicit approval, device-bound identity, protocol compatibility, revocation support, and scoped capabilities.

---

## 17. Chat Logs, Usage Telemetry, and SWRLIE Learning

Conversation history is valuable, but raw chats should not automatically become training data.

### 17.1 Three distinct data classes

**Conversation history**
- user message;
- SWRLZ response;
- tool/command outcome;
- node involved.

**Operational/reasoning telemetry**
- route used;
- module/capability used;
- model/provider version;
- latency;
- fallback;
- success/failure;
- resource usage;
- correction/result evidence.

**Curated learning records**
- redacted, quality-controlled examples selected for evaluation/training;
- explicit expected capability/action/approval/output;
- provenance and evidence status retained.

Do not log private hidden model chain-of-thought. The useful development signal is structured operational evidence, outputs, corrections, and outcomes.

### 17.2 Distributed event lineage

Representative event fields:

```text
eventId
conversationId
nodeId
origin
parentEventId
requestId
timestamp
capability
reasoner/provider/model
contextContractVersion
approvalClass
result
evidenceClass
latency/resource metrics
```

This makes it possible to reconstruct:

```text
USER
 -> CLIENT request
 -> SERVER validation/reasoning
 -> CLIENT local execution
 -> CLIENT observation
 -> SERVER acknowledgement/result
```

### 17.3 Usage-driven model tuning

Aggregate telemetry can show which modules earn their cost. Example dimensions:

- Android/SWRLZ routing frequency and accuracy.
- File analysis usage.
- Forge workload.
- Vision invocation rate.
- General reasoning frequency.
- Code/creative workload.
- Latency and failure rate per engine.

Training and model capacity should move toward high-value/weak areas rather than blindly making every module larger.

---

## 18. Performance, Battery, and Storage Strategy

The CLIENT should be lightweight enough to behave like a responsive game client without running game-style continuous compute.

### 18.1 CLIENT performance goals

- No always-on model inference by default.
- No permanent high-frequency polling.
- Event-driven accessibility/context updates.
- Fast local parsing and deterministic routing.
- LAN streaming to SERVER for heavy work.
- WorkManager/scheduled maintenance for non-urgent background tasks.

### 18.2 SERVER performance goals

- Heavy models remain loaded only when policy/resources justify it.
- Model routing chooses the cheapest engine capable of the task.
- Resource governor can respect CPU/GPU/RAM/idle-time policies on hosted PCs.
- Vision and other expensive specialists are invoked only when useful.

### 18.3 Storage reality observed during design

The current Android device screenshot showed 128 GB total storage, about 110 GB used, and 18.20 GB free. Games and apps dominated space. This reinforces that model packs should be optional, centralized on SERVER where possible, independently updateable, and never multiplied across every CLIENT by default.

---

## 19. Security Model Inspired by Authoritative Multiplayer Systems

The MOBA analogy is useful as an engineering model, not as a literal implementation.

### 19.1 SERVER authoritative for shared/remote state

SERVER validates node identity, trust, shared missions, model state, network/Forge operations, and remote/shared state transitions.

### 19.2 CLIENT authoritative for its local device

CLIENT validates local permission, current UI/device state, and user approval before performing local Android actions. SERVER may propose or authorize but does not bypass Android/user authority.

### 19.3 Fog-of-war becomes least privilege

A CLIENT should receive only the shared state needed for its current role/task. A compromised CLIENT must not automatically reveal every other node's context, credentials, files, or mission details.

### 19.4 One network egress tier

Routing open-web research and heavyweight external work through SERVER reduces attack surface and gives one place to enforce domain controls, provenance, redaction, caching, credential management, rate limits, and malicious-content defenses.

---

## 20. Suggested Contracts

The following contracts should be formalized before model/runtime integration becomes deep.

### 20.1 ReasoningRequest / ReasoningResponse

SWRLZ-owned request/response schema independent of any model provider.

### 20.2 ModelPackManifest

Identity, capability, compatibility, lineage, hash, signature, license, storage, and runtime metadata.

### 20.3 SharedContextContract

Canonical device/app/screen/mission/capability/artifact context used by CLIENT, SERVER, Missions, Chat, Diagnostics, and SWRLIE.

### 20.4 NodeCapabilityContract

What a node can host or execute: reasoning, vision, Forge, research, storage, etc.

### 20.5 ForgeRemoteTransactionContract

CLIENT intent + approved parameters; SERVER validation; transfer identity; remote operation; provenance; cleanup.

### 20.6 LearningTelemetryContract

Structured usage/evaluation evidence separate from conversation history and curated training data.

---

## 21. Implementation Status Boundaries

This architecture document intentionally separates current evidence from future design.

### Demonstrated/current foundations

- CLIENT Missions already generates structured device/app/screen context and semantic accessibility observations.
- CLIENT and SERVER already exist as distinct SWRLZ product lines.
- Forge can validate source ZIP identity/evidence and has demonstrated chunked transfer behavior.
- CLIENT Chat/Command Center, local-first direction, Truth Firewall, missions, and capability architecture provide foundations for model-independent routing.

### Designed/planned direction

- SERVER Chat parity.
- SERVER-exclusive open-web research.
- CLIENT-to-SERVER Forge delegation.
- Model-independent Reasoning Gateway.
- SWRLIE provider implementation.
- Persistent Model Vault.
- Model packs and first-party signing.
- NODE_HOST PC runtime and authenticated admin control.
- Cross-node learning telemetry and curated SWRLIE training pipeline.
- Event-driven game-like CLIENT systems refactor where useful.

No planned item should be presented as implemented until its own source/build/device/integration evidence exists.

---

## 22. Recommended GitHub Documentation Placement

Suggested canonical document path:

```text
swrlz-core/docs/architecture/SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md
```

Recommended companion documents as the design becomes implementation work:

```text
swrlz-core/docs/architecture/SWRLZ_REASONING_GATEWAY_AND_SWRLIE_PROVIDER_V1.md
swrlz-core/docs/architecture/SWRLZ_CLIENT_SERVER_AUTHORITY_AND_NETWORK_EGRESS_V1.md
swrlz-core/docs/contracts/SWRLZ_SHARED_CONTEXT_CONTRACT_V2.md
swrlz-core/docs/contracts/SWRLZ_MODEL_PACK_MANIFEST_V1.md
swrlz-core/docs/contracts/SWRLZ_REMOTE_FORGE_TRANSACTION_V1.md
swrlz-core/docs/contracts/SWRLZ_LEARNING_TELEMETRY_V1.md
swrlz-core/docs/roadmaps/SWRLIE_MODEL_EVOLUTION_ROADMAP_V1.md
```

The main architecture document should be linked from the documentation index and relevant feature/status matrices only after repository documentation approval.

---

## 23. Suggested Future Checkpoints

These are proposed boundaries, not approvals.

1. **Shared Context + SERVER Chat parity** - generalize CLIENT Missions context into a shared contract and add SERVER Chat using shared conversation architecture.
2. **Model-independent Reasoning Gateway** - pluggable engines/runtimes and deterministic no-model fallback.
3. **Model Vault + Model Pack lifecycle** - independent model versioning, verification, rollback, persistence, and node ownership.
4. **SERVER network/Forge authority** - CLIENT-approved intent, authenticated LAN staging, SERVER verification/upload, provenance, and cleanup.
5. **SERVER online research** - policy/provenance/redaction boundary; CLIENT never performs open-ended web research.
6. **Learning telemetry** - privacy-aware event lineage, module-utilization metrics, corrections, and curated training pipeline.
7. **SWRLIE prototype** - benchmark candidate text/vision models behind the Reasoning Gateway without making either mandatory.

Each checkpoint should preserve source/build/device/integration evidence separation and immutable candidate revisions.

---

## Appendix A - Current Size Snapshot

Observed local artifacts during this design session:

| Artifact | Bytes | Approx. MiB |
|---|---:|---:|
| CLIENT CFv2.1.22 R1 source ZIP | 15,021,861 | 14.33 |
| SERVER CFv2.1.8 R3 source ZIP | 40,290,065 | 38.42 |
| CLIENT CFv2.1.20 R1 debug APK bundle ZIP | 34,555,383 | 32.95 |
| SERVER CFv2.1.8 R3 debug APK bundle ZIP | 45,066,224 | 42.98 |

Current research examples are already much larger than app source packages: LFM2.5-350M Q4_K_M is about 229 MB, while a published 4-bit LFM2.5-VL-450M MLX package is about 376 MB. This is why model packages need an independent artifact lifecycle.

---

## Appendix B - External Research References

Verified 2026-07-28. These references support only the current model/GitHub-size research portions of this document; they do not turn design recommendations into implementation claims.

1. Liquid AI, **LFM2.5-350M** model card: https://huggingface.co/LiquidAI/LFM2.5-350M
2. Liquid AI, **LFM2.5-350M-GGUF** files/quantizations: https://huggingface.co/LiquidAI/LFM2.5-350M-GGUF
3. Liquid AI, **LFM2.5-VL-450M** model card: https://huggingface.co/LiquidAI/LFM2.5-VL-450M
4. Liquid AI, **LFM2.5-VL-450M MLX 4-bit** package: https://huggingface.co/LiquidAI/LFM2.5-VL-450M-MLX-4bit
5. GitHub Docs, **About large files on GitHub**: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
6. GitHub Docs, **About releases**: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

---

## Appendix C - Decision Summary

- CLIENT knows Android + SWRLZ comprehensively and executes local device actions.
- SERVER is the heavyweight general-reasoning, online-research, Forge/network, analysis, model, and multi-node tier.
- CLIENT does not perform open-ended web research.
- Offline is not one state: LOCAL and LAN are distinct, with ONLINE as a third primary mode.
- Chat survives without an LLM.
- Neural models and inference runtimes are replaceable modules.
- First-party reasoning provider identity is SWRLIE.
- CLIENT, SERVER, and MODEL have independent version lineages.
- Model weights stay outside ordinary CLIENT/SERVER source/APK lifecycle.
- Model Vault enables persistent verified model packages and avoids needless re-downloads.
- SERVER may run on enrolled PCs with authenticated CLIENT administration and resource limits.
- Forge can evolve toward CLIENT-approved / SERVER-executed repository operations.
- Conversation history, operational telemetry, and curated training records remain distinct.
- Usage/evaluation data should guide where SWRLIE grows or shrinks.
- The architecture borrows authoritative multiplayer/game-system durability while remaining event-driven and battery-conscious.
