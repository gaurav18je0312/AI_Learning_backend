from fastapi import APIRouter
from app.api.v1.endpoints import ai_textbook
from app.api.v1.endpoints import user

api_router = APIRouter()

api_router.include_router(ai_textbook.router, prefix="/aitextbook", tags=["AI Textbook"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])