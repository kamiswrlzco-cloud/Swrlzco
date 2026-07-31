# Swrlzco

Official SWRLZ repository shell.

The active project root is [`swrlz-core/`](swrlz-core/).

GitHub Actions workflows intentionally live at repository-root
[`.github/workflows/`](.github/workflows/) because GitHub only discovers workflow
files from that repository-level location.

## Current documentation entry points

- [`swrlz-core/docs/CURRENT_AUTHORITY.md`](swrlz-core/docs/CURRENT_AUTHORITY.md) — promoted authority and current-candidate pointer
- [`swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md`](swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md) — current CLIENT/SERVER candidate lineage and identity-collision accounting
- [`swrlz-core/docs/patch-notes/CLIENT_PATCH_NOTES.md`](swrlz-core/docs/patch-notes/CLIENT_PATCH_NOTES.md)
- [`swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md`](swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md)
- [`swrlz-core/docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md`](swrlz-core/docs/contracts/SWRLZ_PATCH_NOTE_AND_LINEAGE_ACCOUNTING_V1.md) — mandatory future patch-note/lineage synchronization contract
- [`swrlz-core/docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md`](swrlz-core/docs/checkpoints/INT-CI-061A_ROUTER_DOCUMENTATION_PATCHNOTE_SYNC.md) — current Source Package Integrity / APK Router repair and documentation sync

## Current source lanes

- `swrlz-core/sources/client/`
- `swrlz-core/sources/server/`

## Current request lanes

- `swrlz-core/requests/client/`
- `swrlz-core/requests/server/`
- `swrlz-core/requests/brain/`
- `swrlz-core/requests/inbox/`

Promoted authority, candidate transport, build output, downloaded artifact, installed state, release, and deployment remain separate evidence classes. Start with `swrlz-core/docs/CURRENT_AUTHORITY.md` before treating a later candidate as current authority.
