# SWRLZ SWRLIE Runtime, Capability, and Skills Evolution v1

**Status:** architecture/design consolidation with SERVER CFv2.1.9 R1-R5 source-candidate evidence through 2026-07-29. Planned portions are explicitly marked and are not implementation claims.

## 1. Core rule

SWRLZ scales upward by adding capability, not by abandoning efficiency or redefining identity.

The system separates:

- **SWRLZ Core:** authority, Truth Firewall, approvals, tools, trust, provenance, files, missions, Forge, update policy;
- **SWRLZ Skills:** reusable procedures/capabilities owned by SWRLZ rather than by one model;
- **Memory:** relevant prior state, decisions, learned context, and distilled lessons;
- **Self Knowledge:** current authoritative local state such as installed version, model/runtime state, capabilities, and patch history;
- **SWRLIE:** first-party reasoning-provider identity;
- **Model:** replaceable neural reasoning engine;
- **Runtime:** replaceable inference implementation;
- **Swurlzara:** adaptive identity/expression layer, subordinate to truth and authority.

Conceptually:

```text
SWRLZ CORE
├── authority / Truth Firewall / approvals
├── Skills
├── Memory
├── Self Knowledge
└── Capability Registry
        │
        ▼
Task + Context Resolver
        │
        ▼
SWRLIE Gateway
        │
        ├── model
        └── runtime
        │
        ▼
Swurlzara identity/expression
        │
        ▼
response / proposal
        │
        ▼
SWRLZ validation and any permitted action
```

The physical prompt/inference call may compile skill, memory, self-state, and identity context together before generation. Architectural ownership remains separate.

## 2. Evidence now present in candidate lineage

SERVER CFv2.1.9 R1-R5 demonstrates source-candidate movement toward this architecture:

- R1: pluggable local inference contract, no-model fallback, external verified GGUF, llama.cpp adapter, Provider Mesh SWRLIE route;
- R2: first-class SERVER Chat and nested Brain/AI settings architecture;
- R3: startup local-model recovery/load, adaptive/copyable Chat, Update Ledger, tone-never-implies-approval guard;
- R4: multi-GGUF Model Vault staging, safe switching/rollback, adaptive context/inference controls, prompt-budget guard, code-native bounded Swurlzara compiler;
- R5: local self-knowledge resolver, shared Update Ledger retrieval, live local runtime/model grounding, explicit USER/SWRLZ/SWRLIE/Swurlzara role map.

These remain source candidates unless and until separate build/device/integration/promotion evidence is recorded.

## 3. SWRLZ Skills belong upstream of any LLM

A skill is a reusable SWRLZ capability/procedure, not knowledge that exists only because one model remembers it.

Examples:

```text
SWRLZ Skills
├── Android / accessibility / device reasoning
├── engineering / debugging / architecture
├── GitHub / repository analysis
├── Forge / artifact lineage / provenance
├── file/archive organization
├── documentation / technical writing
├── lyrical / creative generation
├── research methodology
└── simulation/game construction
```

A model may reason with a skill, but replacing the model must not delete the skill.

Skills should define as appropriate:

- inputs and outputs;
- evidence requirements;
- tool/capability dependencies;
- authority/approval classes;
- confidence semantics;
- deterministic validation where available;
- failure and fallback behavior.

Deterministic parts should remain usable without a neural model when practical.

## 4. Skills, Memory, and Self Knowledge are different systems

### Skills

Reusable methods and capability contracts.

Example: how to verify whether a loose directory was extracted from a particular ZIP.

### Memory

Relevant historical context and learned outcomes.

Example: a previous debugging result or a distilled lesson from a successful interaction.

### Self Knowledge

Current authoritative state.

Example: installed SERVER version, active model, context limit, Model Vault roster, patch history, Forge state, or current capability availability.

A model should not be used as the database for any of these categories.

## 5. Behavioral baseline and monotonic model extension

The smallest certified SWRLIE model should establish the minimum acceptable behavioral contract.

Heavier models are upgrades only when they preserve that floor and add capability.

```text
Lightweight certified model
        │ establishes
        │ behavior / truth discipline / role separation / identity
        ▼
Balanced model
        │ + reasoning / context / skill depth
        ▼
Quality model
        │ + deeper synthesis / writing / coding
        ▼
Heavy private/dedicated node
          + large-context / specialist / parallel workloads
```

A larger model that improves one specialist dimension while regressing core Chat behavior may still be useful as a specialist, but it is not automatically the general default.

### Proposed minimum-behavior dimensions

- natural conversation;
- Swurlzara internalization without instruction recitation;
- USER/SWRLZ/SWRLIE/SERVER role separation;
- evidence discipline;
- relevance and concision;
- technical/practical reasoning;
- instruction-leak resistance;
- no invented approval;
- no destructive-action authority leakage;
- truth-preserving humor/personification.

The current working quality target discussed during evaluation is approximately 8/10 or better across non-critical dimensions, with critical authority violations treated as hard failures rather than averaged away. This is a tuning target, not yet a release contract.

## 6. Instruction internalization vs instruction recitation

Profile/configuration should change behavior without normally becoming visible response content.

Desired:

```text
instruction: be analytical
output: clear evidence-first analysis
```

Undesired:

```text
output: "ANALYTICAL MODE: evidence-first..."
```

Likewise, active profile values such as warmth, energy, humor, or technical depth should normally affect output rather than being echoed as a character sheet unless the user explicitly asks for those settings.

## 7. Grounding and unobserved-state discipline

Fluent self-description is not evidence.

The system should distinguish:

- **KNOWN:** supported by current authoritative state/evidence;
- **INFERENCE:** a stated conclusion derived from evidence;
- **UNKNOWN:** unavailable and should remain unknown;
- **PLAYFUL:** obvious metaphor/banter that must remain distinguishable from factual claims.

