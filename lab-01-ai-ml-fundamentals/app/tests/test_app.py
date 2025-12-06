from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_predict_basic():
    payload = {"features": [1.0, 2.0, 3.5]}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] == 6.5
    assert "model_latency_ms" in data
    assert isinstance(data["model_latency_ms"], int)
