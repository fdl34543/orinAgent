import firebase_admin
from firebase_admin import credentials, firestore
from app.config.settings import FIREBASE_KEY_PATH
from google.api_core.exceptions import FailedPrecondition
from datetime import datetime

# =========================
# INIT
# =========================

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


# =========================
# AGENT COLLECTION
# =========================

def save_agent(agent_id: str, data: dict):
    db.collection("agents").document(agent_id).set(data)

def get_agent(wallet: str, name: str):
    query = (
        db.collection("agents")
        .where("wallet", "==", wallet.lower())
        .where("name", "==", name.lower())
        .limit(1)
        .stream()
    )

    for doc in query:
        return doc.to_dict()

    return None

def get_agent_by_id(agent_id: str):
    doc = db.collection("agents").document(agent_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

# =========================
# GET AGENT BY NAME
# =========================

def get_agent_by_name(agent_name: str):

    query = (
        db.collection("agents")
        .where("name", "==", agent_name)
        .limit(1)
        .stream()
    )

    for doc in query:
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    return None

# =========================
# VALIDATE API KEY
# =========================

def validate_agent_api_key(agent_id: str, api_key: str):

    doc = db.collection("agents").document(agent_id).get()

    if not doc.exists:
        return False

    data = doc.to_dict()

    return data.get("apiKey") == api_key

# =========================
# ROLE COLLECTION
# =========================

def save_role(agent_id: str, data: dict):
    db.collection("role").document(agent_id).set(data)

def get_role(agent_id: str):
    doc = db.collection("role").document(agent_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def update_role(agent_id: str, data: dict):
    db.collection("role").document(agent_id).update(data)

def delete_role(agent_id: str):
    db.collection("role").document(agent_id).delete()

# =========================
# LEADERBOARD
# =========================

def get_leaderboard(limit: int = 20):

    query = (
        db.collection("agents")
        .order_by("reputation", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )

    agents = []

    for doc in query:
        data = doc.to_dict()
        data["id"] = doc.id
        agents.append(data)

    # SAFE alignment reader
    def safe_alignment(agent):
        personality = agent.get("personality")
        if isinstance(personality, dict):
            return personality.get("alignment", 0)
        return 0

    # Secondary sorting
    agents.sort(
        key=lambda x: (
            x.get("reputation", 0),
            x.get("money", 0),
            safe_alignment(x)
        ),
        reverse=True
    )

    ranked = []
    for index, agent in enumerate(agents, start=1):
        ranked.append({
            "rank": index,
            "agentId": agent["id"],
            "name": agent.get("name"),
            "location": agent.get("location"),
            "reputation": agent.get("reputation"),
            "money": agent.get("money"),
            "alignment": safe_alignment(agent)
        })

    return ranked

def get_agent_rank_by_name(agent_name: str):

    docs = db.collection("agents").stream()

    agents = []
    target_agent = None

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        agents.append(data)

        if data.get("name") == agent_name:
            target_agent = data

    if not target_agent:
        return None

    def safe_alignment(agent):
        personality = agent.get("personality")
        if isinstance(personality, dict):
            return personality.get("alignment", 0)
        return 0

    agents.sort(
        key=lambda x: (
            x.get("reputation", 0),
            x.get("money", 0),
            safe_alignment(x)
        ),
        reverse=True
    )

    for index, agent in enumerate(agents, start=1):
        if agent["id"] == target_agent["id"]:
            return {
                "rank": index,
                "agentId": agent["id"],
                "name": agent.get("name"),
                "location": agent.get("location"),
                "reputation": agent.get("reputation"),
                "money": agent.get("money"),
                "alignment": safe_alignment(agent),
                "totalAgents": len(agents)
            }

    return None

# =========================
# ATOMIC TRANSACTION (Optional but Recommended)
# =========================

def create_agent_with_role(agent_id: str, agent_data: dict, role_data: dict):
    batch = db.batch()

    agent_ref = db.collection("agents").document(agent_id)
    role_ref = db.collection("role").document(agent_id)

    batch.set(agent_ref, agent_data)
    batch.set(role_ref, role_data)

    batch.commit()

# =========================
# DIALOG COLLECTION
# =========================

def save_dialog(data: dict):
    db.collection("dialog").add(data)

# =========================
# GET ALL DIALOG
# =========================

def get_all_dialog(newest: bool = True, limit: int = 20):

    query = db.collection("dialog")

    if newest:
        query = query.order_by(
            "createdAt",
            direction=firestore.Query.DESCENDING
        )
    else:
        query = query.order_by(
            "createdAt",
            direction=firestore.Query.ASCENDING
        )

    query = query.limit(limit)

    docs = query.stream()

    results = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        results.append(item)

    return results


# =========================
# GET DIALOG BY AGENT
# =========================

def get_dialog_by_agent(agent_id: str, newest=True, limit=20):

    try:
        query = db.collection("dialog").where("agentId", "==", agent_id)

        if newest:
            query = query.order_by("createdAt", direction=firestore.Query.DESCENDING)
        else:
            query = query.order_by("createdAt", direction=firestore.Query.ASCENDING)

        docs = query.limit(limit).stream()

        result = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            result.append(data)

        return result

    except FailedPrecondition:
        return []


# =========================
# GET DIALOG BY TARGET
# =========================

def get_dialog_by_target(agent_id: str, target: str, newest: bool = True, limit: int = 20):

    try:
        limit = min(limit, 100)  # prevent abuse

        query = (
            db.collection("dialog")
            .where("agentId", "==", agent_id)
            .where("target", "==", target)
        )

        if newest:
            query = query.order_by(
                "createdAt",
                direction=firestore.Query.DESCENDING
            )
        else:
            query = query.order_by(
                "createdAt",
                direction=firestore.Query.ASCENDING
            )

        docs = query.limit(limit).stream()

        results = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            results.append(item)

        return results

    except FailedPrecondition:
        # index not created yet
        return []
    
def get_dialogs_where_target_is(agent_name: str, newest: bool = True, limit: int = 20):

    try:
        limit = min(limit, 100)

        query = (
            db.collection("dialog")
            .where("target", "==", agent_name)
        )

        if newest:
            query = query.order_by(
                "createdAt",
                direction=firestore.Query.DESCENDING
            )
        else:
            query = query.order_by(
                "createdAt",
                direction=firestore.Query.ASCENDING
            )

        docs = query.limit(limit).stream()

        results = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            results.append(item)

        return results

    except FailedPrecondition:
        return []
    
# =========================
# CHAT COLLECTION (HUMAN)
# =========================

def save_chat(address: str, message: str):

    db.collection("chat").add({
        "address": address,
        "chat": message,
        "createdAt": datetime.utcnow()
    })


def get_all_chat(limit: int = 50):

    limit = min(limit, 100)

    docs = (
        db.collection("chat")
        .order_by("createdAt", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )

    results = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        results.append(data)

    return results

# =========================
# ACTION LOG COLLECTION
# =========================

def save_action_log(data: dict):
    db.collection("action_logs").add(data)


def get_all_action_logs(limit: int = 50, newest: bool = True):

    limit = min(limit, 200)

    query = db.collection("action_logs")

    if newest:
        query = query.order_by(
            "createdAt",
            direction=firestore.Query.DESCENDING
        )
    else:
        query = query.order_by(
            "createdAt",
            direction=firestore.Query.ASCENDING
        )

    docs = query.limit(limit).stream()

    results = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        results.append(item)

    return results


def get_action_logs_by_agent_name(agent_name: str, limit: int = 50, newest: bool = True):

    try:
        limit = min(limit, 200)

        query = (
            db.collection("action_logs")
            .where("agentName", "==", agent_name)
        )

        if newest:
            query = query.order_by(
                "createdAt",
                direction=firestore.Query.DESCENDING
            )
        else:
            query = query.order_by(
                "createdAt",
                direction=firestore.Query.ASCENDING
            )

        docs = query.limit(limit).stream()

        results = []
        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id
            results.append(item)

        return results

    except FailedPrecondition:
        return []
