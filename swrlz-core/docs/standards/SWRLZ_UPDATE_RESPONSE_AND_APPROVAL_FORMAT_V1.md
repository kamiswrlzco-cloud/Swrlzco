# SWRLZ Update Response and Approval Boundary Standard V1

Date: 2026-08-01  
Purpose: preserve the delivery format used for SWRLZ-Core updates across chat-thread migrations

## Core response order

Every completed source or evidence delivery should use the following order.

### 1. DOWNLOADS block first

Place a fenced `DOWNLOADS` block at the very top. List every deliverable in canonical order.

Dual CLIENT/SERVER source delivery:

```text
DOWNLOADS

1. CLIENT source ZIP
2. CLIENT metadata ZIP
3. SERVER source ZIP
4. SERVER metadata ZIP
5. combined evidence ZIP
```

Single component source delivery:

```text
DOWNLOADS

1. component source ZIP
2. component metadata ZIP
3. checkpoint evidence ZIP
```

### 2. Direct artifact links

Provide one explicit link per file. Do not hide multiple files behind one vague label.

### 3. Checkpoint completion heading

State the bounded checkpoint ID and whether it is complete, pending, blocked, or evidence-only.

### 4. Package receipt table

For every package state:

- exact filename;
- byte size;
- SHA-256.

Never round the values in the authoritative receipt table.

### 5. Identity and lineage

For each affected component include:

- component and candidate identity;
- versionCode and versionName;
- direct parent filename and SHA-256;
- whether lineage is byte-exact, retained byte-exact, derived, or functional-descendant rebase.

### 6. Implementation facts

Explain what changed in operational terms. Separate:

- facts actually implemented;
- requirements from the approved scope;
- assumptions;
- recommendations or next steps.

Do not describe prepared repository patches as applied. Do not describe source/static validation as Android compilation.

### 7. Validation and evidence

List the checks actually run, including pass counts when available. Examples:

- focused verifier results;
- source-manifest entry counts;
- metadata ZIP root-entry count;
- ZIP CRC;
- Kotlin parser or focused compilation;
- resolver fixtures;
- deterministic repackaging.

### 8. Build boundary

State every major activity that was not performed:

```text
Android compile: NOT RUN
APK build: NOT RUN
GitHub write: NONE
Workflow run: NONE
Install: NONE
Promotion/release/deploy: NONE
```

When a workflow failed before Gradle, say the source was not compiled rather than calling it a source failure.

### 9. Approval boundary footer

Every stop ends with exactly these five elements:

1. **Approval waiting** — checkpoint or `None`.
2. **What approval would authorize** — exact bounded actions.
3. **What approval would not authorize** — explicit exclusions.
4. **Expected result** — measurable outcome.
5. **Exact approval phrase** — copyable fenced text, or `None required`.

## Trust and precision rules

- Computed hashes outrank filenames.
- Workflow logs outrank assumptions about CI.
- Device acceptance outranks source-only validation.
- Historical failures remain documented after repair.
- Current-push evidence must not be confused with repository-latest fallback.
- Shared CLIENT/SERVER capabilities default to synchronized updates.
- Retaining one component byte-exact is valid; inventing identity churn to simulate synchronization is not.

## Source-description standard

Before Forge uploads, and in the response describing the upload, include:

- component and APK target;
- exact source filename;
- CF version, candidate revision, and versionCode;
- metadata mode and companion filename;
- SHA-256 and byte size;
- repository lane;
- matching evidence bundle;
- selection reason.

The same identity should persist through upload logs, workflow watch, workflow result, and artifact provenance.

## Incident-response standard

When a workflow fails:

1. identify the exact failing step;
2. state whether Gradle was reached;
3. separate primary errors from cascades;
4. state what was not tested;
5. avoid reissuing a source candidate when the defect is CI-only;
6. define a bounded repair with regression coverage;
7. preserve the failed evidence in the next handoff.

## Documentation and repository writes

A source checkpoint does not automatically authorize repository writes. A documentation-only request authorizes only the stated documentation paths. A CI-only request does not authorize CLIENT or SERVER source churn.

## Tone and readability

Responses should remain direct, technically precise, warm, and easy to scan. Mild SWRLZ/dragon humor is acceptable around the edges, but hashes, boundaries, identities, and approvals must remain unambiguous.

## Migration instruction

A new chat should use this document as the response-format contract unless Kamilion explicitly changes the format.
