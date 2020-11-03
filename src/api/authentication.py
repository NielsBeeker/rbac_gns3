from fastapi import Depends, FastAPI, HTTPException, Security, status, APIRouter

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError

router = APIRouter()

@router.post("/v3/authenticate", response_model=Token)