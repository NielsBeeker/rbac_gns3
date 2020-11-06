"""
A simple file to add endpoint to routeur
"""

from fastapi import APIRouter
from starlette.requests import Request
from src.models.User import User
from src.models.ObjectAcl import ObjectAcl
from fastapi import Depends
from src.dependencies.security import get_current_active_user, get_required_scopes_from_endpoint
router = APIRouter()

@router.get("/v3/me")
async def read_me(request: Request):
    object = get_required_scopes_from_endpoint(request)
    current_user: User = Depends(get_current_active_user(endpoint_object=object))
    return {"username": current_user.username}



