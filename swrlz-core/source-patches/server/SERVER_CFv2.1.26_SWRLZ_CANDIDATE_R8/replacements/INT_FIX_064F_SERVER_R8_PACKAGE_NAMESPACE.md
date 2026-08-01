# INT-FIX-064F — SERVER R8 Forge Package Namespace Repair

## Compiler evidence
Workflow logs for SERVER R7 reached `:app:compileDebugKotlin` after source reconstruction and metadata verification. The two shared Forge files declared `sh.swurlz.nodehost.forge` while their path, imports, and SERVER namespace use `sh.swrlz.nodehost.forge`.

## Repair
- Correct `ForgeAutomatedBuildRunner.kt` package to `sh.swrlz.nodehost.forge`.
- Correct `ForgeBuildMonitor.kt` package to `sh.swrlz.nodehost.forge`.
- Preserve all Downloads-inbox, package pairing, source description, build-watch, artifact extraction, and GitHub reconciliation behavior.
- Advance SERVER to CFv2.1.26 R8 / VC91.
- Add package-path regression verification.

## Boundary
This source candidate does not claim Android build success until the authorized GitHub workflow completes.
