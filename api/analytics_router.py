from fastapi import APIRouter
from modules.google_analytics import get_all_sessions

analytics_router = APIRouter()

@analytics_router.get("/sessions")
async def get_sessions_count():
    count = get_all_sessions()
    return {"session_count" : count}