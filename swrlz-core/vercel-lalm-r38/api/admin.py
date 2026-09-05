from __future__ import annotations

import hashlib
import json
import mimetypes
import os
import platform
import shutil
import stat
import sys
import time
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

app = FastAPI(title="§wyrlz Runtime Admin", version="0.1.0")

ADMIN_ROOT = Path("/tmp/swrlz-admin")
ADMIN_ROOT.mkdir(parents=True, exist_ok=True)
(ADMIN_ROOT / "logs").mkdir(parents=True, exist_ok=True)
(ADMIN_ROOT / "uploads").mkdir(parents=True, exist_ok=True)
(ADMIN_ROOT / "pages").mkdir(parents=True, exist_ok=True)

MAX_LIST_ENTRIES = 1000
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_HASH_BYTES = 512 * 1024 * 1024


def _path(raw: str | None) -> Path:
    if not raw:
        return Path("/")
    p = Path(raw)
    if not p.is_absolute():
        p = Path("/") / p
    return p


def _json_error(message: str, status: int = 400, **extra):
    return JSONResponse(status_code=status, content={"ok": False, "error": message, **extra})


def _fmt_mode(mode: int) -> str:
    try:
        return stat.filemode(mode)
    except Exception:
        return "??????????"


def _entry_info(p: Path) -> dict:
    try:
        st = p.lstat()
        is_link = p.is_symlink()
        is_dir = p.is_dir()
        is_file = p.is_file()
        kind = "dir" if is_dir else "file" if is_file else "link" if is_link else "other"
        target = None
        if is_link:
            try:
                target = os.readlink(p)
            except Exception:
                target = None
        return {
            "name": p.name or "/",
            "path": str(p),
            "kind": kind,
            "size": int(st.st_size),
            "mtime": float(st.st_mtime),
            "mode": _fmt_mode(st.st_mode),
            "uid": getattr(st, "st_uid", None),
            "gid": getattr(st, "st_gid", None),
            "symlinkTarget": target,
            "readable": os.access(p, os.R_OK),
            "writable": os.access(p, os.W_OK),
            "executable": os.access(p, os.X_OK),
        }
    except Exception as exc:
        return {"name": p.name, "path": str(p), "kind": "error", "error": f"{type(exc).__name__}: {exc}"}


def _breadcrumbs(p: Path) -> list[dict]:
    parts = p.parts
    crumbs = [{"name": "/", "path": "/"}]
    cur = Path("/")
    for part in parts[1:]:
        cur = cur / part
        crumbs.append({"name": part, "path": str(cur)})
    return crumbs


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    total = 0
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_HASH_BYTES:
                raise ValueError(f"hash limit exceeded ({MAX_HASH_BYTES} bytes)")
            h.update(chunk)
    return h.hexdigest()


def _runtime_info() -> dict:
    disk = shutil.disk_usage("/")
    tmp_disk = shutil.disk_usage("/tmp")
    load = None
    try:
        load = list(os.getloadavg())
    except Exception:
        pass
    rss = None
    try:
        import resource
        rss_raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss = int(rss_raw * 1024 if sys.platform != "darwin" else rss_raw)
    except Exception:
        pass
    return {
        "ok": True,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpuCount": os.cpu_count(),
        "pid": os.getpid(),
        "cwd": os.getcwd(),
        "loadAverage": load,
        "processPeakRssBytes": rss,
        "diskRoot": {"total": disk.total, "used": disk.used, "free": disk.free},
        "diskTmp": {"total": tmp_disk.total, "used": tmp_disk.used, "free": tmp_disk.free},
        "adminRoot": str(ADMIN_ROOT),
        "quickPaths": ["/", "/tmp", "/tmp/swrlz-admin", "/tmp/swrlz-admin/logs", "/tmp/swrlz-admin/uploads", "/tmp/swrlz-admin/pages", "/var/task", os.getcwd()],
        "warning": "PRE-TEST ADMIN: unauthenticated. Runtime filesystem changes may be ephemeral and deployed source may be read-only or replaced on a cold instance/redeploy.",
    }


