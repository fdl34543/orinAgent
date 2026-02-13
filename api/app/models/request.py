from pydantic import BaseModel

class EnterRequest(BaseModel):
    wallet: str
    name: str
