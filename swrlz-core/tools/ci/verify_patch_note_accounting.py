#!/usr/bin/env python3
"""Audit SWRLZ package-internal and repository patch-note accounting.

This audit is intentionally independent from source integrity and Android build
routing. It never rewrites source packages or documentation.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


GRANDFATHERED_DEBT: dict[str, set[str]] = {
    "5b47857ef039609966669b039042bc69eba64dca48774107db353faeb7419912": {
        "ReleaseNotes.md",
        "SWRLZ_PATCH_LINEAGE_INDEX_V1.json",
    },
    "12f0ed06b8d754a45e952b4042f9418ce8aa46f3be972f5b83f286416e325693": {
        "ReleaseNotes.md",
        "SWRLZ_PATCH_LINEAGE_INDEX_V1.json",
    },
}

REPOSITORY_DOCS = {
    "CLIENT": Path("swrlz-core/docs/patch-notes/CLIENT_PATCH_NOTES.md"),
    "SERVER": Path("swrlz-core/docs/patch-notes/SERVER_PATCH_NOTES.md"),
}
CURRENT_LINEAGE = Path("swrlz-core/docs/reference/CURRENT_CANDIDATE_LINEAGE.md")
CURRENT_AUTHORITY = Path("swrlz-core/docs/CURRENT_AUTHORITY.md")


@dataclass
class AuditResult:
    component: str
    identity: str
    candidate: str
    source_sha256: str
    status: str = "PASS"
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def fail(self, message: str) -> None:
        self.errors.append(message)
        self.status = "FAIL"

    def debt(self, message: str) -> None:
        self.warnings.append(message)
        if self.status != "FAIL":
            self.status = "DEBT_RECORDED"

    def as_dict(self) -> dict:
        return {
            "component": self.component,
            "identity": self.identity,
            "candidate": self.candidate,
            "source_sha256": self.source_sha256,
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _short_candidate(manifest: dict) -> str:
    version = str(manifest.get("version") or "")
    revision = str(manifest.get("revision") or "")
    return f"{version} {revision}".strip()


def _candidate_stem(manifest: dict) -> str:
    source = manifest.get("sourceZip") if isinstance(manifest.get("sourceZip"), dict) else {}
    filename = str(source.get("filename") or manifest.get("zip") or "")
    return filename[:-4] if filename.lower().endswith(".zip") else filename


def _manifest_tokens(manifest: dict) -> tuple[str, str, str, str, int]:
    candidate = _candidate_stem(manifest)
    checkpoint = str(manifest.get("checkpoint") or "")
    version = str(manifest.get("version") or "")
    revision = str(manifest.get("revision") or "")
    version_code = int(manifest.get("versionCode", -1))
    return candidate, checkpoint, version, revision, version_code


def _find_internal_entry(archive: zipfile.ZipFile, basename: str) -> str | None:
    matches = []
    for name in archive.namelist():
        if name.endswith("/"):
            continue
        normalized = name.replace("\\", "/")
        if Path(normalized).name == basename:
            matches.append(normalized)
    if not matches:
        return None
    matches.sort(key=lambda value: (len(Path(value).parts), value.casefold()))
    shallowest = len(Path(matches[0]).parts)
    peers = [item for item in matches if len(Path(item).parts) == shallowest]
    if len(peers) != 1:
        raise ValueError(f"ambiguous internal {basename}: {peers}")
    return peers[0]


def _text_identifies_candidate(text: str, manifest: dict) -> bool:
    candidate, checkpoint, version, revision, version_code = _manifest_tokens(manifest)
    if checkpoint and checkpoint not in text:
        return False
    if candidate and candidate in text:
        return True
    short = f"{version} {revision}".strip()
    vc_tokens = (f"VC{version_code}", f"versionCode: `{version_code}`", f"versionCode {version_code}")
    return bool(short and short in text and any(token in text for token in vc_tokens))


def _check_internal_text(
    result: AuditResult,
    archive: zipfile.ZipFile,
    basename: str,
    manifest: dict,
) -> None:
    entry = _find_internal_entry(archive, basename)
    if entry is None:
        message = f"package is missing {basename}"
        if basename in GRANDFATHERED_DEBT.get(result.source_sha256, set()):
            result.debt(message + " (grandfathered exact SHA)")
        else:
            result.fail(message)
        return
    text = archive.read(entry).decode("utf-8", errors="replace")
    if not _text_identifies_candidate(text, manifest):
        message = f"{basename} does not identify the exact current candidate/checkpoint/VC"
        if basename in GRANDFATHERED_DEBT.get(result.source_sha256, set()):
            result.debt(message + " (grandfathered exact SHA)")
        else:
            result.fail(message)


def _check_internal_lineage(
    result: AuditResult,
    archive: zipfile.ZipFile,
    manifest: dict,
) -> None:
    basename = "SWRLZ_PATCH_LINEAGE_INDEX_V1.json"
    entry = _find_internal_entry(archive, basename)
    debt_allowed = basename in GRANDFATHERED_DEBT.get(result.source_sha256, set())
    if entry is None:
        message = f"package is missing {basename}"
        result.debt(message + " (grandfathered exact SHA)") if debt_allowed else result.fail(message)
        return
    try:
        payload = json.loads(archive.read(entry).decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        message = f"{basename} is not valid JSON: {exc}"
        result.debt(message + " (grandfathered exact SHA)") if debt_allowed else result.fail(message)
        return

    candidate, _, version, _, version_code = _manifest_tokens(manifest)
    mismatches = []
    if str(payload.get("component") or "").upper() != result.component:
        mismatches.append("component")
    if str(payload.get("candidate") or "") != candidate:
        mismatches.append("candidate")
    if str(payload.get("version") or "") != version:
        mismatches.append("version")
    try:
        if int(payload.get("versionCode", -1)) != version_code:
            mismatches.append("versionCode")
    except Exception:  # noqa: BLE001
        mismatches.append("versionCode")
    manifest_version_name = str(manifest.get("versionName") or "")
    if manifest_version_name and str(payload.get("versionName") or "") != manifest_version_name:
        mismatches.append("versionName")

    parent_manifest = manifest.get("parent") if isinstance(manifest.get("parent"), dict) else {}
    parent_payload = payload.get("parent") if isinstance(payload.get("parent"), dict) else {}
    parent_sha = str(parent_manifest.get("sha256") or "")
    if parent_sha and str(parent_payload.get("sha256") or "") != parent_sha:
        mismatches.append("parent.sha256")

    if mismatches:
        message = f"{basename} is stale or mismatched: {', '.join(mismatches)}"
        result.debt(message + " (grandfathered exact SHA)") if debt_allowed else result.fail(message)


def _require_doc_tokens(
    result: AuditResult,
    path: Path,
    manifest: dict,
    require_checkpoint: bool,
) -> None:
    if not path.is_file():
        result.fail(f"repository documentation is missing: {path}")
        return
    text = _read_text(path)
    sha = result.source_sha256
    short = _short_candidate(manifest)
    checkpoint = str(manifest.get("checkpoint") or "")
    missing = []
    if sha not in text:
        missing.append("source SHA-256")
    if short and short not in text:
        missing.append(f"candidate {short}")
    if require_checkpoint and checkpoint and checkpoint not in text:
        missing.append(f"checkpoint {checkpoint}")
    if missing:
        result.fail(f"{path} missing {', '.join(missing)}")


def audit_resolved_candidate(repo_root: Path, component: str, identity: str, work_dir: Path) -> AuditResult:
    from resolve_swrlz_source import resolve_source

    resolved = resolve_source(repo_root, component, identity, work_dir)
    manifest_path = Path(resolved["manifest_file"])
    manifest = json.loads(_read_text(manifest_path))
    candidate = _candidate_stem(manifest)
    result = AuditResult(
        component=component,
        identity=identity,
        candidate=candidate,
        source_sha256=str(resolved["source_sha256"]),
    )

    source = Path(resolved["selected_source"])
    try:
        with zipfile.ZipFile(source) as archive:
            _check_internal_text(result, archive, "CHANGELOG.md", manifest)
            _check_internal_text(result, archive, "ReleaseNotes.md", manifest)
            _check_internal_lineage(result, archive, manifest)
    except (zipfile.BadZipFile, OSError, ValueError) as exc:
        result.fail(f"cannot audit package-internal patch notes: {exc}")

    _require_doc_tokens(result, repo_root / REPOSITORY_DOCS[component], manifest, require_checkpoint=True)
    _require_doc_tokens(result, repo_root / CURRENT_LINEAGE, manifest, require_checkpoint=False)
    _require_doc_tokens(result, repo_root / CURRENT_AUTHORITY, manifest, require_checkpoint=False)
    return result


def _parse_identity_file(path: Path) -> list[tuple[str, str]]:
    identities: list[tuple[str, str]] = []
    if not path.is_file():
        return identities
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        component, identity = raw.split("\t", 1)
        identities.append((component.upper(), identity.strip()))
    return identities


def audit_repository(
    repo_root: Path,
    identities: Iterable[tuple[str, str]] = (),
) -> list[AuditResult]:
    selected = list(identities)
    if not selected:
        selected = [("CLIENT", ""), ("SERVER", "")]

    results: list[AuditResult] = []
    with tempfile.TemporaryDirectory(prefix="swrlz-patch-accounting-") as temp:
        base_work = Path(temp)
        for ordinal, (component, identity) in enumerate(selected, 1):
            try:
                results.append(
                    audit_resolved_candidate(
                        repo_root,
                        component,
                        identity,
                        base_work / component.lower() / str(ordinal),
                    )
                )
            except (OSError, ValueError, json.JSONDecodeError, RuntimeError, ImportError) as exc:
                results.append(
                    AuditResult(
                        component=component,
                        identity=identity,
                        candidate="",
                        source_sha256="",
                        status="FAIL",
                        errors=[f"candidate resolution/audit failed: {exc}"],
                    )
                )
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--identity-file", default="")
    parser.add_argument("--json-output", default="")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    identities = _parse_identity_file(Path(args.identity_file)) if args.identity_file else []
    results = audit_repository(repo_root, identities)
    payload = {
        "schema": "swrlz-patch-accounting-audit-v1",
        "status": "FAIL" if any(item.status == "FAIL" for item in results) else (
            "DEBT_RECORDED" if any(item.status == "DEBT_RECORDED" for item in results) else "PASS"
        ),
        "results": [item.as_dict() for item in results],
    }

    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 1 if payload["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
