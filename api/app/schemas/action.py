from pydantic import BaseModel
from typing import Optional, Dict, Any


class ActionRequest(BaseModel):
    agentId: str
    apiKey: str
    action: str
    target: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
