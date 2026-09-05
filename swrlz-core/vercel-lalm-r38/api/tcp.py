from __future__ import annotations

import errno
import json
import os
import socket
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="§wyrlz TCP Port Lab", version="0.4.0")
DEFAULT_SCAN_FROM = 8000
DEFAULT_SCAN_TO = 9000
MAX_SCAN_PORTS = 2048
MAX_SECONDS = 25
LOG_DIR = Path("/tmp/swrlz-admin/logs")
INSTANCE_ID = f"pid-{os.getpid()}-{uuid.uuid4().hex[:8]}"


def _classify(exc: OSError) -> str:
    if exc.errno == errno.EADDRINUSE: return "address_in_use"
    if exc.errno in (errno.EACCES, errno.EPERM): return "permission_denied"
    if exc.errno == errno.EADDRNOTAVAIL: return "address_not_available"
    return "bind_failed"


def _probe(port: int) -> dict:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(("0.0.0.0", port))
        return {"port": int(s.getsockname()[1]), "available": True, "status": "bind_available"}
    except OSError as exc:
        return {"port": port, "available": False, "status": _classify(exc), "errno": exc.errno, "error": f"{type(exc).__name__}: {exc}"}
    finally:
        s.close()


def _scan(a: int, b: int):
    if b < a: return JSONResponse(status_code=400, content={"ok": False, "error": "end_port must be >= start_port"})
    count = b - a + 1
    if count > MAX_SCAN_PORTS: return JSONResponse(status_code=400, content={"ok": False, "error": f"maximum scan size is {MAX_SCAN_PORTS}"})
    started = time.monotonic(); available=[]; unavailable=[]
    for p in range(a, b + 1):
        r = _probe(p)
        (available if r["available"] else unavailable).append(r["port"] if r["available"] else r)
    return {"ok": True, "action": "scan", "instanceId": INSTANCE_ID, "startPort": a, "endPort": b, "scannedCount": count, "availableCount": len(available), "unavailableCount": len(unavailable), "availablePorts": available, "unavailablePorts": unavailable, "elapsedMs": int((time.monotonic()-started)*1000)}


def _listen(port: int, seconds: int):
    started=time.monotonic(); accepted=[]; s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    result={"ok":False,"action":"listen","instanceId":INSTANCE_ID,"port":port,"requestedSeconds":seconds,"bindOk":False,"acceptedConnections":accepted}
    try:
        s.bind(("0.0.0.0",port)); s.listen(4); s.settimeout(.5); result["bindOk"]=True; result["localSocket"]=list(s.getsockname()); result["bindStatus"]="listening"
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            try: conn,addr=s.accept()
            except socket.timeout: continue
            with conn:
                conn.settimeout(2.0); raw=b""
                try:
                    while b"\n" not in raw and len(raw)<65536:
                        c=conn.recv(4096)
                        if not c: break
                        raw+=c
                    line=raw.split(b"\n",1)[0].decode("utf-8","replace").strip(); req={}
                    try: req=json.loads(line) if line else {}
                    except Exception: req={"type":"invalid_json"}
                    rid=str(req.get("requestId") or f"tcp-{uuid.uuid4().hex[:10]}")
                    event={"type":"health","requestId":rid,"detail":f"§wyrlz TCP listener reached on {port}","metrics":{"transport":"tcp_ndjson","port":str(port),"instanceId":INSTANCE_ID}}
                    conn.sendall((json.dumps(event,separators=(",",":"))+"\n").encode()); accepted.append({"remote":f"{addr[0]}:{addr[1]}","requestType":str(req.get("type") or ""),"requestId":rid})
                except Exception as exc: accepted.append({"remote":f"{addr[0]}:{addr[1]}","error":f"{type(exc).__name__}: {exc}"})
                break
        result.update(ok=True,externalConnectionObserved=bool(accepted),elapsedMs=int((time.monotonic()-started)*1000))
        result["conclusion"]="External TCP reached listener." if accepted else "Runtime listener opened, but no external TCP connection was observed. Vercel ingress may not route arbitrary TCP ports."
        return result
    except OSError as exc:
        result.update(bindStatus=_classify(exc),errno=exc.errno,error=f"{type(exc).__name__}: {exc}",elapsedMs=int((time.monotonic()-started)*1000))
        if port < 1024 and exc.errno in (errno.EACCES,errno.EPERM): result["hint"]="Ports below 1024 are privileged on Linux; permission denied here does not diagnose external Vercel ingress."
        return JSONResponse(status_code=500,content=result)
    finally:
        s.close()


