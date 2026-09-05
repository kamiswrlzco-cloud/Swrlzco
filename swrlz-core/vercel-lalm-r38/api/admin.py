from __future__ import annotations

import hashlib
import mimetypes
import os
import platform
import shutil
import stat
import sys
import time
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

app = FastAPI(title="§wyrlz Runtime Admin", version="0.3.0")

ADMIN_ROOT = Path("/tmp/swrlz-admin")
for d in (ADMIN_ROOT, ADMIN_ROOT / "logs", ADMIN_ROOT / "uploads", ADMIN_ROOT / "pages"):
    d.mkdir(parents=True, exist_ok=True)

MAX_LIST_ENTRIES = 1000
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_HASH_BYTES = 512 * 1024 * 1024


def _path(raw: str | None) -> Path:
    if not raw:
        return Path("/")
    p = Path(raw)
    return p if p.is_absolute() else Path("/") / p


def _err(message: str, status: int = 400, **extra):
    return JSONResponse(status_code=status, content={"ok": False, "error": message, **extra})


def _entry(p: Path) -> dict:
    st = p.lstat()
    kind = "dir" if p.is_dir() else "file" if p.is_file() else "link" if p.is_symlink() else "other"
    return {
        "name": p.name or "/", "path": str(p), "kind": kind, "size": int(st.st_size),
        "mtime": float(st.st_mtime), "mode": stat.filemode(st.st_mode),
        "readable": os.access(p, os.R_OK), "writable": os.access(p, os.W_OK),
    }


def _crumbs(p: Path):
    out = [{"name": "/", "path": "/"}]
    cur = Path("/")
    for part in p.parts[1:]:
        cur /= part
        out.append({"name": part, "path": str(cur)})
    return out


def _sha256(p: Path) -> str:
    h = hashlib.sha256(); total = 0
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            total += len(chunk)
            if total > MAX_HASH_BYTES:
                raise ValueError("hash limit exceeded")
            h.update(chunk)
    return h.hexdigest()


def _runtime():
    def disk(path):
        try:
            d = shutil.disk_usage(path); return {"total": d.total, "used": d.used, "free": d.free}
        except Exception as e:
            return {"error": f"{type(e).__name__}: {e}"}
    rss = None
    try:
        import resource
        raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        rss = int(raw * 1024 if sys.platform != "darwin" else raw)
    except Exception:
        pass
    return {
        "ok": True, "python": sys.version.split()[0], "platform": platform.platform(),
        "machine": platform.machine(), "cpuCount": os.cpu_count(), "pid": os.getpid(),
        "cwd": os.getcwd(), "processPeakRssBytes": rss, "diskRoot": disk("/"), "diskTmp": disk("/tmp"),
        "adminRoot": str(ADMIN_ROOT),
        "quickPaths": ["/", "/tmp", str(ADMIN_ROOT), str(ADMIN_ROOT/"logs"), str(ADMIN_ROOT/"uploads"), str(ADMIN_ROOT/"pages"), "/var/task", os.getcwd()],
        "warning": "PRE-TEST ADMIN: unauthenticated; runtime changes are ephemeral and may be instance-local.",
    }


