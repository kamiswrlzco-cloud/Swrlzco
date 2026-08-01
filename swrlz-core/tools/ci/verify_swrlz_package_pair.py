#!/usr/bin/env python3
"""Verify one SWRLZ source ZIP against metadata ZIP or legacy sidecars."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

SHA_RE = re.compile(r"(?i)(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
REVISION_RE = re.compile(r"(?i)_CANDIDATE_R(\d+)$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stem(name: str, suffix: str) -> str:
    if not name.lower().endswith(suffix.lower()):
        raise ValueError(f"Expected {suffix}: {name}")
    return name[: -len(suffix)].rstrip()


def manifest_source(payload: dict) -> tuple[str, str, int]:
    source = payload.get("sourceZip") if isinstance(payload.get("sourceZip"), dict) else {}
    name = str(source.get("filename") or payload.get("zip") or "")
    digest = str(source.get("sha256") or payload.get("sha256") or "").lower()
    size = source.get("sizeBytes", source.get("size_bytes", payload.get("sizeBytes", payload.get("size_bytes", -1))))
    return name, digest, int(size)


def validate(zip_path: Path, checksum_text: str, payload: dict) -> dict:
    actual_sha = sha256(zip_path)
    actual_size = zip_path.stat().st_size
    match = SHA_RE.search(checksum_text)
    if not match or match.group(1).lower() != actual_sha:
        raise ValueError("Source checksum mismatch")
    target = checksum_text[match.end():].strip().lstrip("*").strip()
    if target and stem(target, ".zip").casefold() != stem(zip_path.name, ".zip").casefold():
        raise ValueError("Checksum target filename mismatch")
    name, manifest_sha, manifest_size = manifest_source(payload)
    if stem(name, ".zip").casefold() != stem(zip_path.name, ".zip").casefold():
        raise ValueError("Manifest source filename mismatch")
    if manifest_sha != actual_sha or manifest_size != actual_size:
        raise ValueError("Manifest source identity mismatch")
    if int(payload.get("versionCode", payload.get("version_code", -1))) <= 0:
        raise ValueError("Manifest versionCode missing or invalid")
    component = str(payload.get("component") or "").upper()
    expected_component = "CLIENT" if zip_path.name.upper().startswith("CLIENT_") else "SERVER" if zip_path.name.upper().startswith("SERVER_") else ""
    if expected_component and component and component != expected_component:
        raise ValueError("Manifest component mismatch")
    revision_match = REVISION_RE.search(stem(zip_path.name, ".zip"))
    if revision_match and str(payload.get("revision") or "").upper() != f"R{revision_match.group(1)}":
        raise ValueError("Manifest revision mismatch")
    if "verified" in payload and payload.get("verified") is not True:
        raise ValueError("Manifest verified flag is false")
    return {"source": str(zip_path), "source_sha256": actual_sha, "size_bytes": actual_size, "verified": True}


def verify(zip_path: Path, metadata: Path | None, checksum: Path | None, manifest: Path | None) -> dict:
    if not zip_path.is_file():
        raise ValueError("Source ZIP is missing")
    if metadata:
        expected_stem = stem(zip_path.name, ".zip")
        checksum_name = f"{expected_stem}.sha256"
        manifest_name = f"{expected_stem}.manifest.json"
        if metadata.stat().st_size > 4 * 1024 * 1024:
            raise ValueError("Metadata ZIP exceeds 4 MiB")
        with zipfile.ZipFile(metadata) as archive:
            files = [item for item in archive.infolist() if not item.is_dir()]
            if len(files) != 2:
                raise ValueError("Metadata ZIP must contain exactly checksum and manifest")
            names = {}
            for item in files:
                normalized = item.filename.replace("\\", "/")
                if "/" in normalized or item.file_size > 1024 * 1024:
                    raise ValueError("Metadata ZIP contains nested or oversized entry")
                names[normalized.casefold()] = item
            if checksum_name.casefold() not in names or manifest_name.casefold() not in names:
                raise ValueError("Metadata ZIP entry names do not match source")
            checksum_text = archive.read(names[checksum_name.casefold()]).decode("utf-8")
            payload = json.loads(archive.read(names[manifest_name.casefold()]).decode("utf-8"))
        result = validate(zip_path, checksum_text, payload)
        result.update({"format": "metadata-bundle-v1", "metadata_bundle": str(metadata), "metadata_bundle_sha256": sha256(metadata)})
        return result
    if not checksum or not manifest:
        raise ValueError("Metadata ZIP or complete legacy sidecars are required")
    result = validate(zip_path, checksum.read_text(encoding="utf-8"), json.loads(manifest.read_text(encoding="utf-8")))
    result.update({"format": "legacy-sidecars", "checksum": str(checksum), "manifest": str(manifest)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--checksum", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.zip_path, args.metadata, args.checksum, args.manifest)
    except (ValueError, OSError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f"SWRLZ package verification failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