PAGE = r'''<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>§wyrlz Runtime Admin</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}
body{font-family:system-ui;background:#090c12;color:#edf5ff;margin:0;padding:16px;max-width:1180px;margin:auto}
h1{margin:4px 0 6px;font-size:clamp(30px,7vw,52px)}
.warnbar{background:#3a2505;border:1px solid #d49a24;color:#ffd985;padding:12px;border-radius:12px;margin:10px 0 16px;font-weight:800}
.panel{background:#121826;border:1px solid #26344d;border-radius:16px;padding:14px;margin:12px 0}
.row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.grow{flex:1;min-width:180px}
input,textarea,select{width:100%;background:#0c1220;color:#fff;border:1px solid #53627d;border-radius:10px;padding:10px;font:inherit}
button{background:#e8edf7;color:#08101c;border:0;border-radius:10px;padding:10px 13px;font-weight:800;cursor:pointer}button.alt{background:#1d2a3f;color:#dff8ff;border:1px solid #36506f}button.danger{background:#5b1821;color:#ffdce0}
#crumbs button{padding:6px 9px}.path{font-family:ui-monospace,monospace;color:#7ee7ff;word-break:break-all}
.grid{display:grid;grid-template-columns:minmax(320px,.9fr) minmax(360px,1.1fr);gap:12px}@media(max-width:820px){.grid{grid-template-columns:1fr}}
.filelist{max-height:520px;overflow:auto;border:1px solid #26344d;border-radius:12px}.entry{display:grid;grid-template-columns:36px 1fr auto;gap:8px;padding:10px;border-bottom:1px solid #202a3c;align-items:center;cursor:pointer}.entry:last-child{border-bottom:0}.entry:hover{background:#182235}.name{font-weight:800;word-break:break-all}.meta{font-size:12px;color:#9eb0c9}
textarea{min-height:360px;font-family:ui-monospace,monospace;font-size:13px;white-space:pre;overflow:auto}
pre{background:#0c1220;border:1px solid #26344d;border-radius:12px;padding:12px;overflow:auto;white-space:pre-wrap}.ok{color:#80ffad}.bad{color:#ff9292}.muted{color:#9eb0c9}
.badge{display:inline-block;padding:3px 7px;border-radius:999px;background:#1c2a3c;color:#8de9ff;font-size:12px;margin-right:5px}.toolbar{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
</style>
</head>
<body>
<h1>§wyrlz Runtime Admin</h1>
<div class="warnbar">⚠ PRE-TEST ADMIN · PUBLIC / UNAUTHENTICATED · runtime files may be ephemeral</div>

<div class="panel">
 <div class="row"><input id="path" class="grow" value="/tmp/swrlz-admin"><button id="go">GO</button><button id="refresh" class="alt">REFRESH</button><button id="runtime" class="alt">RUNTIME</button></div>
 <div id="crumbs" class="toolbar"></div>
 <div id="quick" class="toolbar"></div>
</div>

<div class="grid">
 <div class="panel">
  <div class="row"><h2 class="grow">Files</h2><button id="newFolder" class="alt">NEW FOLDER</button><button id="newFile" class="alt">NEW FILE</button></div>
  <div class="row"><input id="uploadFile" type="file" class="grow"><button id="upload">UPLOAD</button></div>
  <p id="listStatus" class="muted">Loading…</p>
  <div id="files" class="filelist"></div>
 </div>

 <div class="panel">
  <div class="row"><h2 class="grow">Viewer / Editor</h2><button id="download" class="alt">DOWNLOAD</button><button id="hash" class="alt">SHA-256</button></div>
  <div id="selected" class="path">No file selected.</div>
  <div class="toolbar"><button id="save">SAVE TEXT</button><button id="rename" class="alt">RENAME</button><button id="del" class="danger">DELETE</button></div>
  <textarea id="editor" spellcheck="false" placeholder="Select a text file…"></textarea>
  <pre id="detail">Ready.</pre>
 </div>
</div>

<div class="panel"><h2>Operation Log</h2><div class="toolbar"><button id="clearLog" class="alt">CLEAR</button><button id="exportLog">EXPORT LOG TO SERVER</button></div><textarea id="log" readonly style="min-height:220px"></textarea><p id="logStatus" class="muted"></p></div>

<script>
const $=id=>document.getElementById(id);let cwd='/tmp/swrlz-admin', selected=null;
const log=(m,d)=>{const line=`[${new Date().toISOString()}] ${m}${d!==undefined?'\n'+(typeof d==='string'?d:JSON.stringify(d,null,2)):''}\n`; $('log').value+=line;$('log').scrollTop=$('log').scrollHeight};
async function req(action,opts={}){const q=new URLSearchParams({action,...(opts.q||{})});const r=await fetch('/api/admin?'+q.toString(),{method:opts.method||'GET',body:opts.body,headers:opts.headers||{}});const ct=r.headers.get('content-type')||'';if(opts.raw)return r;const txt=await r.text();let data;try{data=JSON.parse(txt)}catch{throw new Error(`HTTP ${r.status}: ${txt.slice(0,1200)}`)}if(!r.ok||data.ok===false)throw new Error(data.error||data.detail||JSON.stringify(data));return data}
const fmt=n=>{if(n==null)return '';const u=['B','KB','MB','GB','TB'];let x=Number(n),i=0;while(x>=1024&&i<u.length-1){x/=1024;i++}return `${x.toFixed(i?1:0)} ${u[i]}`};
function icon(k){return k==='dir'?'📁':k==='file'?'📄':k==='link'?'🔗':'❓'}
async function load(path=cwd){cwd=path;$('path').value=cwd;$('listStatus').textContent='Loading…';selected=null;$('selected').textContent='No file selected.';$('editor').value='';try{const j=await req('list',{q:{path}});cwd=j.path;$('path').value=cwd;$('files').innerHTML='';for(const e of j.entries){const d=document.createElement('div');d.className='entry';d.innerHTML=`<div>${icon(e.kind)}</div><div><div class="name"></div><div class="meta"></div></div><div class="meta">${e.writable?'W':'R'}</div>`;d.querySelector('.name').textContent=e.name;d.querySelector('.meta').textContent=`${e.kind} · ${fmt(e.size)} · ${e.mode||''}`;d.onclick=()=>e.kind==='dir'?load(e.path):selectFile(e);$('files').appendChild(d)}$('listStatus').textContent=`${j.entries.length} entries · ${cwd}`;$('crumbs').innerHTML='';for(const c of j.breadcrumbs){const b=document.createElement('button');b.className='alt';b.textContent=c.name;b.onclick=()=>load(c.path);$('crumbs').appendChild(b)}log('LIST '+cwd,{count:j.entries.length})}catch(e){$('listStatus').textContent=String(e);$('listStatus').className='bad';log('LIST FAILED '+cwd,String(e))}}
async function selectFile(e){selected=e;$('selected').textContent=e.path;$('detail').textContent=JSON.stringify(e,null,2);try{const j=await req('read',{q:{path:e.path}});$('editor').value=j.text;$('detail').textContent=JSON.stringify(j,null,2);log('READ '+e.path,{size:j.size})}catch(err){$('editor').value='';$('detail').textContent=String(err);log('READ FAILED '+e.path,String(err))}}
$('go').onclick=()=>load($('path').value);$('refresh').onclick=()=>load(cwd);
$('runtime').onclick=async()=>{try{const j=await req('runtime');$('detail').textContent=JSON.stringify(j,null,2);const q=$('quick');q.innerHTML='';for(const p of j.quickPaths){const b=document.createElement('button');b.className='alt';b.textContent=p;b.onclick=()=>load(p);q.appendChild(b)}log('RUNTIME',j)}catch(e){log('RUNTIME FAILED',String(e))}};
$('save').onclick=async()=>{if(!selected)return alert('Select a file first');try{const j=await req('save',{method:'POST',q:{path:selected.path},body:$('editor').value,headers:{'content-type':'text/plain;charset=utf-8'}});$('detail').textContent=JSON.stringify(j,null,2);log('SAVE '+selected.path,j);await load(cwd)}catch(e){$('detail').textContent=String(e);log('SAVE FAILED '+selected.path,String(e))}};
$('upload').onclick=async()=>{const f=$('uploadFile').files[0];if(!f)return alert('Choose a file');try{const j=await req('upload',{method:'POST',q:{path:cwd,name:f.name},body:f,headers:{'content-type':'application/octet-stream'}});log('UPLOAD '+f.name,j);await load(cwd)}catch(e){log('UPLOAD FAILED '+f.name,String(e));alert(e)}};
$('download').onclick=()=>{if(!selected)return alert('Select a file');location.href='/api/admin?'+new URLSearchParams({action:'download',path:selected.path}).toString()};
$('hash').onclick=async()=>{if(!selected)return alert('Select a file');try{const j=await req('hash',{q:{path:selected.path}});$('detail').textContent=JSON.stringify(j,null,2);log('HASH '+selected.path,j)}catch(e){log('HASH FAILED',String(e))}};
$('newFolder').onclick=async()=>{const n=prompt('Folder name');if(!n)return;try{const j=await req('mkdir',{method:'POST',q:{path:cwd,name:n}});log('MKDIR '+n,j);await load(cwd)}catch(e){alert(e);log('MKDIR FAILED',String(e))}};
$('newFile').onclick=async()=>{const n=prompt('File name');if(!n)return;try{const j=await req('new-file',{method:'POST',q:{path:cwd,name:n}});log('NEW FILE '+n,j);await load(cwd)}catch(e){alert(e);log('NEW FILE FAILED',String(e))}};
$('rename').onclick=async()=>{if(!selected)return alert('Select a file');const n=prompt('New name',selected.name);if(!n)return;try{const j=await req('rename',{method:'POST',q:{path:selected.path,name:n}});log('RENAME '+selected.path,j);await load(cwd)}catch(e){alert(e);log('RENAME FAILED',String(e))}};
$('del').onclick=async()=>{if(!selected)return alert('Select a file');if(!confirm('Delete '+selected.path+' ?'))return;try{const j=await req('delete',{method:'POST',q:{path:selected.path}});log('DELETE '+selected.path,j);await load(cwd)}catch(e){alert(e);log('DELETE FAILED',String(e))}};
$('clearLog').onclick=()=>{$('log').value=''};
$('exportLog').onclick=async()=>{try{const j=await req('export-log',{method:'POST',body:$('log').value,headers:{'content-type':'text/plain;charset=utf-8'}});$('logStatus').textContent='Saved: '+j.path;log('LOG EXPORTED',j)}catch(e){$('logStatus').textContent=String(e);log('LOG EXPORT FAILED',String(e))}};
(async()=>{await $('runtime').onclick();await load(cwd)})();
</script>
</body>
</html>'''


