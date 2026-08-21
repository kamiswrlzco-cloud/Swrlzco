#!/usr/bin/env python3
"""Verify one SWRLZ source ZIP against metadata and safe archive topology."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

SHA_RE = re.compile(r"(?i)(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])")
REVISION_RE = re.compile(r"(?i)_CANDIDATE_R(\d+)$")
WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:/")
MAX_ARCHIVE_ENTRIES = 100_000
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 2 * 1024 * 1024 * 1024
MAX_SINGLE_ENTRY_BYTES = 512 * 1024 * 1024


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


def validate_archive_topology(zip_path: Path) -> dict:
    expected_root = stem(zip_path.name, ".zip")
    with zipfile.ZipFile(zip_path) as archive:
        infos = archive.infolist()
        if not infos:
            raise ValueError("Source archive is empty")
        if len(infos) > MAX_ARCHIVE_ENTRIES:
            raise ValueError("Source archive has too many entries")

        roots: set[str] = set()
        file_names: set[str] = set()
        total_uncompressed = 0

        for info in infos:
            raw = info.filename
            if "\x00" in raw:
                raise ValueError("Source archive contains NUL in path")
            normalized = raw.replace("\\", "/")
            if normalized.startswith("/") or WINDOWS_ABSOLUTE_RE.match(normalized):
                raise ValueError(f"Source archive contains absolute path: {raw}")
            cleaned = normalized[:-1] if normalized.endswith("/") else normalized
            if not cleaned:
                raise ValueError("Source archive contains empty path")
            path = PurePosixPath(cleaned)
            if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
                raise ValueError(f"Source archive contains unsafe path: {raw}")
            roots.add(path.parts[0])

            mode = (info.external_attr >> 16) & 0xFFFF
            file_type = stat.S_IFMT(mode)
            if file_type == stat.S_IFLNK:
                raise ValueError(f"Source archive contains symlink: {raw}")
            if file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
                raise ValueError(f"Source archive contains unsupported file type: {raw}")

            if info.file_size > MAX_SINGLE_ENTRY_BYTES:
                raise ValueError(f"Source archive entry exceeds safety limit: {raw}")
            total_uncompressed += info.file_size
            if total_uncompressed > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                raise ValueError("Source archive exceeds uncompressed safety limit")

            if not info.is_dir():
                file_names.add(cleaned)

        if roots != {expected_root}:
            raise ValueError(
                f"Source archive must have exactly canonical root {expected_root!r}; found {sorted(roots)}"
            )

        wrappers = {
            name[: -len("/gradlew")]
            for name in file_names
            if name.endswith("/gradlew")
        }
        project_roots = {
            root
            for root in wrappers
            if f"{root}/settings.gradle" in file_names or f"{root}/settings.gradle.kts" in file_names
        }
        if len(project_roots) != 1:
            raise ValueError(
                f"Source archive must contain exactly one Android Gradle project root; found {sorted(project_roots)}"
            )

    return {
        "archive_root": expected_root,
        "android_project_root": next(iter(project_roots)),
        "archive_entry_count": len(infos),
        "archive_uncompressed_bytes": total_uncompressed,
        "archive_topology_verified": True,
    }


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
    topology = validate_archive_topology(zip_path)
    return {
        "source": str(zip_path),
        "source_sha256": actual_sha,
        "size_bytes": actual_size,
        "verified": True,
        **topology,
    }


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
