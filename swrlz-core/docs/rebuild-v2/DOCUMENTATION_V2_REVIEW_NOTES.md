# SWRLZ Documentation Rebuild v2 — Review Notes

## Corrected

- Corrected the Phase B checkpoint date from `2025-01-21` to `2026-07-25`.
- Added explicit evidence classifications to prevent source presence, compilation, device behavior, and inference from being conflated.
- Added package-accounting rules because original source workspace counts and packaged ZIP entry counts represent different measurements.
- Added repository-migration guidance for the planned new official SWRLZ account/repository.
- Clarified that `.reference` CLIENT CFv2.0.69 and SERVER CFv2.0.49 trees are historical evidence baselines, not automatically current source authority.

## Known review item

`docs/server/SERVER_IMPLEMENTATION_ANALYSIS.md` contains wording from an earlier phase that says implementation cannot be labelled because server source was unavailable, even though later sections use the extracted SERVER source. This historical contradiction should be normalized during the next full documentation regeneration against the latest SERVER source.

## Recommended next documentation pass

Regenerate implementation analysis from the latest authoritative CLIENT/SERVER packages and produce evidence-tagged deltas rather than rewriting from memory.
