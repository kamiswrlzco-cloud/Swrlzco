from __future__ import annotations

import json
import socket
import time
import uuid
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="§wyrlz R38 TCP Listener Probe", version="0.1.0")

DEFAULT_PORT = 8765
MAX_SECONDS = 120


def _event(request_id: str, detail: str) -> bytes:
    payload = {
        "type": "health",
        "requestId": request_id,
        "detail": detail,
        "metrics": {
            "transport": "tcp_ndjson",
            "containerVerified": "true",
            "graphReady": "false",
            "interactiveReady": "false",
        },
    }
    return (json.dumps(payload, separators=(",", ":")) + "\n").encode("utf-8")


@app.get("/api/tcp", response_class=HTMLResponse)
def tcp_page():
    return """<!doctype html>
<html>
<head>
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>§wyrlz TCP Listener Probe</title>
<style>
body{font-family:system-ui;background:#0b0d12;color:#eef2ff;max-width:760px;margin:40px auto;padding:20px}
button{font-size:18px;padding:14px 20px;border:0;border-radius:12px;cursor:pointer}
pre{white-space:pre-wrap;background:#141824;padding:16px;border-radius:12px;overflow:auto}.ok{color:#7CFF9B}.bad{color:#ff8f8f}
</style>
</head>
<body>
<h1>§wyrlz TCP Listener Probe</h1>
<p>This deliberately tries to bind <code>0.0.0.0:8765</code> inside the active Python runtime and keeps the request alive for 60 seconds. While it is running, use R294's <b>TEST CONNECT</b> against <code>swrlzco.vercel.app:8765</code>. The test tells us separately whether the runtime can bind the socket and whether Vercel actually exposes that port externally.</p>
<button id=\"run\">Open TCP :8765 for 60s</button>
<p id=\"status\"></p><pre id=\"out\">Ready.</pre>
<script>
const b=document.getElementById('run'),s=document.getElementById('status'),o=document.getElementById('out');
b.onclick=async()=>{
 b.disabled=true;s.textContent='Listener request active — switch to SERVER and press TEST CONNECT now.';o.textContent='Waiting up to 60 seconds…';
 try{const r=await fetch('/api/tcp?seconds=60',{method:'POST'});const j=await r.json();o.textContent=JSON.stringify(j,null,2);s.className=j.bindOk?'ok':'bad';s.textContent=j.bindOk?'Runtime socket bind completed. Check external result below.':'TCP bind failed.'}
 catch(e){s.className='bad';s.textContent='Probe request failed';o.textContent=String(e)}finally{b.disabled=false}
};
</script>
</body>
</html>"""


@app.post("/api/tcp")
def tcp_probe(seconds: int = Query(default=60, ge=5, le=MAX_SECONDS)):
    started = time.monotonic()
    deadline = started + seconds
    accepted = []
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    result = {
        "ok": False,
        "bindAddress": "0.0.0.0",
        "port": DEFAULT_PORT,
        "requestedSeconds": seconds,
        "bindOk": False,
        "acceptedConnections": accepted,
        "note": "A successful bind only proves the sandbox can create a listener. External reachability still depends on the hosting platform routing TCP/8765 to this runtime.",
    }
    try:
        server.bind(("0.0.0.0", DEFAULT_PORT))
        server.listen(4)
        server.settimeout(1.0)
        result["bindOk"] = True
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
                    conn.sendall(_event(request_id, "§wyrlz TCP/NDJSON listener reached on port 8765."))
                    accepted.append({
                        "remote": f"{addr[0]}:{addr[1]}",
                        "requestType": request_type,
                        "requestId": request_id,
                    })
                    if request_type.lower() == "health":
                        break
                except Exception as exc:
                    accepted.append({"remote": f"{addr[0]}:{addr[1]}", "error": f"{type(exc).__name__}: {exc}"})
        result["ok"] = result["bindOk"]
        result["externalConnectionObserved"] = bool(accepted)
        result["elapsedMs"] = int((time.monotonic() - started) * 1000)
        if accepted:
            result["conclusion"] = "At least one external TCP connection reached the Python listener."
        else:
            result["conclusion"] = "The runtime bound TCP/8765, but no external connection reached it during the probe window."
        return result
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["elapsedMs"] = int((time.monotonic() - started) * 1000)
        return JSONResponse(status_code=500, content=result)
    finally:
        try:
            server.close()
        except Exception:
            pass
