from fastapi import APIRouter, HTTPException, status, Depends
from app.db.mongodb import create_object, get_object, update_object, delete_object, find_object
from app.core.security import create_access_token, verify_password

router = APIRouter()

@router.get("/login", response_model=dict, description="Get the access token for the user")
async def login(
    request: dict
):
    email = request.get("email")
    password = request.get("password")
    
    user = await find_object("users", {"email": email})

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(user)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/create-user", response_model=dict, description="Create a new user")
async def createUser(
    request: dict
):
    name = request.get("name")
    email = request.get("email")
    password = request.get("password")
    class_name = request.get("class_name")

    user = await create_object("users", {"name": name, "email": email, "password": password, "class_name": class_name})

    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return {"message": "User created successfully"}




