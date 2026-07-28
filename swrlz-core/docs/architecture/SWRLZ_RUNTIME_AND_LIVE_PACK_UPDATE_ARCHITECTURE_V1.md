# SWRLZ Runtime and Live Pack Update Architecture v1.0

**Status:** Architecture / design contract. This document defines intended updater behavior and does **not** claim implementation, build, device, integration, release, or deployment evidence.

**Project:** SWRLZ-Core  
**Relationship:** Companion to `SWRLZ_DISTRIBUTED_INTELLIGENCE_ARCHITECTURE_V1.md`; it refines model lifecycle, SERVER network authority, update behavior, and game-like runtime/pack separation without changing the existing authority laws.

---

## 1. Purpose

SWRLZ should evolve like a durable game runtime rather than requiring a full application reinstall for every capability, model, knowledge, or presentation change.

The system therefore separates:

1. **SWRLZ runtime products** — CLIENT, SERVER, and optional Launcher/Update Supervisor APK/runtime code.
2. **SWRLZ live packs** — signed, independently versioned, non-APK artifacts that can normally be downloaded, verified, staged, and activated while SWRLZ continues running.
3. **SWRLIE model products** — a relatively stable base model plus independently versioned neural adapters, knowledge assets, routing/configuration, and other model-support files.

Runtime replacement is comparatively rare. Pack activation is the normal update path for content and capabilities that do not require replacing executable Android/native code.

---

## 2. Authority and Control-Plane Rule

SWRLIE or any other model is advisory reasoning infrastructure. SWRLZ remains the control plane.

SWRLZ owns and enforces, outside the neural model:

- Truth Firewall;
- command routing;
- approval policy;
- tool schemas and capability contracts;
- node trust, enrollment, revocation, and authorization;
- file/storage authority;
- Forge validation and repository-operation policy;
- update eligibility, provenance, trust, activation, rollback, and cleanup policy.

A model may propose an action or interpret data, but it does not grant itself permission, bypass Android/device authority, redefine repository authority, or self-promote a build/model/pack.

```text
Reasoner / SWRLIE
      |
      v
SWRLZ CONTROL PLANE
      |
      +-- Truth Firewall
      +-- command/capability routing
      +-- approval policy
      +-- tool contracts
      +-- node trust
      +-- file authority
      +-- Forge/update validation
      |
      v
CLIENT / SERVER / NODE executor
```

---

## 3. Runtime Versus Live Pack

### 3.1 Runtime products

The runtime contains code that must remain under the signed application lifecycle:

- Compose/UI runtime code;
- Android services and components;
- permissions and manifest behavior;
- protocol implementation;
- database/storage implementation;
- security primitives;
- native inference runtime/JNI such as llama.cpp integration;
- installer/updater implementation itself;
- executable Kotlin/DEX/native behavior.

These changes require a new signed APK/runtime candidate and normal Android package replacement semantics.

### 3.2 Live packs

Live packs are data/model/content artifacts interpreted by the existing trusted runtime. Representative pack classes include:

- `MODEL_BASE` — SWRLIE base GGUF or another supported model format;
- `MODEL_ADAPTER` — LoRA or other runtime-supported neural adapter;
- `KNOWLEDGE` — documents, indexes, embeddings, retrieval databases, or curated domain knowledge;
- `THEME` — theme/Kapanion visual assets and declarative presentation data;
- `TOOL_SCHEMA` — declarative tool/capability schemas understood by the runtime;
- `DEVICE_DATA` — declarative device/domain knowledge;
- `CONFIG` — runtime/model routing and inference configuration within an allowed schema.

Live packs must **not** become a path for arbitrary downloaded executable Android code. New DEX/native/runtime implementation remains an APK/runtime update.

---

## 4. SWRLIE Base-Plus-Modules Model

The initial SWRLIE bootstrap may use an open-weight base model such as the selected 350M GGUF target. That base is treated as an engine block, not as the entire SWRLZ intelligence product.

```text
SWRLIE BASE
   |
   +-- Android neural adapter
   +-- SWRLZ/domain neural adapter
   +-- tool/Forge neural adapter
   +-- conversation/style adapter
   +-- knowledge packs
   +-- routing/configuration
   +-- future specialist modules
```

### 4.1 Stable base, smaller ordinary updates

