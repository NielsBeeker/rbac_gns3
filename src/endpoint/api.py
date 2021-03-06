"""
A simple file to add endpoint to router
"""

from fastapi import APIRouter
from endpoint import authentication

router = APIRouter()

router.include_router(authentication.router, tags=["authentication"])



