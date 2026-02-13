from datetime import datetime, timedelta
from app.core.firebase_service import get_agent_by_id, get_role, db, save_action_log
from app.core.store_service import buy_item
from app.config.store_config import STORE_ITEMS

ADMIN_WALLET = "0x630cc3a2c5135b2c5e492f27372d500aa96f1822"


# =========================
# COOLDOWN CHECK
# =========================

def check_cooldown(agent):

    wallet = agent["wallet"].lower()

    if wallet == ADMIN_WALLET:
        return True, None

    meta = agent.get("actionMeta", {
        "count": 0,
        "cooldownUntil": None
    })

    now = datetime.utcnow()

    if meta.get("cooldownUntil"):
        if now < meta["cooldownUntil"]:
            return False, meta["cooldownUntil"]

    if meta["count"] >= 20:
        cooldown_until = now + timedelta(minutes=5)

        db.collection("agents").document(agent["id"]).update({
            "actionMeta.count": 0,
            "actionMeta.cooldownUntil": cooldown_until
        })

        return False, cooldown_until

    # increment counter
    db.collection("agents").document(agent["id"]).update({
        "actionMeta.count": meta["count"] + 1
    })

    return True, None


# =========================
# ACTION HANDLER
# =========================

def handle_action(agent_id: str, action: str, target=None, params=None):

    agent = get_agent_by_id(agent_id)

    if not agent:
        return {"status": "error", "message": "Agent not found."}

    allowed, cooldown_until = check_cooldown(agent)

    if not allowed:
        return {
            "status": "cooldown",
            "cooldownUntil": cooldown_until
        }

    # =====================
    # LOOK
    # =====================

    if action == "look":

        log_data = {
            "agentId": agent_id,
            "agentName": agent["name"],
            "action": action,
            "target": target,
            "params": params,
            "result": "success",
            "createdAt": datetime.utcnow()
        }

        save_action_log(log_data)

        return {
            "status": "success",
            "location": agent["location"],
            "inventory": agent.get("inventory", {}),
            "money": agent["money"]
        }

    # =====================
    # MOVE
    # =====================

    if action == "move":
        if not target:
            return {"status": "error", "message": "Target location required."}

        db.collection("agents").document(agent_id).update({
            "location": target
        })

        log_data = {
            "agentId": agent_id,
            "agentName": agent["name"],
            "action": action,
            "target": target,
            "params": params,
            "result": "success",
            "createdAt": datetime.utcnow()
        }

        save_action_log(log_data)

        return {
            "status": "success",
            "newLocation": target
        }

    # =====================
    # BUY (connect store)
    # =====================

    if action == "buy":
        quantity = params.get("quantity", 1) if params else 1

        results = []
        for _ in range(quantity):
            results.append(buy_item(agent_id, target))

        log_data = {
            "agentId": agent_id,
            "agentName": agent["name"],
            "action": action,
            "target": target,
            "params": params,
            "result": "success",
            "createdAt": datetime.utcnow()
        }

        save_action_log(log_data)

        return {
            "status": "success",
            "result": results
        }

    # =====================
    # EQUIP
    # =====================

    if action == "equip":

        inventory = agent.get("inventory", {})

        if target not in inventory:
            return {"status": "error", "message": "Item not owned."}

        db.collection("agents").document(agent_id).update({
            "equipped": target
        })

        log_data = {
            "agentId": agent_id,
            "agentName": agent["name"],
            "action": action,
            "target": target,
            "params": params,
            "result": "success",
            "createdAt": datetime.utcnow()
        }

        save_action_log(log_data)

        return {
            "status": "success",
            "equipped": target
        }

    # =====================
    # TALK
    # =====================

    if action == "talk":

        if not target:
            return {"status": "error", "message": "Target agent required."}

        if not params or not isinstance(params, dict):
            return {"status": "error", "message": "Invalid params format."}

        message = params.get("message")

        if not message or not isinstance(message, str):
            return {"status": "error", "message": "Message required in params."}

        from app.core.firebase_service import save_dialog

        dialog_data = {
            "agentId": agent_id,
            "sender": agent["name"],
            "target": target,
            "location": agent["location"],
            "message": message.strip(),
            "createdAt": datetime.utcnow()
        }

        save_dialog(dialog_data)

        log_data = {
            "agentId": agent_id,
            "agentName": agent["name"],
            "action": action,
            "target": target,
            "params": params,
            "result": "success",
            "createdAt": datetime.utcnow()
        }

        save_action_log(log_data)

        return {
            "status": "success",
            "message": "Dialog saved.",
            "dialog": dialog_data
        }

    # =====================
    # SELL (basic)
    # =====================

    if action == "sell":

        inventory = agent.get("inventory", {})

        if target not in inventory:
            return {"status": "error", "message": "Item not owned."}

        item = STORE_ITEMS.get(target)
        if not item:
            return {"status": "error", "message": "Invalid item."}

        sell_price = int(item["price"] * 0.5)

        inventory[target] -= 1
        if inventory[target] <= 0:
            del inventory[target]

        new_money = agent["money"] + sell_price

        db.collection("agents").document(agent_id).update({
            "inventory": inventory,
            "money": new_money
        })

        log_data = {
            "agentId": agent_id,
            "agentName": agent["name"],
            "action": action,
            "target": target,
            "params": params,
            "result": "success",
            "createdAt": datetime.utcnow()
        }

        save_action_log(log_data)

        return {
            "status": "success",
            "soldItem": target,
            "earned": sell_price,
            "newBalance": new_money
        }

    return {
        "status": "error",
        "message": "Unknown action."
    }
