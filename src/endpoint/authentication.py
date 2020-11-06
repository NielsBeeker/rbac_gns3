from fastapi import Depends, HTTPException, Security, status, APIRouter
from datetime import datetime, timedelta
from typing import List, Optional, Union
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
    HTTPBasicCredentials
)
from starlette.requests import Request
from src.models.Token import Token, TokenData
from src.models.User import User, UserInDB
from src.dependencies.authentication import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.db.db_ressource import fake_user_db


router = APIRouter()

@router.post("/v3/authenticate", response_model=Token)
async def login_for_access_token(data: Union[HTTPBasicCredentials, OAuth2PasswordRequestForm] = Depends()):
    user = authenticate_user(fake_user_db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": db.get_user_scope(user.username),
              "role": db.get_user_role(user.username),
              "deny_scope": db.get_user_deny_scope(user.username)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

