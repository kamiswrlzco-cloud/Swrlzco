from fastapi import FastAPI

app = FastAPI(title="§wyrlz Vercel Health Probe", version="0.3.0")


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "service": "§wyrlz Vercel Gateway",
        "stage": "direct-function-health",
        "routingReady": True,
        "modelInstalled": False,
        "containerVerified": False,
        "graphReady": False,
        "interactiveReady": False,
    }
