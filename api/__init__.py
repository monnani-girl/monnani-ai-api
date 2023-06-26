from fastapi import APIRouter
from .crop_router import crop_router
from .analytics_router import analytics_router

api_router = APIRouter()
api_router.include_router(crop_router, prefix="/crop", tags=["crop"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])