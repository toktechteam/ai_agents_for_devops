from .memory import Memory
from .tools import Tools
from .cost import CostTracker
from .metrics import agent_requests_total, agent_tokens_total, agent_average_cost


class ChainEngine:
    """
    Simulates LangChain-style planning-execution-summarization pipeline.
    """

    def __init__(self):
        self.memory = Memory()
        self.tools = Tools()

    def _build_plan(self, alert_type: str):
        if alert_type == "high_cpu":
            return ["check_pods", "fetch_metrics"]
        elif alert_type == "high_latency":
            return ["fetch_metrics", "check_logs"]
        return ["check_pods"]

    def _execute_step(self, step: str, service: str):
        if step == "check_pods":
            return self.tools.get_pods(service)
        if step == "fetch_metrics":
            return self.tools.get_metrics(service)
        if step == "check_logs":
            return self.tools.get_logs(service)
        return "[UNKNOWN STEP]"

    def run(self, alert: dict):
        agent_requests_total.inc()

        alert_type = alert["alert_type"]
        service = alert["service"]

        plan = self._build_plan(alert_type)

        self.memory.remember("last_service", service)

        steps_output = []
        cost = CostTracker()

        for step in plan:
            result = self._execute_step(step, service)
            token_usage = len(result)
            cost.add_tokens(token_usage)
            agent_tokens_total.inc(token_usage)

            steps_output.append({
                "step": step,
                "result": result
            })

        cost_summary = cost.summary()
        agent_average_cost.set(cost_summary["usd"])

        return {
            "alert": alert,
            "plan": plan,
            "steps": steps_output,
            "cost": cost_summary,
            "memory": self.memory.dump()
        }
