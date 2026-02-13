from fastapi import APIRouter
from app.core.law_service import (
    evaluate_crime,
    police_arrest,
    get_crime_history
)


router = APIRouter(prefix="/law")

@router.post("/evaluate")
def law_evaluate(agentId: str):
    return evaluate_crime(agentId)

@router.post("/arrest")
def law_arrest(officerId: str, targetId: str, reason: str):
    return police_arrest(officerId, targetId, reason)

@router.get("/history/{agentId}")
def crime_history(agentId: str):
    logs = get_crime_history(agentId)

    return {
        "status": "success",
        "agentId": agentId,
        "totalRecords": len(logs),
        "history": logs
    }
