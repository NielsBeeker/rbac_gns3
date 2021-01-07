"""
This file contains the User class, the UserInDB class and the Auth class.
"""

from pydantic import BaseModel
from typing import Optional

"""
This class contains User model
"""
class User:
    username: str
    disabled: Optional[bool] = None
    #roles: List[Any]
    def __init__(self, username):
        self.username = username

"""
Inherits from User for database use
"""
class UserInDB(User):
    hashed_password: str

"""
This class contains usermane and not hashed password for authentication
"""
class Auth(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None