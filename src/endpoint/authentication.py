from fastapi import Depends, HTTPException, status, APIRouter
from datetime import timedelta
from typing import Optional
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from models.Token import Token
from dependencies.authentication import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.User import User, Auth
from dependencies.security import get_current_active_user, get_user_acl_from_db, get_ressource_acl_from_db
from src.db import fastapi_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v3/token")

@router.on_event("startup")
async def startup():
    await fastapi_db.database.connect()


@router.on_event("shutdown")
async def shutdown():
    await fastapi_db.database.disconnect()

@router.get("/ressources")
async def get_ressource():
    res = await get_ressource_acl_from_db(fastapi_db.database, "MARCEL", 'UPDATE')
    return 1


"""
request with xxx-form-urlencoded
This function is the first way to authenticate on the API.
"""
@router.post("/v3/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = await get_user_acl_from_db(fastapi_db.database, form_data.username)
    scope = []
    for elt in scopes:# convert row into string in a new list
        scope.append((elt[0], elt[1], elt[2]))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": scope,
              }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


"""
request with -d {"username":"username", "password": "secret"}
This function is the second way to authenticate on the API.
"""
@router.post("/v3/token2", response_model=Token)
async def login_for_access_token1(auth: Optional[Auth] = None):
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await authenticate_user(auth.username, auth.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    scopes = await get_user_acl_from_db(fastapi_db.database, auth.username)
    scope = []
    for elt in scopes:  # convert row into string in a new list
        scope.append((elt[0], elt[1], elt[2]))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": auth.username, "scopes": scope,
              }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


"""
An example of a specific endpoint.
"""
#@router.get("/v3/projects/AAAA-BBBB-1113/nodes/CCCC-BBBB-1111")
@router.get("/v3/projects/{project_id}/nodes/{node_id}")
async def get_project_specific(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    if project_id == "" or node_id == "":
        return {"ko"}
    return {"ok"}

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


@router.put("/v3/computes/{compute_id}")
async def update_compute(compute_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/computes/{compute_id}")
async def delete_compute(compute_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/drawings")
async def get_drawing(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/drawings")
async def create_drawing(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/{project_id}/drawings/{drawing_id}")
async def delete_drawing(project_id: str, drawing_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/gns3vm/engines")
async def get_vm_engine(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/gns3vm")
async def update_vm_engine(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/links")
async def get_link(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/links")
async def create_link(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/projects/{project_id}/links/{link_id}")
async def update_link(project_id: str, link_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/{project_id}/links/{link_id}")
async def delete_link(project_id: str, link_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/links/{link_id}/reset")
async def reset_link(project_id: str, link_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/links/{link_id}/capture/start")
async def start_capture_link(project_id: str, link_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/links/{link_id}/capture/stream")
async def stream_link(project_id: str, link_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/nodes")
async def get_nodes(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes")
async def create_node(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/start")
async def start_nodes(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/nodes/{node_id}")
async def get_node(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/projects/{project_id}/nodes/{node_id}")
async def update_node(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/{project_id}/nodes/{node_id}")
async def delete_node(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/{node_id}/start")
async def start_node(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/{node_id}/duplicate")
async def duplicate_node(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/{node_id}/start")
async def start_nodes(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/nodes/{node_id}/links")
async def get_node_links(project_id: str, node_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/nodes/{node_id}/files/{file_id}")
async def get_file(project_id: str, node_id: str, file_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/{node_id}/files/{file_id}")
async def post_file(project_id: str, node_id: str, file_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/console/reset")
async def reset_all_consoles(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/nodes/{node_id}/console/reset")
async def reset_node_console(project_id: str, nodes_id: str, current_user: User = Depends(get_current_active_user)):
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


@router.get("/v3/projects/{project_id}")
async def get_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/projects/{project_id}")
async def update_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/{project_id}")
async def delete_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/stats")
async def get_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/load")
async def load_projects(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}")
async def close_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/export")
async def export_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/duplicate")
async def duplicate_project(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/projects/{project_id}/snapshots")
async def get_snapshots(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/snapshots")
async def create_snapshot(project_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/projects/{project_id}/snapshots/{snapshot_id}")
async def delete_snapshots(project_id: str, snapshot_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/projects/{project_id}/snapshots/{snapshot_id}/restore")
async def restore_snapshot(project_id: str, snapshot_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/symbols")
async def get_symbols(current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.get("/v3/symbols/{symbol_id}/raw")
async def get_symbol(symbol_id: str, current_user: User = Depends(get_current_active_user)):
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


@router.get("/v3/templates/{template_id}")
async def get_template(template_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.delete("/v3/templates/{template_id}")
async def delete_template(template_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.put("/v3/templates/{template_id}")
async def update_template(template_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}


@router.post("/v3/templates/{template_id}/duplicate")
async def duplicate_template(template_id: str, current_user: User = Depends(get_current_active_user)):
    return {"ok"}
