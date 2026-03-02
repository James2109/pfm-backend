from fastapi import APIRouter
from src.api.v1.routes import users, messages, conversations, plans, players

router = APIRouter()
router.include_router(users.router)
router.include_router(messages.router)
router.include_router(conversations.router)
router.include_router(plans.router)
router.include_router(players.router)