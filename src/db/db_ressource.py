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
    "nathan": {
        "username": "nathan",
        "hashed_password": pwd_context.hash("secret"),
        "roles": ["authenticated", "user", "image_admin"],
    },
    "jean": {
        "username": "jean",
        "hashed_password": pwd_context.hash("secret"),
        "roles": ["authenticated", "user", "template_admin"],
    },
    "jesus": {
        "username": "jesus",
        "hashed_password": pwd_context.hash("secret"),
        "roles": [],
    },
    "kevin": {
        "username": "kevin",
        "hashed_password": pwd_context.hash("secret"),
        "roles" : [],
    }
}


"""
This database will provides us the current users in the group and its acl
"""

#a group can contains another group etc...
fake_group_db = {
    "editor": {
        "users": ["alice"],
        "roles": ["template_admin", "image_admin", "user_admin"],
        "scopes": [],
        "groups": []
    },
    "big_editor": {
        "users": ["jesus"],
        "roles": ["project_creator", "image_admin"],
        "scopes": [],
        "groups": []
    },
    "useless": {
        "users": ["kevin"],
        "roles": [],
        "scopes": [("/v3/projects", "get", "Allow")],
        "groups": []

    }
    ,
    "inner_group": {
        "users": ["bob"],
        "roles": ["readonly"],
        "scopes": [],
        "groups": ["useless"]
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


allow_scope_user_db = {
    "bob": [("/v3/projects/project1/*", "all", "Allow"), ("/v3/projects/", "all", "Allow")],
    "alice": [("/v3/projects/project1/*", "all", "Allow"), ("/v3/projects", "create", "Deny"), ("v3/projects/", "all", "Allow")]
}
