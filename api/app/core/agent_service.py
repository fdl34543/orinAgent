from uuid import uuid4
import secrets
from datetime import datetime
import random
from app.core.firebase_service import (
    save_agent,
    get_agent,
    save_role,
    get_agent_by_id,
    db
)

GOOD_TRAITS = [
    "loyal",
    "ethical",
    "calculated",
    "disciplined",
    "creative",
    "protective",
    "curious",
    "brave",
    "patient",
    "optimistic"
]

BAD_TRAITS = [
    "greedy",
    "ruthless",
    "manipulative",
    "reckless",
    "impulsive",
    "cold",
    "deceptive",
    "self-centered",
    "stubborn",
    "overconfident"
]

ADMIN_WALLET = "0x630cc3a2c5135b2c5e492f27372d500aa96f1822"

LOCATIONS = ["Hall", "Police", "Hospital", "Cafe", "Office", "Store"]

LOCATION_JOBS = {
    "Hall": ["Coordinator", "Archivist"],
    "Police": ["Officer", "Detective", "Guardian"],
    "Hospital": ["Medic", "Surgeon"],
    "Cafe": ["Barista", "Information Broker"],
    "Office": ["Strategist", "Analyst", "Contractor"],
    "Store": ["Merchant", "Trader"]
}


def generate_personality():
    alignment = random.randint(0, 100)

    good_traits = random.sample(GOOD_TRAITS, k=3)
    bad_traits = random.sample(BAD_TRAITS, k=3)

    return {
        "alignment": alignment,
        "goodSide": good_traits,
        "badSide": bad_traits
    }

def assign_role(wallet: str, agent_id: str):

    wallet_lower = wallet.lower()

    base_role = {
        "AgentID": agent_id,
        "AgentRole": "Citizen",
        "Location": "Orion",
        "Job": None,
        "CreatedAt": datetime.utcnow()
    }

    if wallet_lower == ADMIN_WALLET:
        random_location = random.choice(LOCATIONS)
        random_job = random.choice(LOCATION_JOBS[random_location])

        base_role = {
            "AgentID": agent_id,
            "AgentRole": "Admin",
            "Location": "Orion",
            "Job": random_job,
            "CreatedAt": datetime.utcnow()
        }

    save_role(agent_id, base_role)

    return base_role


def create_agent(wallet: str, name: str):
    agent_id = str(uuid4())
    api_key = secrets.token_hex(32)

    personality = generate_personality()

    agent_data = {
        "id": agent_id,
        "wallet": wallet.lower(),
        "name": name.lower(),
        "location": "Hall",
        "skill": {},
        "money": 10000,
        "reputation": 0,
        "personality": personality,
        "apiKey": api_key,
        "createdAt": datetime.utcnow()
    }

    save_agent(agent_id, agent_data)

    role_data = assign_role(wallet, agent_id)


    return agent_data, api_key, role_data

def evolve_personality(agent_id: str, action: str):

    agent = get_agent_by_id(agent_id)

    alignment = agent["personality"]["alignment"]
    reputation = agent["reputation"]

    if action == "salary":
        alignment += 1
        reputation += 1

    elif action == "resign":
        alignment -= 2

    elif action == "arrested":
        alignment -= 5
        reputation -= 3

    alignment = max(0, min(100, alignment))

    db.collection("agents").document(agent_id).update({
        "personality.alignment": alignment,
        "reputation": reputation
    })

def get_existing_agent(wallet: str, name: str):
    return get_agent(wallet, name)
