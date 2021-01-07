"""
This file contains the Token class and the TokenData class.
"""

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


    def __init__(self, username, scopes):
        self.username = username
        self.scopes = scopes

