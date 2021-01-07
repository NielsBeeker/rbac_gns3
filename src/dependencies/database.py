####TODO IMPORTANT : THIS FILE IS NO MORE USED

"""
This file contains middleware related to database
"""

from models.User import UserInDB
from db.db_ressource import fake_role_db, fake_group_db, allow_scope_user_db, fake_user_db


"""
This function get user in database
"""
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# get group in a group recursively
def get_rec_group(group, list):
    tmp = fake_group_db[group]
    if tmp.get("groups") != []:
        for elt in tmp.get("groups"):
            return get_rec_group(elt, list)
    if group not in list:
        list.append(group)
    return list

def get_users_groups(username):
    res = []
    for key, value in fake_group_db.items():
        tmp = value["users"]
        if username in tmp:
            res += get_rec_group(key, res)

    return res
"""
get user acl with the role and group
"""
#todo fonction qui doit etre gérée par une query qui recoupère tout du user bien ordonné ou bien une autre maniere ?
#this function will be a query
def get_user_acl(user_roles, username):
    roles = []
    res_acl = []
    groups = get_users_groups(username)

    for elt in groups:
        tmp = fake_group_db[elt]
        for role in tmp.get("roles"): # get roles from group
            if role not in roles:
                roles.append(role)
        for scope in tmp.get("scopes"): # get scope from group
            if scope not in res_acl:
                res_acl.append(scope)
                #l'acl doit etre triée d'une certaine manière, on ne doit pas ajouter comme ça

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