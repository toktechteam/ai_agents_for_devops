import httpx

API = "http://localhost:8000"

def test_health():
    r = httpx.get(f"{API}/health", timeout=10.0)
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
