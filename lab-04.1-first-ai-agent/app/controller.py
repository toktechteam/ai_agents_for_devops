from fastapi import FastAPI
from agent import SimpleAgent

app = FastAPI()
agent = SimpleAgent()

@app.post("/alerts")
def receive_alert(alert: dict):
    return agent.handle_alert(alert)
