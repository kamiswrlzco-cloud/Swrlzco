# SWRLZ Update and Pack Manifest Contract v1.0

**Status:** Design contract / documentation evidence only. No implementation claim.

**Applies to:** CLIENT, SERVER, Launcher/Update Supervisor, SWRLIE model packs, knowledge packs, theme packs, tool/config packs, and future compatible pack types.

**Companion architecture:** `../architecture/SWRLZ_RUNTIME_AND_LIVE_PACK_UPDATE_ARCHITECTURE_V1.md`

---

## 1. Goals

This contract defines a common SWRLZ-owned envelope for discovering, validating, staging, activating, rolling back, and accounting for runtime and live-pack updates without tying trust or identity to a single hosting provider.

The contract must preserve:

- offline-first behavior;
- CLIENT local-device authority;
- SERVER network/heavywork authority;
- Truth Firewall and approval policy;
- independent CLIENT, SERVER, and MODEL version lines;
- explicit provenance and evidence classes;
- rollback and immutable generation identity;
- provider/source replaceability.

---

## 2. Product Classes

`productType` is one of the following initial classes:

```text
CLIENT_RUNTIME
SERVER_RUNTIME
LAUNCHER_RUNTIME
MODEL_BASE
MODEL_ADAPTER
KNOWLEDGE
THEME
TOOL_SCHEMA
DEVICE_DATA
CONFIG
```

Additional pack classes require a contract revision or explicitly compatible extension mechanism.

Executable Android/native behavior must use a runtime product class. Data/model/content packs must not be used to smuggle executable DEX/native code into a live activation path.

---

## 3. Activation Classes

Each update declares an `activationClass`:

- `LIVE` — may activate while the runtime remains active after validation and optional health check.
- `QUIESCE` — runtime remains installed, but affected work must reach a safe boundary before pack/model unload/reload and activation.
- `RUNTIME_REPLACE` — requires signed package/runtime replacement and process restart/relaunch semantics.

Examples:

| Product type | Typical activation |
|---|---|
| THEME | LIVE |
| KNOWLEDGE | LIVE |
| CONFIG | LIVE |
| MODEL_ADAPTER | LIVE or QUIESCE |
| MODEL_BASE | QUIESCE |
| CLIENT_RUNTIME | RUNTIME_REPLACE |
| SERVER_RUNTIME | RUNTIME_REPLACE |
| LAUNCHER_RUNTIME | RUNTIME_REPLACE |

The runtime may impose a stricter activation class than the manifest requests. It must never silently downgrade required safety.

---

## 4. Channel Classes

Runtime update manifests may use:

```text
STABLE
CANDIDATE
DEV
PINNED
```

- `STABLE` requires explicit promotion/release authority.
- `CANDIDATE` represents an eligible candidate and remains distinct from current source authority.
- `DEV` is development-only and requires explicit device policy.
- `PINNED` is a local policy state, not a publication claim.

Live packs may also expose channels when useful, but channel identity does not replace signature/provenance verification.

---

## 5. Manifest Envelope

Representative schema:

```json
{
  "schemaVersion": 1,
  "manifestId": "...",
  "productType": "MODEL_ADAPTER",
  "productId": "swrlie.android",
  "version": "1.8.0",
  "generation": 18,
  "channel": "CANDIDATE",
  "activationClass": "LIVE",
  "provider": "SWRLIE",
  "runtimeContract": {
    "min": 1,
    "max": 1
  },
  "protocolContract": {
    "min": 1,
    "max": 1
  },
  "dependencies": [],
  "capabilities": [],
  "objects": [],
  "lineage": {},
  "signing": {},
  "rollback": {},
  "release": {}
}
```

Exact serialization and signature canonicalization must be frozen before implementation evidence is claimed.

---

## 6. Required Identity Fields

Each manifest must provide enough identity to prevent ambiguous or cross-product activation:

```text
schemaVersion
manifestId
productType
productId
version
generation
activationClass
```

When applicable:

```text
channel
provider
modelFamily
baseModelId
quantization
packageName
versionCode
versionName
```

`generation` identifies one immutable activation generation. Different bytes or object sets must not reuse the same generation identity.

---

## 7. Compatibility Fields

Compatibility is explicit rather than inferred.

Representative fields:

```text
runtimeContract.min
runtimeContract.max
protocolContract.min
protocolContract.max
modelContractVersion
supportedABIs
supportedAccelerators
minimumSdk
maximumSdk
requiredCapabilities
incompatibleCapabilities
```

A target that cannot prove compatibility fails closed or remains on the existing active generation.

---

## 8. Dependencies

Each dependency may specify:

```text
productId
productType
minVersion
maxVersion
requiredGeneration
requiredObjectHash
optional
```

Dependency resolution occurs before activation. Cycles, missing required dependencies, or incompatible version ranges block activation.

---

## 9. Objects

Each immutable object entry should contain at least:

```text
objectId
sha256
sizeBytes
mediaType
role
sourceRef
```

`objectId` should normally be derived from or strongly bound to SHA-256.

Optional fields:

```text
chunkIndex
chunkCount
compression
uncompressedSha256
uncompressedSizeBytes
storageClass
```

If an exact trusted object already exists locally, it may be reused without transfer.

---

## 10. Lineage

Representative lineage fields:

