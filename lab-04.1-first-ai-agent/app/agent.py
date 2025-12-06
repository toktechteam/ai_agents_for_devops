from typing import Any, Dict, List

from memory import Memory
from tools import ToolRegistry
from executor import SafeExecutor


class SimpleAgent:
    """
    A minimal "Infrastructure Investigation Agent".

    - Receives an alert (type + service)
    - Builds a very simple investigation plan
    - Executes tools via SafeExecutor
    - Stores alert in memory
    - Returns investigation report
    """

    def __init__(self) -> None:
        self.memory = Memory()
        self.tools = ToolRegistry()
        self.executor = SafeExecutor()

    def build_plan(self, alert: Dict[str, Any]) -> List[Dict[str, Any]]:
        alert_type = alert.get("type", "unknown")
        service = alert.get("service", "unknown")

        # Very simple branching based on alert type
        if alert_type == "high_cpu":
            return [
                {
                    "step": "list_pods",
                    "tool": "get_pods",
                    "params": {"namespace": "default"},
                },
                {
                    "step": "check_service_metrics",
                    "tool": "get_service_metrics",
                    "params": {"service": service},
                },
            ]
        elif alert_type == "high_memory":
            return [
                {
                    "step": "list_pods",
                    "tool": "get_pods",
                    "params": {"namespace": "default"},
                },
                {
                    "step": "check_logs",
                    "tool": "get_pod_logs",
                    "params": {"pod": f"{service}-pod", "namespace": "default"},
                },
            ]
        else:
            return [
                {
                    "step": "list_pods",
                    "tool": "get_pods",
                    "params": {"namespace": "default"},
                }
            ]

    def handle_alert(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        # Store the latest alert in memory like "working memory"
        self.memory.remember("last_alert", alert)

        plan = self.build_plan(alert)
        investigation_results: List[Dict[str, Any]] = []

        for item in plan:
            tool_name = item["tool"]
            params = item["params"]
            tool_fn = self.tools.get(tool_name)
            exec_result = self.executor.run(tool_fn, params)
            investigation_results.append(
                {
                    "step": item["step"],
                    "tool": tool_name,
                    "params": params,
                    "execution": exec_result,
                }
            )

        return {
            "alert": alert,
            "plan": plan,
            "investigation": investigation_results,
            "memory_snapshot": self.memory.dump(),
        }
