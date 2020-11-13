from pydantic import BaseModel
from typing import Optional, Any, List

"""
This class contains User model
"""
class User(BaseModel):
    username: str
    disabled: Optional[bool] = None
    roles: List[Any]

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