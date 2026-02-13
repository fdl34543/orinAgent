from fastapi import APIRouter
from app.core.firebase_service import get_agent_by_name

router = APIRouter(prefix="/inventory")


@router.get("/{agentName}")
def get_inventory(agentName: str):

    agent = get_agent_by_name(agentName)

    if not agent:
        return {
            "status": "error",
            "message": "Agent not found."
        }

    inventory = agent.get("inventory", {})
    equipped = agent.get("equipped", None)

    total_items = sum(inventory.values())

    return {
        "status": "success",
        "agentId": agent["id"],
        "name": agent["name"],
        "location": agent.get("location"),
        "equipped": equipped,
        "totalItems": total_items,
        "inventory": inventory
    }
