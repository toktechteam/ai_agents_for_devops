from src.agents import create_agents


def test_agent_creation():
    commander, investigator = create_agents("dummy")
    assert commander.name == "incident_commander"
    assert investigator.name == "sre_investigator"
