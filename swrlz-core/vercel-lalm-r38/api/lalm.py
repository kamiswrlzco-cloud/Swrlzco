from __future__ import annotations

import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="§wyrlz R38 HTTP Compute Adapter", version="0.2.0")

ENGINE_ID = "swrlz_r38_python_http_v1"


def _health_event(request_id: str) -> dict:
    return {
        "ok": True,
        "type": "health",
        "requestId": request_id,
        "detail": "§wyrlz R38 HTTP compute adapter is reachable; artifact bootstrap is available, neural executor is not ready yet.",
        "metrics": {
            "transport": "http",
            "engineId": ENGINE_ID,
            "containerVerified": "true",
            "graphReady": "false",
            "interactiveReady": "false",
        },
    }


PAGE = """<!doctype html>
<html><head><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>§wyrlz HTTP LALM Adapter</title>
<style>body{font-family:system-ui;background:#0b0d12;color:#eef2ff;max-width:760px;margin:32px auto;padding:20px}button{font-size:18px;padding:14px 18px;border:0;border-radius:12px;font-weight:800;cursor:pointer}pre{white-space:pre-wrap;background:#141824;padding:16px;border-radius:12px}.ok{color:#7cff9b}.bad{color:#ff8f8f}</style></head>
<body><h1>§wyrlz HTTP LALM Adapter</h1>
<p>Vercel exposes this Python file at <code>/api/lalm</code>. Health and generation actions stay on that route using <code>?action=...</code>.</p>
<button id='health'>TEST HTTP HEALTH</button>
<button id='generate'>TEST GENERATE PLACEHOLDER</button>
<p id='status'></p><pre id='out'>Ready.</pre>
<script>
async function call(action,method='GET',body=null){const r=await fetch('/api/lalm?action='+encodeURIComponent(action),{method,headers:body?{'content-type':'application/json'}:{},body:body?JSON.stringify(body):null});const t=await r.text();let j;try{j=JSON.parse(t)}catch{j={raw:t}};document.getElementById('out').textContent=JSON.stringify({httpStatus:r.status,...j},null,2);document.getElementById('status').className=r.ok?'ok':'bad';document.getElementById('status').textContent=r.ok?'Request completed.':'Request returned HTTP '+r.status;}
document.getElementById('health').onclick=()=>call('health');
document.getElementById('generate').onclick=()=>call('generate','POST',{requestId:'browser-test',prompt:'hello',maxOutputTokens:1});
</script></body></html>"""


@app.get("/api/lalm", response_class=HTMLResponse)
def lalm_get(action: str | None = Query(default=None)):
    if not action:
        return PAGE
    action = action.lower().strip()
    if action == "health":
        return _health_event(f"http-health-{uuid.uuid4().hex[:12]}")
    return JSONResponse(status_code=400, content={"ok": False, "error": "unknown action", "action": action})


@app.post("/api/lalm")
async def lalm_post(request: Request, action: str = Query(...)):
    action = action.lower().strip()
    body = {}
    try:
        body = await request.json()
    except Exception:
        pass
    request_id = str(body.get("requestId") or f"http-{action}-{uuid.uuid4().hex[:12]}")

    if action == "health":
        return _health_event(request_id)

    if action == "generate":
        return JSONResponse(
            status_code=501,
            content={
                "ok": False,
                "type": "failed",
                "requestId": request_id,
                "code": "R38_PYTHON_NEURAL_BACKEND_PENDING",
                "detail": "HTTP transport is wired, but R38 tensor/tokenizer/operator execution is not ready yet.",
                "metrics": {
                    "transport": "http",
                    "engineId": ENGINE_ID,
                    "timestampNs": str(time.time_ns()),
                },
            },
        )

    return JSONResponse(status_code=400, content={"ok": False, "error": "unknown action", "action": action})
