from __future__ import annotations

import hashlib
import hmac
import json
import mimetypes
import os
import platform
import shutil
import stat
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

app = FastAPI(title="§wyrlz Live Runtime Workbench", version="1.1.0")

ROOT = Path("/tmp/swrlz-admin")
LIVE = ROOT / "live"
LOGS = ROOT / "logs"
UPLOADS = ROOT / "uploads"
PAGES = ROOT / "pages"
for d in (ROOT, LIVE, LOGS, UPLOADS, PAGES):
    d.mkdir(parents=True, exist_ok=True)

INSTANCE_ID = f"{os.getpid()}-{uuid.uuid4().hex[:8]}"
FULL_LOG = LOGS / "full-runtime.log"
HOT_GATE5 = LIVE / "gate5_live.py"
MAX_TEXT = 2 * 1024 * 1024
MAX_LIST = 1000
MAX_UPLOAD_CHUNK = 3 * 1024 * 1024
ADMIN_TOKEN = os.environ.get("SWRLZ_ADMIN_TOKEN", "")

DEFAULT_HOT_GATE5 = r'''from __future__ import annotations
import gzip, hashlib, json, os, struct, time, urllib.request
from pathlib import Path

MODEL_URL = "https://raw.githubusercontent.com/kamiswrlzco-cloud/Swrlzco/main/SWYRLZ_LALM_R38_LOCAL_TIME_CONTEXT_CALIBRATED.%25C2%25A7wyrlzx.gz"
PACKED = Path("/tmp/swrlz-admin/live/R38.§wyrlzx.gz")
RAW = Path("/tmp/swrlz-admin/live/R38.§wyrlzx")
EXPECTED_PACKED_SIZE = 17565695
EXPECTED_RAW_SIZE = 233640424
EXPECTED_PACKED_SHA = "b7c673483be5887a901b15ef7c916c71934ea67937d9456240a4b185753543c5"
EXPECTED_RAW_SHA = "e6732c7875f7689019b7e051675f5b4b5a901af4fe4d52f8a1fcadafec3229e7"

def emit(stage, **data):
    print(json.dumps({"stage": stage, "ts": time.time(), **data}), flush=True)

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def main():
    emit("start", pid=os.getpid(), cwd=os.getcwd())
    if not PACKED.exists() or PACKED.stat().st_size != EXPECTED_PACKED_SIZE:
        emit("download-start", url=MODEL_URL)
        tmp=PACKED.with_suffix(PACKED.suffix+".part")
        tmp.unlink(missing_ok=True)
        with urllib.request.urlopen(MODEL_URL, timeout=60) as r, tmp.open("wb") as o:
            total=0
            while True:
                b=r.read(1024*1024)
                if not b: break
                o.write(b); total+=len(b)
                if total % (4*1024*1024) < len(b): emit("download-progress", bytes=total)
        os.replace(tmp, PACKED)
    emit("packed", size=PACKED.stat().st_size)
    packed_sha=sha(PACKED)
    emit("packed-hash", sha256=packed_sha, valid=packed_sha==EXPECTED_PACKED_SHA)
    if packed_sha != EXPECTED_PACKED_SHA: raise RuntimeError("packed sha mismatch")

    if not RAW.exists() or RAW.stat().st_size != EXPECTED_RAW_SIZE:
        emit("decompress-start")
        tmp=RAW.with_suffix(RAW.suffix+".part")
        tmp.unlink(missing_ok=True)
        with gzip.open(PACKED,"rb") as src, tmp.open("wb") as out:
            total=0
            while True:
                b=src.read(1024*1024)
                if not b: break
                out.write(b); total+=len(b)
                if total % (32*1024*1024) < len(b): emit("decompress-progress", bytes=total)
        os.replace(tmp, RAW)
    emit("raw", size=RAW.stat().st_size)

    with RAW.open("rb") as f:
        head=f.read(128)
        f.seek(max(0, RAW.stat().st_size-65536))
        tail=f.read()
    emit("head", magicHex=head[:8].hex(), canonical=head[:8]==b"SWRLZX\r\n")
    idx=tail.rfind(b"SXI1")
    if idx < 0: raise RuntimeError("SXI1 not found in final 64KiB")
    absolute=RAW.stat().st_size-65536+idx
    count=struct.unpack_from("<I", tail, idx+36)[0]
    p=idx+40
    ids=[]
    for _ in range(count):
        if p+36>len(tail): break
        ids.append(struct.unpack_from("<I",tail,p)[0]); p+=36
    emit("integrity", offset=absolute, declaredCount=count, parsedCount=len(ids), required={str(i): i in ids for i in (3,4,5)})
    emit("done", ok=True, next="Edit this live script in /tmp/swrlz-admin/live/gate5_live.py and rerun without redeploying.")

if __name__ == "__main__": main()
'''

