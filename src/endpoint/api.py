"""
A simple file to add endpoint to routeur
"""

from fastapi import APIRouter
from src.endpoint import authentication

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"], prefix="/v3/authentication")
router.include_router(authentication.router, tags=["get_projet"], prefix="/v3/projects/project1")