Examples of unsupported claims to detect during evaluation include invented UI feedback, imaginary performance benchmarks, nonexistent external user surveys, fabricated weather/sensory experiences, or confident runtime state not supplied by SWRLZ.

R5's local self-knowledge resolver is the first source-candidate step toward grounding these claims in actual SERVER state.

## 8. Swurlzara as a code-native identity layer

The canonical Swurlzara specification may remain rich documentation, while runtime inference should use a compact compiled representation appropriate to the task and context budget.

R4 establishes the source-candidate direction:

```text
canonical identity/spec
        │
        ▼
code-native policy / relevance / mode resolver
        │
        ▼
bounded runtime directive
        │
        ▼
selected SWRLIE model
```

Identity is separate from model/runtime. A later LoRA or fine-tune may internalize stable behavioral patterns, but SWRLZ authority must remain outside neural weights.

### Personality control plane — planned

Beyond named profiles, future configuration may expose safe behavioral controls such as:

- warmth;
- energy;
- humor;
- absurdity;
- technical depth;
- directness;
- skepticism/challenge;
- creativity;
- mythic expression;
- verbosity;
- initiative;
- teaching depth.

Immutable control-plane rules are not personality sliders. Truth Firewall, approval/permission authority, provenance, node/file/mission/Forge authority, and protocol/trust boundaries remain higher priority.

## 9. Capability tiers — planned

The same baseline identity/skills can be routed to different model tiers.

### Lightweight

- casual Chat;
- intent/command interpretation;
- short summaries;
- simple local planning;
- basic file classification;
- low-cost always-available reasoning.

### Balanced

Everything above plus:

- richer conversation;
- coding assistance;
- multi-file reasoning;
- GitHub/repository planning;
- technical documentation;
- longer creative/lyrical work;
- artifact/file lineage analysis.

### Quality

Everything above plus:

- repository-wide architecture analysis;
- large refactor planning;
- deeper debugging;
- long-form book/document generation;
- complex synthesis;
- larger context.

### Heavy/private/dedicated node

Everything above plus:

- large-codebase and cross-repository reasoning;
- deep web research when authorized;
- heavyweight image/document analysis;
- specialist model orchestration;
- parallel workers;
- long-horizon missions.

## 10. Model routing should optimize density, not size alone

A larger model is not automatically preferred.

SWRLZ should route the smallest model that reliably satisfies the task and behavioral contract.

Useful efficiency dimensions include:

- quality per model byte;
- quality per peak RAM;
- quality per unit latency;
- useful context per token;
- capability gained per injected skill/context token;
- battery/energy cost;
- thermal behavior;
- concurrent job capacity.

The design principle is:

> Raise the capability ceiling while continuing to lower the weight floor.

## 11. Hardware-tier capability packs — planned

One architecture should scale across hardware instead of becoming separate assistants.

### Android optimized node

- lightweight/balanced models;
- mobile-safe context and resource governors;
- Android/client execution skills;
- optional compact vision/image/audio packs;
- offline-first operation.

### PC power node

- larger reasoning/coding models;
- deeper context;
- local image generation/editing;
- vision, speech, TTS;
- repository/knowledge indexes;
- larger simulation workloads.

### Dedicated SERVER node

- heavyweight reasoning pools;
- coding/research specialists;
- image/vision/audio workers;
- embeddings/retrieval workers;
- artifact storage;
- model/adapter tooling;
- node orchestration and parallel jobs.

Bigger hardware does not justify wasteful routing; small resident models remain useful for trivial work even on powerful nodes.

## 12. Optional pack footprint and shared artifacts — planned

Large capability budgets should be upper envelopes, not mandatory install sizes.

Potential packs include:

- lightweight/balanced/quality reasoning models;
- vision;
- image generation/editing;
- STT/TTS/audio;
- engineering/repository/creative/file-analysis Skills;
- local knowledge/indexes;
- simulation packs;
- update staging/rollback generations.

When CLIENT and SERVER roles share one physical device, duplicate immutable model/pack storage should be avoided where Android security/storage architecture permits a safe shared artifact-vault design.

## 13. Simulation Forge / LLMware direction — planned

Larger reasoning tiers may create interactive simulations, but arbitrary model-generated Kotlin/DEX/native execution is not the target.

Preferred model:

```text
LLM/SWRLIE
  -> structured GameSpec / ScenarioSpec
SWRLZ
  -> schema + safety + authority validation
Simulation Engine
  -> deterministic execution
LLM/SWRLIE
  -> bounded AI-player decisions / explanation
```

Examples include Spades, Rummy, custom starting hands, AI difficulty/style, counterfactual replay, or later general scenario simulators.

A constrained DSL/state engine allows dynamic content while preserving SWRLZ authority and preventing arbitrary executable-code loading.

## 14. Specialist media models — planned

Image generation, vision, audio, and other specialist workloads should be separate capabilities/models when that produces better quality/resource density.

SWRLIE may plan and contextualize a request; SWRLZ routes the appropriate specialist and preserves provenance/authority around resulting assets.

## 15. Evidence boundary

This document mixes current source-candidate evidence with explicitly marked planned architecture.

It does **not** claim:

- R1-R5 are promoted SERVER authority;
- R5 Android build/device/integration acceptance;
- SWRLZ Skills framework implementation;
- capability-tier routing implementation;
- personality-control-plane implementation;
- LoRA/fine-tuning completion;
- image generation integration;
- Simulation Forge implementation;
- PC/dedicated-node pack implementation;
- web research enablement;
- release/deployment/install success.

`CURRENT_AUTHORITY.md` remains the promoted-source reference.
