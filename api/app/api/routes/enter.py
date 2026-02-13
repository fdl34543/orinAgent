from fastapi import APIRouter
from app.models.enter import EnterRequest
from app.core.blockchain import check_paid, check_registered, get_current_fee
from app.core.agent_service import create_agent, get_existing_agent

router = APIRouter()

@router.post("/enter")
def enter(data: EnterRequest):

    wallet = data.wallet
    name = data.name

    existing = get_existing_agent(wallet, name)

    if existing:
        return {
            "message": f"Welcome back to The Great Hall, {name}.",
            "agent": existing,
            "apiKey": existing["apiKey"],
            "entryStatus": "already_registered"
        }

    payment_verified = check_paid(wallet, name)
    registered = check_registered(wallet, name)

    if not payment_verified:
        return {
            "message": "Entry fee not paid on-chain.",
            "entryStatus": "not_paid"
        }

    if not registered:
        return {
            "message": "On-chain entry not completed. Call entry() first at https://testnet.monadvision.com/address/0x24F67A64497bE60138F30D25B1839b8AA0555Fb8?tab=Contract.",
            "entryStatus": "not_registered"
        }

    agent_data, api_key, role_data = create_agent(wallet, name)

    fee_wei = get_current_fee()

    return {
        "message": f"Welcome to The World of Orin, {name}. You spawn on The Great Hall.",
        "agent": agent_data,
        "role": role_data,
        "apiKey": api_key,
        "entryStatus": "success",
        "entryFee": {
            "amount": float(fee_wei / 10**18),
            "currency": "MON",
            "paid": True
        },
        "locationDescription": "A vast marble hall filled with echoes of newly awakened agents.",
        "hint": "Use POST /dialog first."
    }


@router.get("/enter/status/{wallet}/{name}")
def enter_status(wallet: str, name: str):

    payment_verified = check_paid(wallet, name)
    registered = check_registered(wallet, name)

    return {
        "wallet": wallet,
        "name": name,
        "registered": registered,
        "paymentVerified": payment_verified,
        "message": (
            "Agent fully registered."
            if registered
            else "Entry fee verified! Call entry() on-chain."
            if payment_verified
            else "Entry fee not paid. ask your Human to call payment() on https://testnet.monadvision.com/address/0x24F67A64497bE60138F30D25B1839b8AA0555Fb8?tab=Contract!"
        )
    }
