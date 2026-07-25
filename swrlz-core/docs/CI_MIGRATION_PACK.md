# CI Migration Pack

Target repository: `kamiswrlzco-cloud/Swrlzco`

## Install paths

- `.github/workflows/swrlz-apk-router.yml`
- `.github/workflows/source-package-integrity.yml`
- `swrlz-core/requests/000_CURRENT.request`
- `swrlz-core/tools/ci/resolve_swrlz_source.py`
- `swrlz-core/tools/ci/test_resolve_swrlz_source.py`
- `swrlz-core/tools/ci/verify_swrlz_package_pair.py`
- `swrlz-core/tools/ci/build_swrlz_component.sh`

## Migration decisions

- Active build components are currently CLIENT and SERVER only.
- Source lanes are `swrlz-core/sources/client` and `swrlz-core/sources/server`.
- Executable Actions workflows remain at repository-root `.github/workflows/`.
- The unified request file lives at `swrlz-core/requests/000_CURRENT.request`.
- CI helper code lives under `swrlz-core/tools/ci/`.
- Optional committed build outputs live under `swrlz-core/releases/`.
- Normal workflow artifacts remain GitHub Actions artifacts instead of being committed.
- CLIENT builds no longer require an external LLM/API key merely to compile the Android project.
