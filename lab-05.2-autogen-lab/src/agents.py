# src/agents.py

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def respond(self, message: str) -> str:
        raise NotImplementedError


class IncidentCommander(Agent):
    def __init__(self):
        super().__init__(
            name="IncidentCommander",
            role="Orchestrates investigation and delegates tasks"
        )

    def respond(self, message: str) -> str:
        return (
            "Investigation plan created. "
            "Delegating root cause analysis to SRE Investigator."
        )


class SREInvestigator(Agent):
    def __init__(self):
        super().__init__(
            name="SREInvestigator",
            role="Analyzes system signals and finds root cause"
        )

    def respond(self, message: str) -> str:
        return (
            "Analysis complete. High CPU observed due to traffic spike. "
            "Recommend scaling replicas and enabling HPA."
        )
