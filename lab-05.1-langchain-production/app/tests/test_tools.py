from app.tools import Tools

def test_tools_outputs():
    t = Tools()
    assert "pods" in t.get_pods("svc")
    assert "logs" in t.get_logs("svc")
    assert "metrics" in t.get_metrics("svc")
