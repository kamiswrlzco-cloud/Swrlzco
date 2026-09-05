from pathlib import Path
import hashlib
import os
import time
import urllib.request

from fastapi import FastAPI

app = FastAPI(title="§wyrlz Vercel Health Probe", version="0.6.0")

MODEL_URL = (
    "https://raw.githubusercontent.com/kamiswrlzco-cloud/Swrlzco/main/"
    "SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.%25C2%25A7wyrlzx.gz"
)
MODEL_PATH = Path("/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx.gz")
EXPECTED_SIZE = 17_565_695
EXPECTED_SHA256 = "b7c673483be5887a901b15ef7c916c71934ea67937d9456240a4b185753543c5"
_VERIFY_CACHE = {"sig": None, "sha256": None, "valid": False}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _signature(path: Path):
    st = path.stat()
    return (st.st_size, st.st_mtime_ns)


def _download_atomic() -> None:
    tmp_path = MODEL_PATH.with_suffix(MODEL_PATH.suffix + ".part")
    tmp_path.unlink(missing_ok=True)
    with urllib.request.urlopen(MODEL_URL, timeout=60) as response, tmp_path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
        out.flush()
        os.fsync(out.fileno())
    tmp_path.replace(MODEL_PATH)


def _ensure_model() -> dict:
    started = time.monotonic()
    downloaded = False
    hash_reused = False
    try:
        if not MODEL_PATH.exists() or MODEL_PATH.stat().st_size != EXPECTED_SIZE:
            _download_atomic()
            downloaded = True

        sig = _signature(MODEL_PATH)
        if _VERIFY_CACHE["valid"] and _VERIFY_CACHE["sig"] == sig:
            actual_sha256 = _VERIFY_CACHE["sha256"]
            hash_reused = True
        else:
            actual_sha256 = _sha256(MODEL_PATH)
            _VERIFY_CACHE.update(sig=sig, sha256=actual_sha256, valid=actual_sha256 == EXPECTED_SHA256)

        # A correct-size corrupt cache must not get stuck forever.
        if actual_sha256 != EXPECTED_SHA256 and not downloaded:
            MODEL_PATH.unlink(missing_ok=True)
            _VERIFY_CACHE.update(sig=None, sha256=None, valid=False)
            _download_atomic()
            downloaded = True
            sig = _signature(MODEL_PATH)
            actual_sha256 = _sha256(MODEL_PATH)
            _VERIFY_CACHE.update(sig=sig, sha256=actual_sha256, valid=actual_sha256 == EXPECTED_SHA256)
            hash_reused = False

        actual_size = MODEL_PATH.stat().st_size
        size_valid = actual_size == EXPECTED_SIZE
        hash_valid = actual_sha256 == EXPECTED_SHA256
        return {
            "modelDownloaded": downloaded,
            "modelPresent": True,
            "modelPath": str(MODEL_PATH),
            "modelSize": actual_size,
            "modelExpectedSize": EXPECTED_SIZE,
            "modelSizeValid": size_valid,
            "modelSha256": actual_sha256,
            "modelExpectedSha256": EXPECTED_SHA256,
            "modelHashValid": hash_valid,
            "modelHashReused": hash_reused,
            "modelInstalled": size_valid and hash_valid,
            "modelError": None,
            "probeElapsedMs": int((time.monotonic() - started) * 1000),
        }
    except Exception as exc:
        return {
            "modelDownloaded": downloaded,
            "modelPresent": MODEL_PATH.exists(),
            "modelPath": str(MODEL_PATH),
            "modelSize": MODEL_PATH.stat().st_size if MODEL_PATH.exists() else None,
            "modelExpectedSize": EXPECTED_SIZE,
            "modelSizeValid": False,
            "modelSha256": None,
            "modelExpectedSha256": EXPECTED_SHA256,
            "modelHashValid": False,
            "modelHashReused": False,
            "modelInstalled": False,
            "modelError": f"{type(exc).__name__}: {exc}",
            "probeElapsedMs": int((time.monotonic() - started) * 1000),
        }


@app.get("/")
@app.get("/api/health")
def health():
    model = _ensure_model()
    return {
        "ok": model["modelInstalled"],
        "service": "§wyrlz Vercel Gateway",
        "stage": "model-download-integrity-probe",
        "routingReady": True,
        **model,
        "containerVerified": False,
        "graphReady": False,
        "interactiveReady": False,
        "setupUrl": "/api/setup",
    }
