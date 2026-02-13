from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    address: str = Field(..., example="0x630cc3A2C5135B2C5E492F27372D500Aa96f1822")
    chat: str = Field(..., example="Orin is evolving.")