if not HOT_GATE5.exists():
    HOT_GATE5.write_text(DEFAULT_HOT_GATE5, encoding="utf-8")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(event: str, **data) -> None:
    rec = {"ts": now(), "instanceId": INSTANCE_ID, "pid": os.getpid(), "event": event, **data}
    line = json.dumps(rec, ensure_ascii=False, separators=(",", ":"))
    try:
        with FULL_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def path_of(raw: str | None) -> Path:
    if not raw:
        return ROOT
    p = Path(raw)
    return p if p.is_absolute() else ROOT / p


def upload_destination(raw_dir: str | None, name: str) -> Path:
    base = path_of(raw_dir).resolve()
    root = ROOT.resolve()
    if base != root and root not in base.parents:
        raise PermissionError("uploads are restricted to /tmp/swrlz-admin and its subdirectories")
    if not base.exists() or not base.is_dir():
        raise FileNotFoundError("upload destination directory does not exist")
    if not os.access(base, os.W_OK):
        raise PermissionError("upload destination directory is not writable")
    safe_name = Path(name).name.strip()
    if not safe_name or safe_name in {".", ".."}:
        raise ValueError("invalid upload filename")
    return base / safe_name


def unique_destination(target: Path) -> Path:
    if not target.exists():
        return target
    suffixes = "".join(target.suffixes)
    stem = target.name[:-len(suffixes)] if suffixes else target.name
    for i in range(1, 10000):
        candidate = target.with_name(f"{stem} ({i}){suffixes}")
        if not candidate.exists():
            return candidate
    raise RuntimeError("unable to allocate a unique destination filename")


def require_upload_auth(request: Request):
    if not ADMIN_TOKEN:
        return JSONResponse(status_code=503, content={
            "ok": False,
            "error": "upload auth is not configured",
            "code": "UPLOAD_AUTH_NOT_CONFIGURED",
            "hint": "Set SWRLZ_ADMIN_TOKEN in the Vercel project environment, redeploy once, then enter that token in the workbench Upload Auth field.",
        })
    supplied = request.headers.get("x-swrlz-admin-token", "")
    if not supplied or not hmac.compare_digest(supplied, ADMIN_TOKEN):
        return JSONResponse(status_code=401, content={"ok": False, "error": "invalid admin upload token", "code": "UPLOAD_AUTH_INVALID"})
    return None


def upload_meta(upload_id: str) -> Path:
    return UPLOADS / f"{upload_id}.json"


def load_upload(upload_id: str) -> dict:
    meta = upload_meta(upload_id)
    if not meta.is_file():
        raise FileNotFoundError("upload session not found")
    return json.loads(meta.read_text("utf-8"))


def save_upload(upload_id: str, data: dict) -> None:
    upload_meta(upload_id).write_text(json.dumps(data, separators=(",", ":")), "utf-8")


def entry(p: Path) -> dict:
    st = p.lstat()
    kind = "dir" if p.is_dir() else "file" if p.is_file() else "link" if p.is_symlink() else "other"
    return {"name": p.name or "/", "path": str(p), "kind": kind, "size": st.st_size, "mtime": st.st_mtime, "mode": stat.filemode(st.st_mode), "readable": os.access(p, os.R_OK), "writable": os.access(p, os.W_OK)}