The base model should change comparatively infrequently. Ordinary SWRLIE releases should prefer independently versioned modules when technically appropriate.

Example:

```text
SWRLIE MPv1.7

BASE
  350M Q4_K_M          v1   KEEP

NEURAL
  Android adapter      v8   UPDATE
  Tools adapter         v5   KEEP
  Conversation adapter  v3   KEEP

KNOWLEDGE
  SWRLZ knowledge       v18  UPDATE
  Android knowledge      v6  KEEP

CONFIG
  Reasoning profile      v7  UPDATE
```

Only required changed objects are fetched. The installed base is not re-downloaded merely because one adapter, knowledge pack, or configuration file changed.

### 4.2 Major base refresh

A future major SWRLIE base may absorb behavior learned from successful adapters, evaluations, corrections, and distillation. Such a base refresh is a separate model-product update and does not imply a CLIENT/SERVER runtime update when the model contract remains compatible.

---

## 5. Live Pack Manager

The planned **SWRLZ Live Pack Manager** is SERVER-owned for internet discovery/download work and uses SWRLZ-owned manifests and trust policy.

Core responsibilities:

1. discover available pack manifests from an allowed update source;
2. compare installed versions, object hashes, dependencies, and compatibility;
3. calculate an update plan;
4. fetch only required changed/missing objects;
5. validate signature, SHA-256, size, lineage, dependency, contract, and runtime compatibility;
6. stage the new generation without modifying the active generation in place;
7. initialize/load/health-check where the pack type supports it;
8. atomically activate the new generation;
9. retain an approved rollback generation;
10. journal activation and cleanup old unreferenced objects according to policy.

### 5.1 Do not mutate the active generation

```text
Pack v7 ACTIVE
      |
      +-- download v8
      +-- verify v8
      +-- stage v8
      +-- initialize/health-check v8
      +-- ACTIVE POINTER -> v8
      +-- v7 becomes ROLLBACK
```

Existing work may finish against its pinned generation when required. New work uses the newly active generation only after activation succeeds.

### 5.2 Failure behavior

A failed download, signature/hash check, dependency check, load test, or activation must leave the previous active generation usable. Failure is evidence, not permission to silently bypass verification.

---

## 6. Update Discovery and Source Abstraction

SERVER owns normal internet update checking. CLIENT does not become an open-web updater/research agent.

The update subsystem must consume a generic source contract rather than hard-coding one hosting vendor:

```text
UpdateSourceAdapter
   +-- GitHub release/artifact source
   +-- Hugging Face/model source
   +-- object storage/CDN source
   +-- LAN/private node source
   +-- future SWRLZ registry
```

### 6.1 Initial hosting direction

Recommended initial separation:

- **GitHub repository:** source, contracts, manifests, documentation, provenance, and long-term project truth.
- **GitHub release/artifact channel:** immutable distributable runtime/package artifacts when a release/publishing checkpoint explicitly authorizes them.
- **Hugging Face private repository/bucket:** model development workspace, upstream mirrors, experimental weights, checkpoints, adapters, and working artifacts; not automatically production authority.
- **Future object store/CDN:** scalable content-addressed SWRLZ update distribution when needed.

The architecture must permit changing the delivery backend without changing CLIENT/SERVER/model identity or trust rules.

---

## 7. Content-Addressed and Incremental Fetch

Pack files should be independently identified by strong hashes. Where useful, large immutable artifacts may also be split into verified objects/chunks.

Representative object identity:

```text
objectId = SHA-256(bytes)
sizeBytes
mediaType / packType
```

An update manifest references required objects. If the Model Vault/Pack Store already contains an object with the exact trusted hash and size, the updater may reuse it instead of downloading it again.

```text
Installed:
  base hash A       PRESENT
  tools hash B      PRESENT
  android hash C    PRESENT

Remote generation:
  base hash A       REUSE
  tools hash B      REUSE
  android hash D    FETCH
  knowledge hash E  FETCH
```

For a monolithic GGUF, a small training change is **not guaranteed** to produce a proportionally small binary delta. Predictably small normal updates therefore come primarily from keeping the base stable and placing appropriate behavior/knowledge in independently versioned adapters and packs.

---

## 8. Background Download While SWRLZ Runs

Pack download and verification should be independent from foreground UI lifetime.

SWRLZ may continue operating with the currently active packs while new packs download in the background.

