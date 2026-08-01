#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, stat, zipfile
from pathlib import Path

FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def apply_patch(base_zip: Path, patch_path: Path, output: Path) -> dict[str, object]:
    patch = json.loads(patch_path.read_text(encoding="utf-8"))
    if patch.get("schema") != 1 or patch.get("transport") != "derived-zip-patch-v1":
        raise ValueError("Unsupported derived source patch contract")
    if sha256(base_zip) != str(patch["base"]["sha256"]).lower():
        raise ValueError("Base source SHA-256 mismatch")

    patch_root = patch_path.parent
    root_from = str(patch["base"]["root"]).rstrip("/")
    root_to = str(patch["output"]["root"]).rstrip("/")
    deletes = set(patch.get("deletes", []))
    files: dict[str, bytes] = {}
    modes: dict[str, int] = {}

    with zipfile.ZipFile(base_zip) as source:
        for info in source.infolist():
            if info.is_dir():
                continue
            name = info.filename.replace("\\", "/")
            prefix = root_from + "/"
            if not name.startswith(prefix):
                raise ValueError(f"Base entry outside expected root: {name}")
            relative = name[len(prefix):]
            if relative in deletes:
                continue
            files[relative] = source.read(info)
            raw_mode = (info.external_attr >> 16) & 0xFFFF
            modes[relative] = stat.S_IMODE(raw_mode) or 0o644

    for entry in patch.get("replacementFiles", []):
        relative = str(entry["path"]).replace("\\", "/")
        if relative.startswith("/") or ".." in Path(relative).parts:
            raise ValueError(f"Unsafe replacement path: {relative}")
        source_path = (patch_root / str(entry["sourcePath"])).resolve()
        source_path.relative_to(patch_root.resolve())
        if not source_path.is_file():
            raise ValueError(f"Replacement file is missing: {source_path}")
        files[relative] = source_path.read_bytes()
        modes[relative] = int(entry.get("mode", 0o644))

    if patch.get("regenerateSourceManifest") is True:
        files.pop("SOURCE_MANIFEST.sha256", None)
        modes.pop("SOURCE_MANIFEST.sha256", None)
        lines = [f"{hashlib.sha256(files[path]).hexdigest()}  {path}" for path in sorted(files)]
        files["SOURCE_MANIFEST.sha256"] = ("\n".join(lines) + "\n").encode("utf-8")
        modes["SOURCE_MANIFEST.sha256"] = 0o644

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, allowZip64=True) as target:
        for relative in sorted(files):
            info = zipfile.ZipInfo(f"{root_to}/{relative}", FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = ((stat.S_IFREG | modes[relative]) << 16)
            info.flag_bits |= 0x800
            target.writestr(info, files[relative], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    actual_sha = sha256(output)
    actual_size = output.stat().st_size
    if actual_sha != str(patch["output"]["sha256"]).lower() or actual_size != int(patch["output"]["sizeBytes"]):
        raise ValueError(f"Derived source identity mismatch: {actual_sha} / {actual_size}")
    return {"source": str(output), "sha256": actual_sha, "sizeBytes": actual_size, "verified": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_zip", type=Path)
    parser.add_argument("patch", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    result = apply_patch(args.base_zip, args.patch, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            for key, value in result.items():
                handle.write(f"{key}={value}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
