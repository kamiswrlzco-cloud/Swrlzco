#!/usr/bin/env python3
"""Map changed CLIENT/SERVER source-lane paths to lane-root source identities.

This is deliberately transport-aware. Files below .transport/<bundle>/... are evidence
or chunks for the lane-root <bundle>.transport.json identity; they are never treated
as sibling ZIPs. Metadata ZIPs and loose sidecars resolve to their exact direct or
chunked source identity and never become independent build inputs.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

LANES = {
    "CLIENT": Path("swrlz-core/sources/client"),
    "SERVER": Path("swrlz-core/sources/server"),
}
SIDECAR_SUFFIXES = (".manifest.json", ".sha256", ".sha", ".txt")
METADATA_SUFFIX = "_metadata.zip"


class IdentityMappingError(RuntimeError):
    pass


def _strip_sidecar(name: str) -> str | None:
    lower = name.lower()
    for suffix in SIDECAR_SUFFIXES:
        if lower.endswith(suffix):
            return name[: -len(suffix)]
    return None


def _lane_for(path: Path) -> tuple[str, Path, Path] | None:
    for component, lane in LANES.items():
        try:
            relative = path.relative_to(lane)
            return component, lane, relative
        except ValueError:
            continue
    return None


def _resolve_exact_identity(
    repo_root: Path,
    lane: Path,
    stem: str,
    changed: str,
    evidence_class: str,
) -> Path:
    candidates = [
        lane / f"{stem}.zip",
        lane / f"{stem}.transport.json",
    ]
    existing = [path for path in candidates if (repo_root / path).is_file()]
    if len(existing) > 1:
        raise IdentityMappingError(
            f"{evidence_class} is ambiguous between direct and chunked source identities: {changed}"
        )
    if len(existing) == 1:
        return existing[0]
    raise IdentityMappingError(f"{evidence_class} has no source identity: {changed}")


def map_changed_path(repo_root: Path, changed: str) -> tuple[str, str] | None:
    rel_path = Path(changed)
    lane_info = _lane_for(rel_path)
    if lane_info is None:
        return None
    component, lane, relative = lane_info
    parts = relative.parts
    if not parts:
        return None

    # A transport chunk/evidence file belongs to the root transport manifest.
    if parts[0] == ".transport":
        if len(parts) < 3:
            return None
        bundle = parts[1]
        identity = lane / f"{bundle}.transport.json"
        if not (repo_root / identity).is_file():
            raise IdentityMappingError(
                f"Changed transport member has no lane-root transport identity: {changed} -> {identity}"
            )
        return component, identity.as_posix()

    # Source identities and evidence sidecars must live at the lane root.
    if len(parts) != 1:
        return None
    name = parts[0]
    lower = name.lower()

    # Metadata bundles are evidence for exactly one source identity. This branch
    # must run before generic ZIP handling so metadata is never built separately.
    if lower.endswith(METADATA_SUFFIX):
        stem = name[: -len(METADATA_SUFFIX)]
        identity = _resolve_exact_identity(
            repo_root,
            lane,
            stem,
            changed,
            "Metadata ZIP",
        )
        return component, identity.as_posix()

    if lower.endswith(".transport.json") or lower.endswith(".zip"):
        return component, (lane / name).as_posix()

    stem = _strip_sidecar(name)
    if stem is None:
        return None

    identity = _resolve_exact_identity(
        repo_root,
        lane,
        stem,
        changed,
        "Root source sidecar",
    )
    return component, identity.as_posix()


def map_changed_paths(repo_root: Path, changed_paths: Iterable[str]) -> list[tuple[str, str]]:
    mapped = set()
    for raw in changed_paths:
        changed = raw.strip()
        if not changed:
            continue
        item = map_changed_path(repo_root, changed)
        if item is not None:
            mapped.add(item)
    return sorted(mapped, key=lambda item: (item[0], item[1].casefold()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--changed-list", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    changed_paths = Path(args.changed_list).read_text(encoding="utf-8").splitlines()
    try:
        mapped = map_changed_paths(repo_root, changed_paths)
    except IdentityMappingError as exc:
        raise SystemExit(f"SWRLZ source identity mapping failed: {exc}") from exc

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        "".join(f"{component}\t{identity}\n" for component, identity in mapped),
        encoding="utf-8",
    )
    for component, identity in mapped:
        print(f"{component}\t{identity}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
