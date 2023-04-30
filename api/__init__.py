from fastapi import APIRouter
from .crop_router import crop_router

api_router = APIRouter()
api_router.include_router(crop_router, prefix="/crop", tags=["users"])