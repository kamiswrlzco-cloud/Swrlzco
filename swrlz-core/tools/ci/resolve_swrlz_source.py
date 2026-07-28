#!/usr/bin/env python3
"""Resolve direct or verified chunk-transport CLIENT/SERVER Android source archives."""
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

SHA256_RE = re.compile(r"(?i)^[0-9a-f]{64}$")
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
class SourceCandidate:
    kind: str
    identity_path: Path
    transport: TransportName
    sha256: str
    size_bytes: int
    transport_manifest: Path | None = None


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


def ensure_lane_member(path: Path, lane: Path) -> None:
    try:
        path.resolve().relative_to(lane.resolve())
    except ValueError as exc:
        raise ResolutionError(f"Source transport must remain inside {lane}: {path}") from exc


def ensure_lane_root(path: Path, lane: Path) -> None:
    ensure_lane_member(path, lane)
    if path.parent.resolve() != lane.resolve():
        raise ResolutionError(f"Source identity file must be at the active lane root: {path}")


def parse_chunk_manifest(path: Path, component: str, lane: Path) -> SourceCandidate:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ResolutionError(f"Invalid transport manifest {path}: {exc}") from exc
    if payload.get("schema") != 1 or payload.get("transport") != "chunked-git-blobs-v1":
        raise ResolutionError(f"Unsupported source transport manifest: {path.name}")
    if str(payload.get("component") or "").upper() != component:
        raise ResolutionError(f"Transport manifest component mismatch in {path.name}")
    zip_name = str(payload.get("zip") or "")
    transport = parse_transport_name(zip_name, ".zip")
    declared_sha = str(payload.get("sha256") or "").lower()
    if not SHA256_RE.fullmatch(declared_sha):
        raise ResolutionError(f"Transport manifest has invalid whole ZIP SHA-256: {path.name}")
    size = payload.get("size_bytes")
    if not isinstance(size, int) or size < 1:
        raise ResolutionError(f"Transport manifest has invalid size_bytes: {path.name}")
    if payload.get("verified") is not True:
        raise ResolutionError(f"Transport manifest is not verified: {path.name}")
    chunks = payload.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        raise ResolutionError(f"Transport manifest contains no chunks: {path.name}")
    return SourceCandidate("chunked", path, transport, declared_sha, size, path)


def discover_candidates(lane: Path, component: str) -> list[SourceCandidate]:
    if not lane.is_dir():
        raise ResolutionError(f"Source lane does not exist: {lane}")
    candidates: list[SourceCandidate] = []
    for path in sorted(lane.glob("*.zip")):
        transport = parse_transport_name(path.name, ".zip")
        candidates.append(SourceCandidate("direct", path, transport, sha256_file(path), path.stat().st_size))
    for path in sorted(lane.glob("*.transport.json")):
        candidates.append(parse_chunk_manifest(path, component, lane))
    return candidates


def parse_checksum_value(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"(?i)(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])", text)
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


def manifest_aliases(lane: Path, logical_stem: str) -> list[Path]:
    return sorted(
        path for path in lane.glob("*.manifest.json")
        if parse_transport_name(path.name, ".manifest.json").logical_stem.casefold() == logical_stem.casefold()
    )


def choose_checksum_optional(aliases, actual_sha256: str):
    if not aliases:
        return None, []
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


