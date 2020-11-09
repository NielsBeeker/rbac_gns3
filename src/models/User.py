from pydantic import BaseModel
from typing import Optional

"""
This class contains User model
"""
class User:
    username: str
    disabled: Optional[bool] = None
    roles: [str]

"""
Inherits from User for database use
"""
class UserInDB(User):
    hashed_password: str