@app.get("/api/admin", response_class=HTMLResponse)
def admin_get(
    action: str | None = Query(default=None),
    path: str | None = Query(default=None),
):
    if not action:
        return PAGE
    p = _path(path)
    try:
        if action == "runtime":
            return _runtime_info()
        if action == "list":
            if not p.exists():
                return _json_error("path does not exist", 404, path=str(p))
            if not p.is_dir():
                return _json_error("path is not a directory", 400, path=str(p))
            entries = []
            for i, child in enumerate(sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))):
                if i >= MAX_LIST_ENTRIES:
                    break
                entries.append(_entry_info(child))
            return {"ok": True, "path": str(p), "entries": entries, "breadcrumbs": _breadcrumbs(p), "truncated": len(entries) >= MAX_LIST_ENTRIES}
        if action == "read":
            if not p.is_file():
                return _json_error("not a file", 400, path=str(p))
            size = p.stat().st_size
            if size > MAX_TEXT_BYTES:
                return _json_error(f"text preview limit is {MAX_TEXT_BYTES} bytes", 413, path=str(p), size=size)
            raw = p.read_bytes()
            if b"\x00" in raw[:8192]:
                return _json_error("binary file; use download instead", 415, path=str(p), size=size)
            text = raw.decode("utf-8", "replace")
            return {"ok": True, "path": str(p), "size": size, "text": text, "info": _entry_info(p)}
        if action == "download":
            if not p.is_file():
                return _json_error("not a file", 404, path=str(p))
            mime, _ = mimetypes.guess_type(str(p))
            return FileResponse(path=str(p), media_type=mime or "application/octet-stream", filename=p.name)
        if action == "hash":
            if not p.is_file():
                return _json_error("not a file", 400, path=str(p))
            return {"ok": True, "path": str(p), "size": p.stat().st_size, "sha256": _sha256(p)}
        return _json_error("unknown action", 400, action=action)
    except PermissionError as exc:
        return _json_error(f"PermissionError: {exc}", 403, path=str(p))
    except Exception as exc:
        return _json_error(f"{type(exc).__name__}: {exc}", 500, path=str(p))


