from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import oauth2
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from exceptionz import token_exception
from exceptionz import get_user_exception

SECRET_KEY = "&FLqprTW7Y^pN8o6Ak"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
bcypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return bcypt_context.hash(password)

def verify_password(plain, hash):
    return bcypt_context.verify(plain, hash)

def create_token(username: str, userId: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": userId}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()