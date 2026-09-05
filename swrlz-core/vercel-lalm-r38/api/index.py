from __future__ import annotations
from pathlib import Path
import os, time, urllib.request, zipfile

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from swyrlz.container import R38Container
from swyrlz.backend import R38Backend, GenerationConfig

APP_ROOT = Path(__file__).resolve().parents[1]
PACKED_MODEL = Path(os.getenv(
    "SWYRLZ_MODEL_GZIP",
    "/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx.gz"
))
BOOTSTRAP_URL = os.getenv(
    "SWYRLZ_BOOTSTRAP_URL",
    "https://raw.githubusercontent.com/kamiswrlzco-cloud/Swrlzco/main/swrlz-core/SWYRLZ_VERCEL_LALM_R38_BOOTSTRAP.zip"
)
MODEL_PATH = Path(os.getenv(
    "SWYRLZ_MODEL_PATH",
    "/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx"
))

app = FastAPI(title="§wyrlz LALM R38 Python Server", version="0.1.0-bootstrap")
_backend: R38Backend | None = None
_load_error: str | None = None

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=32768)
    max_tokens: int = Field(default=64, ge=1, le=512)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, gt=0.0, le=1.0)

def get_backend() -> R38Backend:
    global _backend, _load_error
    if _backend is not None:
        return _backend
    try:
        if not MODEL_PATH.exists():
            if not PACKED_MODEL.exists():
                bundle = Path("/tmp/SWYRLZ_VERCEL_LALM_R38_BOOTSTRAP.zip")
                urllib.request.urlretrieve(BOOTSTRAP_URL, bundle)
                with zipfile.ZipFile(bundle, "r") as zf:
                    member = "models/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx.gz"
                    with zf.open(member) as src, PACKED_MODEL.open("wb") as dst:
                        while True:
                            chunk = src.read(1024 * 1024)
                            if not chunk:
                                break
                            dst.write(chunk)
            R38Container.expand_gzip(PACKED_MODEL, MODEL_PATH)
        _backend = R38Backend(MODEL_PATH)
        _load_error = None
        return _backend
    except Exception as e:
        _load_error = f"{type(e).__name__}: {e}"
        raise

@app.get("/")
def root():
    return {
        "name": "§wyrlz LALM R38 Python Server",
        "status": "bootstrap",
        "health": "/api/health",
        "model": "/api/model",
        "sections": "/api/sections",
        "generate": "/api/generate",
    }

@app.get("/api/health")
def health():
    started=time.perf_counter()
    try:
        backend=get_backend()
        info=backend.model_info()
        return {
            "ok": True,
            "containerVerified": info["containerVerified"],
            "graphReady": info["graphReady"],
            "interactiveReady": info["interactiveReady"],
            "artifactRevision": info.get("artifactRevision"),
            "loadMs": round((time.perf_counter()-started)*1000, 3),
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "lastLoadError": _load_error}

@app.get("/api/model")
def model():
    try:
        return get_backend().model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")

@app.get("/api/sections")
def sections():
    try:
        return get_backend().container.section_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")

@app.post("/api/generate")
def generate(req: GenerateRequest):
    backend=get_backend()
    cfg=GenerationConfig(req.max_tokens, req.temperature, req.top_p)
    try:
        return {"text": backend.generate(req.prompt, cfg)}
    except RuntimeError as e:
        raise HTTPException(status_code=501, detail=str(e))

@app.post("/api/generate/stream")
def generate_stream(req: GenerateRequest):
    backend=get_backend()
    cfg=GenerationConfig(req.max_tokens, req.temperature, req.top_p)
    if not backend.ready:
        raise HTTPException(
            status_code=501,
            detail="R38_PYTHON_NEURAL_BACKEND_PENDING"
        )
    return StreamingResponse(backend.stream(req.prompt, cfg), media_type="text/plain; charset=utf-8")
