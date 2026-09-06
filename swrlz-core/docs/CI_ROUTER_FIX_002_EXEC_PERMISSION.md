# CI Router Fix 002 — Build Helper Execution Permission

## Failure observed

The CLIENT and SERVER matrix jobs both successfully reached the build stage after:

- source route resolution,
- exact ZIP/checksum selection,
- package-pair SHA-256 verification.

Both then stopped before Gradle compilation with exit code 126:

`swrlz-core/tools/ci/build_swrlz_component.sh: Permission denied`

## Root cause

Repository/Forge uploads should not require POSIX executable-bit preservation for CI helper files.
The router invoked `build_swrlz_component.sh` as an executable path, so a normal mode-100644
checkout fails even though the script contents are valid.

## Fix

Invoke the helper explicitly through Bash:

`bash "$SWRLZ_CI_ROOT/build_swrlz_component.sh" ...`

This makes CLIENT and SERVER builds independent of the helper file's executable bit.

The resolver test setup also clears inherited GitHub push-event variables so isolated unit tests
no longer emit irrelevant `fatal: bad object` messages from the parent workflow event.

## Scope

No CLIENT or SERVER source package, source SHA, mission setting, or repository authority is changed.
