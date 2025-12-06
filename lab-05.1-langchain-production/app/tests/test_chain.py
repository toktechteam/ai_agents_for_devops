from app.chain import ChainEngine

def test_chain_execution():
    engine = ChainEngine()
    alert = {"alert_type": "high_cpu", "service": "payment-api"}
    result = engine.run(alert)

    assert "steps" in result
    assert len(result["steps"]) == 2
    assert result["cost"]["tokens"] > 0
