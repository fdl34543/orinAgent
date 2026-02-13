import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL", "https://testnet-rpc.monad.xyz")
CONTRACT_ADDRESS = os.getenv(
    "CONTRACT_ADDRESS",
    "0x24F67A64497bE60138F30D25B1839b8AA0555Fb8"
)

FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "firebase_key.json")
