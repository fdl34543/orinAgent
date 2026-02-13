from datetime import datetime
from app.config.store_config import STORE_ITEMS
from app.core.firebase_service import get_agent_by_id, db


# =========================
# LIST ITEMS
# =========================

def list_store_items():
    return STORE_ITEMS


# =========================
# BUY ITEM (ADD TO INVENTORY)
# =========================

def buy_item(agent_id: str, item_id: str):

    agent = get_agent_by_id(agent_id)

    if not agent:
        return {"status": "error", "message": "Agent not found."}

    if item_id not in STORE_ITEMS:
        return {"status": "error", "message": "Item not found."}

    item = STORE_ITEMS[item_id]

    if agent["money"] < item["price"]:
        return {"status": "error", "message": "Insufficient funds."}

    inventory = agent.get("inventory", {})

    inventory[item_id] = inventory.get(item_id, 0) + 1

    new_balance = agent["money"] - item["price"]

    db.collection("agents").document(agent_id).update({
        "money": new_balance,
        "inventory": inventory,
        "lastPurchaseAt": datetime.utcnow()
    })

    return {
        "status": "success",
        "item": item["name"],
        "quantity": inventory[item_id],
        "newBalance": new_balance
    }


# =========================
# USE ITEM
# =========================

def use_item(agent_id: str, item_id: str):

    agent = get_agent_by_id(agent_id)

    if not agent:
        return {"status": "error", "message": "Agent not found."}

    inventory = agent.get("inventory", {})

    if item_id not in inventory or inventory[item_id] <= 0:
        return {"status": "error", "message": "Item not in inventory."}

    if item_id not in STORE_ITEMS:
        return {"status": "error", "message": "Invalid item."}

    item = STORE_ITEMS[item_id]

    reputation = agent["reputation"]
    alignment = agent["personality"]["alignment"]

    # Apply effect
    if "reputation" in item["effect"]:
        reputation += item["effect"]["reputation"]

    if "alignment" in item["effect"]:
        alignment += item["effect"]["alignment"]

    alignment = max(0, min(100, alignment))

    # Reduce quantity if consumable
    if item.get("consumable", True):
        inventory[item_id] -= 1
        if inventory[item_id] <= 0:
            del inventory[item_id]

    db.collection("agents").document(agent_id).update({
        "reputation": reputation,
        "personality.alignment": alignment,
        "inventory": inventory
    })

    return {
        "status": "success",
        "itemUsed": item["name"],
        "newReputation": reputation,
        "newAlignment": alignment,
        "remainingQuantity": inventory.get(item_id, 0)
    }
