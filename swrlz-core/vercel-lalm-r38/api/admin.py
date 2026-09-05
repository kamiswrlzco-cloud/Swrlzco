from __future__ import annotations

import hashlib
import mimetypes
import os
import platform
import shutil
import stat
import sys
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

app = FastAPI(title="§wyrlz Runtime Admin", version="0.2.0")

ADMIN_ROOT = Path("/tmp/swrlz-admin")
MAX_LIST_ENTRIES = 1500
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_HASH_BYTES = 512 * 1024 * 1024


def _ensure_workspace() -> None:
    for p in (ADMIN_ROOT, ADMIN_ROOT / "logs", ADMIN_ROOT / "uploads", ADMIN_ROOT / "pages"):
        p.mkdir(parents=True, exist_ok=True)


def _path(raw: str | None) -> Path:
    if not raw:
        return ADMIN_ROOT
    p = Path(raw)
    return p if p.is_absolute() else Path("/") / p


def _err(message: str, status: int = 400, **extra):
    return JSONResponse(status_code=status, content={"ok": False, "error": message, **extra})


def _safe(label: str, fn):
    try:
        return fn()
    except Exception as exc:
        return {"error": f"{label}: {type(exc).__name__}: {exc}"}


def _entry(p: Path) -> dict:
    try:
        st = p.lstat()
        is_link = p.is_symlink()
        is_dir = p.is_dir()
        is_file = p.is_file()
        return {
            "name": p.name or "/",
            "path": str(p),
            "kind": "dir" if is_dir else "file" if is_file else "link" if is_link else "other",
            "size": int(st.st_size),
            "mtime": float(st.st_mtime),
            "mode": stat.filemode(st.st_mode),
            "uid": getattr(st, "st_uid", None),
            "gid": getattr(st, "st_gid", None),
            "readable": os.access(p, os.R_OK),
            "writable": os.access(p, os.W_OK),
            "executable": os.access(p, os.X_OK),
            "symlinkTarget": os.readlink(p) if is_link else None,
        }
    except Exception as exc:
        return {"name": p.name or str(p), "path": str(p), "kind": "error", "error": f"{type(exc).__name__}: {exc}"}


def _breadcrumbs(p: Path):
    crumbs = [{"name": "/", "path": "/"}]
    cur = Path("/")
    for part in p.parts[1:]:
        cur /= part
        crumbs.append({"name": part, "path": str(cur)})
    return crumbs


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    seen = 0
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            seen += len(chunk)
            if seen > MAX_HASH_BYTES:
                raise ValueError(f"hash limit exceeded ({MAX_HASH_BYTES} bytes)")
            h.update(chunk)
    return h.hexdigest()


def _runtime_info() -> dict:
    _ensure_workspace()
    disk_root = _safe("diskRoot", lambda: shutil.disk_usage("/"))
    disk_tmp = _safe("diskTmp", lambda: shutil.disk_usage("/tmp"))
    load = _safe("loadAverage", lambda: list(os.getloadavg()))
    peak = None
    try:
        import resource
        raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak = int(raw * 1024 if sys.platform != "darwin" else raw)
    except Exception as exc:
        peak = {"error": f"resource: {type(exc).__name__}: {exc}"}
    def disk_json(v):
        if isinstance(v, dict):
            return v
        return {"total": int(v.total), "used": int(v.used), "free": int(v.free)}
    return {
        "ok": True,
        "service": "§wyrlz Runtime Admin",
        "version": "0.2.0",
        "python": sys.version.split()[0],
        "platform": _safe("platform", platform.platform),
        "machine": _safe("machine", platform.machine),
        "processor": _safe("processor", platform.processor),
        "cpuCount": os.cpu_count(),
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "loadAverage": load,
        "processPeakRssBytes": peak,
        "diskRoot": disk_json(disk_root),
        "diskTmp": disk_json(disk_tmp),
        "adminRoot": str(ADMIN_ROOT),
        "quickPaths": ["/tmp/swrlz-admin", "/tmp/swrlz-admin/logs", "/tmp/swrlz-admin/uploads", "/tmp/swrlz-admin/pages", "/tmp", "/var/task", os.getcwd(), "/"],
        "note": "Vercel /tmp is ephemeral and may be isolated per function instance. Files exported by another api/*.py function are not guaranteed to appear here.",
    }


