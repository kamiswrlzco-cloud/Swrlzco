# Documentation Manifest and Package Accounting

**Migration generation:** New official `Swrlzco/swrlz-core` bootstrap  
**Prepared:** 2026-07-26

## Current source baseline

| Role | Package | SHA-256 |
|---|---|---|
| CLIENT | `CLIENT_CFv2.1.8_SWRLZ.zip` | `d344e683cc76756020b1a02e118b2417c03d6552eeb032dd5dd91058c0f7f055` |
| SERVER | `SERVER_CFv2.1.0_SWRLZ.zip` | `ca0bcc74ff105dbfd903f44716137eae094890bcaf6ea90ff6230ae5020fa940` |

## Counting policy

Report these separately whenever producing handoffs or releases:

- `workspace_source_count`
- `packaged_source_count`
- `documentation_file_count`
- `excluded_file_count`
- `package_entry_count`

## Imported documentation

The maintained `docs/` seed was imported from `SWRLZ_Documentation_Rebuild_v2_FULL.zip`.

The following were intentionally **not promoted into active repository authority**:

- `.reference/` extracted historical source-tree duplicates
- `_wordmesh_doc/` raw extracted Office/XML internals

Historical rebuild reports were retained under `docs/rebuild-v2/`.

## Version policy

The current source authority is the source package + exact checksum under `sources/`, subject
to later supersession by a newer explicitly verified package or repository HEAD.

Build success, device testing, and integration status remain evidence-gated.

CLIENT CFv2.1.8 is an `IMPLEMENTED — SOURCE ONLY` candidate under `INT-THEME-035C`.
Its manifest, checkpoint record, architecture note, release note, and static progress-geometry
evidence are maintained in this repository. The CFv2.1.7 parent package is retained for rollback.
The SERVER row is preserved from the repository baseline and was not revalidated by this
CLIENT-only checkpoint.
