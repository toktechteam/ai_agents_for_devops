from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import time

app = FastAPI(title="AI Lab Free - Simple Inference API")


class Features(BaseModel):
    features: List[float] = Field(..., min_length=1)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: Features):
    try:
        # Simulated "model": sum of features
        prediction = float(sum(payload.features))
    except Exception as exc:  # defensive
        raise HTTPException(status_code=400, detail=str(exc))

    # Simulate fixed model latency (e.g., 50ms)
    simulated_latency_ms = 50
    time.sleep(simulated_latency_ms / 1000.0)

    return {
        "prediction": prediction,
        "model_latency_ms": simulated_latency_ms,
    }