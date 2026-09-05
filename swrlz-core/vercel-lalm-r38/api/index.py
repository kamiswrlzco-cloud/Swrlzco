from fastapi import FastAPI

app = FastAPI(title="§wyrlz Vercel Routing Probe", version="0.3.0")


def health_payload():
    return {
        "ok": True,
        "service": "§wyrlz Vercel Routing Probe",
        "stage": "routing-only",
        "routingReady": True,
        "modelInstalled": False,
        "containerVerified": False,
        "graphReady": False,
        "interactiveReady": False,
    }


@app.get("/")
def root():
    return {
        "ok": True,
        "service": "§wyrlz Vercel Routing Probe",
        "stage": "routing-only",
        "health": "/health",
        "apiHealth": "/api/health",
    }


@app.get("/health")
def health():
    return health_payload()


@app.get("/api/health")
def api_health():
    return health_payload()
