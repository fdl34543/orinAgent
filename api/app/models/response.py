from pydantic import BaseModel
from typing import Dict, Any

class AgentResponse(BaseModel):
    id: str
    name: str
    location: str
    skill: Dict[str, Any]
    money: int
    reputation: int
    personality: str
