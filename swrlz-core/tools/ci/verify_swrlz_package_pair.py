#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
DUPLICATE_SUFFIX_RE = re.compile(r"\s*\(\d+\)$")
CHECKSUM_EXTENSIONS = (".sha256", ".sha", ".txt")

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def transport_stem(name: str, extension: str) -> str:
    if not name.lower().endswith(extension.lower()):
        return ""
    return DUPLICATE_SUFFIX_RE.sub("", name[:-len(extension)].rstrip()).rstrip()

def aliases(directory: Path, stem: str, extensions: tuple[str, ...]) -> list[Path]:
    found = []
    for extension in extensions:
        for path in directory.glob(f"*{extension}"):
            if transport_stem(path.name, extension).casefold() == stem.casefold():
                found.append(path)
    return sorted(found, key=lambda p: (DUPLICATE_SUFFIX_RE.search(p.stem) is not None, p.name.casefold()))

def resolve_zip(requested: Path) -> Path:
    if requested.is_file():
        return requested
    stem = transport_stem(requested.name, ".zip")
    candidates = aliases(requested.parent, stem, (".zip",))
    if not candidates:
        raise SystemExit(f"Missing ZIP: {requested}")
    hashes = {sha256(path) for path in candidates}
    if len(hashes) != 1:
        raise SystemExit("Package verification failed: ZIP aliases contain different bytes")
    return candidates[0]

def parse_checksum(checksum: Path) -> tuple[str, str | None]:
    parts = checksum.read_text(encoding="utf-8").strip().split()
    if len(parts) == 1:
        declared_hash, declared_name = parts[0], None
    elif len(parts) >= 2:
        declared_hash, declared_name = parts[0], " ".join(parts[1:]).lstrip("*")
    else:
        raise SystemExit("Malformed checksum file")
    if not SHA256_RE.fullmatch(declared_hash):
        raise SystemExit("Malformed checksum file: SHA-256 must be 64 hexadecimal characters")
    return declared_hash.lower(), declared_name

def resolve_checksum(zip_path: Path, explicit: Path | None) -> Path:
    if explicit:
        if explicit.is_file():
            return explicit
        raise SystemExit(f"Missing checksum: {explicit}")
    stem = transport_stem(zip_path.name, ".zip")
    candidates = aliases(zip_path.parent, stem, CHECKSUM_EXTENSIONS)
    if not candidates:
        raise SystemExit(f"Missing checksum for ZIP: {zip_path}")
    values = {parse_checksum(path)[0] for path in candidates}
    if len(values) != 1:
        raise SystemExit("Package verification failed: checksum aliases disagree")
    return candidates[0]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--checksum", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    zip_path = resolve_zip(args.zip_path)
    checksum = resolve_checksum(zip_path, args.checksum)
    manifest = args.manifest or zip_path.with_suffix(".manifest.json")
    declared_hash, declared_name = parse_checksum(checksum)
    actual_hash = sha256(zip_path)
    zip_stem = transport_stem(zip_path.name, ".zip")

    failures = []
    if declared_name is not None and transport_stem(declared_name, ".zip").casefold() != zip_stem.casefold():
        failures.append(f"checksum basename {declared_name!r} does not identify {zip_path.name!r}")
    if declared_hash != actual_hash:
        failures.append(f"checksum hash {declared_hash} != {actual_hash}")

    manifest_name = None
    candidates = [manifest] if manifest.is_file() else aliases(zip_path.parent, zip_stem, (".manifest.json",))
    if candidates:
        manifest = candidates[0]
        manifest_name = manifest.name
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"manifest could not be parsed: {exc}")
        else:
            if transport_stem(str(payload.get("zip") or ""), ".zip").casefold() != zip_stem.casefold():
                failures.append("manifest ZIP basename mismatch")
            if payload.get("sha256") != actual_hash:
                failures.append("manifest SHA-256 mismatch")
            if payload.get("size_bytes") != zip_path.stat().st_size:
                failures.append("manifest size mismatch")
            if payload.get("verified") is not True:
                failures.append("manifest verified flag is not true")

    if failures:
        raise SystemExit("Package verification failed: " + "; ".join(failures))

    print(json.dumps({
        "zip": zip_path.as_posix(),
        "logical_stem": zip_stem,
        "sha256": actual_hash,
        "size_bytes": zip_path.stat().st_size,
        "checksum": checksum.as_posix(),
        "manifest": manifest_name,
        "verified": True,
    }, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
