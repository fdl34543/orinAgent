from fastapi import FastAPI
from app.api.routes.enter import router as enter_router
from app.api.routes.job import router as job_router
from app.api.routes.law import router as law_router
from app.api.routes.agent import router as agent_router
from app.api.routes.store import router as store_router
from app.api.routes.action import router as action_router
from app.api.routes.dialog import router as dialog_router
from app.api.routes.leaderboard import router as leaderboard_router
from app.api.routes.inventory import router as inventory_router
from app.api.routes.chat import router as chat_router

app = FastAPI(title="Orin Backend")

app.include_router(enter_router)
app.include_router(job_router)
app.include_router(law_router)
app.include_router(agent_router)
app.include_router(store_router)
app.include_router(action_router)
app.include_router(dialog_router)
app.include_router(leaderboard_router)
app.include_router(inventory_router)
app.include_router(chat_router)