PAGE = r'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>§wyrlz Runtime Admin</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font-family:system-ui;background:#090c12;color:#edf5ff;margin:0 auto;padding:16px;max-width:1180px}h1{font-size:clamp(32px,7vw,52px)}.panel{background:#121826;border:1px solid #26344d;border-radius:16px;padding:14px;margin:12px 0}.warn{background:#3a2505;color:#ffd985}.row,.tools{display:flex;gap:9px;flex-wrap:wrap;align-items:center}.grow{flex:1;min-width:180px}input,textarea{width:100%;background:#0c1220;color:#fff;border:1px solid #53627d;border-radius:10px;padding:10px;font:inherit}button{background:#e8edf7;color:#08101c;border:0;border-radius:10px;padding:10px 13px;font-weight:800}button.alt{background:#1d2a3f;color:#dff8ff;border:1px solid #36506f}button.danger{background:#641722;color:#fff}.grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:12px}@media(max-width:820px){.grid{grid-template-columns:1fr}}.filelist{max-height:520px;overflow:auto;border:1px solid #26344d;border-radius:12px}.entry{display:grid;grid-template-columns:34px 1fr auto;gap:8px;padding:10px;border-bottom:1px solid #202a3c;cursor:pointer}.entry:hover{background:#182235}.meta{font-size:12px;color:#9eb0c9}.name{font-weight:800;word-break:break-all}.path{font-family:ui-monospace,monospace;color:#7ee7ff;word-break:break-all}textarea{min-height:330px;font-family:ui-monospace,monospace;font-size:13px}pre{background:#0c1220;padding:12px;border-radius:12px;white-space:pre-wrap;overflow:auto}.bad{color:#ff9292}.ok{color:#80ffad}
</style></head><body>
<h1>§wyrlz Runtime Admin</h1><div class="panel warn">⚠ PRE-TEST ADMIN · PUBLIC / UNAUTHENTICATED · runtime files may be instance-local/ephemeral</div>
<div class="panel"><div class="row"><button id="up" class="alt">⬆ UP ONE DIR</button><input id="path" class="grow" value="/tmp/swrlz-admin"><button id="go">GO</button><button id="refresh" class="alt">REFRESH</button><button id="runtime" class="alt">RUNTIME</button></div><div id="crumbs" class="tools"></div><div id="quick" class="tools"></div></div>
<div class="grid"><div class="panel"><div class="row"><h2 class="grow">Files</h2><button id="newFolder" class="alt">NEW FOLDER</button><button id="newFile" class="alt">NEW FILE</button></div><div class="row"><input id="uploadFile" type="file" class="grow"><button id="upload">UPLOAD</button></div><p id="listStatus">Loading…</p><div id="files" class="filelist"></div></div>
<div class="panel"><div class="row"><h2 class="grow">Viewer / Editor</h2><button id="download" class="alt">DOWNLOAD</button><button id="hash" class="alt">SHA-256</button></div><div id="selected" class="path">No file selected.</div><div class="tools"><button id="save">SAVE TEXT</button><button id="rename" class="alt">RENAME</button><button id="del" class="danger">DELETE</button></div><textarea id="editor" spellcheck="false"></textarea><pre id="detail">Ready.</pre></div></div>
<div class="panel"><h2>Operation Log</h2><div class="tools"><button id="clearLog" class="alt">CLEAR</button><button id="exportLog">EXPORT LOG TO SERVER</button><button id="downloadLog" class="alt">DOWNLOAD LOG TO PHONE</button></div><textarea id="log" readonly></textarea><p id="logStatus"></p></div>
<script>
const $=id=>document.getElementById(id);let cwd='/tmp/swrlz-admin',selected=null;const log=(m,d)=>{$('log').value+=`[${new Date().toISOString()}] ${m}${d!==undefined?'\n'+(typeof d==='string'?d:JSON.stringify(d,null,2)):''}\n`;};
async function req(action,o={}){const q=new URLSearchParams({action,...(o.q||{})});const r=await fetch('/api/admin?'+q,{method:o.method||'GET',body:o.body,headers:o.headers||{}});if(o.raw)return r;const t=await r.text();let j;try{j=JSON.parse(t)}catch{throw Error(`HTTP ${r.status}: ${t.slice(0,1500)}`)}if(!r.ok||j.ok===false)throw Error(j.error||j.detail||JSON.stringify(j));return j}
const fmt=n=>{const u=['B','KB','MB','GB'];let x=Number(n||0),i=0;while(x>=1024&&i<3){x/=1024;i++}return `${x.toFixed(i?1:0)} ${u[i]}`};
async function load(path=cwd){cwd=path||'/';$('path').value=cwd;selected=null;$('selected').textContent='No file selected.';$('editor').value='';try{const j=await req('list',{q:{path:cwd}});cwd=j.path;$('path').value=cwd;$('files').innerHTML='';for(const e of j.entries){const d=document.createElement('div');d.className='entry';d.innerHTML=`<div>${e.kind==='dir'?'📁':'📄'}</div><div><div class="name"></div><div class="meta"></div></div><div>${e.writable?'W':'R'}</div>`;d.querySelector('.name').textContent=e.name;d.querySelector('.meta').textContent=`${e.kind} · ${fmt(e.size)} · ${e.mode||''}`;d.onclick=()=>e.kind==='dir'?load(e.path):selectFile(e);$('files').appendChild(d)}$('listStatus').textContent=`${j.entries.length} entries · ${cwd}`;$('crumbs').innerHTML='';for(const c of j.breadcrumbs){const b=document.createElement('button');b.className='alt';b.textContent=c.name;b.onclick=()=>load(c.path);$('crumbs').appendChild(b)}log('LIST '+cwd,{count:j.entries.length})}catch(e){$('listStatus').className='bad';$('listStatus').textContent=String(e);log('LIST FAILED',String(e))}}
async function selectFile(e){selected=e;$('selected').textContent=e.path;try{const j=await req('read',{q:{path:e.path}});$('editor').value=j.text;$('detail').textContent=JSON.stringify(j,null,2)}catch(err){$('editor').value='';$('detail').textContent=String(err)}}
$('up').onclick=()=>{let p=cwd.replace(/\/+$/,'');if(!p||p==='/')return load('/');const i=p.lastIndexOf('/');load(i<=0?'/':p.slice(0,i))};$('go').onclick=()=>load($('path').value);$('refresh').onclick=()=>load(cwd);
$('runtime').onclick=async()=>{try{const j=await req('runtime');$('detail').textContent=JSON.stringify(j,null,2);$('quick').innerHTML='';for(const p of j.quickPaths){const b=document.createElement('button');b.className='alt';b.textContent=p;b.onclick=()=>load(p);$('quick').appendChild(b)}log('RUNTIME',j)}catch(e){log('RUNTIME FAILED',String(e))}};
$('save').onclick=async()=>{if(!selected)return alert('Select a file');try{log('SAVE',await req('save',{method:'POST',q:{path:selected.path},body:$('editor').value,headers:{'content-type':'text/plain;charset=utf-8'}}));await load(cwd)}catch(e){alert(e)}};
$('upload').onclick=async()=>{const f=$('uploadFile').files[0];if(!f)return alert('Choose a file');try{log('UPLOAD',await req('upload',{method:'POST',q:{path:cwd,name:f.name},body:f,headers:{'content-type':'application/octet-stream'}}));await load(cwd)}catch(e){alert(e)}};
$('download').onclick=()=>{if(selected)location.href='/api/admin?'+new URLSearchParams({action:'download',path:selected.path})};$('hash').onclick=async()=>{if(selected)$('detail').textContent=JSON.stringify(await req('hash',{q:{path:selected.path}}),null,2)};
$('newFolder').onclick=async()=>{const n=prompt('Folder name');if(n){await req('mkdir',{method:'POST',q:{path:cwd,name:n}});await load(cwd)}};$('newFile').onclick=async()=>{const n=prompt('File name');if(n){await req('new-file',{method:'POST',q:{path:cwd,name:n}});await load(cwd)}};
$('rename').onclick=async()=>{if(!selected)return;const n=prompt('New name',selected.name);if(n){await req('rename',{method:'POST',q:{path:selected.path,name:n}});await load(cwd)}};$('del').onclick=async()=>{if(selected&&confirm('Delete '+selected.path+'?')){await req('delete',{method:'POST',q:{path:selected.path}});await load(cwd)}};
$('clearLog').onclick=()=>{$('log').value=''};$('exportLog').onclick=async()=>{try{const j=await req('export-log',{method:'POST',body:$('log').value,headers:{'content-type':'text/plain;charset=utf-8'}});$('logStatus').textContent='Saved: '+j.path}catch(e){$('logStatus').textContent=String(e)}};$('downloadLog').onclick=()=>{const b=new Blob([$('log').value],{type:'text/plain'}),u=URL.createObjectURL(b),a=document.createElement('a');a.href=u;a.download='swrlz-admin-'+new Date().toISOString().replace(/[:.]/g,'-')+'.log';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000)};
(async()=>{await $('runtime').onclick();await load(cwd)})();
</script></body></html>'''


@app.get("/")
@app.get("/api/admin")
def admin_get(action: str | None = Query(default=None), path: str | None = Query(default=None)):
    if not action:
        return HTMLResponse(PAGE)
    p = _path(path)
    try:
        if action == "runtime": return _runtime()
        if action == "list":
            if not p.exists(): return _err("path does not exist",404,path=str(p))
            if not p.is_dir(): return _err("not a directory",400,path=str(p))
            entries=[]
            for i,c in enumerate(sorted(p.iterdir(),key=lambda x:(not x.is_dir(),x.name.lower()))):
                if i>=MAX_LIST_ENTRIES: break
                try: entries.append(_entry(c))
                except Exception as e: entries.append({"name":c.name,"path":str(c),"kind":"error","error":str(e)})
            return {"ok":True,"path":str(p),"parent":str(p.parent),"entries":entries,"breadcrumbs":_crumbs(p),"truncated":len(entries)>=MAX_LIST_ENTRIES}
        if action == "read":
            if not p.is_file(): return _err("not a file",400,path=str(p))
            size=p.stat().st_size
            if size>MAX_TEXT_BYTES:return _err("text preview too large",413,size=size)
            raw=p.read_bytes()
            if b"\0" in raw[:8192]: return _err("binary file; download instead",415,size=size)
            return {"ok":True,"path":str(p),"size":size,"text":raw.decode('utf-8','replace'),"info":_entry(p)}
        if action == "download":
            if not p.is_file(): return _err("not a file",404)
            mime,_=mimetypes.guess_type(str(p));return FileResponse(str(p),media_type=mime or 'application/octet-stream',filename=p.name)
        if action == "hash": return {"ok":True,"path":str(p),"size":p.stat().st_size,"sha256":_sha256(p)}
        return _err("unknown action",400,action=action)
    except Exception as e:return _err(f"{type(e).__name__}: {e}",500,path=str(p))


@app.post("/")
@app.post("/api/admin")
async def admin_post(request: Request, action: str = Query(...), path: str | None = Query(default=None), name: str | None = Query(default=None)):
    p=_path(path)
    try:
        if action=='save':
            body=await request.body();p.write_bytes(body);return {"ok":True,"path":str(p),"size":len(body)}
        if action=='upload':
            if not name:return _err('name required')
            t=p/Path(name).name;t.write_bytes(await request.body());return {"ok":True,"path":str(t),"size":t.stat().st_size}
        if action=='mkdir':
            t=p/Path(name or '').name;t.mkdir();return {"ok":True,"path":str(t)}
        if action=='new-file':
            t=p/Path(name or '').name;t.touch(exist_ok=False);return {"ok":True,"path":str(t)}
        if action=='rename':
            t=p.with_name(Path(name or '').name);p.rename(t);return {"ok":True,"path":str(t)}
        if action=='delete':
            shutil.rmtree(p) if p.is_dir() and not p.is_symlink() else p.unlink();return {"ok":True,"deleted":str(p)}
        if action=='export-log':
            body=await request.body();t=ADMIN_ROOT/'logs'/f"admin-{time.strftime('%Y%m%d-%H%M%S',time.gmtime())}-{os.getpid()}.log";t.write_bytes(body);return {"ok":True,"path":str(t),"size":len(body)}
        return _err('unknown action',400,action=action)
    except Exception as e:return _err(f"{type(e).__name__}: {e}",500,path=str(p))
