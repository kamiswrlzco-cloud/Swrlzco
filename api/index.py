from fastapi import FastAPI, HTTPException

app = FastAPI(title="§wyrlz Vercel Gateway", version="0.2.0-routing")


@app.get("/api")
def api_root():
    return {
        "ok": True,
        "service": "§wyrlz Vercel Gateway",
        "stage": "routing-bootstrap",
        "health": "/api/health",
        "model": "/api/model",
    }


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "service": "§wyrlz Vercel Gateway",
        "stage": "routing-bootstrap",
        "routingReady": True,
        "modelInstalled": False,
        "containerVerified": False,
        "graphReady": False,
        "interactiveReady": False,
    }


@app.get("/api/model")
def model():
    raise HTTPException(
        status_code=503,
        detail={
            "code": "SWYRLZ_R38_MODEL_NOT_INSTALLED",
            "message": "Routing is live. The R38 LALM artifact has not been installed in this Vercel project yet.",
        },
    )
