from agent import SimpleAgent


def test_agent_builds_plan_for_high_cpu():
    agent = SimpleAgent()
    alert = {"type": "high_cpu", "service": "payment-api"}
    plan = agent.build_plan(alert)
    assert len(plan) == 2
    assert {step["tool"] for step in plan} == {"get_pods", "get_service_metrics"}


def test_agent_handle_alert_populates_memory_and_investigation():
    agent = SimpleAgent()
    alert = {"type": "high_memory", "service": "web-app"}
    result = agent.handle_alert(alert)

    assert result["alert"] == alert
    assert "plan" in result
    assert "investigation" in result
    assert "memory_snapshot" in result
    assert result["memory_snapshot"]["last_alert"] == alert
    assert len(result["investigation"]) >= 1
