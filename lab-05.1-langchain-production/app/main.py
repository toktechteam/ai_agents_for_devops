from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .models import Alert
from .chain import ChainEngine

app = FastAPI()
engine = ChainEngine()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/investigate")
def investigate(alert: Alert):
    return engine.run(alert.dict())