Example fresh SERVER experience:

```text
SERVER runtime READY
Deterministic SWRLZ features READY
SWRLIE base downloading: 37%

...existing available features remain usable...

SWRLIE base 100%
verify -> register -> load -> health check
SWRLIE capability becomes READY
```

Downloading a new model/adapter/knowledge/theme pack does not itself require an APK reinstall or app relaunch.

---

## 9. Activation Semantics by Pack Type

### 9.1 Model base

Activation may require the inference engine to finish or cancel active requests, unload the prior model, load the verified model generation, perform a health check, and then switch routing to it. The SERVER runtime itself remains alive when the inference runtime supports this lifecycle.

### 9.2 Neural adapters

Adapters may be selected per task or generation when supported by the inference runtime. Adapter activation remains subject to compatibility and evaluation policy. Multiple overlapping adapters should not be accumulated without controlled routing/evaluation.

### 9.3 Knowledge/index packs

Knowledge/index generations may activate by switching a registry/index pointer after integrity and schema validation. Existing requests can remain pinned to the prior generation when consistency matters.

### 9.4 Theme/config/schema packs

Declarative packs may activate live only when the runtime recognizes their schema/version and the pack cannot escape its declared authority boundary.

---

## 10. Application Runtime Update Supervisor

Runtime/APK updates are separate from live packs.

A successful Forge/CI build is not automatically an installable/promoted update. It first passes the applicable update eligibility gates.

### 10.1 Channels

Planned channels:

- **STABLE** — only explicitly promoted/release-approved artifacts;
- **CANDIDATE** — eligible build-verified candidates under candidate policy;
- **DEV** — explicitly allowed development artifacts;
- **PINNED** — remain on a specified version until policy changes.

A device policy chooses which channels it may consume. Channel selection does not alter repository authority.

### 10.2 Runtime update flow

```text
Forge/source candidate
      |
      v
GitHub Actions / build evidence
      |
      v
BUILD + PROVENANCE GATE
      |
      v
eligible signed update manifest
      |
      v
SERVER discovers/downloads/stages
      |
      v
SERVER verifies artifact
      |
      v
CLIENT/SERVER target verifies independently
      |
      v
safe install boundary
      |
      v
Android package replacement
      |
      v
new process / relaunch / state restoration
      |
      v
post-update identity + health verification
```

### 10.3 Target verification is independent

SERVER verification never substitutes for the target device's checks. The target validates package identity, signing identity, artifact hash, version/channel eligibility, protocol compatibility, local approval/update policy, available storage, and safe execution state before committing installation.

### 10.4 Running versus replacing

Runtime APKs may be downloaded, hashed, validated, and staged while SWRLZ is running. Replacing the installed APK is a package/runtime replacement and may terminate/recreate the application process. SWRLZ should preserve safe resumable state and make the transition feel seamless, but documentation must not represent runtime code replacement as the same operation as a hot pack activation.

---

## 11. Launcher / Update Supervisor Role

A separate Launcher/Update Supervisor may coordinate CLIENT/SERVER runtime replacement so an application is not solely responsible for replacing itself while it is executing.

Potential responsibilities:

- own install session coordination;
- verify target runtime update metadata;
- wait for a safe update boundary;
- request/perform installation within Android-supported authority;
- observe package replacement;
- relaunch the updated CLIENT/SERVER when permitted;
- hand back a safe resume envelope;
- preserve recovery/rollback information.

The Launcher does not gain permission to bypass Android/user installation authority.

---

## 12. Resume Envelope

Before runtime replacement, SWRLZ may persist a small `UpdateResumeEnvelope` containing only safe resumable state, for example:

```text
updateTransactionId
conversationId
selectedSurface
missionSafeStateReference
serverConnectionIdentityReference
modelGenerationReference
previousRuntimeIdentity
expectedRuntimeIdentity
```

Do not place plaintext credentials, ephemeral secrets, hidden model reasoning, or unsafe partially executed actions into the resume envelope.

After replacement, the new runtime verifies its own BuildIdentity and update transaction before restoring state.

---

## 13. Update Policy

Representative policy controls:

```text
Update discovery:
  manual / scheduled

Download:
  ask / automatic

Activation:
  ask / automatic for eligible live packs

Runtime installation:
  ask / automatic only where platform + policy permit

Constraints:
  Wi-Fi only
  charging only
  idle only
  minimum battery
  do not interrupt active inference/mission
```

