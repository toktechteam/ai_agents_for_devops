import json
from pathlib import Path

from batch_job import process_record, run_batch


def test_process_record_sum():
    record = {"id": 1, "features": [1.0, 2.0, 3.0]}
    result = process_record(record)
    assert result["id"] == 1
    assert result["prediction"] == 6.0


def test_run_batch_uses_input_file(tmp_path: Path):
    # Prepare a temporary input file
    input_file = tmp_path / "input.jsonl"
    sample_records = [
        {"id": 1, "features": [1.0, 2.0]},
        {"id": 2, "features": [3.0, 4.0]},
    ]
    with input_file.open("w", encoding="utf-8") as f:
        for r in sample_records:
            f.write(json.dumps(r) + "\n")

    results = run_batch(input_file)
    assert len(results) == 2
    assert results[0]["prediction"] == 3.0
    assert results[1]["prediction"] == 7.0