def _export(text: str):
    LOG_DIR.mkdir(parents=True,exist_ok=True); stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"); p=LOG_DIR/f"tcp-lab-{stamp}-{uuid.uuid4().hex[:6]}.log"; p.write_text(text,encoding="utf-8")
    return {"ok":True,"action":"export","path":str(p),"size":p.stat().st_size,"instanceId":INSTANCE_ID,"note":"This /tmp file is function-instance local and may not be visible to api/admin.py on another Vercel instance. Use DOWNLOAD LOG TO PHONE for a guaranteed copy."}


PAGE=r'''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>§wyrlz TCP Port Lab</title><style>:root{color-scheme:dark}*{box-sizing:border-box}body{font-family:system-ui;background:#0b0d12;color:#eef2ff;max-width:920px;margin:24px auto;padding:18px}.panel{background:#141824;border:1px solid #253047;border-radius:16px;padding:16px;margin:16px 0}.row{display:flex;gap:12px;flex-wrap:wrap;align-items:end}.field{flex:1;min-width:130px}label{display:block;font-size:13px;font-weight:800;color:#67e8f9;margin-bottom:6px;text-transform:uppercase}input,select,textarea{width:100%;font-size:17px;padding:12px;border-radius:10px;border:1px solid #526079;background:#0e1320;color:#fff}button{font-size:17px;font-weight:800;padding:13px 18px;border:0;border-radius:12px}.lists{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:650px){.lists{grid-template-columns:1fr}}select{height:260px}.ok{color:#7CFF9B}.bad{color:#ff8f8f}.warn{color:#facc15}.muted{color:#94a3b8}textarea,pre{font-family:ui-monospace,monospace;font-size:13px;white-space:pre-wrap}textarea{height:320px}</style></head><body><h1>§wyrlz TCP Port Lab</h1><p>Internal bind tests and external-ingress tests are separate. Ports below 1024 may fail with Linux permission rules and do not prove anything about Vercel ingress.</p><div class="panel"><div class="row"><div class="field"><label>Scan from</label><input id="a" value="8000" type="number"></div><div class="field"><label>Scan to</label><input id="b" value="9000" type="number"></div><button id="scan">SCAN PORTS</button><button id="auto">AUTO FIND FREE PORT</button></div><p id="scanStatus" class="muted"></p><div class="lists"><div><label>Available</label><select id="avail" size="12"></select></div><div><label>Unavailable</label><select id="used" size="12"></select></div></div></div><div class="panel"><div class="row"><div class="field"><label>Port to open</label><input id="port" value="8765" type="number"></div><div class="field"><label>Hold open seconds</label><input id="secs" value="20" min="2" max="25" type="number"></div><button id="listen">OPEN TCP LISTENER</button></div><p id="status" class="muted"></p><pre id="out">Ready.</pre></div><div class="panel"><div class="row"><button id="clear">CLEAR</button><button id="export">EXPORT LOG TO SERVER</button><button id="download">DOWNLOAD LOG TO PHONE</button></div><textarea id="log" readonly></textarea><p id="exportStatus" class="muted"></p></div><script>
const $=i=>document.getElementById(i),log=(m,d)=>{$('log').value+=`[${new Date().toISOString()}] ${m}${d!==undefined?'\n'+(typeof d==='string'?d:JSON.stringify(d,null,2)):''}\n`; $('log').scrollTop=$('log').scrollHeight};async function req(action,p={},body=null){const q=new URLSearchParams({action,...p});const r=await fetch('/api/tcp?'+q,{method:'POST',body,headers:body?{'content-type':'text/plain;charset=utf-8'}:{}});const raw=await r.text();let j;try{j=JSON.parse(raw)}catch{throw new Error(`HTTP ${r.status}: ${raw.slice(0,2000)}`)}if(!r.ok)throw new Error(j.error||j.detail||JSON.stringify(j));return j}function opt(sel,text,val){const o=document.createElement('option');o.textContent=text;o.value=val;sel.appendChild(o)}$('avail').onchange=()=>{$('port').value=$('avail').value};$('scan').onclick=async()=>{try{const j=await req('scan',{start_port:$('a').value,end_port:$('b').value});$('avail').innerHTML='';$('used').innerHTML='';j.availablePorts.forEach(p=>opt($('avail'),p,p));j.unavailablePorts.forEach(x=>opt($('used'),`${x.port} · ${x.status}`,x.port));$('scanStatus').textContent=`${j.availableCount} available / ${j.unavailableCount} unavailable · ${j.elapsedMs}ms`;$('scanStatus').className='ok';log('SCAN',j)}catch(e){$('scanStatus').textContent=e.message;$('scanStatus').className='bad';log('SCAN FAILED',e.message)}};$('auto').onclick=async()=>{try{const j=await req('free-port');$('port').value=j.port;$('scanStatus').textContent=`OS supplied ${j.port}`;$('scanStatus').className='ok';log('AUTO FIND',j)}catch(e){$('scanStatus').textContent=e.message;$('scanStatus').className='bad';log('AUTO FIND FAILED',e.message)}};$('listen').onclick=async()=>{const p=$('port').value,s=$('secs').value;$('status').textContent=`Opening ${p} for ${s}s…`;$('status').className='warn';log(`LISTEN ${p} ${s}s`);try{const j=await req('listen',{port:p,seconds:s});$('out').textContent=JSON.stringify(j,null,2);$('status').textContent=j.externalConnectionObserved?'External TCP reached listener!':'Internal bind succeeded; no external TCP observed.';$('status').className=j.externalConnectionObserved?'ok':'warn';log('LISTEN RESULT',j)}catch(e){$('out').textContent=e.message;$('status').textContent=e.message;$('status').className='bad';log('LISTEN FAILED',e.message)}};$('clear').onclick=()=>{$('log').value=''};$('export').onclick=async()=>{try{const j=await req('export',{},$('log').value);$('exportStatus').textContent=`Saved ${j.path} · function-local`;log('EXPORT',j)}catch(e){$('exportStatus').textContent=e.message}};$('download').onclick=()=>{const b=new Blob([$('log').value],{type:'text/plain'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='tcp-lab-'+new Date().toISOString().replace(/[:.]/g,'-')+'.log';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)};log('TCP Port Lab loaded');</script></body></html>'''


@app.get("/")
@app.get("/api/tcp")
def page(): return HTMLResponse(PAGE)


@app.post("/")
@app.post("/api/tcp")
async def action(request: Request, action: str = Query(...), start_port: int = Query(DEFAULT_SCAN_FROM,ge=1,le=65535), end_port: int = Query(DEFAULT_SCAN_TO,ge=1,le=65535), port: int = Query(8765,ge=1,le=65535), seconds: int = Query(20,ge=2,le=MAX_SECONDS)):
    if action=="scan": return _scan(start_port,end_port)
    if action=="free-port":
        r=_probe(0); return {"ok":True,"action":"free-port","port":r["port"],"status":r["status"],"instanceId":INSTANCE_ID} if r["available"] else JSONResponse(status_code=500,content={"ok":False,**r})
    if action=="listen": return _listen(port,seconds)
    if action=="export": return _export((await request.body()).decode("utf-8","replace"))
    return JSONResponse(status_code=400,content={"ok":False,"error":"unknown action"})
