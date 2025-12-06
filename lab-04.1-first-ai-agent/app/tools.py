from typing import Any, Callable, Dict


class ToolRegistry:
    """
    Minimal "tool registry" to match Chapter 4's Tool Usage concept.

    In this free lab, tools are just Python functions that return
    fake strings instead of calling real Kubernetes, Prometheus, etc.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., Any]] = {
            "get_pods": self.get_pods,
            "get_pod_logs": self.get_pod_logs,
            "get_service_metrics": self.get_service_metrics,
        }

    def get(self, name: str) -> Callable[..., Any]:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Unknown tool: {name}")
        return tool

    def list_tools(self) -> Dict[str, str]:
        return {
            "get_pods": "Simulate listing pods in a namespace",
            "get_pod_logs": "Simulate fetching pod logs",
            "get_service_metrics": "Simulate service performance metrics",
        }

    # --- Fake tool implementations below ---

    def get_pods(self, namespace: str) -> str:
        return f"[FAKE] Pods in namespace '{namespace}': web-abc, web-def, api-xyz"

    def get_pod_logs(self, pod: str, namespace: str = "default") -> str:
        return f"[FAKE] Last 3 log lines for pod '{pod}' in ns '{namespace}'"

    def get_service_metrics(self, service: str) -> str:
        return f"[FAKE] Metrics for service '{service}': latency_p95=180ms, error_rate=0.2%"
