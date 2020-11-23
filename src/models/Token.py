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
class TokenData:
    username: Optional[str] = None
    scopes: [(str, str, str)] = []
    token_role: [str] = []


    def __init__(self, username, scopes, token_role):
        self.username = username
        self.scopes = scopes
        self.token_role = token_role

