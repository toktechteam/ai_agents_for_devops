import httpx
import time

API = "http://localhost:8000"

def test_ingest_then_search():
    # Ingest
    r = httpx.post(f"{API}/ingest", timeout=120.0)
    assert r.status_code == 200
    assert r.json()["inserted"] > 0

    # Search (semantic)
    payload = {"query": "pod keeps restarting crash loop", "top_k": 3}
    r2 = httpx.post(f"{API}/search", json=payload, timeout=60.0)
    assert r2.status_code == 200
    hits = r2.json()["hits"]
    assert len(hits) >= 1

    # We expect a Kubernetes crash loop runbook to show up near top
    titles = [h["title"].lower() for h in hits]
    assert any("crashloop" in t or "kubernetes" in t for t in titles)
