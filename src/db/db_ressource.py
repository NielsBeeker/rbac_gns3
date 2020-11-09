"""
This file is tempory, it will be replace by a db manager
"""

from src.dependencies.authentication import pwd_context


fake_user_db = {
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("secret"),
        "principals": ["user:bob", "role:user", "user:authenticated"],
    },
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret"),
        "principals": ["user:alice", "role:user", "user:authenticated"],
    },
}

"""
different role possible:
admin
user
owner
authenticated
readonly
templateadmin
imageadmin
useradmin
project_creator // doit on le mettre ?
"""

base_acl_db = {
    "compute":[("user:authenticated", "read"), ("role:admin", "all")],
    "user": [("role:admin", "all")],
    "group": [("role:admin", "all")],
    "role": [("role:admin", "all")],
    "template_public": [("role:admin", "all"), ("user:authenticated", "use")],
    "template_private": [("role:admin", "all"), ("user:owner", "all")],
    "image_public": [("role:admin", "all"), ("user:authenticated", "use")],
    "image_private": [("role:admin", "all"), ("user:owner", "all")],
    "symbol_public": [("role:admin", "all"), ("user:authenticated", "use")],
    "symbol_private": [("role:admin", "all"), ("user:owner", "all")],
    "project": [("role:admin", "all"), ("user:owner", "all"), ("user:authenticated", "node_console")],
    "snapshot": [("role:admin", "all"), ("user:owner", "all")],
    "node": [("role:admin", "all"), ("user:owner", "all"), ("user:authenticated", "node_console")],
    "link": [("role:admin", "all"), ("user:owner", "all")],
    "drawing": [("role:admin", "all"), ("user:owner", "all")],
}

