# Authoritative Source Repository Baseline

Recorded: 2026-07-25

This file documents the authoritative SWRLZ source clone used as evidence for the documentation rebuild. The clone is located at `.reference/swrlz-source/` and must be treated read-only for this reconstruction task.

- Repository URL: https://github.com/ahazus420-stack/Swrlzcore.git
- Owner: ahazus420-stack
- Repository name: Swrlzcore
- Clone path in workspace: `.reference/swrlz-source/`
- Current branch: `main`
- HEAD commit SHA: `7406f66efe119618b77792d2dfddecc49cbfe5ac`
- HEAD commit date: `2026-07-25 10:22:05 -0500`

Source root path: /workspaces/Swrlzco/.reference/swrlz-source

Notes and constraints:

- The `.reference/swrlz-source/` clone is for analysis only. Do NOT modify, commit to, or push changes to this clone from this workspace.
- When producing the final documentation archive, do NOT include `.reference/swrlz-source/.git/`.
- For reproducibility, record the exact commit SHA above when referencing implementation evidence.

Update guidance for future operators:

To update the authoritative clone (manual operation):

```bash
cd .reference/swrlz-source
git fetch origin
git checkout main
git pull --ff-only origin main
# record new commit SHA with: git rev-parse HEAD
```
