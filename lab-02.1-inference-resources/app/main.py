import time
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Lab 2.1 - Resource-Aware Inference API")


class Features(BaseModel):
    features: List[float] = Field(..., min_length=1)


CPU_BURN_MS = 30  # small CPU burn to simulate inference


def cpu_burn(milliseconds: int) -> None:
    """Busy-loop to simulate CPU usage for a given number of milliseconds."""
    end = time.time() + (milliseconds / 1000.0)
    x = 0.0
    while time.time() < end:
        x += 1.0  # noqa: F841


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "free",
        "cpu_burn_ms": CPU_BURN_MS,
    }


@app.post("/predict")
def predict(payload: Features):
    try:
        prediction = float(sum(payload.features))
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=400, detail=str(exc))

    cpu_burn(CPU_BURN_MS)

    return {
        "prediction": prediction,
        "cpu_burn_ms": CPU_BURN_MS,
    }

