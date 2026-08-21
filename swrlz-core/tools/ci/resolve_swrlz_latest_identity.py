#!/usr/bin/env python3
"""Resolve the highest-ranked verified SWRLZ source identity without hydrating its payload."""
from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

from resolve_swrlz_source import (
    canonical_zip,
    manifest_source,
    parse_checksum_text,
    revision_number,
    source_stem,
    validate_manifest,
    version_tuple,
)

LANES = {
    "CLIENT": PurePosixPath("swrlz-core/sources/client"),
    "SERVER": PurePosixPath("swrlz-core/sources/server"),
}
SHA_RE = re.compile(r"(?i)^[0-9a-f]{64}$")


class LatestIdentityError(RuntimeError):
    pass


def _run(repo_root: Path, *args: str, text: bool = True):
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() if text else result.stderr.decode("utf-8", "replace").strip()
        raise LatestIdentityError(f"git {' '.join(args)} failed: {detail or 'unknown git error'}")
    return result.stdout


def _show_bytes(repo_root: Path, ref: str, path: PurePosixPath) -> bytes:
    return _run(repo_root, "show", f"{ref}:{path.as_posix()}", text=False)


def _show_text(repo_root: Path, ref: str, path: PurePosixPath) -> str:
    return _show_bytes(repo_root, ref, path).decode("utf-8")


def _exists(repo_root: Path, ref: str, path: PurePosixPath) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path.as_posix()}"],
        cwd=repo_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0



def _root_entries(repo_root: Path, ref: str, lane: PurePosixPath) -> set[str]:
    raw = _run(repo_root, "ls-tree", "-z", f"{ref}:{lane.as_posix()}", text=False)
    names: set[str] = set()
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            _, name = record.split(b"\t", 1)
        except ValueError as exc:
            raise LatestIdentityError("Unable to parse lane tree entry") from exc
        names.add(name.decode("utf-8"))
    return names


def _safe_lane_path(lane: PurePosixPath, raw: str) -> PurePosixPath:
    value = raw.replace("\\", "/").strip()
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(part in {"", ".", "..", ".git"} for part in path.parts):
        raise LatestIdentityError(f"unsafe repository path: {raw!r}")
    if path.parts[: len(lane.parts)] != lane.parts:
        raise LatestIdentityError(f"path leaves source lane: {raw!r}")
    return path


def _metadata_bundle(
    repo_root: Path,
    ref: str,
    lane: PurePosixPath,
    bundle_path: PurePosixPath,
    source_name: str,
    component: str,
    declared_bundle_sha: str = "",
) -> tuple[int, str, str, int]:
    if not _exists(repo_root, ref, bundle_path):
        raise LatestIdentityError(f"metadata bundle is missing: {bundle_path}")
    data = _show_bytes(repo_root, ref, bundle_path)
    if len(data) > 4 * 1024 * 1024:
        raise LatestIdentityError("metadata bundle exceeds 4 MiB")
    if declared_bundle_sha:
        import hashlib
        actual = hashlib.sha256(data).hexdigest()
        if actual != declared_bundle_sha.lower():
            raise LatestIdentityError("metadata bundle SHA-256 mismatch")
    stem = source_stem(source_name)
    checksum_name = f"{stem}.sha256"
    manifest_name = f"{stem}.manifest.json"
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        files = [item for item in archive.infolist() if not item.is_dir()]
        if len(files) != 2:
            raise LatestIdentityError("metadata ZIP must contain exactly checksum and manifest")
        by_name = {item.filename.replace("\\", "/").casefold(): item for item in files}
        checksum_item = by_name.get(checksum_name.casefold())
        manifest_item = by_name.get(manifest_name.casefold())
        if checksum_item is None or manifest_item is None:
            raise LatestIdentityError("metadata bundle entry names do not match source")
        checksum_text = archive.read(checksum_item).decode("utf-8")
        manifest = json.loads(archive.read(manifest_item).decode("utf-8"))
    source_sha, target = parse_checksum_text(checksum_text)
    if target and canonical_zip(target).casefold() != canonical_zip(source_name).casefold():
        raise LatestIdentityError("checksum target filename mismatch")
    _, _, source_size = manifest_source(manifest)
    version_code, revision = validate_manifest(
        manifest, source_name, source_sha, source_size, component
    )
    return version_code, revision, source_sha, source_size


