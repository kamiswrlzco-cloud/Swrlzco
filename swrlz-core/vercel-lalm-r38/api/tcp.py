from __future__ import annotations

import errno
import json
import socket
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="§wyrlz R38 TCP Port Lab", version="0.3.0")

DEFAULT_PORT = 8765
DEFAULT_SCAN_FROM = 8000
DEFAULT_SCAN_TO = 9000
MAX_SCAN_PORTS = 2048
MAX_SECONDS = 120
LOG_DIR = Path("/tmp/swrlz-admin/logs")


def _event(request_id: str, detail: str, port: int) -> bytes:
    payload = {
        "type": "health",
        "requestId": request_id,
        "detail": detail,
        "metrics": {
            "transport": "tcp_ndjson",
            "port": str(port),
            "containerVerified": "true",
            "graphReady": "false",
            "interactiveReady": "false",
        },
    }
    return (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")


def _classify_bind_error(exc: OSError) -> str:
    if exc.errno == errno.EADDRINUSE:
        return "address_in_use"
    if exc.errno in (errno.EACCES, errno.EPERM):
        return "permission_denied"
    if exc.errno == errno.EADDRNOTAVAIL:
        return "address_not_available"
    return "bind_failed"


def _probe_port(port: int) -> dict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("0.0.0.0", port))
        return {"port": int(sock.getsockname()[1]), "available": True, "status": "bind_available"}
    except OSError as exc:
        return {
            "port": port,
            "available": False,
            "status": _classify_bind_error(exc),
            "errno": exc.errno,
            "error": f"{type(exc).__name__}: {exc}",
        }
    finally:
        try:
            sock.close()
        except Exception:
            pass


def _scan(start_port: int, end_port: int):
    if end_port < start_port:
        return JSONResponse(status_code=400, content={"ok": False, "detail": "end_port must be >= start_port"})
    count = end_port - start_port + 1
    if count > MAX_SCAN_PORTS:
        return JSONResponse(status_code=400, content={"ok": False, "detail": f"maximum scan size is {MAX_SCAN_PORTS} ports"})
    started = time.monotonic()
    available, unavailable = [], []
    for p in range(start_port, end_port + 1):
        result = _probe_port(p)
        if result["available"]:
            available.append(result["port"])
        else:
            unavailable.append(result)
    return {
        "ok": True,
        "action": "scan",
        "bindAddress": "0.0.0.0",
        "startPort": start_port,
        "endPort": end_port,
        "scannedCount": count,
        "availableCount": len(available),
        "unavailableCount": len(unavailable),
        "availablePorts": available,
        "unavailablePorts": unavailable,
        "elapsedMs": int((time.monotonic() - started) * 1000),
    }


def _free_port():
    result = _probe_port(0)
    if not result["available"]:
        return JSONResponse(status_code=500, content={"ok": False, "action": "free-port", **result})
    return {
        "ok": True,
        "action": "free-port",
        "port": result["port"],
        "status": result["status"],
        "note": "The OS-selected port is released after this check; OPEN TCP LISTENER claims it again.",
    }


def _listen(port: int, seconds: int):
    started = time.monotonic()
    deadline = started + seconds
    accepted = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    result = {
        "ok": False,
        "action": "listen",
        "bindAddress": "0.0.0.0",
        "port": port,
        "requestedSeconds": seconds,
        "bindOk": False,
        "acceptedConnections": accepted,
    }
    try:
        server.bind(("0.0.0.0", port))
        server.listen(4)
        server.settimeout(1.0)
        result["bindOk"] = True
        result["bindStatus"] = "listening"
        result["localSocket"] = list(server.getsockname())
        while time.monotonic() < deadline:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue
            except Exception as exc:
                result["acceptError"] = f"{type(exc).__name__}: {exc}"
                break
            with conn:
                conn.settimeout(3.0)
                raw = b""
                try:
                    while b"\n" not in raw and len(raw) < 65536:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        raw += chunk
                    line = raw.split(b"\n", 1)[0].decode("utf-8", "replace").strip()
                    request_id = f"tcp-health-{uuid.uuid4().hex[:12]}"
                    request_type = ""
                    if line:
                        try:
                            request = json.loads(line)
                            request_id = str(request.get("requestId") or request_id)
                            request_type = str(request.get("type") or "")
                        except Exception:
                            request_type = "invalid_json"
                    conn.sendall(_event(request_id, f"§wyrlz TCP/NDJSON listener reached on port {port}.", port))
                    accepted.append({"remote": f"{addr[0]}:{addr[1]}", "requestType": request_type, "requestId": request_id})
                    if request_type.lower() == "health":
                        break
                except Exception as exc:
                    accepted.append({"remote": f"{addr[0]}:{addr[1]}", "error": f"{type(exc).__name__}: {exc}"})
        result["ok"] = True
        result["externalConnectionObserved"] = bool(accepted)
        result["elapsedMs"] = int((time.monotonic() - started) * 1000)
        result["conclusion"] = (
            f"At least one TCP connection reached the Python listener on port {port}."
            if accepted else
            f"The runtime bound TCP/{port}, but no connection reached it during the probe window."
        )
        return result
    except OSError as exc:
        result["bindStatus"] = _classify_bind_error(exc)
        result["errno"] = exc.errno
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["elapsedMs"] = int((time.monotonic() - started) * 1000)
        return JSONResponse(status_code=500, content=result)
    except Exception as exc:
        result["bindStatus"] = "bind_failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["elapsedMs"] = int((time.monotonic() - started) * 1000)
        return JSONResponse(status_code=500, content=result)
    finally:
        try:
            server.close()
        except Exception:
            pass


