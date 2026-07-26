# Checkpoint INT-THEME-035D: CLIENT Package Pair Repair

Mode: IMPLEMENT
Lifecycle state: IMPLEMENTATION_VERIFIED / DOCUMENTATION_SYNCED
Status: `PACKAGE PAIR VERIFIED LOCALLY; REPOSITORY CI PENDING`

## Objective

Repair the canonical CLIENT source ZIP/checksum/manifest contract after both
automatic workflows stopped before compilation on the published CFv2.1.8 manifest.

## Success criteria

- Preserve CFv2.1.8 theme/application behavior.
- Preserve the failed CFv2.1.8 pair and workflow evidence.
- Advance a distinct successor identity.
- Pass the repository package-pair verifier.
- Synchronize authority, lineage, release, engineering, and handoff documentation.

## Confirmed facts

- PR #1 merged CFv2.1.8 to `main` at
  `bc80d7a4d28d656f640ac1a511b9ae340e8b45ee`.
- Source Package Integrity run `30222384992` failed manifest verification.
- APK Router run `30222384996` passed resolver tests and failed the same manifest
  verification before Android compilation.
- The CFv2.1.8 ZIP/SHA pair matched.
- Its manifest used `sourcePackage` and `bytes` rather than canonical `zip` and
  `size_bytes`, and omitted `verified: true`.

## Requirements

- Integrate; do not overwrite.
- Preserve CLIENT/SERVER separation, offline-first behavior, identity, trust,
  Truth Firewall, local/remote distinctions, and protocol discipline.
- Do not replace the failed package under the same version.
- No release or deployment.

## Assumptions

None material. The failure contract and verifier implementation were directly inspected.

## Recommendations

Perform device validation only after a successful CI APK build.

## Sources of truth inspected

- Merge commit `bc80d7a4d28d656f640ac1a511b9ae340e8b45ee`
- Workflow runs `30222384992` and `30222384996`
- `swrlz-core/tools/ci/verify_swrlz_package_pair.py`
- CFv2.1.8 ZIP, SHA-256, manifest, and checkpoint record

## Files changed

- CLIENT build/package identity and in-package checkpoint documentation
- `sources/client/CLIENT_CFv2.1.9_SWRLZ.{zip,sha256,manifest.json}`
- current authority, compatibility, checkpoint, release, engineering, index,
  source-lane, and handoff documentation

## Implementation summary

CLIENT advances to CFv2.1.9 / versionCode 107 /
`2.1.9-package-pair-repair-v1`. Theme source is unchanged. The manifest retains
rich checkpoint fields and adds canonical `zip`, `sha256`, `size_bytes`, and
`verified: true` fields.

## Documentation impact set

- Categories: AUTHORITY / INDEX; CHECKPOINT / DELIVERY RECEIPT; CHANGELOG /
  RELEASE NOTE; BUILD / PACKAGING; KNOWN ISSUES / LIMITATIONS; PROVENANCE /
  LINEAGE; HANDOFF
- Documents updated: current authority, documentation index/manifest, status and
  compatibility matrices, Engineering Log, CFv2.1.8 historical evidence, CLIENT
  source-lane README, CFv2.1.9 release and handoff
- Architecture/contracts intentionally unchanged because application behavior and
  protocol semantics did not change
- Documentation gate: PASS

## Verification

- Behavior diff from CFv2.1.8: 9 paths, limited to build/package identity and documentation
- Archive: 688 entries; CRC PASS; one canonical root; traversal/absolute paths absent
- Bytes: `36,527,185`
- SHA-256: `87a09a5032751dbf74f5a277a6d9b0e1f9bc48e38e48006c50d0c107cd3d30ac`
- Independent deterministic repackage: byte-identical
- Repository package-pair verifier: PASS locally

## Build evidence

- Status: BUILD PENDING
- Failed predecessor runs: `30222384992`, `30222384996`
- CFv2.1.9 workflow/run: pending repository promotion
- Artifact: none yet

## Device evidence

- Status: DEVICE TEST PENDING
- Evidence: none
- Acceptance: not claimed

## Provenance and lineage

CFv2.1.7 → CFv2.1.8 / INT-THEME-035C → CFv2.1.9 / INT-THEME-035D.
CFv2.1.8 remains preserved as failed package-pair lineage.

## Known limitations

Package verification does not prove Android compilation or device behavior.

## Unresolved issues

CI compilation and device acceptance remain evidence-gated.

## Current disposition

Repository promotion and automatic CI are authorized. Release, deployment, and
installation are excluded.

## Approval required to continue

- Waiting for: NOT APPLICABLE within the currently authorized repair/CI gate
- Approval would authorize: NOT APPLICABLE
- Approval would not authorize: release, deployment, installation, SERVER, protocol, or authority changes
- Expected result: repository verification followed by CLIENT debug APK CI evidence
- Exact approval phrase: NOT APPLICABLE
