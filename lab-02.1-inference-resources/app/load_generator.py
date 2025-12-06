import argparse
import json
import time
from statistics import mean
from typing import List

import requests


def send_requests(url: str, num_requests: int) -> None:
    latencies: List[float] = []
    errors = 0
    payload = {"features": [1.0, 2.0, 3.0]}

    start = time.time()
    for _ in range(num_requests):
        t0 = time.time()
        try:
            resp = requests.post(url, json=payload, timeout=5)
            latency_ms = (time.time() - t0) * 1000.0
            if resp.status_code != 200:
                errors += 1
            else:
                latencies.append(latency_ms)
        except Exception:
            errors += 1
    total_time = time.time() - start

    if latencies:
        avg_latency = mean(latencies)
    else:
        avg_latency = 0.0

    summary = {
        "url": url,
        "requests": num_requests,
        "total_time_sec": round(total_time, 3),
        "avg_latency_ms": round(avg_latency, 2),
        "errors": errors,
    }
    print(json.dumps(summary))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple load generator for Lab 2.1 FREE API"
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Target /predict URL (e.g. http://localhost:8001/predict)",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=20,
        help="Number of requests to send (default: 20)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    send_requests(args.url, args.requests)


if __name__ == "__main__":
    main()