def runtime() -> dict:
    def disk(p):
        try:
            d = shutil.disk_usage(p); return {"total": d.total, "used": d.used, "free": d.free}
        except Exception as e:
            return {"error": f"{type(e).__name__}: {e}"}
    rss = None
    try:
        import resource
        r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss = int(r * 1024 if sys.platform != "darwin" else r)
    except Exception:
        pass
    return {"ok": True, "instanceId": INSTANCE_ID, "python": sys.version.split()[0], "platform": platform.platform(), "machine": platform.machine(), "cpuCount": os.cpu_count(), "pid": os.getpid(), "cwd": os.getcwd(), "peakRssBytes": rss, "diskRoot": disk("/"), "diskTmp": disk("/tmp"), "root": str(ROOT), "hotScript": str(HOT_GATE5), "fullLog": str(FULL_LOG), "uploadAuthConfigured": bool(ADMIN_TOKEN), "uploadRoot": str(ROOT), "uploadChunkBytes": MAX_UPLOAD_CHUNK, "note": "/tmp is writable and hot-editable but ephemeral and instance-local on Vercel."}


def crumbs(p: Path):
    out = [{"name": "/", "path": "/"}]; cur = Path("/")
    for part in p.parts[1:]:
        cur /= part; out.append({"name": part, "path": str(cur)})
    return out


def run_hot(timeout_s: int = 45) -> dict:
    started = time.monotonic()
    log("hot-run-start", script=str(HOT_GATE5), timeout=timeout_s)
    try:
        cp = subprocess.run([sys.executable, "-u", str(HOT_GATE5)], capture_output=True, text=True, timeout=timeout_s, cwd=str(LIVE), env={**os.environ, "PYTHONUNBUFFERED": "1"})
        result = {"ok": cp.returncode == 0, "returnCode": cp.returncode, "stdout": cp.stdout[-200000:], "stderr": cp.stderr[-200000:], "elapsedMs": int((time.monotonic() - started) * 1000), "instanceId": INSTANCE_ID}
        log("hot-run-end", returnCode=cp.returncode, elapsedMs=result["elapsedMs"], stdout=result["stdout"], stderr=result["stderr"])
        return result
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
        result = {"ok": False, "timeout": True, "stdout": out[-200000:], "stderr": err[-200000:], "elapsedMs": int((time.monotonic() - started) * 1000), "instanceId": INSTANCE_ID}
        log("hot-run-timeout", elapsedMs=result["elapsedMs"], stdout=result["stdout"], stderr=result["stderr"])
        return result


