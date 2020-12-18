"""
File that contains middleware for the api
"""

from fastapi import Depends, FastAPI, HTTPException, Security, status, APIRouter
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import jwt
from passlib.context import CryptContext


from dependencies.database import get_user
from models.User import UserInDB, User2
from db import fastapi_db, models


router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v3/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(username: str, password: str) -> User2:
    query = f"""SELECT PASSWORD FROM USERS WHERE USERNAME='{username}';"""
    user_password = await fastapi_db.database.fetch_all(query=query)
    if user_password == []:
        return False
    #if not verify_password(password, user_password):
    if password != user_password:
        return False
    return User2(username=username)


#TODO gerer la notion de refresh avec les tokens
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

