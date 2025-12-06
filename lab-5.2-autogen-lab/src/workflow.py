def run_workflow(commander, investigator, alert: str):
    print(f" Incident Commander received alert: {alert}\n")

    prompt = (
        f"Alert received: {alert}\n"
        "Please investigate the issue and provide root cause, summary, "
        "and remediation steps."
    )

    response = investigator.complete(prompt)

    print(" Investigator Analysis:")
    print(response.content)

    return response.content
