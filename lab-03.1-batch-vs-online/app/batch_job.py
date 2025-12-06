import json
from pathlib import Path
from typing import List, Dict


DATA_PATH = Path(__file__).parent / "data" / "input.jsonl"


def process_record(record: Dict) -> Dict:
    """
    Given a record like:
      {"id": 1, "features": [1.0, 2.0, 3.0]}
    Return:
      {"id": 1, "prediction": 6.0}
    """
    features = record.get("features", [])
    prediction = float(sum(features))
    return {"id": record.get("id"), "prediction": prediction}


def run_batch(input_path: Path = DATA_PATH) -> List[Dict]:
    """
    Runs batch inference over all lines in input_path.
    Returns list of prediction dicts.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    results: List[Dict] = []

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            result = process_record(record)
            results.append(result)

    return results


def main() -> None:
    results = run_batch(DATA_PATH)
    # Print each prediction as JSONL
    for r in results:
        print(json.dumps(r))

    if results:
        avg_pred = sum(r["prediction"] for r in results) / len(results)
        summary = {
            "summary": {
                "records": len(results),
                "avg_prediction": avg_pred,
            }
        }
        print(json.dumps(summary))


if __name__ == "__main__":
    main()
