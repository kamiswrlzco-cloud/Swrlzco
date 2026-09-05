from __future__ import annotations

import gzip
import hashlib
import json
import os
import struct
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np

from .container import R38Container

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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_artifact() -> dict[str, Any]:
    packed_reused = PACKED.exists() and PACKED.stat().st_size == EXPECTED_PACKED_SIZE
    if packed_reused and sha256_file(PACKED) != EXPECTED_PACKED_SHA256:
        PACKED.unlink(missing_ok=True); packed_reused = False
    if not packed_reused:
        tmp = PACKED.with_suffix(PACKED.suffix + ".part")
        tmp.unlink(missing_ok=True)
        with urllib.request.urlopen(MODEL_URL, timeout=60) as r, tmp.open("wb") as out:
            while True:
                chunk = r.read(1024 * 1024)
                if not chunk: break
                out.write(chunk)
        if tmp.stat().st_size != EXPECTED_PACKED_SIZE or sha256_file(tmp) != EXPECTED_PACKED_SHA256:
            tmp.unlink(missing_ok=True)
            raise ValueError("R38_PACKED_INTEGRITY_FAILED")
        os.replace(tmp, PACKED)

    raw_reused = RAW.exists() and RAW.stat().st_size == EXPECTED_RAW_SIZE
    if raw_reused and sha256_file(RAW) != EXPECTED_RAW_SHA256:
        RAW.unlink(missing_ok=True); raw_reused = False
    if not raw_reused:
        tmp = RAW.with_suffix(RAW.suffix + ".part")
        tmp.unlink(missing_ok=True)
        with gzip.open(PACKED, "rb") as src, tmp.open("wb") as out:
            while True:
                chunk = src.read(1024 * 1024)
                if not chunk: break
                out.write(chunk)
        if tmp.stat().st_size != EXPECTED_RAW_SIZE or sha256_file(tmp) != EXPECTED_RAW_SHA256:
            tmp.unlink(missing_ok=True)
            raise ValueError("R38_RAW_INTEGRITY_FAILED")
        os.replace(tmp, RAW)
    return {"packedReused": packed_reused, "rawReused": raw_reused, "path": str(RAW)}