def validate_manifest_optional(path: Path | None, candidate: SourceCandidate) -> None:
    if path is None:
        return
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ResolutionError(f"Package manifest could not be parsed: {path}: {exc}") from exc
    zip_name = str(payload.get("zip") or "")
    if parse_transport_name(zip_name, ".zip").logical_stem.casefold() != candidate.transport.logical_stem.casefold():
        raise ResolutionError(f"Package manifest ZIP basename mismatch: {path}")
    if str(payload.get("sha256") or "").lower() != candidate.sha256:
        raise ResolutionError(f"Package manifest SHA-256 mismatch: {path}")
    if "size_bytes" in payload and payload.get("size_bytes") != candidate.size_bytes:
        raise ResolutionError(f"Package manifest size mismatch: {path}")
    if payload.get("verified") is not True:
        raise ResolutionError(f"Package manifest verified flag is not true: {path}")


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
    cmd = ["git", "show", "--pretty=", "--name-only", after] if (not before or set(before) == {"0"}) else ["git", "diff", "--name-only", before, after]
    try:
        out = subprocess.check_output(cmd, cwd=repo_root, text=True)
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def current_push_candidate(repo_root: Path, lane: Path, candidates: Sequence[SourceCandidate]):
    changed = git_changed_paths(repo_root)
    if not changed:
        return None
    prefix = lane.relative_to(repo_root).as_posix().rstrip("/") + "/"
    lane_changed = [p for p in changed if p.startswith(prefix)]
    identities = {
        (repo_root / rel).resolve()
        for rel in lane_changed
        if rel.lower().endswith(".zip") or rel.lower().endswith(".transport.json")
    }
    matched = [c for c in candidates if c.identity_path.resolve() in identities]
    if len(matched) == 1:
        return matched[0]
    if len(matched) > 1:
        raise ResolutionError("Multiple source identities changed in one lane; dispatch explicitly")
    return None


def last_commit_timestamp(repo_root: Path, path: Path) -> int:
    try:
        rel = path.relative_to(repo_root).as_posix()
        value = subprocess.check_output(["git", "log", "-1", "--format=%ct", "--", rel], cwd=repo_root, text=True).strip()
        return int(value) if value else 0
    except Exception:
        return 0


def choose_latest(repo_root: Path, candidates: Sequence[SourceCandidate]) -> SourceCandidate:
    if not candidates:
        raise ResolutionError("No direct ZIP or chunked source transport exists in the active lane")
    return sorted(
        candidates,
        key=lambda c: (last_commit_timestamp(repo_root, c.identity_path), c.transport.version or (), c.identity_path.name.casefold()),
        reverse=True,
    )[0]


def reconstruct_chunked(repo_root: Path, lane: Path, candidate: SourceCandidate, work_dir: Path) -> tuple[Path, str | None, str | None]:
    assert candidate.transport_manifest is not None
    payload = json.loads(candidate.transport_manifest.read_text(encoding="utf-8"))
    chunks = payload["chunks"]
    work_dir.mkdir(parents=True, exist_ok=True)
    output = work_dir / candidate.transport.canonical_zip_name
    digest = hashlib.sha256()
    total = 0
    expected_indexes = list(range(1, len(chunks) + 1))
    actual_indexes = [int(chunk.get("index", -1)) for chunk in chunks]
    if actual_indexes != expected_indexes:
        raise ResolutionError(f"Transport chunks are not sequential in {candidate.transport_manifest.name}")
    with output.open("wb") as target:
        for chunk in chunks:
            rel = Path(str(chunk.get("path") or ""))
            chunk_path = (repo_root / rel).resolve()
            ensure_lane_member(chunk_path, lane)
            if not chunk_path.is_file():
                raise ResolutionError(f"Missing transport chunk: {rel}")
            expected_size = int(chunk.get("size_bytes", -1))
            expected_sha = str(chunk.get("sha256") or "").lower()
            if not SHA256_RE.fullmatch(expected_sha):
                raise ResolutionError(f"Invalid chunk SHA-256 in {candidate.transport_manifest.name}")
            if chunk_path.stat().st_size != expected_size:
                raise ResolutionError(f"Chunk size mismatch: {rel}")
            chunk_sha = sha256_file(chunk_path)
            if chunk_sha != expected_sha:
                raise ResolutionError(f"Chunk SHA-256 mismatch: {rel}")
            with chunk_path.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    target.write(block)
                    digest.update(block)
                    total += len(block)
    actual_sha = digest.hexdigest()
    if total != candidate.size_bytes:
        raise ResolutionError(f"Reassembled ZIP size mismatch: expected {candidate.size_bytes}, got {total}")
    if actual_sha != candidate.sha256:
        raise ResolutionError(f"Reassembled ZIP SHA-256 mismatch: expected {candidate.sha256}, got {actual_sha}")

    checksum_path = str(payload.get("checksum_evidence") or "").strip()
    manifest_path = str(payload.get("manifest_evidence") or "").strip()
    checksum = (repo_root / checksum_path).resolve() if checksum_path else None
    manifest = (repo_root / manifest_path).resolve() if manifest_path else None
    for evidence in (checksum, manifest):
        if evidence is not None:
            ensure_lane_member(evidence, lane)
            if not evidence.is_file():
                raise ResolutionError(f"Transport evidence path is missing: {evidence}")
    return output, str(checksum) if checksum else None, str(manifest) if manifest else None


