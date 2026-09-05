from pathlib import Path
import gzip
import hashlib
import json
import os
import urllib.request

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from swyrlz.container import R38Container

app = FastAPI(title="§wyrlz R38 Setup", version="0.1.0")

MODEL_URL = (
    "https://raw.githubusercontent.com/kamiswrlzco-cloud/Swrlzco/main/"
    "SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.%25C2%25A7wyrlzx.gz"
)
PACKED_PATH = Path("/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx.gz")
RAW_PATH = Path("/tmp/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.§wyrlzx")

EXPECTED_PACKED_SIZE = 17_565_695
EXPECTED_PACKED_SHA256 = "b7c673483be5887a901b15ef7c916c71934ea67937d9456240a4b185753543c5"
EXPECTED_RAW_SIZE = 233_640_424
EXPECTED_RAW_SHA256 = "e6732c7875f7689019b7e051675f5b4b5a901af4fe4d52f8a1fcadafec3229e7"
EXPECTED_ROOT_DIGEST = "7f9d3a52a57f6b5bab79ebcd5557e96c7ff8b650abfdb2cad22d7189905ecb94"
EXPECTED_INTEGRITY_RECORDS = 176


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download_packed() -> dict:
    if PACKED_PATH.exists():
        size = PACKED_PATH.stat().st_size
        digest = _sha256(PACKED_PATH)
        if size == EXPECTED_PACKED_SIZE and digest == EXPECTED_PACKED_SHA256:
            return {"reused": True, "size": size, "sha256": digest}
        PACKED_PATH.unlink(missing_ok=True)

    tmp = PACKED_PATH.with_suffix(PACKED_PATH.suffix + ".part")
    tmp.unlink(missing_ok=True)
    with urllib.request.urlopen(MODEL_URL, timeout=120) as response, tmp.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    os.replace(tmp, PACKED_PATH)

    size = PACKED_PATH.stat().st_size
    digest = _sha256(PACKED_PATH)
    if size != EXPECTED_PACKED_SIZE:
        raise ValueError(f"Packed size mismatch: {size} != {EXPECTED_PACKED_SIZE}")
    if digest != EXPECTED_PACKED_SHA256:
        raise ValueError(f"Packed SHA-256 mismatch: {digest}")
    return {"reused": False, "size": size, "sha256": digest}


def _expand_raw() -> dict:
    if RAW_PATH.exists():
        size = RAW_PATH.stat().st_size
        digest = _sha256(RAW_PATH)
        if size == EXPECTED_RAW_SIZE and digest == EXPECTED_RAW_SHA256:
            return {"reused": True, "size": size, "sha256": digest}
        RAW_PATH.unlink(missing_ok=True)

    tmp = RAW_PATH.with_suffix(RAW_PATH.suffix + ".part")
    tmp.unlink(missing_ok=True)
    with gzip.open(PACKED_PATH, "rb") as src, tmp.open("wb") as dst:
        while True:
            chunk = src.read(1024 * 1024)
            if not chunk:
                break
            dst.write(chunk)
    os.replace(tmp, RAW_PATH)

    size = RAW_PATH.stat().st_size
    digest = _sha256(RAW_PATH)
    if size != EXPECTED_RAW_SIZE:
        raise ValueError(f"Raw size mismatch: {size} != {EXPECTED_RAW_SIZE}")
    if digest != EXPECTED_RAW_SHA256:
        raise ValueError(f"Raw SHA-256 mismatch: {digest}")
    return {"reused": False, "size": size, "sha256": digest}


def _verify_container() -> dict:
    container = R38Container(RAW_PATH)
    summary = container.summary()
    root_ok = container.root_digest == EXPECTED_ROOT_DIGEST
    records_ok = len(container.section_hashes) == EXPECTED_INTEGRITY_RECORDS
    if not root_ok:
        raise ValueError(f"Container root digest mismatch: {container.root_digest}")
    if not records_ok:
        raise ValueError(
            f"Integrity record count mismatch: {len(container.section_hashes)} != {EXPECTED_INTEGRITY_RECORDS}"
        )
    return {
        "rootDigest": container.root_digest,
        "rootDigestValid": root_ok,
        "integrityRecordCount": len(container.section_hashes),
        "integrityRecordCountValid": records_ok,
        "recoveredJsonSectionCount": len(container.section_hits),
        "summary": summary,
    }


@app.get("/api/setup", response_class=HTMLResponse)
def setup_page():
    return """<!doctype html>
<html>
<head>
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>§wyrlz R38 Setup</title>
<style>
body{font-family:system-ui;background:#0b0d12;color:#eef2ff;max-width:760px;margin:40px auto;padding:20px}
button{font-size:18px;padding:14px 20px;border:0;border-radius:12px;cursor:pointer}
pre{white-space:pre-wrap;background:#141824;padding:16px;border-radius:12px;overflow:auto}
.ok{color:#7CFF9B}.bad{color:#ff8f8f}
</style>
</head>
<body>
<h1>§wyrlz R38 Setup</h1>
<p>This runs the remaining artifact bootstrap in one request: download → compressed hash → decompress → raw hash → SXI1/container verification.</p>
<button id=\"run\">Run R38 Setup</button>
<p id=\"status\"></p>
<pre id=\"out\">Ready.</pre>
<script>
const b=document.getElementById('run'),s=document.getElementById('status'),o=document.getElementById('out');
b.onclick=async()=>{
 b.disabled=true;s.textContent='Running… this can take a while on a cold start.';o.textContent='Working…';
 try{
  const r=await fetch('/api/setup',{method:'POST'});
  const j=await r.json();
  o.textContent=JSON.stringify(j,null,2);
  s.className=j.ok?'ok':'bad';s.textContent=j.ok?'R38 artifact setup verified ✅':'Setup failed ❌';
 }catch(e){s.className='bad';s.textContent='Request failed';o.textContent=String(e)}
 finally{b.disabled=false}
};
</script>
</body>
</html>"""


@app.post("/api/setup")
def run_setup():
    result = {
        "ok": False,
        "stage": "starting",
        "graphReady": False,
        "interactiveReady": False,
        "note": "This verifies the R38 artifact/container only. The R38 neural executor is still a separate implementation gate.",
    }
    try:
        result["stage"] = "packed-model"
        result["packed"] = _download_packed()
        result["packedValid"] = True

        result["stage"] = "raw-model"
        result["raw"] = _expand_raw()
        result["rawValid"] = True

        result["stage"] = "container"
        result["container"] = _verify_container()
        result["containerVerified"] = True

        result["stage"] = "artifact-ready"
        result["ok"] = True
        return result
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result.setdefault("containerVerified", False)
        return JSONResponse(status_code=500, content=result)