def q4_scale_min(sc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    nb = sc.shape[0]
    s = np.empty((nb, 8), np.int16); m = np.empty((nb, 8), np.int16)
    s[:, :4] = sc[:, :4] & 63; m[:, :4] = sc[:, 4:8] & 63
    for j in range(4, 8):
        s[:, j] = (sc[:, j + 4] & 15) | ((sc[:, j - 4] >> 6) << 4)
        m[:, j] = (sc[:, j + 4] >> 4) | ((sc[:, j] >> 6) << 4)
    return s, m


def deq_q4k(raw: np.ndarray, cols: int, rows: int) -> np.ndarray:
    if cols % 256: raise ValueError("Q4_K_COLS_NOT_BLOCK_ALIGNED")
    b = raw.reshape(rows * (cols // 256), 144)
    d = b[:, 0:2].copy().view('<f2').reshape(-1).astype(np.float32)
    dm = b[:, 2:4].copy().view('<f2').reshape(-1).astype(np.float32)
    sc = b[:, 4:16]; qs = b[:, 16:]; s, m = q4_scale_min(sc)
    out = np.empty((b.shape[0], 256), np.float32)
    for g in range(4):
        q = qs[:, g*32:(g+1)*32]
        out[:, g*64:g*64+32] = (d*s[:, 2*g])[:, None]*(q & 15) - (dm*m[:, 2*g])[:, None]
        out[:, g*64+32:g*64+64] = (d*s[:, 2*g+1])[:, None]*(q >> 4) - (dm*m[:, 2*g+1])[:, None]
    return out.reshape(rows, cols)


def deq_q6k(raw: np.ndarray, cols: int, rows: int) -> np.ndarray:
    if cols % 256: raise ValueError("Q6_K_COLS_NOT_BLOCK_ALIGNED")
    b = raw.reshape(rows * (cols // 256), 210)
    ql = b[:, :128]; qh = b[:, 128:192]; sc = b[:, 192:208].view(np.int8).astype(np.int16)
    d = b[:, 208:210].copy().view('<f2').reshape(-1).astype(np.float32)
    out = np.empty((b.shape[0], 256), np.float32); ix = np.arange(32) // 16
    for half in range(2):
        lo0 = ql[:, half*64:half*64+32]; lo1 = ql[:, half*64+32:half*64+64]; hi = qh[:, half*32:(half+1)*32]
        s = half*8; o = half*128
        q1 = ((lo0 & 15) | (((hi >> 0) & 3) << 4)).astype(np.int16) - 32
        q2 = ((lo1 & 15) | (((hi >> 2) & 3) << 4)).astype(np.int16) - 32
        q3 = (((lo0 >> 4) & 15) | (((hi >> 4) & 3) << 4)).astype(np.int16) - 32
        q4 = (((lo1 >> 4) & 15) | (((hi >> 6) & 3) << 4)).astype(np.int16) - 32
        out[:, o:o+32] = d[:, None]*sc[:, s+ix]*q1
        out[:, o+32:o+64] = d[:, None]*sc[:, s+2+ix]*q2
        out[:, o+64:o+96] = d[:, None]*sc[:, s+4+ix]*q3
        out[:, o+96:o+128] = d[:, None]*sc[:, s+6+ix]*q4
    return out.reshape(rows, cols)


def kernel_selftest() -> dict[str, Any]:
    # Zero blocks are a deterministic geometry/safety test; numerical parity with R294
    # is gated on real tensor bytes later.
    q4 = deq_q4k(np.zeros(144, dtype=np.uint8), 256, 1)
    q6 = deq_q6k(np.zeros(210, dtype=np.uint8), 256, 1)
    return {
        "ok": bool(q4.shape == (1,256) and q6.shape == (1,256)),
        "q4kShape": list(q4.shape), "q6kShape": list(q6.shape),
        "q4kFinite": bool(np.isfinite(q4).all()), "q6kFinite": bool(np.isfinite(q6).all()),
    }


def inspect_gate5() -> dict[str, Any]:
    artifact = ensure_artifact()
    c = R38Container(RAW)
    lineage = c.section_json(10) if 10 in c.section_hits else {}
    provenance = c.section_json(20) if 20 in c.section_hits else {}
    runtime = c.section_json(38) if 38 in c.section_hits else {}
    schedule = c.section_json(88) if 88 in c.section_hits else {}
    tokenizer_contract = c.section_json(31) if 31 in c.section_hits else {}

    with RAW.open("rb") as f:
        head = f.read(128)
    header_magic = head[:8]
    canonical_header_present = header_magic == b"SWRLZX\r\n"
    first_nonzero = None
    with RAW.open("rb") as f:
        pos = 0
        while True:
            block = f.read(1024 * 1024)
            if not block: break
            nz = next((i for i,b in enumerate(block) if b), None)
            if nz is not None:
                first_nonzero = pos + nz; break
            pos += len(block)

    tensor_provenance = provenance.get("tensors") if isinstance(provenance, dict) else []
    if not isinstance(tensor_provenance, list): tensor_provenance = []
    nodes = schedule.get("nodes") if isinstance(schedule, dict) else []
    if not isinstance(nodes, list): nodes = []

    # R38's recoverable integrity-indexed metadata says where the canonical sections should be,
    # but the current transferred artifact does not expose sections 3/4/5 as directly recoverable
    # payloads and its first 128 bytes are zero. Fail closed instead of fabricating tensor access.
    direct_required = {sid: sid in c.section_hits for sid in (3,4,5)}
    blockers = []
    if not canonical_header_present: blockers.append("CANONICAL_SWRLZX_HEADER_NOT_PRESENT_AT_OFFSET_0")
    if not direct_required[3]: blockers.append("TOKENIZER_PAYLOAD_SECTION_3_NOT_DIRECTLY_RECOVERABLE")
    if not direct_required[4]: blockers.append("TENSOR_DIRECTORY_SECTION_4_NOT_DIRECTLY_RECOVERABLE")
    if not direct_required[5]: blockers.append("TENSOR_DATA_SECTION_5_NOT_DIRECTLY_RECOVERABLE")

    return {
        "ok": True,
        "stage": "gate5-executor-readiness",
        "artifact": artifact,
        "artifactRevision": lineage.get("artifactRevision"),
        "generation": lineage.get("generation"),
        "containerVerified": True,
        "canonicalHeaderPresent": canonical_header_present,
        "headerMagicHex": header_magic.hex(),
        "firstNonZeroOffset": first_nonzero,
        "integrityRecordCount": len(c.section_hashes),
        "recoveredJsonSectionCount": len(c.section_hits),
        "runtimeContractRecovered": bool(runtime),
        "runtimeStatus": runtime.get("status"),
        "runtimeArchitecture": runtime.get("architectureId"),
        "executionScheduleRecovered": bool(schedule),
        "executionNodeCount": schedule.get("nodeCount", len(nodes)),
        "tensorProvenanceCount": len(tensor_provenance),
        "sourceTensorCount": (provenance.get("source") or {}).get("tensorCount") if isinstance(provenance, dict) else None,
        "tokenizerContractRecovered": bool(tokenizer_contract),
        "tokenizerVocabSize": tokenizer_contract.get("vocabSize") if isinstance(tokenizer_contract, dict) else None,
        "directRequiredSections": direct_required,
        "kernelSelftest": kernel_selftest(),
        "oneTokenReady": not blockers,
        "interactiveReady": False,
        "blockers": blockers,
        "nextRequiredAction": "Recover or reconstruct canonical tokenizer/tensor-directory/tensor-data payload access from the R38 lineage before claiming one-token inference." if blockers else "Wire tokenizer and graph execution for deterministic one-token inference.",
    }
