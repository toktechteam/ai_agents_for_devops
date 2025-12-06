from tools import ToolRegistry


def test_tool_registry_get_and_list():
    reg = ToolRegistry()
    tools = reg.list_tools()
    assert "get_pods" in tools
    assert "get_pod_logs" in tools
    assert "get_service_metrics" in tools

    tool_fn = reg.get("get_pods")
    out = tool_fn(namespace="default")
    assert "[FAKE]" in out
    assert "Pods in namespace" in out
