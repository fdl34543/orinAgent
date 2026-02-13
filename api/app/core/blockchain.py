import json
from web3 import Web3
from pathlib import Path
from app.config.settings import RPC_URL, CONTRACT_ADDRESS

w3 = Web3(Web3.HTTPProvider(RPC_URL))

abi_path = Path("abi/OrinEntry.json")

with open(abi_path, "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=contract_abi
)

def check_paid(wallet: str, name: str) -> bool:
    wallet = Web3.to_checksum_address(wallet)
    return contract.functions.isPaid(wallet, name).call()

def check_registered(wallet: str, name: str) -> bool:
    wallet = Web3.to_checksum_address(wallet)
    return contract.functions.isRegister(wallet, name).call()

def get_current_fee() -> int:
    return contract.functions.currentFee().call()
