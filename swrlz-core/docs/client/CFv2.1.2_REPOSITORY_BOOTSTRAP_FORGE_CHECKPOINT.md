# CLIENT CFv2.1.2 — Repository Bootstrap Forge Checkpoint

Prepared: 2026-07-25

## Target

The CLIENT Forge now defaults to the new official repository shell:

- owner: `kamiswrlzco-cloud`
- repository: `Swrlzco`
- branch: `main`
- CLIENT source lane: `swrlz-core/sources/client`
- SERVER source lane: `swrlz-core/sources/server`
- generic/request lane: `swrlz-core/requests/inbox`

Existing installs using the old exact default source lanes are migrated only when targeting the new official repository. Custom repository targets remain user-controlled.

## Repository bootstrap expansion

Forge can stage a generic ZIP and expand its contents directly into repository root in one atomic Git commit. CLIENT_/SERVER_ protected source ZIPs are never unpacked by this path.

Two controls are exposed in the Forge menu and chat Forge card:

1. `EXPAND GENERIC ZIP TO REPOSITORY ROOT`
2. `REMOVE OUTER ZIP AFTER EXPANSION`

When removal is armed, Forge commits the expanded contents but does not retain the selected outer bootstrap ZIP. Nested ZIPs inside the bootstrap, including CLIENT/SERVER source packages, remain ordinary repository files.

Archive safety preflight rejects traversal paths, absolute paths, `.git` metadata injection, case-colliding paths, more than 2,500 expanded files, more than 512 MiB total expanded content, or any individual entry above GitHub's 100 MiB regular Git blob boundary.

## Chat route

Deterministic chat intent now recognizes bootstrap upload/expand/unzip requests. A phrase such as `upload the bootstrap and unzip it in the repo` opens a bootstrap Forge session. Phrases containing `remove zip`, `delete zip`, `without zip`, `clean up zip`, or `discard zip` arm outer-ZIP removal automatically.

## Repository operations

The Forge client now has direct repository primitives for:

- list repository path
- read UTF-8 text file
- create/update UTF-8 text file
- delete one repository file with explicit UI confirmation
- create a branch from the currently configured branch

The Forge menu exposes these under `REPOSITORY TOOLS`.

## Evidence boundary

Source changes were statically inspected and packaged. Android compilation remains unverified in this environment because the Gradle wrapper cannot reach `services.gradle.org` to obtain Gradle 8.7. Device and GitHub integration testing remain pending.
