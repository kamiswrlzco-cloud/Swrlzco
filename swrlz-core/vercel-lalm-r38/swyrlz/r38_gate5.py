from __future__ import annotations

import gzip
import hashlib
import os
import struct
import time
import urllib.request
from pathlib import Path
from typing import Any

MODEL_URL = (
    "https://raw.githubusercontent.com/kamiswrlzco-cloud/Swrlzco/main/"
    "SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.%25C2%25A7wyrlzx.gz"
)
PACKED = Path("/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx.gz")
RAW = Path("/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx")
EXPECTED_PACKED_SIZE = 17_565_695
EXPECTED_RAW_SIZE = 233_640_424
EXPECTED_PACKED_SHA256 = "b7c673483be5887a901b15ef7c916c71934ea67937d9456240a4b185753543c5"
EXPECTED_RAW_SHA256 = "e6732c7875f7689019b7e051675f5b4b5a901af4fe4d52f8a1fcadafec3229e7"
INTEGRITY_MAGIC = b"SXI1"

_verified_packed_key: tuple[int, int] | None = None
_verified_raw_key: tuple[int, int] | None = None
_gate5_cache: tuple[tuple[int, int], dict[str, Any]] | None = None


def _key(path: Path) -> tuple[int, int]:
    st = path.stat()
    return int(st.st_size), int(st.st_mtime_ns)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _valid_cached(path: Path, expected_size: int, expected_sha: str, which: str) -> bool:
    global _verified_packed_key, _verified_raw_key
    if not path.exists() or path.stat().st_size != expected_size:
        return False
    k = _key(path)
    cached = _verified_packed_key if which == "packed" else _verified_raw_key
    if cached == k:
        return True
    if sha256_file(path) != expected_sha:
        return False
    if which == "packed":
        _verified_packed_key = k
    else:
        _verified_raw_key = k
    return True


def ensure_artifact() -> dict[str, Any]:
    global _verified_packed_key, _verified_raw_key
    started = time.monotonic()

    packed_reused = _valid_cached(PACKED, EXPECTED_PACKED_SIZE, EXPECTED_PACKED_SHA256, "packed")
    if not packed_reused:
        PACKED.unlink(missing_ok=True)
        tmp = PACKED.with_suffix(PACKED.suffix + ".part")
        tmp.unlink(missing_ok=True)
        with urllib.request.urlopen(MODEL_URL, timeout=60) as r, tmp.open("wb") as out:
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        if tmp.stat().st_size != EXPECTED_PACKED_SIZE or sha256_file(tmp) != EXPECTED_PACKED_SHA256:
            tmp.unlink(missing_ok=True)
            raise ValueError("R38_PACKED_INTEGRITY_FAILED")
        os.replace(tmp, PACKED)
        _verified_packed_key = _key(PACKED)

    raw_reused = _valid_cached(RAW, EXPECTED_RAW_SIZE, EXPECTED_RAW_SHA256, "raw")
    if not raw_reused:
        RAW.unlink(missing_ok=True)
        tmp = RAW.with_suffix(RAW.suffix + ".part")
        tmp.unlink(missing_ok=True)
        with gzip.open(PACKED, "rb") as src, tmp.open("wb") as out:
            while True:
                chunk = src.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        if tmp.stat().st_size != EXPECTED_RAW_SIZE or sha256_file(tmp) != EXPECTED_RAW_SHA256:
            tmp.unlink(missing_ok=True)
            raise ValueError("R38_RAW_INTEGRITY_FAILED")
        os.replace(tmp, RAW)
        _verified_raw_key = _key(RAW)

    return {
        "packedReused": packed_reused,
        "rawReused": raw_reused,
        "path": str(RAW),
        "artifactEnsureMs": int((time.monotonic() - started) * 1000),
    }


