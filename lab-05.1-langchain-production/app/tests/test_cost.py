from app.cost import CostTracker

def test_cost_tracker():
    c = CostTracker()
    c.add_tokens(100)
    summary = c.summary()
    assert summary["tokens"] == 100
    assert summary["usd"] > 0
