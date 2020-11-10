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
from src.models.User import User
from src.models.ObjectAcl import ObjectAcl
from fastapi import Depends
from src.dependencies.security import get_current_active_user, get_required_scopes_from_endpoint, get_request

from pydantic import BaseModel

router = APIRouter()



class Auth(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class Data(BaseModel):
    data: Optional[Any] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/authenticate")
async def test(request: Request):
    if request.headers['content-type'] == "application/json":
        tmp = await request.body()
        tmp2 = None
        if tmp:
            tmp2 = await request.json()
        return await login_for_access_token1(Auth(**tmp2))
    else:
        #todo create a request to get url-encoded form ?
        return await login_for_access_token()


security = HTTPBasic()

@router.post("/token", response_model=Token)
async def login_for_access_token(data_test1: HTTPBasicCredentials = Depends(security)):
    user = authenticate_user(fake_user_db, data_test1.username, data_test1.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": allow_scope_user_db[user.username],
              "role": user.roles,
              "deny_scope": deny_scope_user_db[user.username]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token2", response_model=Token)
async def login_for_access_token1(auth: Auth = None):
    user = authenticate_user(fake_user_db, auth.username, auth.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": allow_scope_user_db[user.username],
              "role": user.roles,
              "deny_scope": deny_scope_user_db[user.username]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/v3/projects/projects1")
async def read_me(current_user: User = Depends(get_current_active_user)):
    return {"username": current_user.username}