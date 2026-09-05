from __future__ import annotations

import hashlib
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

app = FastAPI(title="§wyrlz Live Runtime Workbench", version="1.0.0")

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
    p=Path(raw)
    return p if p.is_absolute() else ROOT/p


def entry(p: Path) -> dict:
    st=p.lstat()
    kind="dir" if p.is_dir() else "file" if p.is_file() else "link" if p.is_symlink() else "other"
    return {"name":p.name or "/","path":str(p),"kind":kind,"size":st.st_size,"mtime":st.st_mtime,"mode":stat.filemode(st.st_mode),"readable":os.access(p,os.R_OK),"writable":os.access(p,os.W_OK)}


def runtime() -> dict:
    def disk(p):
        try:
            d=shutil.disk_usage(p); return {"total":d.total,"used":d.used,"free":d.free}
        except Exception as e:return {"error":f"{type(e).__name__}: {e}"}
    rss=None
    try:
        import resource
        r=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss=int(r*1024 if sys.platform!="darwin" else r)
    except Exception: pass
    return {"ok":True,"instanceId":INSTANCE_ID,"python":sys.version.split()[0],"platform":platform.platform(),"machine":platform.machine(),"cpuCount":os.cpu_count(),"pid":os.getpid(),"cwd":os.getcwd(),"peakRssBytes":rss,"diskRoot":disk("/"),"diskTmp":disk("/tmp"),"root":str(ROOT),"hotScript":str(HOT_GATE5),"fullLog":str(FULL_LOG),"note":"/tmp is writable and hot-editable but ephemeral and instance-local on Vercel."}


def crumbs(p: Path):
    out=[{"name":"/","path":"/"}]; cur=Path("/")
    for part in p.parts[1:]:
        cur/=part; out.append({"name":part,"path":str(cur)})
    return out


def run_hot(timeout_s: int=45) -> dict:
    started=time.monotonic()
    log("hot-run-start", script=str(HOT_GATE5), timeout=timeout_s)
    try:
        cp=subprocess.run([sys.executable,"-u",str(HOT_GATE5)],capture_output=True,text=True,timeout=timeout_s,cwd=str(LIVE),env={**os.environ,"PYTHONUNBUFFERED":"1"})
        result={"ok":cp.returncode==0,"returnCode":cp.returncode,"stdout":cp.stdout[-200000:],"stderr":cp.stderr[-200000:],"elapsedMs":int((time.monotonic()-started)*1000),"instanceId":INSTANCE_ID}
        log("hot-run-end", returnCode=cp.returncode, elapsedMs=result["elapsedMs"], stdout=result["stdout"], stderr=result["stderr"])
        return result
    except subprocess.TimeoutExpired as e:
        out=e.stdout.decode() if isinstance(e.stdout,bytes) else (e.stdout or "")
        err=e.stderr.decode() if isinstance(e.stderr,bytes) else (e.stderr or "")
        result={"ok":False,"timeout":True,"stdout":out[-200000:],"stderr":err[-200000:],"elapsedMs":int((time.monotonic()-started)*1000),"instanceId":INSTANCE_ID}
        log("hot-run-timeout", elapsedMs=result["elapsedMs"], stdout=result["stdout"], stderr=result["stderr"])
        return result

