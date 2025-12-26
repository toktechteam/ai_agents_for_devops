# tests/test_agents.py

from agents import IncidentCommander, SREInvestigator


def test_incident_commander_response():
    commander = IncidentCommander()
    response = commander.respond("test alert")
    assert "Delegating" in response


def test_sre_investigator_response():
    investigator = SREInvestigator()
    response = investigator.respond("investigate")
    assert "Analysis complete" in response