@app.post("/api/admin")
async def admin_post(
    request: Request,
    action: str = Query(...),
    path: str | None = Query(default=None),
    name: str | None = Query(default=None),
):
    p = _path(path)
    try:
        if action == "save":
            if not p.exists() or not p.is_file():
                return _json_error("target is not an existing file", 400, path=str(p))
            body = await request.body()
            p.write_bytes(body)
            return {"ok": True, "path": str(p), "size": len(body), "mtime": p.stat().st_mtime}
        if action == "upload":
            if not name:
                return _json_error("name is required")
            if not p.exists() or not p.is_dir():
                return _json_error("upload path is not a directory", 400, path=str(p))
            target = p / Path(name).name
            body = await request.body()
            target.write_bytes(body)
            return {"ok": True, "path": str(target), "size": len(body)}
        if action == "mkdir":
            if not name:
                return _json_error("name is required")
            target = p / Path(name).name
            target.mkdir(parents=False, exist_ok=False)
            return {"ok": True, "path": str(target)}
        if action == "new-file":
            if not name:
                return _json_error("name is required")
            target = p / Path(name).name
            target.touch(exist_ok=False)
            return {"ok": True, "path": str(target)}
        if action == "rename":
            if not name:
                return _json_error("name is required")
            if not p.exists() and not p.is_symlink():
                return _json_error("path does not exist", 404, path=str(p))
            target = p.with_name(Path(name).name)
            p.rename(target)
            return {"ok": True, "from": str(p), "path": str(target)}
        if action == "delete":
            if not p.exists() and not p.is_symlink():
                return _json_error("path does not exist", 404, path=str(p))
            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p)
            else:
                p.unlink()
            return {"ok": True, "deleted": str(p)}
        if action == "export-log":
            body = await request.body()
            stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
            target = ADMIN_ROOT / "logs" / f"admin-{stamp}-{os.getpid()}.log"
            target.write_bytes(body)
            return {"ok": True, "path": str(target), "size": len(body)}
        return _json_error("unknown action", 400, action=action)
    except PermissionError as exc:
        return _json_error(f"PermissionError: {exc}", 403, path=str(p))
    except FileExistsError as exc:
        return _json_error(f"FileExistsError: {exc}", 409, path=str(p))
    except Exception as exc:
        return _json_error(f"{type(exc).__name__}: {exc}", 500, path=str(p))