PAGE = r'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>§wyrlz Live Workbench</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font-family:system-ui;background:#080b10;color:#eef5ff;margin:0 auto;padding:16px;max-width:1100px}.p{background:#121826;border:1px solid #293750;border-radius:16px;padding:14px;margin:12px 0}.r{display:flex;gap:9px;flex-wrap:wrap;align-items:center}button{padding:11px 14px;border-radius:10px;border:0;font-weight:800}button.alt{background:#1d2a3f;color:#dff8ff;border:1px solid #36506f}input,textarea{width:100%;background:#0b1120;color:#fff;border:1px solid #53627d;border-radius:10px;padding:10px;font:inherit}.grow{flex:1;min-width:180px}.files{max-height:430px;overflow:auto}.e{padding:9px;border-bottom:1px solid #26344d;cursor:pointer}.e:hover{background:#182235}textarea{min-height:300px;font-family:ui-monospace,monospace}pre{white-space:pre-wrap;overflow:auto;background:#0b1120;padding:12px;border-radius:10px}.warn{color:#ffd166}.ok{color:#80ffad}.bad{color:#ff9292}</style></head><body>
<h1>§wyrlz Live Workbench</h1><div class="p warn">One deployed shell, then edit/run diagnostics from writable /tmp without a redeploy. Vercel can recycle the instance, so /tmp is not permanent.</div>
<div class="p"><div class="r"><button id="up" class="alt">⬆ UP ONE DIR</button><input id="path" class="grow" value="/tmp/swrlz-admin"><button id="go">GO</button><button id="refresh" class="alt">REFRESH</button><button id="rt" class="alt">RUNTIME</button></div><div id="status"></div></div>
<div class="p"><div class="r"><button id="hot">🔥 RUN HOT GATE 5</button><button id="openhot" class="alt">OPEN HOT SCRIPT</button><button id="logbtn" class="alt">OPEN FULL LOG</button><a href="/api/admin?action=log" target="_blank"><button class="alt">RAW FULL LOG</button></a></div><pre id="runout">Ready.</pre></div>
<div class="p"><h2>Files</h2><div id="files" class="files"></div></div>
<div class="p"><h2>Editor</h2><div id="sel"></div><div class="r"><button id="save">SAVE LIVE FILE</button><button id="download" class="alt">DOWNLOAD</button></div><textarea id="ed"></textarea></div>
<script>
const $=x=>document.getElementById(x);let cwd='/tmp/swrlz-admin',sel=null;async function req(action,o={}){const q=new URLSearchParams({action,...(o.q||{})});const r=await fetch('/api/admin?'+q,{method:o.method||'GET',body:o.body,headers:o.headers||{}});const t=await r.text();if(o.text)return t;let j;try{j=JSON.parse(t)}catch{throw Error('HTTP '+r.status+': '+t.slice(0,2000))}if(!r.ok||j.ok===false&&action!=='hot-run')throw Error(j.error||j.detail||JSON.stringify(j));return j}
async function load(p=cwd){cwd=p||'/';$('path').value=cwd;const j=await req('list',{q:{path:cwd}});$('files').innerHTML='';for(const e of j.entries){const d=document.createElement('div');d.className='e';d.textContent=(e.kind==='dir'?'📁 ':'📄 ')+e.name+' · '+e.kind+' · '+e.size+' B';d.onclick=()=>e.kind==='dir'?load(e.path):openFile(e.path);$('files').appendChild(d)}$('status').textContent=j.entries.length+' entries · '+j.path}
async function openFile(p){sel=p;$('sel').textContent=p;const j=await req('read',{q:{path:p}});$('ed').value=j.text}
$('up').onclick=()=>{let p=cwd.replace(/\/+$/,'');if(!p||p==='/')return load('/');let i=p.lastIndexOf('/');load(i<=0?'/':p.slice(0,i))};$('go').onclick=()=>load($('path').value);$('refresh').onclick=()=>load(cwd);$('rt').onclick=async()=>{$('runout').textContent=JSON.stringify(await req('runtime'),null,2)};$('hot').onclick=async()=>{$('runout').textContent='Running…';try{$('runout').textContent=JSON.stringify(await req('hot-run',{method:'POST'}),null,2)}catch(e){$('runout').textContent=String(e)}};$('openhot').onclick=()=>openFile('/tmp/swrlz-admin/live/gate5_live.py');$('logbtn').onclick=()=>openFile('/tmp/swrlz-admin/logs/full-runtime.log');$('save').onclick=async()=>{if(!sel)return;await req('save',{method:'POST',q:{path:sel},body:$('ed').value,headers:{'content-type':'text/plain;charset=utf-8'}});alert('Saved live — no redeploy required.')};$('download').onclick=()=>{if(sel)location.href='/api/admin?'+new URLSearchParams({action:'download',path:sel})};load();
</script></body></html>'''

@app.get("/")
@app.get("/api/admin")
def admin_get(action: str|None=Query(default=None), path: str|None=Query(default=None)):
    if not action:return HTMLResponse(PAGE)
    p=path_of(path)
    try:
        if action=="runtime": return runtime()
        if action=="list":
            if not p.exists(): return JSONResponse(status_code=404,content={"ok":False,"error":"path does not exist","path":str(p)})
            if not p.is_dir(): return JSONResponse(status_code=400,content={"ok":False,"error":"not a directory","path":str(p)})
            es=[]
            for i,c in enumerate(sorted(p.iterdir(),key=lambda x:(not x.is_dir(),x.name.lower()))):
                if i>=MAX_LIST:break
                try:es.append(entry(c))
                except Exception as e:es.append({"name":c.name,"path":str(c),"kind":"error","error":str(e)})
            return {"ok":True,"path":str(p),"parent":str(p.parent),"breadcrumbs":crumbs(p),"entries":es}
        if action=="read":
            if not p.is_file(): return JSONResponse(status_code=404,content={"ok":False,"error":"not a file","path":str(p)})
            if p.stat().st_size>MAX_TEXT:return JSONResponse(status_code=413,content={"ok":False,"error":"preview too large","size":p.stat().st_size})
            raw=p.read_bytes()
            if b"\0" in raw[:8192]:return JSONResponse(status_code=415,content={"ok":False,"error":"binary file"})
            return {"ok":True,"path":str(p),"size":len(raw),"text":raw.decode("utf-8","replace")}
        if action=="download":
            if not p.is_file():return JSONResponse(status_code=404,content={"ok":False,"error":"not a file"})
            mt,_=mimetypes.guess_type(str(p));return FileResponse(str(p),media_type=mt or "application/octet-stream",filename=p.name)
        if action=="log":
            txt=FULL_LOG.read_text("utf-8","replace") if FULL_LOG.exists() else ""
            return PlainTextResponse(txt)
        return JSONResponse(status_code=400,content={"ok":False,"error":"unknown action","action":action})
    except Exception as e:
        log("get-error",action=action,path=str(p),error=f"{type(e).__name__}: {e}")
        return JSONResponse(status_code=500,content={"ok":False,"error":f"{type(e).__name__}: {e}","instanceId":INSTANCE_ID})

@app.post("/")
@app.post("/api/admin")
async def admin_post(request:Request,action:str=Query(...),path:str|None=Query(default=None)):
    p=path_of(path)
    try:
        if action=="save":
            body=await request.body();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(body);log("save",path=str(p),size=len(body),sha256=hashlib.sha256(body).hexdigest());return {"ok":True,"path":str(p),"size":len(body),"instanceId":INSTANCE_ID}
        if action=="hot-run":
            result=run_hot();return JSONResponse(status_code=200 if result.get("ok") else 500,content=result)
        return JSONResponse(status_code=400,content={"ok":False,"error":"unknown action","action":action})
    except Exception as e:
        log("post-error",action=action,path=str(p),error=f"{type(e).__name__}: {e}")
        return JSONResponse(status_code=500,content={"ok":False,"error":f"{type(e).__name__}: {e}","instanceId":INSTANCE_ID})

log("workbench-import",version="1.0.0",hotScript=str(HOT_GATE5))
