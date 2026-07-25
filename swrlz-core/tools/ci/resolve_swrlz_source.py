#!/usr/bin/env python3
"""Resolve the exact CLIENT or SERVER Android source archive selected by a SWRLZ build event."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

SHA256_RE = re.compile(r"(?i)(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
DUPLICATE_SUFFIX_RE = re.compile(r"\s*\((\d+)\)$")
CHECKSUM_EXTENSIONS = (".sha256", ".sha", ".txt")
KNOWN_VERSION_RE = re.compile(r"(?i)CFv(?P<version>\d+\.\d+\.\d+)")

class ResolutionError(RuntimeError):
    pass

@dataclass(frozen=True)
class ComponentSpec:
    component: str
    lane: str

@dataclass(frozen=True)
class TransportName:
    original_name: str
    logical_stem: str
    artifact_stem: str
    duplicate_suffix: int | None
    version: tuple[int, ...] | None

    @property
    def canonical_zip_name(self) -> str:
        return f"{self.logical_stem}.zip"

@dataclass(frozen=True)
class FileCandidate:
    path: Path
    transport: TransportName
    sha256: str

COMPONENTS: dict[str, ComponentSpec] = {
    "CLIENT": ComponentSpec("CLIENT", "swrlz-core/sources/client"),
    "SERVER": ComponentSpec("SERVER", "swrlz-core/sources/server"),
}

def parse_version(stem: str) -> tuple[int, ...] | None:
    match = KNOWN_VERSION_RE.search(stem)
    return tuple(int(x) for x in match.group("version").split(".")) if match else None

def artifact_safe_stem(stem: str) -> str:
    value = re.sub(r"\s+", "_", stem.strip())
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("._-")
    return value or "android-source"

def parse_transport_name(name: str, extension: str) -> TransportName:
    if not name.lower().endswith(extension.lower()):
        raise ResolutionError(f"Unsupported extension for {name!r}; expected {extension}")
    stem = name[:-len(extension)].rstrip()
    duplicate_suffix = None
    match = DUPLICATE_SUFFIX_RE.search(stem)
    if match:
        duplicate_suffix = int(match.group(1))
        stem = stem[:match.start()].rstrip()
    if not stem:
        raise ResolutionError(f"Source filename has no usable stem: {name!r}")
    return TransportName(
        original_name=name,
        logical_stem=stem,
        artifact_stem=artifact_safe_stem(stem),
        duplicate_suffix=duplicate_suffix,
        version=parse_version(stem),
    )

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def ensure_lane_root(path: Path, lane: Path) -> None:
    try:
        path.resolve().relative_to(lane.resolve())
    except ValueError as exc:
        raise ResolutionError(f"Source must remain inside {lane}: {path}") from exc
    if path.parent.resolve() != lane.resolve():
        raise ResolutionError(f"Source must be at the active lane root: {path}")

def discover_zip_candidates(lane: Path) -> list[FileCandidate]:
    if not lane.is_dir():
        raise ResolutionError(f"Source lane does not exist: {lane}")
    return [
        FileCandidate(path, parse_transport_name(path.name, ".zip"), sha256_file(path))
        for path in sorted(lane.glob("*.zip"))
    ]

def parse_checksum_value(path: Path) -> str:
    match = SHA256_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    if not match:
        raise ResolutionError(f"No SHA-256 value found in checksum file: {path}")
    return match.group(1).lower()

def checksum_aliases(lane: Path, logical_stem: str):
    found = []
    for ext in CHECKSUM_EXTENSIONS:
        for path in sorted(lane.glob(f"*{ext}")):
            parsed = parse_transport_name(path.name, ext)
            if parsed.logical_stem.casefold() == logical_stem.casefold():
                found.append((path, parse_checksum_value(path), parsed))
    return found

def validate_alias_group(candidates: Sequence[FileCandidate], preferred: Path | None = None) -> FileCandidate:
    if not candidates:
        raise ResolutionError("No source aliases were supplied")
    hashes = {c.sha256 for c in candidates}
    if len(hashes) != 1:
        raise ResolutionError(
            "Transport aliases map to the same logical source name but contain different bytes: "
            + ", ".join(f"{c.path.name}={c.sha256}" for c in candidates)
        )
    if preferred:
        for c in candidates:
            if c.path.resolve() == preferred.resolve():
                return c
    return sorted(candidates, key=lambda c: (
        c.transport.duplicate_suffix is not None,
        c.transport.duplicate_suffix or -1,
        c.path.name.casefold(),
    ))[0]

def choose_checksum(aliases, actual_sha256: str):
    if not aliases:
        raise ResolutionError("No matching checksum file exists for the selected source ZIP")
    values = {value for _, value, _ in aliases}
    if len(values) != 1:
        raise ResolutionError("Checksum aliases disagree")
    expected = next(iter(values))
    if expected != actual_sha256:
        raise ResolutionError(f"Source checksum mismatch: expected {expected}, calculated {actual_sha256}")
    preferred = sorted(aliases, key=lambda item: (
        item[2].duplicate_suffix is not None,
        item[2].duplicate_suffix or -1,
        item[0].name.casefold(),
    ))[0][0]
    return preferred, [p.name for p, _, _ in aliases]

def git_changed_paths(repo_root: Path) -> list[str]:
    if os.environ.get("GITHUB_EVENT_NAME") != "push":
        return []
    before = os.environ.get("GITHUB_EVENT_BEFORE", "")
    after = os.environ.get("GITHUB_SHA", "")
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    if event_path and Path(event_path).is_file():
        try:
            payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
            before = str(payload.get("before") or before)
            after = str(payload.get("after") or after)
        except Exception:
            pass
    if not after:
        return []
    cmd = ["git", "show", "--pretty=", "--name-only", after] if (not before or set(before) == {"0"}) \
        else ["git", "diff", "--name-only", before, after]
    try:
        out = subprocess.check_output(cmd, cwd=repo_root, text=True)
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]

def current_push_candidate(repo_root: Path, lane: Path, candidates: Sequence[FileCandidate]):
    changed = git_changed_paths(repo_root)
    if not changed:
        return None
    prefix = lane.relative_to(repo_root).as_posix().rstrip("/") + "/"
    lane_changed = [p for p in changed if p.startswith(prefix)]
    zip_paths = [p for p in lane_changed if p.lower().endswith(".zip")]
    by_path = {c.path.resolve(): c for c in candidates}
    selected = [by_path[(repo_root / p).resolve()] for p in zip_paths if (repo_root / p).resolve() in by_path]
    if len(selected) == 1:
        return selected[0]
    if len(selected) > 1:
        raise ResolutionError("Multiple source ZIPs changed in one lane; dispatch explicitly")

    stems = set()
    for rel in lane_changed:
        lower = rel.lower()
        ext = next((e for e in CHECKSUM_EXTENSIONS if lower.endswith(e)), None)
        if ext:
            stems.add(parse_transport_name(Path(rel).name, ext).logical_stem.casefold())
        elif lower.endswith(".manifest.json"):
            stems.add(parse_transport_name(Path(rel).name, ".manifest.json").logical_stem.casefold())
    matched = [c for c in candidates if c.transport.logical_stem.casefold() in stems]
    return validate_alias_group(matched) if matched else None

def last_commit_timestamp(repo_root: Path, path: Path) -> int:
    try:
        rel = path.relative_to(repo_root).as_posix()
        value = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", rel],
            cwd=repo_root, text=True,
        ).strip()
        return int(value) if value else 0
    except Exception:
        return 0

def choose_latest(repo_root: Path, candidates: Sequence[FileCandidate]) -> FileCandidate:
    if not candidates:
        raise ResolutionError("No source ZIP exists in the active lane")
    return sorted(
        candidates,
        key=lambda c: (last_commit_timestamp(repo_root, c.path), c.path.stat().st_mtime_ns, c.path.name.casefold()),
        reverse=True,
    )[0]

def resolve_source(repo_root: Path, component: str, explicit_source: str | None = None) -> dict[str, object]:
    component = component.upper()
    if component not in COMPONENTS:
        raise ResolutionError(f"Unsupported component {component!r}; choose CLIENT or SERVER")
    lane = (repo_root / COMPONENTS[component].lane).resolve()
    candidates = discover_zip_candidates(lane)

    reason = "repository-latest"
    if explicit_source:
        selected_path = (repo_root / explicit_source).resolve()
        ensure_lane_root(selected_path, lane)
        if not selected_path.is_file():
            raise ResolutionError(f"Explicit source ZIP does not exist: {explicit_source}")
        parsed = parse_transport_name(selected_path.name, ".zip")
        group = [c for c in candidates if c.transport.logical_stem.casefold() == parsed.logical_stem.casefold()]
        if not any(c.path.resolve() == selected_path for c in group):
            group.append(FileCandidate(selected_path, parsed, sha256_file(selected_path)))
        selected = validate_alias_group(group, selected_path)
        reason = "explicit-source"
    else:
        selected = current_push_candidate(repo_root, lane, candidates)
        if selected is not None:
            reason = "current-push"
        else:
            selected = choose_latest(repo_root, candidates)
        group = [c for c in candidates if c.transport.logical_stem.casefold() == selected.transport.logical_stem.casefold()]
        selected = validate_alias_group(group, selected.path)

    checksum_file, checksum_names = choose_checksum(
        checksum_aliases(lane, selected.transport.logical_stem),
        selected.sha256,
    )
    result = {
        "schema": 2,
        "component": component,
        "lane": str(lane.relative_to(repo_root.resolve())),
        "selected_source": str(selected.path.relative_to(repo_root.resolve())),
        "uploaded_filename": selected.path.name,
        "logical_stem": selected.transport.logical_stem,
        "canonical_stem": selected.transport.artifact_stem,
        "canonical_filename": selected.transport.canonical_zip_name,
        "duplicate_suffix": selected.transport.duplicate_suffix,
        "version": ".".join(map(str, selected.transport.version)) if selected.transport.version else None,
        "source_sha256": selected.sha256,
        "checksum_file": str(checksum_file.relative_to(repo_root.resolve())),
        "source_aliases": sorted(c.path.name for c in group),
        "checksum_aliases": sorted(checksum_names),
        "selection_reason": reason,
        "filename_policy": "lane-and-content-authoritative",
    }
    return result

def write_outputs(path: Path, result: dict[str, object]) -> None:
    keys = (
        "component", "lane", "selected_source", "uploaded_filename", "logical_stem",
        "canonical_stem", "canonical_filename", "duplicate_suffix", "version",
        "source_sha256", "checksum_file", "selection_reason",
    )
    with path.open("a", encoding="utf-8") as handle:
        for key in keys:
            value = result.get(key)
            handle.write(f"{key}={'' if value is None else value}\n")
        handle.write("resolution_json<<SWRLZ_RESOLUTION_JSON\n")
        handle.write(json.dumps(result, sort_keys=True))
        handle.write("\nSWRLZ_RESOLUTION_JSON\n")

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--component", required=True, choices=sorted(COMPONENTS))
    parser.add_argument("--source-zip", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args(argv)
    try:
        result = resolve_source(Path(args.repo_root).resolve(), args.component, args.source_zip or None)
    except ResolutionError as exc:
        print(f"SWRLZ source resolution failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.github_output:
        write_outputs(Path(args.github_output), result)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
