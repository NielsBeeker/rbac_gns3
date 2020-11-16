"""
This file contains middleware related to database
"""

from src.models.User import UserInDB
from src.db.db_ressource import fake_role_db, fake_group_db, allow_scope_user_db, fake_user_db

#les roles peuvent-il mettre des restrictions

"""
get user in database
"""
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

"""
get user acl with the role and group
"""
def get_user_acl(user_roles, username):
    roles = []
    for key, value in fake_group_db.items():
        tmp = value["users"]
        if username in tmp:
            for elt in value["roles"]:
                if elt not in roles:
                    roles.append(elt)


    for elt in user_roles:
        if elt not in roles:
            roles.append(elt)# add user_role to group_role
    res_acl = []
    for elt in roles:
        for tmp in fake_role_db[elt]:
            res_acl.append(tmp) #get the acl from roles
    allow_scope = allow_scope_user_db[username]
    res_acl += allow_scope # dirty way to add scope to res_acl
    #todo faire en sorte d'avoir une acl propre sans redondance sur les endpoints
    """for elt in allow_scope:
        for tmp in res_acl:
            if elt[0] == tmp[0] and (elt[0] == tmp[]
    """

    return res_acl, roles