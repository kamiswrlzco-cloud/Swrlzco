#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from resolve_push_changed_paths import ChangedRangeError, resolve_push_changed_paths

COMPONENTS = ("CLIENT", "SERVER")
TOOLING_PATHS = {
    "swrlz-core/tools/ci/resolve_swrlz_source.py",
    "swrlz-core/tools/ci/resolve_changed_source_identities.py",
    "swrlz-core/tools/ci/resolve_push_changed_paths.py",
    "swrlz-core/tools/ci/resolve_swrlz_latest_identity.py",
    "swrlz-core/tools/ci/plan_swrlz_build_route.py",
    "swrlz-core/tools/ci/plan_swrlz_candidate_checkout.py",
    "swrlz-core/tools/ci/plan_swrlz_integrity_route.py",
    "swrlz-core/tools/ci/prepare_swrlz_sparse_checkout.py",
    "swrlz-core/tools/ci/verify_swrlz_package_pair.py",
    ".github/workflows/source-package-integrity.yml",
}


class IntegrityRouteError(RuntimeError):
    pass


def expand_integrity_route(
    repo_root: Path,
    matrix: dict,
    has_work: bool,
    *,
    event_name: str,
    before_sha: str = "",
    after_sha: str = "",
) -> dict:
    if event_name != "push":
        return {"matrix": matrix, "has_work": has_work, "reason": "base-route"}
    try:
        changed, _ = resolve_push_changed_paths(repo_root, before_sha, after_sha, remote="origin")
    except ChangedRangeError as exc:
        raise IntegrityRouteError(str(exc)) from exc

    tooling_changed = bool(TOOLING_PATHS.intersection(changed))
    if not tooling_changed:
        return {"matrix": matrix, "has_work": has_work, "reason": "base-route"}

    include = matrix.get("include")
    if not isinstance(include, list):
        raise IntegrityRouteError("matrix.include must be a list")
    rows = include if has_work else []
    by_component: dict[str, dict] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise IntegrityRouteError("matrix include row must be an object")
        component = str(row.get("component") or "").upper()
        if component in COMPONENTS:
            by_component[component] = dict(row)

    for component in COMPONENTS:
        by_component.setdefault(component, {"component": component, "source_identity": ""})

    expanded = {"include": [by_component[component] for component in COMPONENTS]}
    return {
        "matrix": expanded,
        "has_work": True,
        "reason": "integrity-tooling-self-check",
    }


def write_outputs(path: Path, plan: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write("matrix=" + json.dumps(plan["matrix"], separators=(",", ":")) + "\n")
        handle.write(f"has_work={'true' if plan['has_work'] else 'false'}\n")
        handle.write(f"reason={plan['reason']}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-json", required=True)
    parser.add_argument("--has-work", required=True, choices=("true", "false"))
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--github-output")
    args = parser.parse_args()
    try:
        matrix = json.loads(args.matrix_json)
        plan = expand_integrity_route(
            Path(args.repo_root).resolve(),
            matrix,
            args.has_work == "true",
            event_name=args.event_name,
            before_sha=args.before,
            after_sha=args.after,
        )
    except (IntegrityRouteError, json.JSONDecodeError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"SWRLZ integrity route planning failed: {exc}") from exc
    print(json.dumps(plan, indent=2, sort_keys=True))
    if args.github_output:
        write_outputs(Path(args.github_output), plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
