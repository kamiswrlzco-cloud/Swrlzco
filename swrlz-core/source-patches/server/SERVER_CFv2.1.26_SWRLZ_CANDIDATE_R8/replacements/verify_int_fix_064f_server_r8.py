#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    ROOT / "app/src/main/java/sh/swrlz/nodehost/forge/ForgeAutomatedBuildRunner.kt": "sh.swrlz.nodehost.forge",
    ROOT / "app/src/main/java/sh/swrlz/nodehost/forge/ForgeBuildMonitor.kt": "sh.swrlz.nodehost.forge",
}

checks = []
def check(name: str, ok: bool, detail: str = "") -> None:
    checks.append((name, ok, detail))

for path, package in EXPECTED.items():
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^package\s+([A-Za-z0-9_.]+)", text, re.MULTILINE)
    check(f"{path.name}: declaration", match is not None, match.group(1) if match else "missing")
    check(f"{path.name}: package/path", bool(match and match.group(1) == package), match.group(1) if match else "missing")
    check(f"{path.name}: no swurlz namespace", "sh.swurlz.nodehost" not in text)

build = (ROOT / "app/build.gradle.kts").read_text(encoding="utf-8")
check("versionCode 91", "versionCode = 91" in build)
check("versionName R8", 'versionName = "2.1.26-forge-package-namespace-fix-r8"' in build)
wrong = []
for path in (ROOT / "app/src/main/java").rglob("*.kt"):
    text = path.read_text(encoding="utf-8")
    if "package sh.swurlz.nodehost" in text:
        wrong.append(str(path.relative_to(ROOT)))
check("no wrong SERVER package declarations", not wrong, ", ".join(wrong))

for name, ok, detail in checks:
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" :: {detail}" if detail else ""))
failed = [name for name, ok, _ in checks if not ok]
print(f"SUMMARY {len(checks)-len(failed)}/{len(checks)} PASS")
if failed:
    print("FAILED: " + ", ".join(failed), file=sys.stderr)
    raise SystemExit(1)