def _legacy_evidence(
    repo_root: Path,
    ref: str,
    lane: PurePosixPath,
    entries: set[str],
    source_name: str,
    component: str,
) -> tuple[int, str, str, int]:
    stem = source_stem(source_name)
    checksum_names = [f"{stem}.sha256", f"{stem}.sha", f"{stem}.sha256.txt"]
    present = [name for name in checksum_names if name in entries]
    manifest_name = f"{stem}.manifest.json"
    if len(present) != 1 or manifest_name not in entries:
        raise LatestIdentityError(f"legacy evidence is incomplete or ambiguous for {source_name}")
    checksum_text = _show_text(repo_root, ref, lane / present[0])
    source_sha, target = parse_checksum_text(checksum_text)
    if target and canonical_zip(target).casefold() != canonical_zip(source_name).casefold():
        raise LatestIdentityError("legacy checksum target mismatch")
    manifest = json.loads(_show_text(repo_root, ref, lane / manifest_name))
    _, _, source_size = manifest_source(manifest)
    version_code, revision = validate_manifest(
        manifest, source_name, source_sha, source_size, component
    )
    return version_code, revision, source_sha, source_size


def _transport_candidate(
    repo_root: Path,
    ref: str,
    lane: PurePosixPath,
    identity: PurePosixPath,
    entries: set[str],
    component: str,
) -> tuple[tuple, str]:
    payload = json.loads(_show_text(repo_root, ref, identity))
    schema = int(payload.get("schema", -1))
    transport = str(payload.get("transport") or "")
    if str(payload.get("component") or "").upper() != component:
        raise LatestIdentityError("transport component mismatch")
    if payload.get("verified") is not True:
        raise LatestIdentityError("transport verified flag is false")

    if schema == 2 and transport == "chunked-git-blobs-v2":
        source_name = canonical_zip(str(payload.get("source_zip") or ""))
        source_sha = str(payload.get("source_sha256") or "").lower()
        source_size = int(payload.get("source_size_bytes", -1))
        bundle_rel = str(payload.get("metadata_bundle_path") or "")
        if not bundle_rel:
            bundle_rel = (lane / str(payload.get("metadata_bundle") or "")).as_posix()
        bundle_path = _safe_lane_path(lane, bundle_rel)
        version_code, _, evidence_sha, evidence_size = _metadata_bundle(
            repo_root,
            ref,
            lane,
            bundle_path,
            source_name,
            component,
            str(payload.get("metadata_bundle_sha256") or ""),
        )
    elif schema == 1 and transport == "chunked-git-blobs-v1":
        source_name = canonical_zip(str(payload.get("zip") or ""))
        source_sha = str(payload.get("sha256") or "").lower()
        source_size = int(payload.get("size_bytes", -1))
        checksum_path = _safe_lane_path(lane, str(payload.get("checksum_evidence") or ""))
        manifest_path = _safe_lane_path(lane, str(payload.get("manifest_evidence") or ""))
        checksum_text = _show_text(repo_root, ref, checksum_path)
        evidence_sha, target = parse_checksum_text(checksum_text)
        if target and canonical_zip(target).casefold() != source_name.casefold():
            raise LatestIdentityError("schema-1 checksum target mismatch")
        manifest = json.loads(_show_text(repo_root, ref, manifest_path))
        _, _, evidence_size = manifest_source(manifest)
        version_code, _ = validate_manifest(
            manifest, source_name, evidence_sha, evidence_size, component
        )
    else:
        raise LatestIdentityError("unsupported transport schema")

    if not SHA_RE.fullmatch(source_sha) or source_size < 1:
        raise LatestIdentityError("transport source identity is invalid")
    if evidence_sha != source_sha or evidence_size != source_size:
        raise LatestIdentityError("transport and evidence source identity disagree")

    chunks = payload.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        raise LatestIdentityError("transport has no chunks")
    if [int(item.get("index", -1)) for item in chunks] != list(range(1, len(chunks) + 1)):
        raise LatestIdentityError("transport chunk indexes are not sequential")
    total = 0
    seen: set[PurePosixPath] = set()
    for item in chunks:
        chunk_path = _safe_lane_path(lane, str(item.get("path") or ""))
        if chunk_path in seen:
            raise LatestIdentityError("transport contains duplicate chunk paths")
        seen.add(chunk_path)
        size = int(item.get("size_bytes", -1))
        sha = str(item.get("sha256") or "").lower()
        if size < 1 or not SHA_RE.fullmatch(sha) or not _exists(repo_root, ref, chunk_path):
            raise LatestIdentityError(f"transport chunk declaration is invalid: {chunk_path}")
        total += size
    if total != source_size:
        raise LatestIdentityError("transport chunk sizes do not match source size")

    rank = (
        version_code,
        revision_number(source_name),
        version_tuple(source_name),
        identity.name.casefold(),
    )
    return rank, identity.as_posix()