def resolve_source(repo_root: Path, component: str, explicit_source: str | None = None, work_dir: Path | None = None) -> dict[str, object]:
    component = component.upper()
    if component not in COMPONENTS:
        raise ResolutionError(f"Unsupported component {component!r}; choose CLIENT or SERVER")
    lane = (repo_root / COMPONENTS[component].lane).resolve()
    candidates = discover_candidates(lane, component)

    reason = "repository-latest"
    if explicit_source:
        selected_path = (repo_root / explicit_source).resolve()
        ensure_lane_root(selected_path, lane)
        matched = [c for c in candidates if c.identity_path.resolve() == selected_path]
        if len(matched) != 1:
            raise ResolutionError(f"Explicit source identity does not exist or is ambiguous: {explicit_source}")
        selected = matched[0]
        reason = "explicit-source"
    else:
        selected = current_push_candidate(repo_root, lane, candidates)
        if selected is not None:
            reason = "current-push"
        else:
            selected = choose_latest(repo_root, candidates)

    checksum_file: Path | None = None
    manifest_file: Path | None = None
    if selected.kind == "chunked":
        if work_dir is None:
            work_dir = repo_root / ".swrlz-work" / component.lower()
        materialized, checksum_text, manifest_text = reconstruct_chunked(repo_root, lane, selected, work_dir)
        selected_source = materialized
        if checksum_text:
            checksum_file = Path(checksum_text)
        if manifest_text:
            manifest_file = Path(manifest_text)
    else:
        selected_source = selected.identity_path
        checksum_file, _ = choose_checksum_optional(checksum_aliases(lane, selected.transport.logical_stem), selected.sha256)
        manifests = manifest_aliases(lane, selected.transport.logical_stem)
        if len(manifests) > 1:
            raise ResolutionError("Package manifest aliases are ambiguous")
        manifest_file = manifests[0] if manifests else None
        validate_manifest_optional(manifest_file, selected)

    if checksum_file is not None:
        declared = parse_checksum_value(checksum_file)
        if declared != selected.sha256:
            raise ResolutionError(f"Source checksum mismatch: expected {declared}, calculated {selected.sha256}")

    result = {
        "schema": 3,
        "component": component,
        "lane": str(lane.relative_to(repo_root.resolve())),
        "source_kind": selected.kind,
        "selected_source": str(selected_source),
        "uploaded_filename": selected.identity_path.name,
        "logical_stem": selected.transport.logical_stem,
        "canonical_stem": selected.transport.artifact_stem,
        "canonical_filename": selected.transport.canonical_zip_name,
        "duplicate_suffix": selected.transport.duplicate_suffix,
        "version": ".".join(map(str, selected.transport.version)) if selected.transport.version else None,
        "source_sha256": selected.sha256,
        "checksum_file": str(checksum_file) if checksum_file else "",
        "manifest_file": str(manifest_file) if manifest_file else "",
        "transport_manifest": str(selected.transport_manifest.relative_to(repo_root.resolve())) if selected.transport_manifest else "",
        "selection_reason": reason,
        "evidence_policy": "ZIP required; checksum/manifest optional but validated when supplied",
    }
    return result


def write_outputs(path: Path, result: dict[str, object]) -> None:
    keys = (
        "component", "lane", "source_kind", "selected_source", "uploaded_filename", "logical_stem",
        "canonical_stem", "canonical_filename", "duplicate_suffix", "version", "source_sha256",
        "checksum_file", "manifest_file", "transport_manifest", "selection_reason",
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
    parser.add_argument("--work-dir", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args(argv)
    try:
        result = resolve_source(
            Path(args.repo_root).resolve(),
            args.component,
            args.source_zip or None,
            Path(args.work_dir).resolve() if args.work_dir else None,
        )
    except ResolutionError as exc:
        print(f"SWRLZ source resolution failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.github_output:
        write_outputs(Path(args.github_output), result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
