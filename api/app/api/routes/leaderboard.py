from fastapi import APIRouter, Query
from app.core.firebase_service import get_leaderboard, get_agent_rank_by_name

router = APIRouter(prefix="/leaderboard")


@router.get("")
def leaderboard(limit: int = Query(20)):
    data = get_leaderboard(limit)

    return {
        "status": "success",
        "total": len(data),
        "topAgents": data
    }

@router.get("/{agentName}")
def leaderboard_by_name(agentName: str):

    result = get_agent_rank_by_name(agentName)

    if not result:
        return {
            "status": "error",
            "message": "Agent not found."
        }

    return {
        "status": "success",
        "agent": result
    }