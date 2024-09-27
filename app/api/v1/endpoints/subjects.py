from fastapi import APIRouter, HTTPException, status, Depends
from app.models.models import User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/subjects", response_model=dict, description="Get all subjects with their details")
async def get_subjects(
    current_user: User = Depends(get_current_user)
):
    class_name = current_user.class_name
    subjects = await find_object("subjects", {"class_name": class_name})