from fastapi import APIRouter
from app.core.firebase_service import get_agent_by_id, get_role, get_agent_by_name

router = APIRouter(prefix="/agent")

@router.get("/{agentId}")
def get_agent(agentId: str):

    agent = get_agent_by_id(agentId)
    role = get_role(agentId)

    if not agent:
        return {"status": "error", "message": "Agent not found."}

    return {
        "status": "success",
        "agent": agent,
        "role": role
    }

@router.get("/name/{agentName}")
def get_agent_by_name_endpoint(agentName: str):

    agent = get_agent_by_name(agentName)

    if not agent:
        return {
            "status": "error",
            "message": "Agent not found."
        }

    from app.core.firebase_service import get_role
    role = get_role(agent["id"])

    return {
        "status": "success",
        "agent": agent,
        "role": role
    }
