# src/workflow.py

from agents import IncidentCommander, SREInvestigator


class IncidentWorkflow:
    def __init__(self):
        self.commander = IncidentCommander()
        self.investigator = SREInvestigator()

    def run(self, alert: str) -> dict:
        commander_msg = self.commander.respond(alert)
        investigator_msg = self.investigator.respond(commander_msg)

        return {
            "alert": alert,
            "commander_output": commander_msg,
            "investigator_output": investigator_msg,
        }
