"""
This file contains middleware for security
"""

from fastapi import Depends, FastAPI, HTTPException, Security, status, APIRouter
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from src.models.Token import Token, TokenData
from src.models.User import UserInDB, User
from src.dependencies.authentication import oauth2_scheme, SECRET_KEY, ALGORITHM
from src.dependencies.database import get_user
from src.db.db_ressource import fake_user_db

async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", []) # TODO permet de récuprer les scopes du current user
        token_role = payload.get("role", []) #TODO permet de recuperer les roles du current user
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_user_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes: ## TODO ici on peut comparé les scopes du token avec les scopes requis
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
