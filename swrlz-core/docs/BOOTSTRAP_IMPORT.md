# Repository Bootstrap Import

The current CLIENT source includes a deterministic Forge bootstrap route for this repository.

## Forge menu

1. Target `kamiswrlzco-cloud/Swrlzco` on `main`.
2. Stage `SWRLZCO_NEW_REPOSITORY_BOOTSTRAP.zip`.
3. Arm **EXPAND GENERIC ZIP TO REPOSITORY ROOT**.
4. Optionally arm **REMOVE OUTER ZIP AFTER EXPANSION**.
5. Commit the transaction.

Forge expands the outer bootstrap ZIP locally and creates Git blobs for each contained file. The final repository tree is committed atomically. Protected nested CLIENT/SERVER source ZIPs are retained as ZIP files and are not recursively expanded.

## Chat

A request such as `upload the bootstrap and unzip it in the repo` starts the same bootstrap Forge flow. Adding `remove the zip` arms outer-ZIP removal. Android may still require the user to select the local bootstrap document so Forge receives storage permission.

## Safety boundary

Archive traversal paths, `.git` injection, duplicate/case-colliding paths, archives above 2,500 files or 512 MiB expanded size, and individual files above GitHub's regular 100 MiB Git blob boundary are rejected before commit.
