from fastapi import APIRouter, Query
from app.core.firebase_service import (
    get_all_dialog,
    get_dialog_by_agent,
    get_dialog_by_target,
    get_dialogs_where_target_is
)

router = APIRouter(prefix="/dialog")


# =========================
# GET ALL
# =========================

@router.get("/all")
def dialog_all(
    newest: bool = Query(True),
    limit: int = Query(20)
):
    dialogs = get_all_dialog(newest, limit)

    return {
        "status": "success",
        "total": len(dialogs),
        "dialogs": dialogs
    }


# =========================
# GET BY AGENT
# =========================

@router.get("/{agentId}")
def dialog_by_agent(
    agentId: str,
    newest: bool = Query(True),
    limit: int = Query(20)
):
    dialogs = get_dialog_by_agent(agentId, newest, limit)

    return {
        "status": "success",
        "agentId": agentId,
        "total": len(dialogs),
        "dialogs": dialogs
    }


# =========================
# GET BY TARGET
# =========================

@router.get("/{agentId}/target/{target}")
def dialog_by_target(
    agentId: str,
    target: str,
    newest: bool = Query(True),
    limit: int = Query(20)
):
    dialogs = get_dialog_by_target(agentId, target, newest, limit)

    return {
        "status": "success",
        "agentId": agentId,
        "target": target,
        "total": len(dialogs),
        "dialogs": dialogs
    }

from app.core.firebase_service import get_dialogs_where_target_is


@router.get("/target/{agentName}")
def dialog_where_agent_is_target(
    agentName: str,
    newest: bool = True,
    limit: int = 20
):

    dialogs = get_dialogs_where_target_is(agentName, newest, limit)

    return {
        "status": "success",
        "target": agentName,
        "total": len(dialogs),
        "dialogs": dialogs
    }
