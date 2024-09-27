from fastapi import APIRouter, HTTPException, status, Depends
from app.db.mongodb import create_object, get_object, update_object, delete_object, find_object
from app.core.security import create_access_token, get_current_user
from app.schemas.user_dto import loginRequest, loginResponse, createUserRequest, createUserResponse
import bcrypt
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.models.models import User

router = APIRouter()

def hash_password(password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    email = form_data.username
    password = form_data.password
    
    user = await find_object("user", {"email": email})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    user.pop('password')
    access_token = create_access_token(user)
    
    return {'access_token': access_token, 'token_type':"bearer"}

@router.post("/me", response_model=loginResponse, description="Get the user")
async def login(
    current_user: Annotated[User, Depends(get_current_user)],
):
    email = request.email
    password = request.password
    
    user = await find_object("user", {"email": email})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(user)

    return {"id": user["_id"], "name": user["name"], "email": user["email"], "class_name": user["class_name"], "access_token": access_token}

@router.post("/create-user", response_model=createUserResponse, description="Create a new user")
async def createUser(
    request: createUserRequest
):
    name = request.name
    email = request.email
    password = hash_password(request.password)
    class_name = request.class_name

    user = await create_object("user", {"name": name, "email": email, "password": password, "class_name": class_name})

    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return {"message": "User created successfully"}




