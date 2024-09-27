from pydantic import BaseModel

class loginRequest(BaseModel):
    email: str
    password: str

class loginResponse(BaseModel):
    id: str
    name: str
    email: str
    class_name: str
    access_token: str

class createUserRequest(BaseModel):
    name: str
    email: str
    password: str
    class_name: str

class createUserResponse(BaseModel):
    message: str