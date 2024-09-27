from fastapi import APIRouter, HTTPException, status, Depends
from app.db.mongodb import create_object, get_object, update_object, delete_object, find_object
from app.core.security import create_access_token
from app.schemas.user_dto import loginRequest, loginResponse, createUserRequest, createUserResponse
import bcrypt

router = APIRouter()

def hash_password(password):
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/login", response_model=loginResponse, description="Get the access token for the user")
async def login(
    request: loginRequest
):
    email = request.email
    password = request.password
    
    user = await find_object("users", {"email": email})

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

    user = await create_object("users", {"name": name, "email": email, "password": password, "class_name": class_name})

    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return {"message": "User created successfully"}




