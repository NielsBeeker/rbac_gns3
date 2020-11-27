"""
This file contains middleware related to database
"""

from models.User import UserInDB
from db.db_ressource import fake_role_db, fake_group_db, allow_scope_user_db, fake_user_db

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
    res_acl = []
    for key, value in fake_group_db.items():
        if "user" not in tmp:
            return
        tmp = value["users"]
        if username in tmp:
            for elt in value["roles"]:#get roles from groupes
                if elt not in roles:
                    roles.append(elt)
            for elt in value["scopes"]:#get scopes from groupes
                if elt not in res_acl:
                    res_acl.append(elt)

    #todo rajouter la notion de groupe dans un groupe
    for elt in user_roles:
        if elt not in roles:
            roles.append(elt)# add user_role to group_role

    for elt in roles:
        for tmp in fake_role_db[elt]:
            res_acl.append(tmp) #get the acl from roles
    allow_scope = allow_scope_user_db[username]
    #a faire: rajouter de maniere propre les scopes en fonction des permissions avec l'ordre a mettre en place ==> je en sais pas faire
    res_acl += allow_scope # dirty way to add scope to res_acl

    return res_acl, roles