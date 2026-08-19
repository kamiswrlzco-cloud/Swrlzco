#!/usr/bin/env python3
"""Expand a known SWRLZ source identity into exact sparse-checkout paths."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

LANES = {
    "CLIENT": Path("swrlz-core/sources/client"),
    "SERVER": Path("swrlz-core/sources/server"),
}
BASE_PATHS = [Path("swrlz-core/tools/ci"), Path("swrlz-core/requests")]
RELEASES_PATH = Path("swrlz-core/releases")


class SparseCheckoutError(RuntimeError):
    pass


def _git(repo_root: Path, *args: str, input_text: str | None = None) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=repo_root, text=True, input=input_text
    ).strip()


def _path_exists(repo_root: Path, ref: str, path: Path) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path.as_posix()}"],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def _safe_repo_path(raw: str) -> Path:
    value = raw.replace("\\", "/").strip()
    if not value or value.startswith("/"):
        raise SparseCheckoutError(f"Unsafe repository path: {raw!r}")
    path = Path(value)
    if any(part in {"", ".", "..", ".git"} for part in path.parts):
        raise SparseCheckoutError(f"Unsafe repository path: {raw!r}")
    return path


def _safe_lane_path(component: str, raw: str) -> Path:
    path = _safe_repo_path(raw)
    lane = LANES[component]
    try:
        path.relative_to(lane)
    except ValueError as exc:
        raise SparseCheckoutError(f"Source path leaves {component} lane: {raw!r}") from exc
    return path


def _normalize_identity(component: str, source_identity: str) -> Path:
    value = source_identity.replace("\\", "/").strip()
    if not value:
        raise SparseCheckoutError("Source identity is empty")
    if "/" not in value:
        value = (LANES[component] / value).as_posix()
    return _safe_lane_path(component, value)


def _show_json(repo_root: Path, ref: str, path: Path) -> dict:
    try:
        text = _git(repo_root, "show", f"{ref}:{path.as_posix()}")
        payload = json.loads(text)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise SparseCheckoutError(f"Unable to read transport manifest: {path}") from exc
    if not isinstance(payload, dict):
        raise SparseCheckoutError(f"Transport manifest is not an object: {path}")
    return payload


def _existing(repo_root: Path, ref: str, paths: list[Path]) -> list[Path]:
    return [path for path in paths if _path_exists(repo_root, ref, path)]


def build_sparse_paths(
    repo_root: Path,
    component: str,
    source_identity: str,
    *,
    ref: str = "HEAD",
    include_releases: bool = False,
    extra_paths: list[str] | None = None,
) -> tuple[list[Path], Path]:
    component = component.upper()
    if component not in LANES:
        raise SparseCheckoutError("component must be CLIENT or SERVER")

    requested = _normalize_identity(component, source_identity)
    lane = LANES[component]
    actual = requested

    if requested.name.lower().endswith(".zip") and not _path_exists(repo_root, ref, requested):
        transport = requested.with_name(requested.name[:-4] + ".transport.json")
        if not _path_exists(repo_root, ref, transport):
            raise SparseCheckoutError(f"Source identity does not exist at {ref}: {requested}")
        actual = transport
    elif not _path_exists(repo_root, ref, requested):
        raise SparseCheckoutError(f"Source identity does not exist at {ref}: {requested}")

    paths: set[Path] = set(BASE_PATHS)
    if include_releases:
        paths.add(RELEASES_PATH)
    for raw in extra_paths or []:
        extra = _safe_repo_path(raw)
        if not _path_exists(repo_root, ref, extra):
            raise SparseCheckoutError(f"Extra sparse path is missing at {ref}: {extra}")
        try:
            object_type = _git(repo_root, "cat-file", "-t", f"{ref}:{extra.as_posix()}")
        except subprocess.CalledProcessError as exc:
            raise SparseCheckoutError(f"Unable to inspect extra sparse path: {extra}") from exc
        if object_type != "blob":
            raise SparseCheckoutError(f"Extra sparse path must be an exact file: {extra}")
        paths.add(extra)
    paths.add(actual)

    lower = actual.name.lower()
    if lower.endswith(".transport.json"):
        payload = _show_json(repo_root, ref, actual)
        if str(payload.get("component") or "").upper() != component:
            raise SparseCheckoutError("Transport component does not match requested component")
        if payload.get("verified") is not True:
            raise SparseCheckoutError("Transport verified flag is false")
        schema = int(payload.get("schema", -1))
        transport_kind = str(payload.get("transport") or "")
        if (schema, transport_kind) not in {
            (1, "chunked-git-blobs-v1"),
            (2, "chunked-git-blobs-v2"),
        }:
            raise SparseCheckoutError(
                f"Unsupported transport contract: schema={schema}, transport={transport_kind!r}"
            )

        declared_paths: list[str] = []
        if schema == 2:
            bundle_path = str(payload.get("metadata_bundle_path") or "").strip()
            if not bundle_path:
                bundle_name = str(payload.get("metadata_bundle") or "").strip()
                if bundle_name:
                    bundle_path = (lane / bundle_name).as_posix()
            if bundle_path:
                declared_paths.append(bundle_path)
        else:
            for key in ("checksum_evidence", "manifest_evidence"):
                value = str(payload.get(key) or "").strip()
                if value:
                    declared_paths.append(value)

        chunks = payload.get("chunks")
        if not isinstance(chunks, list) or not chunks:
            raise SparseCheckoutError("Transport has no chunks")
        for chunk in chunks:
            if not isinstance(chunk, dict):
                raise SparseCheckoutError("Transport chunk declaration is invalid")
            value = str(chunk.get("path") or "").strip()
            if not value:
                raise SparseCheckoutError("Transport chunk path is empty")
            declared_paths.append(value)

        for raw in declared_paths:
            path = _safe_lane_path(component, raw)
            if not _path_exists(repo_root, ref, path):
                raise SparseCheckoutError(f"Declared transport path is missing at {ref}: {path}")
            paths.add(path)
    elif lower.endswith(".zip"):
        stem = actual.name[:-4]
        evidence_candidates = [
            lane / f"{stem}_METADATA.zip",
            lane / f"{stem}.sha256",
            lane / f"{stem}.sha",
            lane / f"{stem}.sha256.txt",
            lane / f"{stem}.manifest.json",
        ]
        paths.update(_existing(repo_root, ref, evidence_candidates))
    else:
        raise SparseCheckoutError(f"Unsupported source identity: {actual}")

    return sorted(paths, key=lambda path: path.as_posix()), actual


def _pattern(path: Path) -> str:
    value = path.as_posix()
    if path in BASE_PATHS or path == RELEASES_PATH:
        return f"/{value}/"
    return f"/{value}"


def apply_sparse_checkout(repo_root: Path, paths: list[Path]) -> None:
    patterns = "\n".join(_pattern(path) for path in paths) + "\n"
    subprocess.run(
        ["git", "sparse-checkout", "set", "--no-cone", "--stdin"],
        cwd=repo_root,
        text=True,
        input=patterns,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--component", required=True, choices=sorted(LANES))
    parser.add_argument("--source-identity", required=True)
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--include-releases", action="store_true")
    parser.add_argument("--extra-path", action="append", default=[])
    parser.add_argument("--plan-only", action="store_true")
    args = parser.parse_args()

    repo_root = Path(".").resolve()
    try:
        paths, actual = build_sparse_paths(
            repo_root,
            args.component,
            args.source_identity,
            ref=args.ref,
            include_releases=args.include_releases,
            extra_paths=args.extra_path,
        )
        if not args.plan_only:
            apply_sparse_checkout(repo_root, paths)
    except (SparseCheckoutError, OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"SWRLZ targeted sparse checkout failed: {exc}") from exc

    print(
        json.dumps(
            {
                "component": args.component,
                "requested_identity": args.source_identity,
                "actual_identity": actual.as_posix(),
                "path_count": len(paths),
                "paths": [path.as_posix() for path in paths],
                "mode": "targeted" if not args.plan_only else "plan-only",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