Policies must remain role-aware. An Android phone and a continuously powered NODE_HOST PC do not require identical defaults.

---

## 14. LOCAL / LAN / ONLINE Behavior

### SWRLZ LOCAL

CLIENT continues using installed runtime and packs. No ordinary internet update discovery occurs. A narrowly scoped bootstrap/recovery update path may exist as separately designed policy.

### SWRLZ LAN

CLIENT can receive update metadata/artifacts from an authenticated SERVER/private node when available. SERVER may serve already-cached verified packs even without internet.

### SWRLZ ONLINE

SERVER may check authorized update sources, fetch eligible artifacts, verify provenance, stage updates, and offer/activate them according to user policy and target authority.

### DEGRADED

Failure to reach update infrastructure must not break existing installed runtime/packs. Current verified generations remain active.

---

## 15. Manifest and Trust Requirements

Every official update generation requires signed, versioned metadata sufficient to verify identity and compatibility before activation.

The companion contract `../contracts/SWRLZ_UPDATE_AND_PACK_MANIFEST_CONTRACT_V1.md` defines representative fields and state transitions.

At minimum, update metadata should identify:

- product/pack ID and type;
- version and generation;
- channel when applicable;
- minimum/maximum compatible runtime/contract versions;
- dependencies;
- capabilities provided;
- object/artifact hashes and sizes;
- signing/provenance identity;
- activation class (`LIVE`, `QUIESCE`, `RUNTIME_REPLACE`);
- rollback compatibility;
- source/release lineage.

Trust verification occurs before activation, not after.

---

## 16. Forge and Update Eligibility

Forge may eventually upload a source candidate and request a build, but the following remain separate evidence classes:

1. source/static evidence;
2. compile evidence;
3. APK/build evidence;
4. device evidence;
5. integration evidence;
6. repository promotion/release/deployment evidence.

A successful workflow build can make an artifact **eligible for a configured candidate/dev update channel** only when the update policy and provenance contract permit it. It does not automatically:

- promote source authority;
- become STABLE;
- release/deploy itself;
- install on user devices;
- bypass signing/protocol/compatibility checks.

---

## 17. Relationship to Current Checkpoints

### INT-AI-040B

The approved 350M local-inference foundation remains the first bounded implementation checkpoint. Its job is to prove one detachable GGUF path through SWRLIE/local inference with model-independent contracts. This update architecture does not expand 040B into an updater implementation.

### INT-PACK-040C

Proposed future implementation checkpoint for the generic SERVER-owned Live Pack Manager: signed manifests, update-source abstraction, changed-object fetch, staging, hot activation, rollback, cleanup, and CLIENT administrative policy.

**Status:** planned/design only until separately approved and evidenced.

### INT-UPD-040D

Proposed future implementation checkpoint for signed CLIENT/SERVER/Launcher runtime update discovery, staging, verification, Android package replacement, safe relaunch/resume, and post-update health verification.

**Status:** planned/design only until separately approved and evidenced.

---

## 18. Non-Goals and Hard Boundaries

This architecture does not authorize or imply:

- arbitrary downloaded executable code hot-loading;
- bypassing Android package/install authority;
- treating a successful CI build as automatic repository promotion;
- allowing an LLM to approve its own update/action;
- silently replacing user-provided/custom models;
- deleting rollback generations before policy permits;
- weakening Truth Firewall or local-device authority during updates;
- open-ended CLIENT web access;
- embedding large model weights in ordinary CLIENT/SERVER source ZIPs or APKs.

---

## 19. Design Summary

```text
SWRLZ = stable control plane + replaceable runtime products + live capability packs

Runtime update:
  download -> verify -> safe boundary -> package replace -> relaunch -> verify

Live pack update:
  discover -> fetch changed objects -> verify -> stage -> health-check -> atomic activate -> rollback/cleanup

SWRLIE evolution:
  stable base + independent adapters/knowledge/config + occasional base refresh
```

The intended user experience is game-like: SWRLZ remains useful while large optional content downloads, capabilities become READY after verification, and most evolving model/content functionality can activate without reinstalling the application. The trust model remains stricter than the presentation: every transition is explicit, evidence-aware, rollback-capable, and bounded by SWRLZ/Android authority.