```text
baseLineage
parentManifestId
parentGeneration
sourceRepository
sourceCommit
sourcePackage
sourceSha256
workflowRun
buildArtifactId
upstreamModel
upstreamRevision
license
```

The presence of lineage metadata does not itself prove validity; the updater validates the applicable evidence independently.

---

## 11. Signing and Trust

Official manifests must be signed under a SWRLZ-controlled trust policy.

Representative signing fields:

```text
algorithm
keyId
signature
signedAt
trustClass
```

Trust classes should distinguish at least:

```text
OFFICIAL_VERIFIED
USER_PROVIDED_UNVERIFIED
MODIFIED
SIGNATURE_INVALID
UNKNOWN
```

The LLM/model must not be able to override signature or trust classification.

---

## 12. Runtime Package Fields

For `CLIENT_RUNTIME`, `SERVER_RUNTIME`, or `LAUNCHER_RUNTIME`, include sufficient package identity to validate an Android/runtime replacement:

```text
packageName
versionCode
versionName
apkSha256
apkSizeBytes
signingCertificateDigest
sourceSha256
workflowRun
protocolContract
channel
```

A build success alone is not an install authorization.

---

## 13. Model and Adapter Fields

For model products, representative fields include:

```text
provider = SWRLIE
modelId
modelFamily
modelVersion
runtimeFormat
quantization
contextWindow
memoryRequirement
supportedABIs
supportedAccelerators
baseModelId
baseModelGeneration
adapterType
capabilities
license
```

A model adapter must declare the base model/model-contract range it is compatible with.

---

## 14. Update Index

An update source may expose a small signed index that points to product manifests.

Representative logical form:

```json
{
  "schemaVersion": 1,
  "channel": "CANDIDATE",
  "products": {
    "client": { "manifest": "..." },
    "server": { "manifest": "..." },
    "swrlie": { "manifest": "..." }
  }
}
```

The index is discovery metadata. Each referenced manifest and artifact remains independently verified.

---

## 15. Update Planning

Before downloading, the updater computes a plan:

```text
KEEP
FETCH
REUSE_LOCAL_OBJECT
STAGE
ACTIVATE
REMOVE_AFTER_ROLLBACK_WINDOW
BLOCK
```

The plan should be inspectable in diagnostics and suitable for user approval when policy requires it.

Example:

```text
BASE A          REUSE_LOCAL_OBJECT
TOOLS B         KEEP
ANDROID C->D    FETCH D
KNOWLEDGE E     FETCH E
```

---

## 16. State Machine

A generation may move through:

```text
DISCOVERED
  -> PLANNED
  -> DOWNLOADING
  -> DOWNLOADED
  -> VERIFIED
  -> STAGED
  -> HEALTH_CHECKING
  -> READY
  -> ACTIVATING
  -> ACTIVE
```

Failure states:

```text
BLOCKED
FAILED_DOWNLOAD
FAILED_VERIFICATION
FAILED_COMPATIBILITY
FAILED_HEALTH_CHECK
FAILED_ACTIVATION
ROLLED_BACK
SUPERSEDED
```

The previously active generation remains active until the new generation reaches a valid activation point.

---

## 17. Atomic Activation

Never patch the active generation in place.

The updater stages a complete candidate generation, verifies it, and then changes an active-generation reference atomically or through the strongest equivalent primitive available on the target platform.

For requests that span an activation boundary, the runtime may pin them to the generation they started with.

---

## 18. Rollback

Rollback metadata may define:

```text
previousManifestId
previousGeneration
minimumRetention
rollbackCompatible
```

A new generation should not cause immediate destruction of the last known-good generation. Cleanup occurs only after the applicable health/retention/policy conditions are satisfied.

---

## 19. Source Adapter Contract

The updater should depend on an abstract source interface with operations equivalent to:

```text
fetchIndex()
fetchManifest(ref)
fetchObject(ref, expectedIdentity)
health()
```

Possible implementations include GitHub release/artifact sources, Hugging Face/model sources, object stores/CDNs, and authenticated LAN/private-node sources.

Source adapters deliver bytes and metadata. They do not redefine SWRLZ trust, promotion, approval, or activation policy.

---

## 20. SERVER and CLIENT Responsibilities

### SERVER

- normal internet discovery;
- remote manifest/object fetch;
- heavy verification/provenance work;
- caching and LAN distribution;
- model/pack lifecycle on SERVER-owned storage;
- update-plan reporting.

### CLIENT

- local-device update policy;
- independent target verification;
- Android package-install authority boundary;
- local pack activation only for CLIENT-owned pack classes;
- user approval where required;
- post-update local observation/result reporting.

SERVER verification never substitutes for CLIENT/device verification.

---

## 21. Resume Envelope Contract

Runtime replacement may use a separate resumable-state envelope. It must not be confused with an update manifest and must not contain credentials or hidden reasoning.

Representative safe references:

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

---

## 22. Evidence Boundary

This contract is documentation/architecture evidence only.

It does not prove:

- a Live Pack Manager exists;
- automatic update discovery exists;
- a signing infrastructure exists;
- model adapters are trained or compatible;
- Launcher runtime replacement is implemented;
- any GitHub/Hugging Face/object-store release path is configured;
- any update was downloaded, activated, installed, released, or deployed.

Implementation, build, device, integration, promotion, release, and deployment evidence remain separate.