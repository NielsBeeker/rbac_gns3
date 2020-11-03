from pydantic import BaseModel
from typing import Optional

"""
This class contains User model
"""
class User(BaseModel):
    username: str
    disabled: Optional[bool] = None

"""
Inherits from User for database use
"""
class UserInDB(User):
    hashed_password: str
