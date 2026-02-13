from datetime import datetime, timedelta
import random
from uuid import uuid4
from app.core.firebase_service import (
    get_agent_by_id,
    get_role,
    update_role,
    db
)
from google.api_core.exceptions import FailedPrecondition
from firebase_admin import firestore

def log_crime(agent_id: str, reason: str, crime_score: int, arrested_by: str = None):

    log_id = str(uuid4())

    db.collection("crime_logs").document(log_id).set({
        "agentId": agent_id,
        "reason": reason,
        "crimeScore": crime_score,
        "arrestedBy": arrested_by,
        "createdAt": datetime.utcnow()
    })


def evaluate_crime(agent_id: str):

    agent = get_agent_by_id(agent_id)
    role = get_role(agent_id)

    if not agent:
        return {"status": "error", "message": "Agent not found."}

    if role.get("isJailed"):
        return {
            "status": "already_jailed",
            "jailUntil": role.get("jailUntil")
        }

    personality = agent["personality"]
    reputation = agent["reputation"]

    crime_score = 0

    crime_score += len(personality["badSide"]) * 2
    crime_score -= len(personality["goodSide"])
    crime_score -= int(personality["alignment"] / 25)
    crime_score -= int(reputation / 10)
    crime_score += random.randint(-5, 5)

    if crime_score >= 5:
        jail_minutes = 5

        update_role(agent_id, {
            "isJailed": True,
            "jailUntil": datetime.utcnow() + timedelta(minutes=jail_minutes)
        })

        log_crime(
            agent_id=agent_id,
            reason="Automatic crime evaluation",
            crime_score=crime_score
        )

        return {
            "status": "arrested",
            "crimeScore": crime_score,
            "jailMinutes": jail_minutes
        }

    return {"status": "safe", "crimeScore": crime_score}

def police_arrest(officer_id: str, target_id: str, reason: str):

    officer_role = get_role(officer_id)
    target_role = get_role(target_id)

    if not officer_role:
        return {"status": "error", "message": "Officer not found."}

    if officer_role.get("Job") not in ["Officer", "Detective", "Guardian"]:
        return {
            "status": "forbidden",
            "message": "Only Police roles can arrest."
        }

    if target_role.get("isJailed"):
        return {
            "status": "error",
            "message": "Target already jailed."
        }

    jail_minutes = 10

    update_role(target_id, {
        "isJailed": True,
        "jailUntil": datetime.utcnow() + timedelta(minutes=jail_minutes)
    })

    log_crime(
        agent_id=target_id,
        reason=reason,
        crime_score=999,
        arrested_by=officer_id
    )

    return {
        "status": "success",
        "message": "Target arrested.",
        "jailMinutes": jail_minutes
    }

def get_crime_history(agentId: str):

    try:
        logs = (
            db.collection("crime_logs")
            .where("agentId", "==", agentId)
            .order_by("createdAt", direction=firestore.Query.DESCENDING)
            .stream()
        )

        result = []
        for doc in logs:
            data = doc.to_dict()
            data["id"] = doc.id
            result.append(data)

        return result

    except FailedPrecondition:
        return []