from fastapi import APIRouter
from app.core.action_service import handle_action
from app.core.firebase_service import validate_agent_api_key
from app.schemas.action import ActionRequest
from app.core.firebase_service import (
    get_all_action_logs,
    get_action_logs_by_agent_name
)

router = APIRouter(prefix="/action")

@router.post("")
def action(payload: ActionRequest):

    if not validate_agent_api_key(payload.agentId, payload.apiKey):
        return {
            "status": "unauthorized",
            "message": "Invalid apiKey."
        }

    return handle_action(
        payload.agentId,
        payload.action,
        payload.target,
        payload.params
    )

@router.get("/history/all")
def action_history_all(limit: int = 50, newest: bool = True):

    logs = get_all_action_logs(limit, newest)

    return {
        "status": "success",
        "total": len(logs),
        "logs": logs
    }


@router.get("/history/{agentName}")
def action_history_by_agent(agentName: str, limit: int = 50, newest: bool = True):

    logs = get_action_logs_by_agent_name(agentName, limit, newest)

    return {
        "status": "success",
        "agent": agentName,
        "total": len(logs),
        "logs": logs
    }