def _read_integrity_tail(path: Path) -> dict[str, Any]:
    size = path.stat().st_size
    # SXI1 is near the end of R38. Read only the final 64 KiB rather than scanning
    # or mapping the full 223 MiB artifact inside a serverless request.
    tail_size = min(size, 64 * 1024)
    with path.open("rb") as f:
        f.seek(size - tail_size)
        tail = f.read(tail_size)
    rel = tail.find(INTEGRITY_MAGIC)
    if rel < 0:
        raise ValueError("SXI1_NOT_FOUND_IN_TAIL")
    abs_off = size - tail_size + rel
    if rel + 40 > len(tail):
        raise ValueError("SXI1_HEADER_TRUNCATED")
    root = tail[rel + 4:rel + 36].hex()
    count = struct.unpack_from("<I", tail, rel + 36)[0]
    p = rel + 40
    ids: list[int] = []
    for _ in range(count):
        if p + 36 > len(tail):
            raise ValueError("SXI1_RECORD_TABLE_TRUNCATED")
        ids.append(struct.unpack_from("<I", tail, p)[0])
        p += 36
    return {
        "integrityOffset": abs_off,
        "rootDigestSha256": root,
        "integrityRecordCount": count,
        "sectionIds": ids,
    }


def inspect_gate5(force: bool = False) -> dict[str, Any]:
    """Cheap Gate-5 boundary probe safe for Vercel serverless execution.

    The previous implementation performed a full R38 container walk and JSON
    discovery on every cold invocation. That can be terminated by the platform
    before Python can return an exception. This probe deliberately touches only
    the artifact header and final 64 KiB integrity table.
    """
    global _gate5_cache
    started = time.monotonic()
    artifact = ensure_artifact()
    raw_key = _key(RAW)
    if not force and _gate5_cache is not None and _gate5_cache[0] == raw_key:
        result = dict(_gate5_cache[1])
        result["cacheHit"] = True
        result["inspectionMs"] = int((time.monotonic() - started) * 1000)
        return result

    with RAW.open("rb") as f:
        head = f.read(128)
    header_magic = head[:8]
    canonical_header_present = header_magic == b"SWRLZX\r\n"
    integrity = _read_integrity_tail(RAW)
    section_ids = set(integrity["sectionIds"])

    required_registered = {sid: sid in section_ids for sid in (3, 4, 5)}
    blockers: list[str] = []
    if not canonical_header_present:
        blockers.append("CANONICAL_SWRLZX_HEADER_NOT_PRESENT_AT_OFFSET_0")
    if not required_registered[3]:
        blockers.append("TOKENIZER_SECTION_3_NOT_REGISTERED")
    if not required_registered[4]:
        blockers.append("TENSOR_DIRECTORY_SECTION_4_NOT_REGISTERED")
    if not required_registered[5]:
        blockers.append("TENSOR_DATA_SECTION_5_NOT_REGISTERED")

    # Presence in the integrity table does not yet give physical payload offsets.
    # Therefore one-token inference remains blocked until directory/data location
    # reconstruction is implemented, even when 3/4/5 are registered.
    blockers.append("SECTION_PAYLOAD_LOCATIONS_NOT_RECONSTRUCTED")

    result = {
        "ok": True,
        "stage": "gate5-lightweight-readiness",
        "artifact": artifact,
        "containerVerified": True,
        "canonicalHeaderPresent": canonical_header_present,
        "headerMagicHex": header_magic.hex(),
        "integrityOffset": integrity["integrityOffset"],
        "rootDigestSha256": integrity["rootDigestSha256"],
        "integrityRecordCount": integrity["integrityRecordCount"],
        "requiredSectionsRegistered": required_registered,
        "oneTokenReady": False,
        "interactiveReady": False,
        "blockers": blockers,
        "cacheHit": False,
        "probeMode": "tail-only",
        "bytesInspectedApprox": 64 * 1024 + 128,
        "nextRequiredAction": "Reconstruct physical payload locations for tokenizer section 3, tensor directory section 4, and tensor data section 5 without full-artifact scanning.",
    }
    result["inspectionMs"] = int((time.monotonic() - started) * 1000)
    _gate5_cache = (raw_key, dict(result))
    return result
