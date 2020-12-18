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
from models.Token import Token, TokenData
from models.User import User, UserInDB
from dependencies.authentication import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db.db_ressource import fake_user_db, allow_scope_user_db

from starlette.requests import Request
from starlette.responses import RedirectResponse
from models.User import User, Auth
from models.ObjectAcl import ObjectAcl
from fastapi import Depends
from dependencies.security import get_current_active_user, get_required_scopes_from_endpoint, get_user_acl_from_db, get_ressource_acl_from_db
from dependencies.database import get_user_acl
from pydantic import BaseModel

from src.db import models, fastapi_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
request with xxx-form-urlencoded
sert de moyen d'authentification pour l'api
"""


@router.on_event("startup")
async def startup():
    await fastapi_db.database.connect()


@router.on_event("shutdown")
async def shutdown():
    await fastapi_db.database.disconnect()

@router.get("/users/")
async def get_users_acl():
    res = await get_user_acl_from_db(database=fastapi_db.database, username="MAURICE")
    return 0

@router.post("/v3/token", response_model=Token)
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
              }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


"""
request with -d {"username":"username", "password": "secret"}
sert de moyen d'authentification en envoyant un curl avec un --data
"""


@router.post("/v3/token2", response_model=Token)
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
    # get scope related to group/role
    scope, role = get_user_acl(user.roles, user.username)
    # todo gerer le fait que les roles peuvent deny
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": scope,
              "role": role,
              }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


"""
Simple endpoints pour donner un exemple
"""


@router.get("/v3/version")
async def get_version(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/version")
async def check_version(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/iou_license")
async def update_iou_license(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/appliances")
async def get_appliances(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/computes")
async def get_computes(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/computes")
async def create_compute(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/computes/compute1234")
async def update_compute(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/computes/compute1234")
async def delete_compute(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/drawings")
async def get_drawing(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/drawings")
async def create_drawing(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/project1234/drawings/drawing1234")
async def delete_drawing(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/gns3vm/engines")
async def get_vm_engine(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/gns3vm")
async def update_vm_engine(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/links")
async def get_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/links")
async def create_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/projects/project1234/links/link1234")
async def update_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/project1234/links/link1234")
async def delete_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/links/link1234/reset")
async def reset_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/links/link1234/capture/start")
async def start_capture_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/links/link1234/capture/stream")
async def stream_link(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/nodes")
async def get_nodes(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes")
async def create_node(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/start")
async def start_nodes(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/nodes/node1234")
async def get_node(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/projects/project1234/nodes/node1234")
async def update_node(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/project1234/nodes/node1234")
async def delete_node(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/node1234/start")
async def start_node(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/node1234/duplicate")
async def duplicate_node(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/node1234/start")
async def start_nodes(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


# todo check logique avec le get projects/project1234/links
@router.get("/v3/projects/project1234/nodes/node1234/links")
async def get_node_links(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/nodes/node1234/files/file1234")
async def get_file(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/node1234/files/file1234")
async def post_file(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/console/reset")
async def reset_all_consoles(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/nodes/node1234/console/reset")
async def reset_node_console(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/notification")
async def get_notification(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects")
async def get_projects(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects")
async def create_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234")
async def get_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/projects/project1234")
async def update_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/project1234")
async def delete_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/stats")
async def get_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/load")
async def load_projects(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234")
async def close_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/export")
async def export_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/duplicate")
async def duplicate_project(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/project1234/snapshots")
async def get_snapshots(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/snapshots")
async def create_snapshot(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/project1234/snapshots/snapshot1234")
async def delete_snapshots(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/project1234/snapshots/snapshot1234/restore")
async def restore_snapshot(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/symbols")
async def get_symbols(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/symbols/symbol1234/raw")
async def get_symbol(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/symbols/default_symbols")
async def get_default_symbols(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/templates")
async def get_templates(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/templates")
async def create_templates(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/templates/template1234")
async def get_template(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/templates/template1234")
async def delete_template(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/templates/template1234")
async def update_template(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/templates/template1234/duplicate")
async def duplicate_template(current_user: User = Depends(get_current_active_user)):
    return {"ok"}
