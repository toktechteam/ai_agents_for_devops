import argparse
import time
import requests


def load(url: str, count: int):
    payload = {"features": [1.0, 2.0, 3.0]}

    for i in range(count):
        t0 = time.time()
        try:
            r = requests.post(url, json=payload, timeout=5)
            print(f"{i} -> {r.status_code}, {round((time.time()-t0)*1000,2)}ms")
        except Exception as e:
            print(f"{i} -> error: {e}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--count", type=int, default=10)
    args = ap.parse_args()
    load(args.url, args.count)
