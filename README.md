# Swrlzco

Official SWRLZ repository shell.

The active project root is [`swrlz-core/`](swrlz-core/).

GitHub Actions workflows intentionally live at repository-root [`.github/workflows/`](.github/workflows/) because GitHub only discovers workflow files from that repository-level location.

## Current documentation entry points

- [`swrlz-core/docs/CURRENT_AUTHORITY.md`](swrlz-core/docs/CURRENT_AUTHORITY.md) — promoted authority and current-candidate pointer
- [`swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md`](swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md) — current CLIENT/SERVER candidate lineage and evidence boundaries
- [`swrlz-core/docs/patch-notes/CLIENT_PATCH_NOTES.md`](swrlz-core/docs/patch-notes/CLIENT_PATCH_NOTES.md)
- [`swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md`](swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md)
- [`swrlz-core/docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`](swrlz-core/docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md) — mandatory every-update patch-note/lineage synchronization contract
- [`swrlz-core/docs/checkpoints/INT-DOC-065A_PATCH_NOTE_CATCHUP_AND_ENFORCEMENT.md`](swrlz-core/docs/checkpoints/INT-DOC-065A_PATCH_NOTE_CATCHUP_AND_ENFORCEMENT.md) — current patch-note catch-up and CI-audit checkpoint

## Documentation accounting

The independent `SWRLZ Patch Note Accounting` workflow audits package-internal and repository patch-history surfaces whenever CLIENT/SERVER sources or current patch documentation change. It is intentionally separate from Source Package Integrity and APK Router so documentation debt is never confused with source corruption or build failure.

Every future CLIENT/SERVER update must synchronize:

- package `ReleaseNotes.md`;
- package `CHANGELOG.md`;
- package `SWRLZ_PATCH_LINEAGE_INDEX_V1.json`;
- repository component patch notes;
- current candidate lineage and candidate pointer.

## Current source lanes

- `swrlz-core/sources/client/`
- `swrlz-core/sources/server/`

## Current request lanes

- `swrlz-core/requests/client/`
- `swrlz-core/requests/server/`
- `swrlz-core/requests/brain/`
- `swrlz-core/requests/inbox/`

Promoted authority, candidate transport, build output, downloaded artifact, installed state, device acceptance, release, and deployment remain separate evidence classes. Start with `swrlz-core/docs/CURRENT_AUTHORITY.md` before treating a later candidate as current authority.
