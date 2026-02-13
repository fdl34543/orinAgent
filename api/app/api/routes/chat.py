from fastapi import APIRouter
from app.core.firebase_service import save_chat, get_all_chat
from app.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat")


@router.post("")
def post_chat(payload: ChatRequest):

    save_chat(payload.address, payload.chat)

    return {
        "status": "success",
        "message": "Chat message posted."
    }


@router.get("/all")
def chat_all(limit: int = 50):

    chats = get_all_chat(limit)

    return {
        "status": "success",
        "total": len(chats),
        "chats": chats
    }
