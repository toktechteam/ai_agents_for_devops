import httpx

API = "http://localhost:8000"

if __name__ == "__main__":
    r = httpx.post(f"{API}/ingest", timeout=120.0)
    r.raise_for_status()
    print(r.json())
