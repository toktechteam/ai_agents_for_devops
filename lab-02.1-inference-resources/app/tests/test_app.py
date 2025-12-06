from fastapi.testclient import TestClient
from main import app, CPU_BURN_MS

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["mode"] == "free"
    assert data["cpu_burn_ms"] == CPU_BURN_MS


def test_predict():
    payload = {"features": [1.0, 2.0, 3.0]}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["prediction"] == 6.0
    assert data["cpu_burn_ms"] == CPU_BURN_MS
