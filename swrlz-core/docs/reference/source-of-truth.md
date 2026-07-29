# Source of Truth

Authority for implementation evidence in the official repository:

1. `docs/CURRENT_AUTHORITY.md` for the currently promoted CLIENT/SERVER source identities and their exact SHA-256 values.
2. Exact candidate source identities under `swrlz-core/sources/` plus matching transport/checksum/manifest evidence where present, treated according to their evidence class rather than as automatic promotion.
3. Current `kamiswrlzco-cloud/Swrlzco` repository HEAD and direct code evidence.
4. Build/workflow logs, provenance, artifacts, and verified release evidence.
5. Maintained documentation under `swrlz-core/docs/`.
6. WordMesh architecture/specification documents.
7. Historical Documentation Rebuild v2, prior repository snapshots, and `.reference` evidence.

Project-owner/operator reports and supplied device screenshots may establish **working project state** when no concrete contradictory evidence is present. They must be labeled as operator/device evidence and do not silently become promoted source authority, exact source-SHA→build provenance, release evidence, or deployment evidence.

Historical source is evidence of lineage, not automatic authority for current behavior.

Candidate transport/checksum presence proves the represented source identity/evidence only. It does not silently prove compilation, APK build, device behavior, integration, promotion, release, deployment, or installation.

Compilation, source/static evidence, APK/build evidence, device behavior, operator-reported working state, integration behavior, repository promotion, release, and deployment are separate evidence classes and must not be conflated.
