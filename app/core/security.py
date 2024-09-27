from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from app.models.models import User
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: User):
    expire_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_access_token(token)
    if user is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return user
