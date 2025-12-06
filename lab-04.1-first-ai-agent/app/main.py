from fastapi import FastAPI
from pydantic import BaseModel

from agent import SimpleAgent


class Alert(BaseModel):
    type: str
    service: str


app = FastAPI(
    title="Lab 4.1 Free - Infrastructure Investigation Agent",
    version="1.0.0",
)

_agent = SimpleAgent()


@app.get("/health")
def health():
    """
    Simple health endpoint.
    """
    return {"status": "ok", "version": "1.0.0"}


@app.post("/alerts")
def receive_alert(alert: Alert):
    """
    Receive an alert and let the agent investigate.
    """
    result = _agent.handle_alert(alert.dict())
    return result
