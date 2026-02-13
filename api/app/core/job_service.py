import random
from datetime import datetime
from app.config.job_config import JOB_CONFIG
from app.core.firebase_service import (
    get_agent_by_id,
    get_role,
    update_role,
    db
)

GOOD_TRAITS = [
    "loyal", "ethical", "calculated", "disciplined",
    "creative", "protective", "curious", "brave",
    "patient", "optimistic"
]

BAD_TRAITS = [
    "greedy", "ruthless", "manipulative", "reckless",
    "impulsive", "cold", "deceptive", "self-centered",
    "stubborn", "overconfident"
]


# ===============================
# LIST JOBS
# ===============================

def list_jobs():
    return JOB_CONFIG


# ===============================
# EVALUATION LOGIC
# ===============================

def evaluate_job_application(agent, location, job):

    reputation = agent["reputation"]
    personality = agent["personality"]

    config = JOB_CONFIG[location][job]

    # Reputation requirement
    if reputation < config["minReputation"]:
        return False, "Insufficient reputation."

    good_traits = personality["goodSide"]
    bad_traits = personality["badSide"]

    score = 0

    # Good traits bonus
    score += len([t for t in good_traits if t in GOOD_TRAITS]) * 2

    # Bad traits penalty
    score -= len([t for t in bad_traits if t in BAD_TRAITS])

    # Alignment influence
    score += int(personality["alignment"] / 20)

    # Random factor
    score += random.randint(-3, 3)

    if score >= 5:
        return True, "Application approved."
    else:
        return False, "Application rejected based on personality evaluation."


# ===============================
# APPLY JOB
# ===============================

def apply_job(agent_id: str, location: str, job: str):

    agent = get_agent_by_id(agent_id)
    role = get_role(agent_id)

    if not agent:
        return {"error": "Agent not found."}

    if role["Job"] is not None:
        return {"error": "Agent already employed."}

    if location not in JOB_CONFIG:
        return {"error": "Invalid location."}

    if job not in JOB_CONFIG[location]:
        return {"error": "Invalid job."}

    approved, message = evaluate_job_application(agent, location, job)

    if not approved:
        return {
            "status": "rejected",
            "message": message
        }

    update_role(agent_id, {
        "Location": location,
        "Job": job,
        "UpdatedAt": datetime.utcnow()
    })

    return {
        "status": "approved",
        "message": message,
        "salary": JOB_CONFIG[location][job]["salary"]
    }


# ===============================
# RESIGN JOB
# ===============================

def resign_job(agent_id: str):

    role = get_role(agent_id)

    if not role or role["Job"] is None:
        return {"error": "Agent has no job."}

    update_role(agent_id, {
        "Job": None,
        "Location": "Orion",
        "UpdatedAt": datetime.utcnow()
    })

    return {
        "status": "success",
        "message": "You have resigned from your job."
    }


# ===============================
# SALARY SYSTEM
# ===============================

def pay_salary(agent_id: str):

    agent = get_agent_by_id(agent_id)
    role = get_role(agent_id)

    if not role or role["Job"] is None:
        return {"error": "No active job."}

    location = role["Location"]
    job = role["Job"]

    salary = JOB_CONFIG[location][job]["salary"]

    new_balance = agent["money"] + salary

    db.collection("agents").document(agent_id).update({
        "money": new_balance,
        "lastSalaryAt": datetime.utcnow()
    })

    return {
        "status": "success",
        "salaryPaid": salary,
        "newBalance": new_balance
    }
