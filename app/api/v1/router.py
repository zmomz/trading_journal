from fastapi import APIRouter
from app.api.v1.endpoints import user, trade, note

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(trade.router, prefix="/trades", tags=["Trades"])
api_router.include_router(note.router, prefix="/notes", tags=["Trade Notes"])