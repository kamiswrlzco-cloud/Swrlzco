#!/usr/bin/env python3
"""Resolve verified SWRLZ CLIENT/SERVER Android source packages.

Accepted package contracts:
- direct source ZIP + metadata ZIP;
- direct source ZIP + complete legacy checksum/manifest sidecars;
- chunked-git-blobs-v2 + metadata ZIP;
- chunked-git-blobs-v1 + complete legacy sidecars.

Discovery validates package identity and metadata without reconstructing every
historical source payload. Expensive source-byte hashing/reassembly is deferred
until a candidate is actually selected. Current-push and explicitly selected
sources remain fail-closed; verified-latest fallback may quarantine a broken
historical payload and try the next ranked verified identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

SHA_RE = re.compile(r"(?i)^[0-9a-f]{64}$")
SHA_FIND_RE = re.compile(r"(?i)(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
VERSION_RE = re.compile(r"(?i)CFv(?P<version>\d+\.\d+\.\d+)")
REVISION_RE = re.compile(r"(?i)_CANDIDATE_R(?P<revision>\d+)$")
COPY_SUFFIX_RE = re.compile(r"\s*\(\d+\)$")
COMPONENT_LANES = {
    "CLIENT": Path("swrlz-core/sources/client"),
    "SERVER": Path("swrlz-core/sources/server"),
}


class ResolutionError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_stem(name: str) -> str:
    if not name.lower().endswith(".zip"):
        raise ResolutionError(f"Source name must end in .zip: {name!r}")
    return COPY_SUFFIX_RE.sub("", name[:-4].rstrip()).rstrip()


def canonical_zip(name: str) -> str:
    return source_stem(name) + ".zip"


def version_tuple(name: str) -> tuple[int, int, int]:
    match = VERSION_RE.search(name)
    return tuple(map(int, match.group("version").split("."))) if match else (0, 0, 0)


def revision_number(name: str) -> int:
    match = REVISION_RE.search(source_stem(name))
    return int(match.group("revision")) if match else 0


def safe_repo_path(repo_root: Path, relative: str) -> Path:
    value = relative.replace("\\", "/").strip()
    if not value or value.startswith("/") or re.match(r"^[A-Za-z]:/", value):
        raise ResolutionError(f"Unsafe repository path: {relative!r}")
    parts = [part for part in value.split("/") if part not in ("", ".")]
    if not parts or any(part == ".." or part.casefold() == ".git" for part in parts):
        raise ResolutionError(f"Unsafe repository path: {relative!r}")
    path = (repo_root / Path(*parts)).resolve()
    try:
        path.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ResolutionError(f"Repository path escapes root: {relative!r}") from exc
    return path


def ensure_in_lane(path: Path, lane: Path) -> None:
    try:
        path.resolve().relative_to(lane.resolve())
    except ValueError as exc:
        raise ResolutionError(f"Transport path leaves source lane: {path}") from exc


def explicit_identity_path(repo_root: Path, component: str, explicit: str) -> Path:
    """Resolve a workflow identity as either lane-root filename or repo-relative path."""
    value = explicit.replace("\\", "/").strip()
    if not value:
        raise ResolutionError("Explicit source identity is empty")
    if "/" not in value:
        value = (COMPONENT_LANES[component] / value).as_posix()
    path = safe_repo_path(repo_root, value)
    ensure_in_lane(path, (repo_root / COMPONENT_LANES[component]).resolve())
    return path


def parse_checksum_text(text: str) -> tuple[str, str]:
    match = SHA_FIND_RE.search(text)
    if not match:
        raise ResolutionError("Checksum does not contain a SHA-256 value")
    target = text[match.end():].strip().lstrip("*").strip()
    return match.group(1).lower(), target


def manifest_source(payload: dict) -> tuple[str, str, int]:
    source = payload.get("sourceZip") if isinstance(payload.get("sourceZip"), dict) else {}
    name = str(source.get("filename") or payload.get("zip") or "")
    sha = str(source.get("sha256") or payload.get("sha256") or "").lower()
    size = source.get(
        "sizeBytes",
        source.get("size_bytes", payload.get("sizeBytes", payload.get("size_bytes", -1))),
    )
    try:
        return name, sha, int(size)
    except Exception as exc:
        raise ResolutionError("Manifest source size is invalid") from exc


@dataclass(frozen=True)
class Evidence:
    mode: str
    checksum_path: Path
    manifest_path: Path
    bundle_path: Path | None
    bundle_sha256: str
    source_sha256: str
    source_size: int
    version_code: int
    revision: str


@dataclass(frozen=True)
class Candidate:
    kind: str
    identity_path: Path
    component: str
    source_name: str
    source_sha256: str
    source_size: int
    version: tuple[int, int, int]
    revision: int
    evidence: Evidence
    transport: dict | None = None


def validate_manifest(
    payload: dict,
    source_name: str,
    source_sha: str,
    source_size: int,
    component: str,
) -> tuple[int, str]:
    manifest_name, manifest_sha, manifest_size = manifest_source(payload)
    if canonical_zip(manifest_name).casefold() != canonical_zip(source_name).casefold():
        raise ResolutionError("Manifest source filename mismatch")
    if not SHA_RE.fullmatch(manifest_sha) or manifest_sha != source_sha:
        raise ResolutionError("Manifest source SHA-256 mismatch")
    if manifest_size != source_size:
        raise ResolutionError("Manifest source size mismatch")
    if str(payload.get("component") or component).upper() != component:
        raise ResolutionError("Manifest component mismatch")
    if "verified" in payload and payload.get("verified") is not True:
        raise ResolutionError("Manifest verified flag is false")
    version_code = int(payload.get("versionCode", payload.get("version_code", -1)))
    if version_code <= 0:
        raise ResolutionError("Manifest versionCode is missing or invalid")
    revision = str(payload.get("revision") or "")
    expected_revision = revision_number(source_name)
    if expected_revision and revision.upper() != f"R{expected_revision}":
        raise ResolutionError("Manifest revision does not match source filename")
    return version_code, revision


def extract_metadata_bundle(
    bundle: Path,
    work_dir: Path,
    source_name: str,
    component: str,
    declared_sha: str = "",
) -> Evidence:
    if not bundle.is_file():
        raise ResolutionError(f"Metadata bundle is missing: {bundle}")
    if bundle.stat().st_size > 4 * 1024 * 1024:
        raise ResolutionError(f"Metadata bundle exceeds 4 MiB: {bundle}")
    bundle_sha = sha256_file(bundle)
    if declared_sha and bundle_sha != declared_sha.lower():
        raise ResolutionError("Metadata bundle SHA-256 mismatch")
    stem = source_stem(source_name)
    checksum_name = f"{stem}.sha256"
    manifest_name = f"{stem}.manifest.json"
    out_dir = work_dir / "metadata" / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(bundle) as archive:
        files = [item for item in archive.infolist() if not item.is_dir()]
        if len(files) != 2:
            raise ResolutionError("Metadata ZIP must contain exactly checksum and manifest")
        by_name = {}
        for item in files:
            normalized = item.filename.replace("\\", "/")
            if "/" in normalized or item.file_size > 1024 * 1024:
                raise ResolutionError(f"Unsafe metadata entry: {item.filename}")
            key = normalized.casefold()
            if key in by_name:
                raise ResolutionError("Duplicate metadata entry")
            by_name[key] = item
        checksum_item = by_name.get(checksum_name.casefold())
        manifest_item = by_name.get(manifest_name.casefold())
        if checksum_item is None or manifest_item is None:
            raise ResolutionError("Metadata entry names do not match source")
        checksum_path = out_dir / checksum_name
        manifest_path = out_dir / manifest_name
        checksum_path.write_bytes(archive.read(checksum_item))
        manifest_path.write_bytes(archive.read(manifest_item))
    source_sha, target = parse_checksum_text(checksum_path.read_text(encoding="utf-8"))
    if target and canonical_zip(target).casefold() != canonical_zip(source_name).casefold():
        raise ResolutionError("Checksum target filename mismatch")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    _, _, source_size = manifest_source(payload)
    version_code, revision = validate_manifest(
        payload, source_name, source_sha, source_size, component
    )
    return Evidence(
        "metadata-bundle-v1",
        checksum_path,
        manifest_path,
        bundle,
        bundle_sha,
        source_sha,
        source_size,
        version_code,
        revision,
    )


def exact_legacy_evidence(lane: Path, source_name: str, component: str) -> Evidence | None:
    stem = source_stem(source_name)
    checksum_candidates = [
        lane / f"{stem}.sha256",
        lane / f"{stem}.sha",
        lane / f"{stem}.sha256.txt",
    ]
    checksums = [path for path in checksum_candidates if path.is_file()]
    manifest_path = lane / f"{stem}.manifest.json"
    if not checksums and not manifest_path.exists():
        return None
    if len(checksums) != 1 or not manifest_path.is_file():
        raise ResolutionError(f"Legacy evidence is incomplete or ambiguous for {source_name}")
    checksum_path = checksums[0]
    source_sha, target = parse_checksum_text(checksum_path.read_text(encoding="utf-8"))
    if target and canonical_zip(target).casefold() != canonical_zip(source_name).casefold():
        raise ResolutionError("Legacy checksum target filename mismatch")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    _, _, source_size = manifest_source(payload)
    version_code, revision = validate_manifest(
        payload, source_name, source_sha, source_size, component
    )
    return Evidence(
        "legacy-loose-sidecars",
        checksum_path,
        manifest_path,
        None,
        "",
        source_sha,
        source_size,
        version_code,
        revision,
    )


def validate_chunk_declarations(
    repo_root: Path,
    lane: Path,
    payload: dict,
    source_size: int,
) -> list[tuple[dict, Path]]:
    chunks = payload.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        raise ResolutionError("Transport has no chunks")
    indexes = [int(chunk.get("index", -1)) for chunk in chunks]
    if indexes != list(range(1, len(chunks) + 1)):
        raise ResolutionError("Transport chunk indexes are not sequential")

    declared: list[tuple[dict, Path]] = []
    seen: set[Path] = set()
    total_size = 0
    for chunk in chunks:
        chunk_path = safe_repo_path(repo_root, str(chunk.get("path") or ""))
        ensure_in_lane(chunk_path, lane)
        if chunk_path in seen:
            raise ResolutionError("Transport contains duplicate chunk paths")
        seen.add(chunk_path)
        expected_size = int(chunk.get("size_bytes", -1))
        expected_sha = str(chunk.get("sha256") or "").lower()
        if expected_size < 1 or not SHA_RE.fullmatch(expected_sha):
            raise ResolutionError("Transport chunk declaration is invalid")
        total_size += expected_size
        declared.append((chunk, chunk_path))
    if total_size != source_size:
        raise ResolutionError("Transport chunk sizes do not match source size")
    return declared


def reconstruct_chunks(
    repo_root: Path,
    lane: Path,
    payload: dict,
    source_name: str,
    source_sha: str,
    source_size: int,
    work_dir: Path,
) -> Path:
    declared = validate_chunk_declarations(repo_root, lane, payload, source_size)
    output_dir = work_dir / "sources"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / canonical_zip(source_name)
    digest = hashlib.sha256()
    total = 0
    try:
        with output.open("wb") as target:
            for chunk, chunk_path in declared:
                if not chunk_path.is_file():
                    raise ResolutionError(f"Transport chunk is missing: {chunk_path}")
                expected_size = int(chunk["size_bytes"])
                expected_sha = str(chunk["sha256"]).lower()
                if chunk_path.stat().st_size != expected_size or sha256_file(chunk_path) != expected_sha:
                    raise ResolutionError(f"Transport chunk verification failed: {chunk_path}")
                with chunk_path.open("rb") as source:
                    for block in iter(lambda: source.read(1024 * 1024), b""):
                        target.write(block)
                        digest.update(block)
                        total += len(block)
        if total != source_size or digest.hexdigest() != source_sha:
            raise ResolutionError("Reassembled source size or SHA-256 mismatch")
    except Exception:
        output.unlink(missing_ok=True)
        raise
    return output


def parse_transport(
    path: Path,
    repo_root: Path,
    lane: Path,
    component: str,
    work_dir: Path,
    *,
    materialize: bool = True,
) -> Candidate:
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema = int(payload.get("schema", -1))
    transport = str(payload.get("transport") or "")
    if str(payload.get("component") or "").upper() != component:
        raise ResolutionError("Transport component mismatch")

    if schema == 2 and transport == "chunked-git-blobs-v2":
        source_name = str(payload.get("source_zip") or "")
        source_sha = str(payload.get("source_sha256") or "").lower()
        source_size = int(payload.get("source_size_bytes", -1))
        bundle_rel = str(payload.get("metadata_bundle_path") or "")
        bundle_sha = str(payload.get("metadata_bundle_sha256") or "").lower()
        if not bundle_rel:
            bundle_rel = (lane / str(payload.get("metadata_bundle") or "")).relative_to(repo_root).as_posix()
        bundle_path = safe_repo_path(repo_root, bundle_rel)
        ensure_in_lane(bundle_path, lane)
        evidence = extract_metadata_bundle(
            bundle_path, work_dir, source_name, component, bundle_sha
        )
        kind = "chunked-v2"
    elif schema == 1 and transport == "chunked-git-blobs-v1":
        source_name = str(payload.get("zip") or "")
        source_sha = str(payload.get("sha256") or "").lower()
        source_size = int(payload.get("size_bytes", -1))
        checksum_rel = str(payload.get("checksum_evidence") or "")
        manifest_rel = str(payload.get("manifest_evidence") or "")
        if not checksum_rel or not manifest_rel:
            raise ResolutionError("Schema-1 transport requires complete legacy evidence")
        checksum_path = safe_repo_path(repo_root, checksum_rel)
        manifest_path = safe_repo_path(repo_root, manifest_rel)
        ensure_in_lane(checksum_path, lane)
        ensure_in_lane(manifest_path, lane)
        source_checksum, target = parse_checksum_text(
            checksum_path.read_text(encoding="utf-8")
        )
        if target and canonical_zip(target).casefold() != canonical_zip(source_name).casefold():
            raise ResolutionError("Schema-1 checksum target mismatch")
        manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        version_code, revision = validate_manifest(
            manifest_payload, source_name, source_checksum, source_size, component
        )
        evidence = Evidence(
            "legacy-loose-sidecars",
            checksum_path,
            manifest_path,
            None,
            "",
            source_checksum,
            source_size,
            version_code,
            revision,
        )
        kind = "chunked-v1"
    else:
        raise ResolutionError(f"Unsupported source transport manifest: {path.name}")

    if not SHA_RE.fullmatch(source_sha) or source_size < 1:
        raise ResolutionError("Transport source identity is invalid")
    if payload.get("verified") is not True:
        raise ResolutionError("Transport verified flag is false")
    if evidence.source_sha256 != source_sha or evidence.source_size != source_size:
        raise ResolutionError("Transport and metadata source identity disagree")

    # Validate the complete chunk declaration graph during discovery, but do not
    # read/hash/reassemble every historical chunk payload. Source bytes are
    # materialized only after selection.
    validate_chunk_declarations(repo_root, lane, payload, source_size)
    if materialize:
        reconstruct_chunks(
            repo_root, lane, payload, source_name, source_sha, source_size, work_dir
        )

    return Candidate(
        kind,
        path,
        component,
        canonical_zip(source_name),
        source_sha,
        source_size,
        version_tuple(source_name),
        revision_number(source_name),
        evidence,
        payload,
    )


def changed_paths(repo_root: Path) -> set[Path]:
    if os.environ.get("GITHUB_EVENT_NAME") != "push":
        return set()
    before = os.environ.get("GITHUB_EVENT_BEFORE", "")
    after = os.environ.get("GITHUB_SHA", "")
    event_file = os.environ.get("GITHUB_EVENT_PATH", "")
    if event_file and Path(event_file).is_file():
        try:
            event = json.loads(Path(event_file).read_text(encoding="utf-8"))
            before = str(event.get("before") or before)
            after = str(event.get("after") or after)
        except Exception:
            pass
    if not after:
        return set()
    command = (
        ["git", "show", "--pretty=", "--name-only", after]
        if not before or set(before) == {"0"}
        else ["git", "diff", "--name-only", before, after]
    )
    try:
        text = subprocess.check_output(command, cwd=repo_root, text=True)
    except Exception:
        return set()
    return {
        (repo_root / line.strip()).resolve()
        for line in text.splitlines()
        if line.strip()
    }


def discover(
    repo_root: Path,
    component: str,
    work_dir: Path,
    strict_paths: Iterable[Path] = (),
) -> list[Candidate]:
    lane = (repo_root / COMPONENT_LANES[component]).resolve()
    if not lane.is_dir():
        raise ResolutionError(f"Source lane does not exist: {lane}")
    strict = {path.resolve() for path in strict_paths}
    candidates: list[Candidate] = []

    for source in sorted(lane.glob("*.zip")):
        upper = source.name.upper()
        if (
            upper.endswith("_METADATA.ZIP")
            or upper.endswith("_EVIDENCE.ZIP")
            or not upper.startswith(component + "_")
        ):
            continue
        try:
            bundle = lane / f"{source_stem(source.name)}_METADATA.zip"
            evidence = (
                extract_metadata_bundle(bundle, work_dir, source.name, component)
                if bundle.is_file()
                else exact_legacy_evidence(lane, source.name, component)
            )
            if evidence is None:
                continue
            source_size = source.stat().st_size
            if evidence.source_size != source_size:
                raise ResolutionError("Direct source evidence size mismatch")
            candidates.append(
                Candidate(
                    "direct-bundle" if evidence.bundle_path else "direct-legacy",
                    source,
                    component,
                    canonical_zip(source.name),
                    evidence.source_sha256,
                    source_size,
                    version_tuple(source.name),
                    revision_number(source.name),
                    evidence,
                )
            )
        except Exception as exc:
            if source.resolve() in strict:
                raise
            print(
                f"SWRLZ resolver warning: quarantined historical source {source.name}: {exc}",
                file=sys.stderr,
            )

    for transport_path in sorted(lane.glob("*.transport.json")):
        try:
            candidates.append(
                parse_transport(
                    transport_path,
                    repo_root,
                    lane,
                    component,
                    work_dir,
                    materialize=False,
                )
            )
        except Exception as exc:
            if transport_path.resolve() in strict:
                raise
            print(
                f"SWRLZ resolver warning: quarantined historical transport {transport_path.name}: {exc}",
                file=sys.stderr,
            )
    return candidates


def candidate_rank(candidate: Candidate) -> tuple:
    return (
        candidate.evidence.version_code,
        candidate.revision,
        candidate.version,
        candidate.identity_path.name.casefold(),
    )


def select_candidate(
    candidates: list[Candidate], repo_root: Path, explicit: str = ""
) -> tuple[Candidate, str]:
    if not candidates:
        raise ResolutionError("No verified source package was found")
    if explicit:
        component = candidates[0].component
        explicit_path = explicit_identity_path(repo_root, component, explicit)
        matches = [
            candidate
            for candidate in candidates
            if candidate.identity_path.resolve() == explicit_path
            or (candidate.identity_path.parent / candidate.source_name).resolve() == explicit_path
        ]
        if len(matches) != 1:
            raise ResolutionError("Explicit source identity is absent or ambiguous")
        return matches[0], "explicit-source"
    changed = changed_paths(repo_root)
    current = [
        candidate
        for candidate in candidates
        if candidate.identity_path.resolve() in changed
        or (
            candidate.evidence.bundle_path
            and candidate.evidence.bundle_path.resolve() in changed
        )
    ]
    if len(current) == 1:
        return current[0], "current-push"
    if len(current) > 1:
        raise ResolutionError("Multiple verified source identities changed in one component lane")
    ranked = sorted(candidates, key=candidate_rank, reverse=True)
    return ranked[0], "verified-latest"


def materialize_candidate(
    candidate: Candidate,
    repo_root: Path,
    work_dir: Path,
) -> Path:
    lane = (repo_root / COMPONENT_LANES[candidate.component]).resolve()
    if candidate.kind.startswith("chunked"):
        if candidate.transport is None:
            raise ResolutionError("Chunked candidate has no transport payload")
        return reconstruct_chunks(
            repo_root,
            lane,
            candidate.transport,
            candidate.source_name,
            candidate.source_sha256,
            candidate.source_size,
            work_dir,
        )

    source = candidate.identity_path
    if not source.is_file():
        raise ResolutionError(f"Direct source is missing: {source}")
    if source.stat().st_size != candidate.source_size:
        raise ResolutionError("Direct source size changed after discovery")
    if sha256_file(source) != candidate.source_sha256:
        raise ResolutionError("Direct source SHA-256 mismatch")
    return source


def resolve(
    repo_root: Path,
    component: str,
    explicit: str = "",
    work_dir: Path | None = None,
) -> dict:
    component = component.upper()
    if component not in COMPONENT_LANES:
        raise ResolutionError("component must be CLIENT or SERVER")
    work_dir = (work_dir or repo_root / ".swrlz-work" / component.lower()).resolve()
    strict = changed_paths(repo_root)
    if explicit:
        explicit_path = explicit_identity_path(repo_root, component, explicit)
        strict.add(explicit_path)
        if explicit_path.name.lower().endswith(".zip"):
            strict.add(
                explicit_path.with_name(
                    f"{source_stem(explicit_path.name)}.transport.json"
                )
            )

    candidates = discover(repo_root, component, work_dir, strict)
    selected, reason = select_candidate(candidates, repo_root, explicit)

    if reason == "verified-latest":
        materialization_error: Exception | None = None
        for candidate in sorted(candidates, key=candidate_rank, reverse=True):
            try:
                selected_source = materialize_candidate(candidate, repo_root, work_dir)
                selected = candidate
                break
            except Exception as exc:
                materialization_error = exc
                print(
                    f"SWRLZ resolver warning: quarantined historical payload "
                    f"{candidate.identity_path.name}: {exc}",
                    file=sys.stderr,
                )
        else:
            raise ResolutionError(
                f"No verified source payload could be materialized: {materialization_error}"
            )
    else:
        # Explicit and current-push identities remain strictly fail-closed.
        selected_source = materialize_candidate(selected, repo_root, work_dir)

    lane = COMPONENT_LANES[component]
    evidence = selected.evidence
    description = (
        f"{component} {selected.source_name} · CFv{'.'.join(map(str, selected.version))} "
        f"R{selected.revision} · VC{evidence.version_code} · {selected.kind} · {evidence.mode} · "
        f"SHA-256 {selected.source_sha256} · {selected.source_size} bytes"
    )
    result = {
        "schema": 5,
        "component": component,
        "source_kind": selected.kind,
        "metadata_mode": evidence.mode,
        "source_description": description,
        "build_description": f"Build {component} APK from {description} · selected by {reason}",
        "evidence_description": (
            str(evidence.bundle_path.relative_to(repo_root))
            if evidence.bundle_path
            else f"{evidence.checksum_path} + {evidence.manifest_path}"
        ),
        "selected_source": str(selected_source),
        "canonical_filename": selected.source_name,
        "canonical_stem": source_stem(selected.source_name),
        "logical_stem": source_stem(selected.source_name),
        "uploaded_filename": selected.identity_path.name,
        "duplicate_suffix": "",
        "lane": lane.as_posix(),
        "source_sha256": selected.source_sha256,
        "source_size_bytes": selected.source_size,
        "version": ".".join(map(str, selected.version)),
        "version_code": evidence.version_code,
        "revision": f"R{selected.revision}",
        "metadata_bundle": (
            str(evidence.bundle_path.relative_to(repo_root)) if evidence.bundle_path else ""
        ),
        "metadata_bundle_sha256": evidence.bundle_sha256,
        "checksum_file": str(evidence.checksum_path),
        "manifest_file": str(evidence.manifest_path),
        "transport_manifest": (
            str(selected.identity_path.relative_to(repo_root))
            if selected.kind.startswith("chunked")
            else ""
        ),
        "selection_reason": reason,
        "verified": True,
        "build_eligible": True,
    }
    return result


def resolve_source(
    repo_root: Path,
    component: str,
    explicit_source: str | None = None,
    work_dir: Path | None = None,
) -> dict:
    """Stable compatibility surface for workflow and external resolver callers."""
    return resolve(repo_root, component, explicit_source or "", work_dir)


def write_outputs(path: Path, result: dict) -> None:
    keys = (
        "component",
        "source_kind",
        "metadata_mode",
        "source_description",
        "build_description",
        "evidence_description",
        "selected_source",
        "canonical_filename",
        "canonical_stem",
        "logical_stem",
        "uploaded_filename",
        "duplicate_suffix",
        "lane",
        "source_sha256",
        "source_size_bytes",
        "version",
        "version_code",
        "revision",
        "metadata_bundle",
        "metadata_bundle_sha256",
        "checksum_file",
        "manifest_file",
        "transport_manifest",
        "selection_reason",
    )
    with path.open("a", encoding="utf-8") as handle:
        for key in keys:
            handle.write(f"{key}={result.get(key, '')}\n")
        handle.write("resolution_json<<SWRLZ_RESOLUTION_JSON\n")
        handle.write(json.dumps(result, sort_keys=True) + "\nSWRLZ_RESOLUTION_JSON\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--component", required=True, choices=sorted(COMPONENT_LANES))
    parser.add_argument("--source-zip", default="")
    parser.add_argument("--work-dir", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args(argv)
    try:
        repo_root = Path(args.repo_root).resolve()
        work_dir = Path(args.work_dir).resolve() if args.work_dir else None
        result = resolve(repo_root, args.component, args.source_zip, work_dir)
    except (
        ResolutionError,
        ValueError,
        OSError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"SWRLZ source resolution failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.github_output:
        write_outputs(Path(args.github_output), result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
