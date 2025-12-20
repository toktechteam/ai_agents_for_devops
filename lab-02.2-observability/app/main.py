import time
import logging
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("lab-2.2-free")

app = FastAPI(title="Lab 2.2 Free - Observability Lite API")


class Features(BaseModel):
    features: List[float] = Field(..., min_length=1)


@app.get("/health")
def health():
    log.info("Health check called")
    return {
        "status": "ok",
        "version": "free",
    }


@app.get("/metrics-lite")
def metrics_lite():
    """
    Lightweight metrics endpoint.
    This is intentionally NOT Prometheus-compatible.
    """
    ts = time.time()
    return {
        "uptime_ms": int(ts * 1000),
        "cpu_simulated_ms": 25,
        "requests_total_estimate": 100,
    }


@app.post("/predict")
def predict(payload: Features):
    log.info(f"Prediction requested with {payload.features}")
    result = float(sum(payload.features))

    # simulate inference latency
    time.sleep(0.02)

    return {
        "prediction": result,
    }
