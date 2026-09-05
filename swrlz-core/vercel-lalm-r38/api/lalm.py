from __future__ import annotations

import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

from swyrlz.r38_gate5 import inspect_gate5

app = FastAPI(title="§wyrlz R38 HTTP Compute Adapter", version="0.3.0")
ENGINE_ID = "swrlz_r38_python_http_v1"


def _health_event(request_id: str) -> dict:
    return {
        "ok": True, "type": "health", "requestId": request_id,
        "detail": "§wyrlz R38 HTTP compute adapter is reachable.",
        "metrics": {"transport": "http", "engineId": ENGINE_ID, "containerVerified": "true", "graphReady": "false", "interactiveReady": "false"},
    }

PAGE = """<!doctype html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>§wyrlz HTTP LALM Adapter</title>
<style>body{font-family:system-ui;background:#0b0d12;color:#eef2ff;max-width:780px;margin:32px auto;padding:20px}button{font-size:18px;padding:14px 18px;border:0;border-radius:12px;font-weight:800;margin:4px;cursor:pointer}pre{white-space:pre-wrap;background:#141824;padding:16px;border-radius:12px;overflow:auto}.ok{color:#7cff9b}.bad{color:#ff8f8f}.warn{color:#ffd166}</style></head><body>
<h1>§wyrlz HTTP LALM Adapter</h1><p>HTTP transport is live. Gate 5 inspects the actual R38 artifact and fails closed if canonical tensor/tokenizer payload access is not ready.</p>
<button id='health'>TEST HTTP HEALTH</button><button id='gate5'>RUN GATE 5</button><button id='generate'>TEST GENERATE</button><p id='status'></p><pre id='out'>Ready.</pre>
<script>async function call(action,method='GET',body=null){const s=document.getElementById('status'),o=document.getElementById('out');s.className='warn';s.textContent='Running '+action+'…';const r=await fetch('/api/lalm?action='+encodeURIComponent(action),{method,headers:body?{'content-type':'application/json'}:{},body:body?JSON.stringify(body):null});const t=await r.text();let j;try{j=JSON.parse(t)}catch{j={raw:t}};o.textContent=JSON.stringify({httpStatus:r.status,...j},null,2);s.className=r.ok?'ok':'bad';s.textContent=r.ok?'Request completed.':'Request returned HTTP '+r.status;}health.onclick=()=>call('health');gate5.onclick=()=>call('gate5');generate.onclick=()=>call('generate','POST',{requestId:'browser-test',prompt:'hello',maxOutputTokens:1});</script></body></html>"""

@app.get("/api/lalm", response_class=HTMLResponse)
def lalm_get(action: str | None = Query(default=None)):
    if not action: return PAGE
    action = action.lower().strip()
    if action == "health": return _health_event(f"http-health-{uuid.uuid4().hex[:12]}")
    if action == "gate5":
        try: return inspect_gate5()
        except Exception as exc: return JSONResponse(status_code=500, content={"ok":False,"stage":"gate5-executor-readiness","error":f"{type(exc).__name__}: {exc}"})
    return JSONResponse(status_code=400, content={"ok":False,"error":"unknown action","action":action})

@app.post("/api/lalm")
async def lalm_post(request: Request, action: str = Query(...)):
    action = action.lower().strip(); body={}
    try: body=await request.json()
    except Exception: pass
    request_id=str(body.get("requestId") or f"http-{action}-{uuid.uuid4().hex[:12]}")
    if action=="health": return _health_event(request_id)
    if action=="gate5":
        try: return inspect_gate5()
        except Exception as exc: return JSONResponse(status_code=500, content={"ok":False,"stage":"gate5-executor-readiness","error":f"{type(exc).__name__}: {exc}"})
    if action=="generate":
        try:
            readiness=inspect_gate5()
        except Exception as exc:
            return JSONResponse(status_code=500,content={"ok":False,"type":"failed","requestId":request_id,"code":"R38_GATE5_INSPECTION_FAILED","detail":f"{type(exc).__name__}: {exc}"})
        if not readiness.get("oneTokenReady"):
            return JSONResponse(status_code=501,content={"ok":False,"type":"failed","requestId":request_id,"code":"R38_ONE_TOKEN_BLOCKED_BY_ARTIFACT_LAYOUT","detail":"HTTP transport and reference quantization kernels are wired, but the transferred R38 artifact does not yet expose the canonical tokenizer/tensor-directory/tensor-data payloads required for truthful one-token inference.","blockers":readiness.get("blockers",[]),"metrics":{"transport":"http","engineId":ENGINE_ID,"timestampNs":str(time.time_ns())}})
        return JSONResponse(status_code=501,content={"ok":False,"type":"failed","requestId":request_id,"code":"R38_GRAPH_EXECUTOR_PENDING","detail":"Required payloads are visible; graph execution wiring is the remaining gate."})
    return JSONResponse(status_code=400, content={"ok":False,"error":"unknown action","action":action})
