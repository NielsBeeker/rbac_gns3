"""
This file contains middleware related to database
"""

from src.models.User import UserInDB

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)