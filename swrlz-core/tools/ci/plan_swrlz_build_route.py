#!/usr/bin/env python3
"""Plan the CLIENT/SERVER build matrix and preserve an exact source identity when known."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from resolve_push_changed_paths import ChangedRangeError, resolve_push_changed_paths

LANES = {
    "CLIENT": Path("swrlz-core/sources/client"),
    "SERVER": Path("swrlz-core/sources/server"),
}
MANUAL_COMPONENTS = {"CLIENT", "SERVER", "BOTH"}
SIDECAR_SUFFIXES = (".manifest.json", ".sha256", ".sha", ".txt")
METADATA_SUFFIX = "_metadata.zip"


class RoutePlanningError(RuntimeError):
    pass


def _git(repo_root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo_root, text=True).strip()


def _path_exists(repo_root: Path, ref: str, path: Path) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path.as_posix()}"],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def _changed_paths(repo_root: Path, before: str, after: str) -> list[str]:
    """Resolve the exact GitHub push range, fetching a missing boundary by SHA."""
    if not after:
        return []
    if not before:
        return [
            line.strip()
            for line in _git(repo_root, "show", "--format=", "--name-only", "--no-renames", after).splitlines()
            if line.strip()
        ]
    try:
        paths, _ = resolve_push_changed_paths(repo_root, before, after, remote="origin")
    except ChangedRangeError as exc:
        raise RoutePlanningError(f"Unable to prove declared push range: {exc}") from exc
    return paths


def _parse_request(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _identity_for_stem(
    repo_root: Path,
    ref: str,
    lane: Path,
    stem: str,
    changed: str,
) -> str:
    candidates = [lane / f"{stem}.zip", lane / f"{stem}.transport.json"]
    existing = [path for path in candidates if _path_exists(repo_root, ref, path)]
    if len(existing) != 1:
        state = "ambiguous" if len(existing) > 1 else "missing"
        raise RoutePlanningError(f"Source identity is {state} for changed evidence: {changed}")
    return existing[0].as_posix()


def _map_changed_source(repo_root: Path, ref: str, changed: str) -> tuple[str, str] | None:
    path = Path(changed)
    for component, lane in LANES.items():
        try:
            relative = path.relative_to(lane)
        except ValueError:
            continue
        parts = relative.parts
        if not parts:
            return None

        if parts[0] == ".transport":
            if len(parts) < 3:
                return None
            identity = lane / f"{parts[1]}.transport.json"
            if not _path_exists(repo_root, ref, identity):
                raise RoutePlanningError(
                    f"Changed transport member has no lane-root identity: {changed}"
                )
            return component, identity.as_posix()

        if len(parts) != 1:
            return None
        name = parts[0]
        lower = name.lower()
        if lower.endswith(METADATA_SUFFIX):
            stem = name[: -len(METADATA_SUFFIX)]
            return component, _identity_for_stem(repo_root, ref, lane, stem, changed)
        if lower.endswith(".transport.json"):
            return component, (lane / name).as_posix()
        if lower.endswith(".zip"):
            return component, (lane / name).as_posix()
        for suffix in SIDECAR_SUFFIXES:
            if lower.endswith(suffix):
                stem = name[: -len(suffix)]
                return component, _identity_for_stem(repo_root, ref, lane, stem, changed)
        return None
    return None


def _lane_component(changed: str) -> str | None:
    path = Path(changed)
    for component, lane in LANES.items():
        try:
            relative = path.relative_to(lane)
        except ValueError:
            continue
        if relative.parts:
            return component
    return None


def plan_route(
    repo_root: Path,
    *,
    event_name: str,
    before_sha: str = "",
    after_sha: str = "",
    manual_component: str = "",
    manual_source_identity: str = "",
    manual_variant: str = "debug",
    manual_commit_release: bool = False,
    request_file: Path = Path("swrlz-core/requests/000_CURRENT.request"),
) -> dict:
    variant = "debug"
    identities: dict[str, set[str]] = {"CLIENT": set(), "SERVER": set()}
    components: set[str] = set()

    if event_name == "workflow_dispatch":
        component = manual_component.upper()
        if component not in MANUAL_COMPONENTS:
            raise RoutePlanningError(f"Unsupported manual component: {component!r}")
        source_identity = manual_source_identity.strip()
        if component == "BOTH":
            if source_identity:
                raise RoutePlanningError("BOTH dispatch cannot use one explicit source identity")
            if manual_commit_release:
                raise RoutePlanningError("BOTH dispatch cannot commit release artifacts concurrently")
            components.update(("CLIENT", "SERVER"))
        else:
            components.add(component)
            if source_identity:
                identities[component].add(source_identity)
        variant = manual_variant.lower()
    else:
        changed = _changed_paths(repo_root, before_sha, after_sha)
        for path in changed:
            # Deleted or renamed-away historical files are archival maintenance,
            # not build requests. A rename's new path still exists and routes normally.
            if not _path_exists(repo_root, after_sha, Path(path)):
                continue
            lane_component = _lane_component(path)
            if lane_component is not None:
                components.add(lane_component)
            mapped = _map_changed_source(repo_root, after_sha, path)
            if mapped is not None:
                component, identity = mapped
                identities[component].add(identity)

        request_rel = request_file.as_posix()
        if request_rel in changed:
            request = _parse_request(repo_root / request_file)
            if request.get("enabled", "false").lower() == "true":
                target = request.get("target", "").upper()
                if target not in LANES:
                    raise RoutePlanningError(f"Enabled build request has invalid target: {target!r}")
                components.add(target)
                variant = request.get("build_variant", "debug").lower()
                if request.get("commit_release_artifacts", "false").lower() != "false":
                    raise RoutePlanningError(
                        "Automatic request builds may not commit release artifacts; use manual dispatch"
                    )

    if variant not in {"debug", "release"}:
        raise RoutePlanningError(f"Unsupported build variant: {variant!r}")

    include = []
    for component in ("CLIENT", "SERVER"):
        if component not in components:
            continue
        component_identities = identities[component]
        if len(component_identities) > 1:
            raise RoutePlanningError(
                f"Multiple source identities changed for {component}: {sorted(component_identities)}"
            )
        source_identity = next(iter(component_identities), "")
        include.append({"component": component, "source_identity": source_identity})

    has_work = bool(include)
    matrix = {"include": include or [{"component": "CLIENT", "source_identity": ""}]}
    return {"matrix": matrix, "has_work": has_work, "build_variant": variant}


def write_github_outputs(path: Path, plan: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write("matrix=" + json.dumps(plan["matrix"], separators=(",", ":")) + "\n")
        handle.write(f"has_work={'true' if plan['has_work'] else 'false'}\n")
        handle.write(f"build_variant={plan['build_variant']}\n")


def main() -> int:
    repo_root = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    try:
        plan = plan_route(
            repo_root,
            event_name=os.environ.get("EVENT_NAME", os.environ.get("GITHUB_EVENT_NAME", "")),
            before_sha=os.environ.get("BEFORE_SHA", ""),
            after_sha=os.environ.get("AFTER_SHA", os.environ.get("GITHUB_SHA", "")),
            manual_component=os.environ.get("MANUAL_COMPONENT", ""),
            manual_source_identity=os.environ.get("MANUAL_SOURCE_IDENTITY", ""),
            manual_variant=os.environ.get("MANUAL_VARIANT", "debug"),
            manual_commit_release=os.environ.get("MANUAL_COMMIT_RELEASE", "false").lower() == "true",
            request_file=Path(os.environ.get("REQUEST_FILE", "swrlz-core/requests/000_CURRENT.request")),
        )
    except (RoutePlanningError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"SWRLZ build route planning failed: {exc}") from exc

    print(json.dumps(plan, indent=2, sort_keys=True))
    output = os.environ.get("GITHUB_OUTPUT", "")
    if output:
        write_github_outputs(Path(output), plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
