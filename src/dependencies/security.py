"""
This file contains middleware for security
"""

from fastapi import Depends, HTTPException, status
from starlette.requests import Request
from jose import JWTError, jwt
from pydantic import ValidationError
from dependencies.authentication import oauth2_scheme, SECRET_KEY, ALGORITHM

from models.ObjectAcl import Endpoint
from db.fastapi_db import database
from models.Token import TokenData
from models.User import User


"""
This function get all the user_acl from the given user.
"""
async def get_user_acl_from_db(database, username):
    query = f"""SELECT RESOURCES.NAME, PERMISSIONS.NAME, ACE.ALLOWED, ACE.PRIORITY
                FROM ACE, RESOURCES, RESOURCES_GROUP, RESOURCES_GROUP_MEMBERS, USERS, USERS_GROUP, USERS_GROUP_MEMBERS, PERMISSIONS, PERMISSIONS_GROUPS, PERMISSIONS_GROUP_MEMBERS
                WHERE ACE.RSC_GROUP_ID=RESOURCES_GROUP.RSC_GROUP_ID AND RESOURCES_GROUP.RSC_GROUP_ID=RESOURCES_GROUP_MEMBERS.RESOURCES_GROUP_ID 
                    AND RESOURCES.RSC_ID=RESOURCES_GROUP_MEMBERS.RESOURCE_ID AND RESOURCES.RSC_TYPE='ENDPOINT'
                    AND ACE.PERM_GROUP_ID=PERMISSIONS_GROUPS.PERM_GROUP_ID AND PERMISSIONS_GROUPS.PERM_GROUP_ID=PERMISSIONS_GROUP_MEMBERS.PERMISSIONS_GROUP_ID
                    AND PERMISSIONS.PERM_ID=PERMISSIONS_GROUP_MEMBERS.PERMISSION_ID AND ACE.USER_GROUP_ID=USERS_GROUP.USER_GROUP_ID 
                    AND USERS_GROUP.USER_GROUP_ID=USERS_GROUP_MEMBERS.USERS_GROUP_ID
                    AND USERS_GROUP_MEMBERS.USER_ID=USERS.USER_ID AND USERS.NAME='{username}'
                ORDER BY ACE.PRIORITY;
            """
    res = await database.fetch_all(query=query)
    return res

"""
Needed ?
"""
async def get_ressource_acl_from_db(database,username ,permission):
    query = f"""SELECT RESOURCES.NAME, ACE.ALLOWED
                FROM ACE, RESOURCES, RESOURCES_GROUP, RESOURCES_GROUP_MEMBERS, USERS, USERS_GROUP, USERS_GROUP_MEMBERS, PERMISSIONS, PERMISSIONS_GROUPS, PERMISSIONS_GROUP_MEMBERS
                WHERE ACE.RSC_GROUP_ID=RESOURCES_GROUP.RSC_GROUP_ID AND RESOURCES_GROUP.RSC_GROUP_ID=RESOURCES_GROUP_MEMBERS.RESOURCES_GROUP_ID
                    AND RESOURCES.RSC_ID=RESOURCES_GROUP_MEMBERS.RESOURCE_ID AND RESOURCES.RSC_TYPE='ENDPOINT' 
                    AND ACE.PERM_GROUP_ID=PERMISSIONS_GROUPS.PERM_GROUP_ID AND PERMISSIONS_GROUPS.PERM_GROUP_ID=PERMISSIONS_GROUP_MEMBERS.PERMISSIONS_GROUP_ID
                    AND PERMISSIONS.PERM_ID=PERMISSIONS_GROUP_MEMBERS.PERMISSION_ID AND PERMISSIONS.NAME='{permission}'
                    AND ACE.USER_GROUP_ID=USERS_GROUP.USER_GROUP_ID AND USERS_GROUP.USER_GROUP_ID=USERS_GROUP_MEMBERS.USERS_GROUP_ID
                    AND USERS_GROUP_MEMBERS.USER_ID=USERS.USER_ID AND USERS.NAME='{username}'
                ORDER BY RESOURCES.NAME;"""
    res = await database.fetch_all(query=query)
    return res

"""
This function return True if the scope match with the url of the endpoint.
"""
def scope_matching(matching_scope: str, scope: str) -> bool:
    #matching scope is the endpoint url
    ms_len = len(matching_scope)
    if len(scope) > ms_len:
        return False #if the length of the scope is longer than one of the matching scope, it can't match
    for i in range (ms_len):
        if i == len(scope) - 1 and scope[i] == '/':
            return True # the / at the end of the url mean that you have the right to request endpoint/* (example: /v3/projects/ mean you can request /v3/projects/AAAA-BBBB-1111/)
        elif scope[i] != matching_scope[i]:
            return False
    return True


"""
This function create the ObjectAcl with the path of the endpoint for the delete request.
"""
def get_delete_permission_scope(path: str) -> Endpoint:
    if "snapshots" in path:
        return Endpoint("NODE_SNAPSHOT", path)
    if "links" in path:
        return Endpoint("LINK_FILTER", path)
    return Endpoint("DELETE", path)


"""
This function create the ObjectAcl with the path of the endpoint for the get request
"""
#Todo determiner la logique pour determiner les differences entre les differents get
def get_get_permission_scope(path: str) -> Endpoint:
    if "stream" in path:#condition a determiner pour la permission use
        return Endpoint("USE", path)
    return Endpoint("READ", path)


"""
This function create the ObjectAcl with the path of the endpoint for the post request
"""
#Todo determiner la logique pour determiner les differences entre les differents post
def get_post_permission_scope(path: str) -> Endpoint:
    # create project: droit: project_creator
    return Endpoint("CREATE", path)

"""
This function create the ObjectAcl with the path of the endpoint for the get request
"""
def get_put_permission_scope(path: str) -> Endpoint:
    if 'links' in path:
        return Endpoint("LINK_FILTER", path)
    return Endpoint('UPDATE', path)


"""
This function return the good object for the endpoint
"""
def get_required_scopes_from_endpoint(request: Request) -> Endpoint:
    if request.method == "POST":
        return get_post_permission_scope(request.url.path)
    elif request.method == "PUT":
        return get_put_permission_scope(request.url.path)
    elif request.method == "GET":
        return get_get_permission_scope(request.url.path)
    else:
        return get_delete_permission_scope(request.url.path)


"""
This function is the one that verify everything
"""
def verify_permission(endpoint_object: Endpoint, user_data):

    try:
        for elt in user_data.scopes:
            if elt[1] == endpoint_object.action:
                res = scope_matching(endpoint_object.roles, elt[0])
                if res and elt[2] == 1:#1 mean True
                    return True
                elif res and elt[2] == 0: #0 mean false
                    return False
    except IndexError:
        return False
    return False # base case


"""
This function will get the token and decode it.
Then it verifies that the user has the right to call this endpoint.
"""
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    #todo add private key, or public key for token ?
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        tmp_token_scopes = payload.get("scopes", []) # get user acl

        #for some reason when you encode a list a triple if become a list of list with 3 elt
        token_scopes = []
        try:
            for elt in tmp_token_scopes:
                token_scopes.append((elt[0], elt[1], elt[2])) #creating a new list of triples
        except IndexError:
            raise credentials_exception
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    query = f"""SELECT USER_ID FROM USERS WHERE NAME='{username}';"""
    if not database.is_connected:
        await database.connect()
    res = await database.fetch_one(query=query)
    if not res[0]:
        raise credentials_exception
    if not verify_permission(get_required_scopes_from_endpoint(request), token_data):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
        )

    return User(username=username)


"""
This function is the one to depends with.
It will manage automatically the permission of the user
"""
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