def _export_log(text: str):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = LOG_DIR / f"tcp-lab-{stamp}-{uuid.uuid4().hex[:6]}.log"
    path.write_text(text, encoding="utf-8")
    return {
        "ok": True,
        "action": "export",
        "path": str(path),
        "size": path.stat().st_size,
        "note": "Saved in the runtime workspace for the upcoming admin file browser/downloader.",
    }


@app.get("/api/tcp", response_class=HTMLResponse)
def tcp_page():
    return r'''<!doctype html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>§wyrlz TCP Port Lab</title>
<style>
:root{color-scheme:dark}*{box-sizing:border-box}body{font-family:system-ui;background:#0b0d12;color:#eef2ff;max-width:920px;margin:24px auto;padding:18px}h1{font-size:clamp(32px,7vw,52px);line-height:1;margin:0 0 18px}p{line-height:1.5;color:#cbd5e1}.panel{background:#141824;border:1px solid #253047;border-radius:16px;padding:16px;margin:16px 0}.row{display:flex;gap:12px;flex-wrap:wrap;align-items:end}.field{flex:1;min-width:130px}label{display:block;font-size:13px;font-weight:800;color:#67e8f9;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}input,select,textarea{width:100%;font-size:17px;padding:12px;border-radius:10px;border:1px solid #526079;background:#0e1320;color:#fff}button{font-size:17px;font-weight:800;padding:13px 18px;border:0;border-radius:12px;cursor:pointer;background:#e8edf7;color:#071019}button:disabled{opacity:.55}.lists{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}@media(max-width:650px){.lists{grid-template-columns:1fr}}.listbox select{height:260px;font-family:ui-monospace,monospace;font-size:14px}.ok{color:#7CFF9B}.bad{color:#ff8f8f}.muted{color:#94a3b8}.warn{color:#facc15}pre,textarea{white-space:pre-wrap;background:#0e1320;padding:14px;border-radius:12px;overflow:auto;border:1px solid #253047;font-family:ui-monospace,monospace;font-size:13px}textarea{height:330px;resize:vertical}
</style></head><body>
<h1>§wyrlz TCP Port Lab</h1>
<p>All actions stay on <code>/api/tcp</code> and use an <code>action</code> query parameter so Vercel does not need nested function routes.</p>
<div class="panel"><div class="row"><div class="field"><label>Scan from</label><input id="fromPort" type="number" min="1" max="65535" value="8000"></div><div class="field"><label>Scan to</label><input id="toPort" type="number" min="1" max="65535" value="9000"></div><button id="scan">SCAN PORTS</button><button id="auto">AUTO FIND FREE PORT</button></div><p id="scanStatus" class="muted">Ready. Maximum 2048 ports per scan.</p><div class="lists"><div><label>Available ports</label><select id="available" size="12"></select></div><div><label>Used / unavailable ports</label><select id="used" size="12"></select></div></div></div>
<div class="panel"><div class="row"><div class="field"><label>Port to open</label><input id="port" type="number" min="1" max="65535" value="8765"></div><div class="field"><label>Hold open seconds</label><input id="seconds" type="number" min="5" max="120" value="60"></div><button id="run">OPEN TCP LISTENER</button></div><p id="status" class="muted">Choose an available port or type one manually.</p><pre id="out">Ready.</pre></div>
<div class="panel"><div class="row"><div class="field"><label>Live test log</label></div><button id="clearLog">CLEAR</button><button id="exportLog">EXPORT LOG TO SERVER</button></div><textarea id="log" readonly></textarea><p id="exportStatus" class="muted">Exports save under <code>/tmp/swrlz-admin/logs/</code> for the upcoming file browser.</p></div>
<script>
const $=id=>document.getElementById(id);const scan=$('scan'),auto=$('auto'),avail=$('available'),used=$('used'),port=$('port'),seconds=$('seconds'),scanStatus=$('scanStatus'),status=$('status'),out=$('out'),run=$('run'),logBox=$('log'),exportStatus=$('exportStatus');
function ts(){return new Date().toISOString()}function log(msg,data){let line=`[${ts()}] ${msg}`;if(data!==undefined)line+='\n'+(typeof data==='string'?data:JSON.stringify(data,null,2));logBox.value+=(logBox.value?'\n':'')+line+'\n';logBox.scrollTop=logBox.scrollHeight}function addOption(sel,text,value){const o=document.createElement('option');o.textContent=text;o.value=value;sel.appendChild(o)}avail.onchange=()=>{if(avail.value)port.value=avail.value};
async function request(action,params={},body=null){const q=new URLSearchParams({action,...params});const r=await fetch('/api/tcp?'+q.toString(),{method:'POST',headers:body?{'content-type':'text/plain;charset=utf-8'}:undefined,body});const raw=await r.text();let data;try{data=JSON.parse(raw)}catch(e){throw new Error(`HTTP ${r.status} ${r.statusText}\n${raw.slice(0,4000)}`)}if(!r.ok)throw new Error(data.detail||data.error||JSON.stringify(data));return data}
scan.onclick=async()=>{const a=Number($('fromPort').value),b=Number($('toPort').value);scan.disabled=auto.disabled=true;scanStatus.className='warn';scanStatus.textContent=`Scanning ${a}-${b}…`;avail.innerHTML='';used.innerHTML='';log(`SCAN requested ${a}-${b}`);try{const j=await request('scan',{start_port:a,end_port:b});for(const p of j.availablePorts)addOption(avail,String(p),String(p));for(const x of j.unavailablePorts)addOption(used,`${x.port} · ${x.status}${x.errno!=null?' · errno '+x.errno:''}`,String(x.port));scanStatus.className='ok';scanStatus.textContent=`Scanned ${j.scannedCount} · ${j.availableCount} available · ${j.unavailableCount} unavailable · ${j.elapsedMs} ms`;log('SCAN result',j)}catch(e){scanStatus.className='bad';scanStatus.textContent='Scan failed: '+e.message;log('SCAN failed',e.message)}finally{scan.disabled=auto.disabled=false}};
auto.onclick=async()=>{auto.disabled=scan.disabled=true;scanStatus.className='warn';scanStatus.textContent='Asking OS for a free port…';log('AUTO FIND requested');try{const j=await request('free-port');port.value=j.port;scanStatus.className='ok';scanStatus.textContent=`OS supplied ${j.port}.`;log('AUTO FIND result',j)}catch(e){scanStatus.className='bad';scanStatus.textContent='Auto-find failed: '+e.message;log('AUTO FIND failed',e.message)}finally{auto.disabled=scan.disabled=false}};
run.onclick=async()=>{const p=Number(port.value),secs=Number(seconds.value);run.disabled=true;status.className='warn';status.textContent=`Trying 0.0.0.0:${p}; TEST CONNECT against swrlzco.vercel.app:${p} while this runs.`;out.textContent=`Holding request for up to ${secs}s…`;log(`LISTEN requested port=${p} seconds=${secs}`);try{const j=await request('listen',{port:p,seconds:secs});out.textContent=JSON.stringify(j,null,2);status.className=j.bindOk?'ok':'bad';status.textContent=j.bindOk?(j.externalConnectionObserved?'External TCP reached listener!':'Runtime bind succeeded; no external TCP observed.'):`Bind failed: ${j.error||j.bindStatus||'unknown'}`;log('LISTEN result',j)}catch(e){status.className='bad';status.textContent='Listener request failed';out.textContent=e.message;log('LISTEN failed',e.message)}finally{run.disabled=false}};
$('clearLog').onclick=()=>{logBox.value='';exportStatus.className='muted';exportStatus.textContent='Log cleared.'};$('exportLog').onclick=async()=>{if(!logBox.value.trim()){exportStatus.className='bad';exportStatus.textContent='Nothing to export.';return}exportStatus.className='warn';exportStatus.textContent='Saving log to runtime workspace…';try{const j=await request('export',{},logBox.value);exportStatus.className='ok';exportStatus.textContent=`Saved ${j.size} bytes → ${j.path}`;log('EXPORT result',j)}catch(e){exportStatus.className='bad';exportStatus.textContent='Export failed: '+e.message;log('EXPORT failed',e.message)}};log('TCP Port Lab loaded');
</script></body></html>'''


@app.post("/api/tcp")
async def tcp_action(
    request: Request,
    action: str = Query(default="listen"),
    start_port: int = Query(default=DEFAULT_SCAN_FROM, ge=1, le=65535),
    end_port: int = Query(default=DEFAULT_SCAN_TO, ge=1, le=65535),
    port: int = Query(default=DEFAULT_PORT, ge=1, le=65535),
    seconds: int = Query(default=60, ge=5, le=MAX_SECONDS),
):
    action = action.strip().lower()
    if action == "scan":
        return _scan(start_port, end_port)
    if action in {"free", "free-port", "auto"}:
        return _free_port()
    if action == "listen":
        return _listen(port, seconds)
    if action == "export":
        raw = await request.body()
        text = raw.decode("utf-8", "replace")
        if not text.strip():
            return JSONResponse(status_code=400, content={"ok": False, "detail": "log body is empty"})
        return _export_log(text)
    return JSONResponse(status_code=400, content={"ok": False, "detail": f"unknown action: {action}"})
