from fastapi import APIRouter, HTTPException, status
from app.schemas.ai_textbook_dto import AIRequest, AIResponse

router = APIRouter()

@router.post("/getAIResponse", response_model=AIResponse, description="Get the response from the AI model")

async def get_ai_response(
    request: AIRequest
):
    pass