import os
from agents import create_agents
from workflow import run_workflow


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Missing OPENAI_API_KEY. Set it using:")
        print('export OPENAI_API_KEY="your-key"')
        return

    commander, investigator = create_agents(api_key)

    alert = "High CPU detected on pod payment-service-1123."
    run_workflow(commander, investigator, alert)


if __name__ == "__main__":
    main()
