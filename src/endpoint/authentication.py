from fastapi import Depends, HTTPException, Security, status, APIRouter
from datetime import datetime, timedelta
from typing import List, Optional, Union, Any
from fastapi.responses import JSONResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
    HTTPBasicCredentials,
    HTTPBasic
)
from starlette.requests import Request
from src.models.Token import Token, TokenData
from src.models.User import User, UserInDB
from src.dependencies.authentication import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.db.db_ressource import fake_user_db, base_acl_db, deny_scope_user_db, allow_scope_user_db

from starlette.requests import Request
from starlette.responses import RedirectResponse
from src.models.User import User, Auth
from src.models.ObjectAcl import ObjectAcl
from fastapi import Depends
from src.dependencies.security import get_current_active_user, get_required_scopes_from_endpoint
from src.dependencies.database import get_user_acl
from pydantic import BaseModel

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


"""
request with xxx-form-urlencoded
sert de moyen d'authentification pour l'api
"""
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_user_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # get scope related to group/role
    scope, role = get_user_acl(user.roles, user.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scope,
              "role": role,
              "deny_scope": deny_scope_user_db[user.username]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

"""
request with -d {"username":"username", "password": "secret"}
sert de moyen d'authentification en envoyant un curl avec un --data
"""
@router.post("/token2", response_model=Token)
async def login_for_access_token1(auth: Optional[Auth] = None):
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = authenticate_user(fake_user_db, auth.username, auth.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #get scope related to group/role
    scope, role = get_user_acl(user.roles, user.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scope,
              "role": role,
              "deny_scope": deny_scope_user_db[user.username]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

"""
Simple endpoint pour donner un exemple
"""
@router.get("/v3/projects/project1")
async def read_me(current_user: User = Depends(get_current_active_user)):
    return {"username": current_user.username}

@router.post("/v3/templates")
async def create_template(current_user: User = Depends(get_current_active_user)):
    return {f"{current_user.username} can create templates !"}