PAGE = r'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>§wyrlz Runtime Admin</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font-family:system-ui;background:#090c12;color:#edf5ff;margin:0 auto;padding:16px;max-width:1180px}h1{font-size:clamp(32px,7vw,52px);margin:4px 0}.warn{background:#3a2505;border:1px solid #d49a24;color:#ffd985;padding:12px;border-radius:12px;font-weight:800}.panel{background:#121826;border:1px solid #26344d;border-radius:16px;padding:14px;margin:12px 0}.row{display:flex;gap:9px;flex-wrap:wrap;align-items:center}.grow{flex:1;min-width:180px}input,textarea{width:100%;background:#0c1220;color:#fff;border:1px solid #53627d;border-radius:10px;padding:10px;font:inherit}button{background:#e8edf7;color:#08101c;border:0;border-radius:10px;padding:10px 13px;font-weight:800}button.alt{background:#1d2a3f;color:#dff8ff;border:1px solid #36506f}button.danger{background:#5b1821;color:#ffdce0}.grid{display:grid;grid-template-columns:minmax(300px,.9fr) minmax(340px,1.1fr);gap:12px}@media(max-width:820px){.grid{grid-template-columns:1fr}}.filelist{max-height:520px;overflow:auto;border:1px solid #26344d;border-radius:12px}.entry{display:grid;grid-template-columns:34px 1fr auto;gap:8px;padding:10px;border-bottom:1px solid #202a3c;cursor:pointer}.entry:hover{background:#182235}.name{font-weight:800;word-break:break-all}.meta,.muted{font-size:12px;color:#9eb0c9}.path{font-family:ui-monospace,monospace;color:#7ee7ff;word-break:break-all}textarea{min-height:330px;font-family:ui-monospace,monospace;font-size:13px}pre{background:#0c1220;border:1px solid #26344d;border-radius:12px;padding:12px;overflow:auto;white-space:pre-wrap}.bad{color:#ff9292}.ok{color:#80ffad}</style></head><body>
<h1>§wyrlz Runtime Admin</h1><div class="warn">⚠ PRE-TEST ADMIN · PUBLIC / UNAUTHENTICATED · /tmp is ephemeral and may be per-function</div>
<div class="panel"><div class="row"><input id="path" class="grow" value="/tmp/swrlz-admin"><button id="go">GO</button><button id="refresh" class="alt">REFRESH</button><button id="runtime" class="alt">RUNTIME</button></div><div id="quick" class="row" style="margin-top:9px"></div><div id="crumbs" class="row" style="margin-top:9px"></div></div>
<div class="grid"><div class="panel"><div class="row"><h2 class="grow">Files</h2><button id="newFolder" class="alt">NEW FOLDER</button><button id="newFile" class="alt">NEW FILE</button></div><div class="row"><input id="uploadFile" type="file" class="grow"><button id="upload">UPLOAD</button></div><p id="listStatus" class="muted">Loading…</p><div id="files" class="filelist"></div></div>
<div class="panel"><div class="row"><h2 class="grow">Viewer / Editor</h2><button id="download" class="alt">DOWNLOAD</button><button id="hash" class="alt">SHA-256</button></div><div id="selected" class="path">No file selected.</div><div class="row" style="margin:8px 0"><button id="save">SAVE TEXT</button><button id="rename" class="alt">RENAME</button><button id="del" class="danger">DELETE</button></div><textarea id="editor" spellcheck="false"></textarea><pre id="detail">Ready.</pre></div></div>
<div class="panel"><h2>Operation Log</h2><div class="row"><button id="clearLog" class="alt">CLEAR</button><button id="exportLog">EXPORT LOG TO SERVER</button><button id="downloadLog" class="alt">DOWNLOAD LOG TO PHONE</button></div><textarea id="log" readonly style="min-height:220px"></textarea><p id="logStatus" class="muted"></p></div>
<script>
const $=id=>document.getElementById(id);let cwd='/tmp/swrlz-admin',selected=null;const log=(m,d)=>{let s=`[${new Date().toISOString()}] ${m}`;if(d!==undefined)s+='\n'+(typeof d==='string'?d:JSON.stringify(d,null,2));$('log').value+=( $('log').value?'\n':'')+s+'\n';$('log').scrollTop=$('log').scrollHeight};
async function req(action,opts={}){const q=new URLSearchParams({action,...(opts.q||{})});const r=await fetch('/api/admin?'+q,{method:opts.method||'GET',body:opts.body,headers:opts.headers||{}});const raw=await r.text();let j;try{j=JSON.parse(raw)}catch{throw new Error(`HTTP ${r.status} ${r.statusText}\n${raw.slice(0,2000)}`)}if(!r.ok||j.ok===false)throw new Error(j.error||j.detail||JSON.stringify(j));return j}
const fmt=n=>{const u=['B','KB','MB','GB'];let x=Number(n||0),i=0;while(x>=1024&&i<u.length-1){x/=1024;i++}return `${x.toFixed(i?1:0)} ${u[i]}`};const icon=k=>k==='dir'?'📁':k==='file'?'📄':k==='link'?'🔗':'❓';
async function load(p=cwd){cwd=p;$('path').value=p;$('listStatus').textContent='Loading…';try{const j=await req('list',{q:{path:p}});cwd=j.path;$('path').value=cwd;$('files').innerHTML='';for(const e of j.entries){const d=document.createElement('div');d.className='entry';d.innerHTML=`<div>${icon(e.kind)}</div><div><div class="name"></div><div class="meta">${e.kind} · ${fmt(e.size)} · ${e.mode||''}</div></div><div class="meta">${e.writable?'W':'R'}</div>`;d.querySelector('.name').textContent=e.name;d.onclick=()=>e.kind==='dir'?load(e.path):openFile(e);$('files').appendChild(d)}$('crumbs').innerHTML='';for(const c of j.breadcrumbs){const b=document.createElement('button');b.className='alt';b.textContent=c.name;b.onclick=()=>load(c.path);$('crumbs').appendChild(b)}$('listStatus').textContent=`${j.entries.length} entries · ${cwd}`;$('listStatus').className='muted';log('LIST '+cwd,{count:j.entries.length})}catch(e){$('listStatus').textContent=e.message;$('listStatus').className='bad';log('LIST FAILED '+p,e.message)}}
async function openFile(e){selected=e;$('selected').textContent=e.path;$('detail').textContent=JSON.stringify(e,null,2);try{const j=await req('read',{q:{path:e.path}});$('editor').value=j.text;$('detail').textContent=JSON.stringify(j,null,2);log('READ '+e.path,{size:j.size})}catch(x){$('editor').value='';$('detail').textContent=x.message;log('READ FAILED '+e.path,x.message)}}
$('runtime').onclick=async()=>{try{const j=await req('runtime');$('detail').textContent=JSON.stringify(j,null,2);$('quick').innerHTML='';for(const p of j.quickPaths){const b=document.createElement('button');b.className='alt';b.textContent=p;b.onclick=()=>load(p);$('quick').appendChild(b)}log('RUNTIME',j)}catch(e){$('detail').textContent=e.message;log('RUNTIME FAILED',e.message)}};$('go').onclick=()=>load($('path').value);$('refresh').onclick=()=>load(cwd);
$('save').onclick=async()=>{if(!selected)return alert('Select a file');try{const j=await req('save',{method:'POST',q:{path:selected.path},body:$('editor').value,headers:{'content-type':'text/plain;charset=utf-8'}});log('SAVE '+selected.path,j);await load(cwd)}catch(e){alert(e.message);log('SAVE FAILED',e.message)}};$('upload').onclick=async()=>{const f=$('uploadFile').files[0];if(!f)return alert('Choose a file');try{const j=await req('upload',{method:'POST',q:{path:cwd,name:f.name},body:f,headers:{'content-type':'application/octet-stream'}});log('UPLOAD '+f.name,j);await load(cwd)}catch(e){alert(e.message);log('UPLOAD FAILED',e.message)}};
$('download').onclick=()=>{if(selected)location.href='/api/admin?'+new URLSearchParams({action:'download',path:selected.path})};$('hash').onclick=async()=>{if(!selected)return alert('Select a file');try{const j=await req('hash',{q:{path:selected.path}});$('detail').textContent=JSON.stringify(j,null,2);log('HASH',j)}catch(e){log('HASH FAILED',e.message)}};$('newFolder').onclick=async()=>{const n=prompt('Folder name');if(!n)return;try{await req('mkdir',{method:'POST',q:{path:cwd,name:n}});await load(cwd)}catch(e){alert(e.message)}};$('newFile').onclick=async()=>{const n=prompt('File name');if(!n)return;try{await req('new-file',{method:'POST',q:{path:cwd,name:n}});await load(cwd)}catch(e){alert(e.message)}};$('rename').onclick=async()=>{if(!selected)return alert('Select a file');const n=prompt('New name',selected.name);if(!n)return;try{await req('rename',{method:'POST',q:{path:selected.path,name:n}});await load(cwd)}catch(e){alert(e.message)}};$('del').onclick=async()=>{if(!selected||!confirm('Delete '+selected.path+'?'))return;try{await req('delete',{method:'POST',q:{path:selected.path}});selected=null;await load(cwd)}catch(e){alert(e.message)}};
$('clearLog').onclick=()=>{$('log').value=''};$('exportLog').onclick=async()=>{try{const j=await req('export-log',{method:'POST',body:$('log').value,headers:{'content-type':'text/plain;charset=utf-8'}});$('logStatus').textContent='Saved: '+j.path;log('LOG EXPORTED',j)}catch(e){$('logStatus').textContent=e.message;log('LOG EXPORT FAILED',e.message)}};$('downloadLog').onclick=()=>{const b=new Blob([$('log').value],{type:'text/plain'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='swrlz-admin-'+new Date().toISOString().replace(/[:.]/g,'-')+'.log';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};(async()=>{await $('runtime').onclick();await load(cwd)})();
</script></body></html>'''


def _get(action: str | None, path: str | None):
    try:
        _ensure_workspace()
        if not action:
            return HTMLResponse(PAGE)
        p = _path(path)
        if action == "runtime":
            return _runtime_info()
        if action == "list":
            if not p.exists(): return _err("path does not exist", 404, path=str(p))
            if not p.is_dir(): return _err("path is not a directory", 400, path=str(p))
            entries = []
            for child in p.iterdir():
                entries.append(_entry(child))
                if len(entries) >= MAX_LIST_ENTRIES: break
            entries.sort(key=lambda e: (e.get("kind") != "dir", str(e.get("name", "")).lower()))
            return {"ok": True, "path": str(p), "entries": entries, "breadcrumbs": _breadcrumbs(p), "truncated": len(entries) >= MAX_LIST_ENTRIES}
        if action == "read":
            if not p.is_file(): return _err("not a file", 400, path=str(p))
            size = p.stat().st_size
            if size > MAX_TEXT_BYTES: return _err("text preview too large", 413, path=str(p), size=size)
            raw = p.read_bytes()
            if b"\0" in raw[:8192]: return _err("binary file; use download", 415, path=str(p), size=size)
            return {"ok": True, "path": str(p), "size": size, "text": raw.decode("utf-8", "replace"), "info": _entry(p)}
        if action == "download":
            if not p.is_file(): return _err("not a file", 404, path=str(p))
            mime, _ = mimetypes.guess_type(str(p))
            return FileResponse(str(p), media_type=mime or "application/octet-stream", filename=p.name)
        if action == "hash":
            if not p.is_file(): return _err("not a file", 400, path=str(p))
            return {"ok": True, "path": str(p), "size": p.stat().st_size, "sha256": _sha256(p)}
        return _err("unknown action", 400, action=action)
    except Exception as exc:
        return _err(f"{type(exc).__name__}: {exc}", 500, action=action, path=path)


async def _post(request: Request, action: str, path: str | None, name: str | None):
    try:
        _ensure_workspace()
        p = _path(path)
        body = await request.body()
        if action == "save":
            if not p.is_file(): return _err("target is not an existing file", 400, path=str(p))
            p.write_bytes(body); return {"ok": True, "path": str(p), "size": len(body)}
        if action == "upload":
            if not name or not p.is_dir(): return _err("valid directory path and name required", 400)
            t = p / Path(name).name; t.write_bytes(body); return {"ok": True, "path": str(t), "size": len(body)}
        if action == "mkdir":
            if not name: return _err("name required"); t = p / Path(name).name; t.mkdir(exist_ok=False); return {"ok": True, "path": str(t)}
        if action == "new-file":
            if not name: return _err("name required"); t = p / Path(name).name; t.touch(exist_ok=False); return {"ok": True, "path": str(t)}
        if action == "rename":
            if not name: return _err("name required"); t = p.with_name(Path(name).name); p.rename(t); return {"ok": True, "from": str(p), "path": str(t)}
        if action == "delete":
            if p.is_dir() and not p.is_symlink(): shutil.rmtree(p)
            else: p.unlink()
            return {"ok": True, "deleted": str(p)}
        if action == "export-log":
            t = ADMIN_ROOT / "logs" / f"admin-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}-{uuid.uuid4().hex[:6]}.log"; t.write_bytes(body); return {"ok": True, "path": str(t), "size": len(body)}
        return _err("unknown action", 400, action=action)
    except Exception as exc:
        return _err(f"{type(exc).__name__}: {exc}", 500, action=action, path=path)


@app.get("/")
@app.get("/api/admin")
def admin_get(action: str | None = Query(default=None), path: str | None = Query(default=None)):
    return _get(action, path)


@app.post("/")
@app.post("/api/admin")
async def admin_post(request: Request, action: str = Query(...), path: str | None = Query(default=None), name: str | None = Query(default=None)):
    return await _post(request, action, path, name)
