#!/usr/bin/env python3
"""Resolve the complete changed-path range for a GitHub push.

GitHub's push event supplies an exact ``before`` and ``after`` commit. A shallow
checkout may contain ``after`` without containing ``before`` when one push adds
multiple commits. This helper keeps the checkout shallow, fetches only a missing
event-boundary commit, and fails closed if the declared range cannot be proven.
"""
from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


SHA_RE = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")


class ChangedRangeError(RuntimeError):
    """Raised when the declared push range cannot be resolved exactly."""


def _run_git(
    repo_root: Path,
    *args: str,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise ChangedRangeError(f"git {' '.join(args)} failed: {detail}")
    return result


def _is_zero_sha(value: str) -> bool:
    return bool(value) and set(value) == {"0"}


def _validate_sha(label: str, value: str, *, allow_zero: bool = False) -> str:
    normalized = value.strip()
    if allow_zero and _is_zero_sha(normalized) and len(normalized) in {40, 64}:
        return normalized
    if not SHA_RE.fullmatch(normalized):
        raise ChangedRangeError(f"{label} must be a full hexadecimal Git object ID")
    return normalized.lower()


def commit_is_available(repo_root: Path, sha: str) -> bool:
    return _run_git(repo_root, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode == 0


def ensure_commit_available(repo_root: Path, sha: str, remote: str) -> bool:
    """Ensure ``sha`` is available, returning True only when a fetch was needed."""
    if commit_is_available(repo_root, sha):
        return False

    fetch_ref = f"refs/remotes/{remote}/swrlz-range-{sha[:12]}"
    result = _run_git(
        repo_root,
        "-c",
        "protocol.version=2",
        "fetch",
        "--no-tags",
        "--no-recurse-submodules",
        "--depth=1",
        remote,
        f"+{sha}:{fetch_ref}",
        check=False,
    )
    if result.returncode != 0 or not commit_is_available(repo_root, sha):
        detail = result.stderr.strip() or result.stdout.strip() or "commit remained unavailable"
        raise ChangedRangeError(
            f"declared push boundary {sha} is absent and could not be fetched from {remote}: {detail}"
        )
    return True


def resolve_push_changed_paths(
    repo_root: Path,
    before: str,
    after: str,
    *,
    remote: str = "origin",
) -> tuple[list[str], list[str]]:
    """Return changed paths and the commit IDs fetched to prove the range."""
    root = repo_root.resolve()
    before_sha = _validate_sha("before", before, allow_zero=True)
    after_sha = _validate_sha("after", after)
    fetched: list[str] = []

    if ensure_commit_available(root, after_sha, remote):
        fetched.append(after_sha)

    if _is_zero_sha(before_sha):
        result = _run_git(root, "show", "--format=", "--name-only", "--no-renames", after_sha)
    else:
        if ensure_commit_available(root, before_sha, remote):
            fetched.append(before_sha)
        result = _run_git(root, "diff", "--name-only", "--no-renames", before_sha, after_sha)

    paths = sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})
    return paths, fetched


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        paths, fetched = resolve_push_changed_paths(
            Path(args.repo_root),
            args.before,
            args.after,
            remote=args.remote,
        )
    except ChangedRangeError as exc:
        raise SystemExit(f"SWRLZ changed-range resolution failed: {exc}") from exc

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(f"{path}\n" for path in paths), encoding="utf-8")

    for sha in fetched:
        print(f"Fetched missing push-range commit: {sha}")
    print(f"Resolved {len(paths)} changed path(s) for {args.before}..{args.after}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
