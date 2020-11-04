"""
This file is tempory, it will be replace by a db manager
"""

from src.depencies.authentication import pwd_context


fake_user_db = {
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("secret"),
        "principals": ["user:bob", "role: user"],
    },
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret"),
        "principals": ["user:alice", "role:user"],
    },
}

