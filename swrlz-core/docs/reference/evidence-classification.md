# Evidence Classification and Documentation Truth Model

**Status:** Accepted documentation governance foundation for CFv2.1.x and later.

## Purpose

SWRLZ documentation must distinguish implementation evidence from inference. A feature is not considered fully verified simply because source exists or a previous document claims it.

## Evidence levels

- `SOURCE_VERIFIED` — implementation is directly present in the referenced source.
- `STATIC_VERIFIED` — syntax/resource/schema/static checks passed.
- `COMPILE_VERIFIED` — the relevant project compiled successfully.
- `APK_BUILT` — an installable APK artifact was produced.
- `DEVICE_VERIFIED` — behavior was observed on a real device.
- `INTEGRATION_VERIFIED` — cross-component behavior was exercised end-to-end.
- `DOCUMENTED` — behavior is described but not independently verified.
- `INFERRED` — conclusion is derived from surrounding evidence and must not be presented as fact.
- `UNKNOWN` — evidence is insufficient.

## Required rule

Every status matrix, feature registry, architecture claim, checkpoint, and future Brain Pack entry should preserve an evidence level and provenance path whenever practical.

## Brain ingestion rule

Machine knowledge generated from documentation must retain:
- source path or source commit;
- evidence level;
- version scope;
- confidence;
- supersession relationship;
- last verification date.

An `INFERRED` statement must never overwrite a `SOURCE_VERIFIED` or stronger fact without explicit review.
