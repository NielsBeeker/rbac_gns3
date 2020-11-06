from typing import Optional, List
from pydantic import BaseModel


"""
This class contains the Token that is use to access endpoints
"""
class Token(BaseModel):
    access_token: str
    token_type: str


"""
This class contains all user information
"""
class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[(str, str)] = []
    role: List[str] = []
    deny_uri: List[(str, str)] = []