PAGE = r'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>§wyrlz Live Workbench</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font-family:system-ui;background:#080b10;color:#eef5ff;margin:0 auto;padding:16px;max-width:1100px}.p{background:#121826;border:1px solid #293750;border-radius:16px;padding:14px;margin:12px 0}.r{display:flex;gap:9px;flex-wrap:wrap;align-items:center}button{padding:11px 14px;border-radius:10px;border:0;font-weight:800}button.alt{background:#1d2a3f;color:#dff8ff;border:1px solid #36506f}input,textarea{width:100%;background:#0b1120;color:#fff;border:1px solid #53627d;border-radius:10px;padding:10px;font:inherit}.grow{flex:1;min-width:180px}.files{max-height:430px;overflow:auto}.e{padding:9px;border-bottom:1px solid #26344d;cursor:pointer}.e:hover{background:#182235}textarea{min-height:300px;font-family:ui-monospace,monospace}pre{white-space:pre-wrap;overflow:auto;background:#0b1120;padding:12px;border-radius:10px}.warn{color:#ffd166}.ok{color:#80ffad}.bad{color:#ff9292}.small{font-size:12px;color:#9fb0c8}.bar{height:10px;background:#0b1120;border:1px solid #31425f;border-radius:999px;overflow:hidden}.fill{height:100%;width:0;background:linear-gradient(90deg,#26d9ff,#80ffad);transition:width .12s linear}.hidden{display:none}</style></head><body>
<h1>§wyrlz Live Workbench</h1><div class="p warn">One deployed shell, then edit/run diagnostics from writable /tmp without a redeploy. Vercel can recycle the instance, so /tmp is not permanent.</div>
<div class="p"><div class="r"><button id="up" class="alt">⬆ UP ONE DIR</button><input id="path" class="grow" value="/tmp/swrlz-admin"><button id="go">GO</button><button id="refresh" class="alt">REFRESH</button><button id="rt" class="alt">RUNTIME</button></div><div id="status"></div></div>
<div class="p"><div class="r"><button id="hot">🔥 RUN HOT GATE 5</button><button id="openhot" class="alt">OPEN HOT SCRIPT</button><button id="logbtn" class="alt">OPEN FULL LOG</button><a href="/api/admin?action=log" target="_blank"><button class="alt">RAW FULL LOG</button></a></div><pre id="runout">Ready.</pre></div>
<div class="p"><div class="r"><h2 class="grow">Files</h2><button id="uploadPick">⬆ UPLOAD FROM PHONE</button></div><input id="fileInput" class="hidden" type="file" multiple><div class="r"><input id="uploadToken" class="grow" type="password" autocomplete="off" placeholder="SWRLZ_ADMIN_TOKEN · kept only in this browser session"><button id="rememberToken" class="alt">SET UPLOAD AUTH</button></div><div class="small">Uploads land in the directory currently open below. Large files are sent in 2 MiB chunks. Uploads are restricted to /tmp/swrlz-admin. Vercel /tmp remains ephemeral and instance-local.</div><div id="uploadName" class="small"></div><div class="bar"><div id="uploadFill" class="fill"></div></div><div id="uploadStatus" class="small">Upload ready.</div><div id="files" class="files"></div></div>
<div class="p"><h2>Editor</h2><div id="sel"></div><div class="r"><button id="save">SAVE LIVE FILE</button><button id="download" class="alt">DOWNLOAD</button></div><textarea id="ed"></textarea></div>
<script>
const $=x=>document.getElementById(x);let cwd='/tmp/swrlz-admin',sel=null;const CHUNK=2*1024*1024;let uploadBusy=false;let adminToken=sessionStorage.getItem('swrlzAdminUploadToken')||'';$('uploadToken').value=adminToken;
async function req(action,o={}){const q=new URLSearchParams({action,...(o.q||{})});const headers={...(o.headers||{})};if(o.auth&&adminToken)headers['x-swrlz-admin-token']=adminToken;const r=await fetch('/api/admin?'+q,{method:o.method||'GET',body:o.body,headers});const t=await r.text();if(o.text)return t;let j;try{j=JSON.parse(t)}catch{throw Error('HTTP '+r.status+': '+t.slice(0,2000))}if(!r.ok||j.ok===false&&action!=='hot-run'){const e=Error(j.error||j.detail||JSON.stringify(j));e.data=j;e.status=r.status;throw e}return j}
async function load(p=cwd){cwd=p||='/';$('path').value=cwd;const j=await req('list',{q:{path:cwd}});$('files').innerHTML='';for(const e of j.entries){const d=document.createElement('div');d.className='e';d.textContent=(e.kind==='dir'?'📁 ':'📄 ')+e.name+' · '+e.kind+' · '+e.size+' B';d.onclick=()=>e.kind==='dir'?load(e.path):openFile(e.path);$('files').appendChild(d)}$('status').textContent=j.entries.length+' entries · '+j.path}
async function openFile(p){sel=p;$('sel').textContent=p;const j=await req('read',{q:{path:p}});$('ed').value=j.text}
function setUploadProgress(name,done,total,msg){$('uploadName').textContent=name||'';$('uploadFill').style.width=(total?Math.min(100,(done/total)*100):0)+'%';$('uploadStatus').textContent=msg||''}
async function uploadFile(file){let conflict='ask',init;while(true){try{init=await req('upload-init',{method:'POST',auth:true,q:{path:cwd,name:file.name,size:String(file.size),conflict}});break}catch(e){if(e.status===409&&e.data&&e.data.code==='UPLOAD_EXISTS'){const replace=confirm(file.name+' already exists in '+cwd+'.\n\nOK = Replace\nCancel = choose automatic rename');conflict=replace?'replace':'rename';continue}throw e}}
const uploadId=init.uploadId,instanceId=init.instanceId,target=init.path;let offset=0;setUploadProgress(file.name,0,file.size,'Starting · '+target);while(offset<file.size){const end=Math.min(offset+CHUNK,file.size);const blob=file.slice(offset,end);const j=await req('upload-chunk',{method:'POST',auth:true,q:{uploadId,offset:String(offset),instanceId},body:blob,headers:{'content-type':'application/octet-stream'}});offset=j.received;setUploadProgress(file.name,offset,file.size,Math.floor((offset/file.size)*100)+'% · '+offset+' / '+file.size+' bytes')}const done=await req('upload-finish',{method:'POST',auth:true,q:{uploadId,instanceId}});setUploadProgress(file.name,file.size,file.size,'DONE · '+done.path+' · sha256 '+done.sha256);return done}
async function uploadSelected(files){if(uploadBusy||!files.length)return;if(!adminToken){alert('Set the SWRLZ_ADMIN_TOKEN upload auth first.');return}if(!(cwd==='/tmp/swrlz-admin'||cwd.startsWith('/tmp/swrlz-admin/'))){alert('Uploads are restricted to /tmp/swrlz-admin and its subdirectories.');return}uploadBusy=true;$('uploadPick').disabled=true;try{for(const f of files)await uploadFile(f);await load(cwd)}catch(e){setUploadProgress('',0,1,'UPLOAD FAILED · '+e.message);alert('Upload failed: '+e.message)}finally{uploadBusy=false;$('uploadPick').disabled=false;$('fileInput').value=''}}
$('rememberToken').onclick=()=>{adminToken=$('uploadToken').value.trim();if(adminToken)sessionStorage.setItem('swrlzAdminUploadToken',adminToken);else sessionStorage.removeItem('swrlzAdminUploadToken');$('uploadStatus').textContent=adminToken?'Upload auth set for this browser session.':'Upload auth cleared.'};$('uploadPick').onclick=()=>$('fileInput').click();$('fileInput').onchange=()=>uploadSelected([...$('fileInput').files]);
$('up').onclick=()=>{let p=cwd.replace(/\/+$/,'');if(!p||p==='/')return load('/');let i=p.lastIndexOf('/');load(i<=0?'/':p.slice(0,i))};$('go').onclick=()=>load($('path').value);$('refresh').onclick=()=>load(cwd);$('rt').onclick=async()=>{$('runout').textContent=JSON.stringify(await req('runtime'),null,2)};$('hot').onclick=async()=>{$('runout').textContent='Running…';try{$('runout').textContent=JSON.stringify(await req('hot-run',{method:'POST'}),null,2)}catch(e){$('runout').textContent=String(e)}};$('openhot').onclick=()=>openFile('/tmp/swrlz-admin/live/gate5_live.py');$('logbtn').onclick=()=>openFile('/tmp/swrlz-admin/logs/full-runtime.log');$('save').onclick=async()=>{if(!sel)return;await req('save',{method:'POST',q:{path:sel},body:$('ed').value,headers:{'content-type':'text/plain;charset=utf-8'}});alert('Saved live — no redeploy required.')};$('download').onclick=()=>{if(sel)location.href='/api/admin?'+new URLSearchParams({action:'download',path:sel})};load();
</script></body></html>'''


@app.get("/")
@app.get("/api/admin")
def admin_get(action: str | None = Query(default=None), path: str | None = Query(default=None)):
    if not action:
        return HTMLResponse(PAGE)
    p = path_of(path)
    try:
        if action == "runtime":
            return runtime()
        if action == "list":
            if not p.exists():
                return JSONResponse(status_code=404, content={"ok": False, "error": "path does not exist", "path": str(p)})
            if not p.is_dir():
                return JSONResponse(status_code=400, content={"ok": False, "error": "not a directory", "path": str(p)})
            es = []
            for i, c in enumerate(sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))):
                if i >= MAX_LIST:
                    break
                try:
                    es.append(entry(c))
                except Exception as e:
                    es.append({"name": c.name, "path": str(c), "kind": "error", "error": str(e)})
            return {"ok": True, "path": str(p), "parent": str(p.parent), "breadcrumbs": crumbs(p), "entries": es}
        if action == "read":
            if not p.is_file():
                return JSONResponse(status_code=404, content={"ok": False, "error": "not a file", "path": str(p)})
            if p.stat().st_size > MAX_TEXT:
                return JSONResponse(status_code=413, content={"ok": False, "error": "preview too large", "size": p.stat().st_size})
            raw = p.read_bytes()
            if b"\0" in raw[:8192]:
                return JSONResponse(status_code=415, content={"ok": False, "error": "binary file"})
            return {"ok": True, "path": str(p), "size": len(raw), "text": raw.decode("utf-8", "replace")}
        if action == "download":
            if not p.is_file():
                return JSONResponse(status_code=404, content={"ok": False, "error": "not a file"})
            mt, _ = mimetypes.guess_type(str(p))
            return FileResponse(str(p), media_type=mt or "application/octet-stream", filename=p.name)
        if action == "log":
            txt = FULL_LOG.read_text("utf-8", "replace") if FULL_LOG.exists() else ""
            return PlainTextResponse(txt)
        return JSONResponse(status_code=400, content={"ok": False, "error": "unknown action", "action": action})
    except Exception as e:
        log("get-error", action=action, path=str(p), error=f"{type(e).__name__}: {e}")
        return JSONResponse(status_code=500, content={"ok": False, "error": f"{type(e).__name__}: {e}", "instanceId": INSTANCE_ID})


@app.post("/")
@app.post("/api/admin")
async def admin_post(
    request: Request,
    action: str = Query(...),
    path: str | None = Query(default=None),
    name: str | None = Query(default=None),
    size: int | None = Query(default=None),
    conflict: str = Query(default="ask"),
    uploadId: str | None = Query(default=None),
    offset: int = Query(default=0),
    instanceId: str | None = Query(default=None),
):
    p = path_of(path)
    try:
        if action == "save":
            body = await request.body(); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(body); log("save", path=str(p), size=len(body), sha256=hashlib.sha256(body).hexdigest()); return {"ok": True, "path": str(p), "size": len(body), "instanceId": INSTANCE_ID}
        if action == "hot-run":
            result = run_hot(); return JSONResponse(status_code=200 if result.get("ok") else 500, content=result)
        if action.startswith("upload-"):
            auth_error = require_upload_auth(request)
            if auth_error is not None:
                return auth_error
        if action == "upload-init":
            if name is None or size is None or size < 0:
                return JSONResponse(status_code=400, content={"ok": False, "error": "name and non-negative size are required"})
            target = upload_destination(path, name)
            if target.exists():
                if conflict == "replace":
                    if target.is_dir():
                        return JSONResponse(status_code=409, content={"ok": False, "error": "destination is a directory", "code": "UPLOAD_EXISTS"})
                elif conflict == "rename":
                    target = unique_destination(target)
                else:
                    return JSONResponse(status_code=409, content={"ok": False, "error": "destination already exists", "code": "UPLOAD_EXISTS", "path": str(target), "size": target.stat().st_size if target.is_file() else None})
            upload_id = uuid.uuid4().hex
            part = UPLOADS / f"{upload_id}.part"
            part.unlink(missing_ok=True)
            part.touch()
            meta = {"uploadId": upload_id, "instanceId": INSTANCE_ID, "target": str(target), "part": str(part), "expected": size, "received": 0, "created": now()}
            save_upload(upload_id, meta)
            log("upload-init", uploadId=upload_id, target=str(target), expected=size)
            return {"ok": True, "uploadId": upload_id, "instanceId": INSTANCE_ID, "path": str(target), "expected": size, "chunkBytes": MAX_UPLOAD_CHUNK}
        if action == "upload-chunk":
            if not uploadId:
                return JSONResponse(status_code=400, content={"ok": False, "error": "uploadId is required"})
            if instanceId != INSTANCE_ID:
                return JSONResponse(status_code=409, content={"ok": False, "error": "Vercel routed this chunk to a different runtime instance; retry the upload", "code": "INSTANCE_CHANGED", "expectedInstanceId": instanceId, "actualInstanceId": INSTANCE_ID})
            meta = load_upload(uploadId)
            if meta.get("instanceId") != INSTANCE_ID:
                return JSONResponse(status_code=409, content={"ok": False, "error": "upload session belongs to another runtime instance", "code": "INSTANCE_CHANGED"})
            body = await request.body()
            if len(body) > MAX_UPLOAD_CHUNK:
                return JSONResponse(status_code=413, content={"ok": False, "error": "upload chunk too large", "maxChunkBytes": MAX_UPLOAD_CHUNK})
            part = Path(meta["part"])
            received = int(meta.get("received", 0))
            if offset != received:
                return JSONResponse(status_code=409, content={"ok": False, "error": "upload offset mismatch", "code": "OFFSET_MISMATCH", "received": received})
            expected = int(meta["expected"])
            if received + len(body) > expected:
                return JSONResponse(status_code=400, content={"ok": False, "error": "chunk exceeds declared upload size"})
            with part.open("ab") as f:
                f.write(body)
            received += len(body)
            meta["received"] = received
            save_upload(uploadId, meta)
            return {"ok": True, "uploadId": uploadId, "received": received, "expected": expected, "instanceId": INSTANCE_ID}
        if action == "upload-finish":
            if not uploadId:
                return JSONResponse(status_code=400, content={"ok": False, "error": "uploadId is required"})
            if instanceId != INSTANCE_ID:
                return JSONResponse(status_code=409, content={"ok": False, "error": "Vercel routed finalization to a different runtime instance; retry the upload", "code": "INSTANCE_CHANGED"})
            meta = load_upload(uploadId)
            part = Path(meta["part"])
            target = Path(meta["target"])
            expected = int(meta["expected"])
            received = int(meta.get("received", 0))
            if received != expected or not part.is_file() or part.stat().st_size != expected:
                return JSONResponse(status_code=409, content={"ok": False, "error": "upload is incomplete", "code": "UPLOAD_INCOMPLETE", "received": received, "expected": expected})
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(part, target)
            h = hashlib.sha256()
            with target.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            digest = h.hexdigest()
            upload_meta(uploadId).unlink(missing_ok=True)
            log("upload-finish", uploadId=uploadId, target=str(target), size=expected, sha256=digest)
            return {"ok": True, "path": str(target), "size": expected, "sha256": digest, "instanceId": INSTANCE_ID}
        if action == "upload-cancel":
            if not uploadId:
                return JSONResponse(status_code=400, content={"ok": False, "error": "uploadId is required"})
            meta = load_upload(uploadId)
            Path(meta["part"]).unlink(missing_ok=True)
            upload_meta(uploadId).unlink(missing_ok=True)
            log("upload-cancel", uploadId=uploadId)
            return {"ok": True, "uploadId": uploadId, "instanceId": INSTANCE_ID}
        return JSONResponse(status_code=400, content={"ok": False, "error": "unknown action", "action": action})
    except Exception as e:
        log("post-error", action=action, path=str(p), error=f"{type(e).__name__}: {e}")
        return JSONResponse(status_code=500, content={"ok": False, "error": f"{type(e).__name__}: {e}", "instanceId": INSTANCE_ID})


log("workbench-import", version="1.1.0", hotScript=str(HOT_GATE5), uploadAuthConfigured=bool(ADMIN_TOKEN))
