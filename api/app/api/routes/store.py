from fastapi import APIRouter
from app.core.store_service import (
    list_store_items,
    buy_item,
    use_item
)

router = APIRouter(prefix="/store")


@router.get("/list")
def store_list():
    return {
        "status": "success",
        "items": list_store_items()
    }


@router.post("/buy")
def store_buy(agentId: str, itemId: str):
    return buy_item(agentId, itemId)


@router.post("/use")
def store_use(agentId: str, itemId: str):
    return use_item(agentId, itemId)