def _direct_candidate(
    repo_root: Path,
    ref: str,
    lane: PurePosixPath,
    identity: PurePosixPath,
    entries: set[str],
    component: str,
) -> tuple[tuple, str]:
    source_name = canonical_zip(identity.name)
    stem = source_stem(source_name)
    bundle_name = f"{stem}_METADATA.zip"
    if bundle_name in entries:
        version_code, _, _, _ = _metadata_bundle(
            repo_root, ref, lane, lane / bundle_name, source_name, component
        )
    else:
        version_code, _, _, _ = _legacy_evidence(
            repo_root, ref, lane, entries, source_name, component
        )
    rank = (
        version_code,
        revision_number(source_name),
        version_tuple(source_name),
        identity.name.casefold(),
    )
    return rank, identity.as_posix()


def resolve_latest_identity(repo_root: Path, component: str, *, ref: str = "HEAD") -> str:
    component = component.upper()
    if component not in LANES:
        raise LatestIdentityError(f"unsupported component: {component!r}")
    lane = LANES[component]
    entries = _root_entries(repo_root, ref, lane)
    candidates: list[tuple[tuple, str]] = []

    for name in sorted(entries):
        upper = name.upper()
        identity = lane / name
        try:
            if upper.endswith(".TRANSPORT.JSON") and upper.startswith(component + "_"):
                candidates.append(
                    _transport_candidate(repo_root, ref, lane, identity, entries, component)
                )
            elif (
                upper.endswith(".ZIP")
                and upper.startswith(component + "_")
                and not upper.endswith("_METADATA.ZIP")
                and not upper.endswith("_EVIDENCE.ZIP")
            ):
                candidates.append(
                    _direct_candidate(repo_root, ref, lane, identity, entries, component)
                )
        except Exception as exc:
            print(
                f"SWRLZ latest-identity warning: quarantined {identity.as_posix()}: {exc}",
                file=sys.stderr,
            )

    if not candidates:
        raise LatestIdentityError(f"no verified {component} source identity found at {ref}")
    return max(candidates, key=lambda item: item[0])[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--component", required=True, choices=sorted(LANES))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--github-output")
    args = parser.parse_args()
    try:
        identity = resolve_latest_identity(
            Path(args.repo_root).resolve(), args.component, ref=args.ref
        )
    except (LatestIdentityError, OSError, subprocess.CalledProcessError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        raise SystemExit(f"SWRLZ latest identity resolution failed: {exc}") from exc
    print(identity)
    if args.github_output:
        with Path(args.github_output).open("a", encoding="utf-8") as handle:
            handle.write(f"source_identity={identity}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
