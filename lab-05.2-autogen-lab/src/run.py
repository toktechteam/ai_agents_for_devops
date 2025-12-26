# src/run.py

from workflow import IncidentWorkflow


def main():
    workflow = IncidentWorkflow()
    alert = "High CPU alert on payment-service"
    result = workflow.run(alert)

    print("=== INCIDENT WORKFLOW RESULT ===")
    print(f"Alert: {result['alert']}")
    print(f"Commander: {result['commander_output']}")
    print(f"Investigator: {result['investigator_output']}")


if __name__ == "__main__":
    main()

