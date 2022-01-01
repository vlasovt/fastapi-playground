import sys
sys.path.append("..")
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from security import get_password_hash, verify_password, create_token
import models
from user import CreateUser
from db import engine, get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from exceptionz import token_exception 

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)

models.db_base.metadata.create_all(bind=engine)

@router.post("/user")
async def create_user(new_user: CreateUser, database:Session = Depends(get_db)):
    new_user_model = models.Users()
    new_user_model.username = new_user.username
    new_user_model.email = new_user.email
    new_user_model.first_name = new_user.first_name
    new_user_model.last_name = new_user.last_name
    new_user_model.hashed_password = get_password_hash(new_user.password)
    new_user_model.isActive = True

    database.add(new_user_model)
    database.commit()

    return new_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), database:Session = Depends(get_db)):

    user = authenticate_user(form_data.username, form_data.password, database)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    return create_token(user.username, user.id, expires_delta=token_expires)

def authenticate_user(username: str, password: str, database):
    user = database.query(models.Users).filter(models.Users.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        return False
    
    return user