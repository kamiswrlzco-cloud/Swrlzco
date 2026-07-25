# Official SWRLZ Repository Migration Foundation

## Selected repository layout

```text
/
├── README.md
├── .github/
│   └── workflows/
└── swrlz-core/
    ├── README.md
    ├── AGENTS.md
    ├── docs/
    ├── schemas/
    ├── brain/
    │   ├── core/
    │   ├── packs/
    │   └── manifests/
    ├── sources/
    │   ├── client/
    │   └── server/
    ├── requests/
    │   ├── client/
    │   ├── server/
    │   ├── brain/
    │   └── inbox/
    ├── releases/
    ├── reports/
    └── tools/
```

## Authority model

- `sources/*` contains current build-input packages and checksum siblings.
- `docs/` contains maintained engineering documentation.
- `requests/*` contains structured requests and request inboxes, not executable authority.
- `releases/` stores release/provenance records.
- `brain/` is reserved for machine-readable brain schemas, packs, manifests, and metadata.
- Historical `.reference` material remains archival evidence only.

## GitHub Actions rule

Executable GitHub Actions YAML must remain at repository-root:

```text
/.github/workflows/
```

It must not be moved under `/swrlz-core/.github/workflows/`.

## Migration gate

Before declaring a new source version production-authoritative:

1. Store the exact source ZIP and checksum sibling.
2. Verify SHA-256.
3. Record version metadata and source lineage.
4. Run the correct CLIENT/SERVER workflow.
5. Preserve logs and produced artifact provenance.
6. Record the migration/build commit and any repair attempts.
