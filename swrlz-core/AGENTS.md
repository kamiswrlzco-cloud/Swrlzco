# AGENTS

Guidance for automated agents working inside `swrlz-core/`.

## Authority order

1. Current verified source package + matching SHA-256 under `sources/`.
2. Current repository HEAD and source-derived evidence.
3. Build/workflow evidence and release provenance.
4. Current maintained documentation under `docs/`.
5. WordMesh architectural specifications.
6. Historical Documentation Rebuild v2 and `.reference` evidence.

Use the implementation labels:

`IMPLEMENTED`, `PARTIAL`, `PLANNED`, `EXPERIMENTAL`, `DEPRECATED`, `UNKNOWN`.

## Rules

- Do not silently treat historical `.reference` trees as current implementation authority.
- Do not claim compilation, device testing, or integration success without corresponding evidence.
- Keep CLIENT and SERVER source lineage separate.
- Source ZIPs must remain paired with their exact `.sha256` sibling.
- Record exact paths, hashes, workflow/run evidence, and rollback lineage for automated repairs.
- GitHub Actions YAML belongs at repository-root `/.github/workflows/`, not under `swrlz-core/`.
