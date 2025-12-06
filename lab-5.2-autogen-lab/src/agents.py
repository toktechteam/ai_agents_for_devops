from autogen import AssistantAgent


def create_agents(api_key: str):
    commander = AssistantAgent(
        name="incident_commander",
        system_message=(
            "You are the Incident Commander. Your role is to receive alerts and "
            "request investigation from the SRE Investigator."
        ),
        llm_config={"model": "gpt-4o-mini", "api_key": api_key},
    )

    investigator = AssistantAgent(
        name="sre_investigator",
        system_message=(
            "You are an SRE Investigator. Provide:\n"
            "- Root cause\n"
            "- Summary of findings\n"
            "- 1–2 remediation steps\n"
            "Keep responses short and precise."
        ),
        llm_config={"model": "gpt-4o-mini", "api_key": api_key},
    )

    return commander, investigator
