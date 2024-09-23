from fastapi import APIRouter
from app.api.v1.endpoints import ai_textbook

api_router = APIRouter()

api_router.include_router(ai_textbook.router, prefix="/aitextbook", tags=["AI Textbook"])