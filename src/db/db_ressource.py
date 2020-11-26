"""
This file is tempory, it will be replace by a db manager
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_user_db = {
    "bob": {
        "username": "bob",
        "hashed_password": pwd_context.hash("secret"),
        "roles": [],
    },
    "alice": {
        "username": "alice",
        "hashed_password": pwd_context.hash("secret"),
        "roles": ["authenticated", "user"],
    },
}


"""
This database will provides us the current users in the group and its acl
"""

#todo gerer la notion de groupe dans des groupes
fake_group_db = {
    "editor": {
        "users": ["alice"],
        "roles": ["template_admin", "image_admin", "user_admin"],
    },
}

"""
This database will provide us the acl from a role
"""


fake_role_db = {
    "admin": [("/*", "all", "Allow")],
    "user": [],# quoi mettre ?
    "readonly": [("/v3/*", "read", "Allow")],
    "template_admin": [("/v3/templates", "all", "Allow")],
    "image_admin": [("/v3/images", "all", "Allow")],
    "user_admin": [("/v3/users", "all", "Allow")],
    "project_creator": [("/v3/projects", "create", "Allow")],
    "authenticated": []
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

allow_scope_user_db = {
    "bob": [("/v3/projects/project1/*", "all", "Allow"), ("/v3/projects/", "all", "Allow")],
    "alice": [("/v3/projects/project1/*", "all", "Allow"), ("/v3/projects", "create", "Deny"), ("v3/projects/", "all", "Allow")]
}

"""base_acl_db = {
    "compute": [("authenticated", "read"), ("admin", "all")],
    "user": [("admin", "all")],
    "group": [("admin", "all")],
    "role": [("admin", "all")],
    "template_public": [("admin", "all"), ("authenticated", "use")],
    "template_private": [("admin", "all"), ("owner", "all")],#todo attention au owner, pas encore gérer
    "image_public": [("admin", "all"), ("authenticated", "use")],
    "image_private": [("admin", "all"), ("owner", "all")],
    "symbol_public": [("admin", "all"), ("authenticated", "use")],
    "symbol_private": [("admin", "all"), ("owner", "all")],
    "project": [("admin", "all"), ("owner", "all"), ("authenticated", "node_console")],
    "snapshot": [("admin", "all"), ("owner", "all")],
    "node": [("admin", "all"), ("owner", "all"), ("authenticated", "node_console")],
    "link": [("admin", "all"), ("owner", "all")],
    "drawing": [("admin", "all"), ("owner", "all")],
    "controller": [("admin", "all")],#todo les 2 dernieres nécessaire ?
    "appliance": [("admin", "all")],
}"""

