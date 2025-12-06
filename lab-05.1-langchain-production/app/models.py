from pydantic import BaseModel

class Alert(BaseModel):
    alert_type: str
    service: str
