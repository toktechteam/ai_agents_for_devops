from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

def test_investigate():
    resp = client.post("/investigate", json={
        "alert_type": "high_cpu",
        "service": "svc"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "steps" in data
