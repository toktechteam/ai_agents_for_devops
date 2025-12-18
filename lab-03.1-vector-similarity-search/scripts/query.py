import sys
import httpx

API = "http://localhost:8000"

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/query.py \"your query here\"")
        raise SystemExit(1)

    query = sys.argv[1]
    payload = {"query": query, "top_k": 5}

    r = httpx.post(f"{API}/search", json=payload, timeout=60.0)
    r.raise_for_status()
    data = r.json()

    print(f"\nQuery: {data['query']}\n")
    for i, h in enumerate(data["hits"], start=1):
        print(f"{i}. score={h['score']:.4f} | {h['title']} | service={h['service']} | severity={h['severity']}")
        print(f"   {h['content']}\n")

if __name__ == "__main__":
    main()
