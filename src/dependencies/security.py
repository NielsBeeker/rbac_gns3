"""
This file contains middleware for security
"""

from fastapi import Depends, FastAPI, HTTPException, Security, status, APIRouter

from starlette.requests import Request
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from models.Token import Token, TokenData
from models.User import UserInDB, User
from models.ObjectAcl import ObjectAcl
from dependencies.authentication import oauth2_scheme, SECRET_KEY, ALGORITHM
from dependencies.database import get_user
from db.db_ressource import fake_user_db, base_acl_db


"""
3 cas: to match ==> needed for match
1-get  : v3/projects ==> v3/projects obligatoire
2-post : v3/projetcs/1234 ==> v3/projects/1234/*
3-post : v3/projetcs/1234/nodes/12345/duplicate ==> v3/projects/1234/nodes/12345/*
                                                ou   v3/projetcs/1234/*

This function check if the 2 scopes are matching together with different cases
"""

def scope_matching(matching_scope: str, scope: str) -> bool:
    if matching_scope == scope:#cas 1
        return True
    sub_match = matching_scope.split("/") # /v3/projects => ["", "v3", "projects"]
    sub_scope = scope.split("/")
    for i in range(1, len(sub_match)): ## skiping the first elt which is "" because of the split on "/v3/projects"
        if not sub_scope[i]:#en cas de probleme de check
            return False
        if sub_scope[i] and sub_scope[i] != sub_match[i]: # cas 3 ou
            if sub_scope[i] == "*":
                return True
            return False
    tmp = len(sub_match)
    if sub_scope[tmp]:
        if not sub_scope[tmp] == "*":#cas 2
            return False
    return True

"""
This function get base acl ressource from database or something else
"""
#todo delete this function and the ressource in db
def get_base_acl_from_ressource(path: str):
    if "computes" in path:
        return base_acl_db["compute"]
    if "appliances" in path:
        return base_acl_db["appliance"]
    if "drawings" in path:
        return base_acl_db["drawing"]
    if "links" in path:
        return base_acl_db["link"]
    if "nodes" in path:
        return base_acl_db["node"]
    if "users" in path: # pour futur endpoint api ,pas encore mis en place
        return base_acl_db["user"]
    if "groups" in path:#
        return base_acl_db["group"]
    if "snapshot" in path:
        return base_acl_db["snapshot"]
    if "templates" in path:
        return base_acl_db["template_public"]
    if "images" in path:
        return base_acl_db["image_public"]
    if "symbols" in path:
        return base_acl_db["symbol_public"]
    if "projects" in path:
        return base_acl_db["project"]
    return base_acl_db["controller"]


"""
This function create the ObjectAcl with the path of the endpoint for the delete request

Ps: An objectAcl is an object with different fields about permissions needed for current endpoint, the path, and the ressource needed for the endpoint 
"""
def get_delete_permission_scope(path: str) -> ObjectAcl:
    if "snapshots" in path:
        return ObjectAcl("node_snapshot", path)
    if "links" in path:
        return ObjectAcl("link_filter", path)
    return ObjectAcl("DELETE", path)


"""
This function create the ObjectAcl with the path of the endpoint for the get request
"""
#Todo determiner la logique pour determiner les differences entre les differents get
def get_get_permission_scope(path: str) -> ObjectAcl:
    if "stream" in path:#condition a determiner pour la permission use
        return ObjectAcl("use", path)
    return ObjectAcl("read", path)


"""
This function create the ObjectAcl with the path of the endpoint for the post request
"""
#Todo determiner la logique pour determiner les differences entre les differents post
def get_post_permission_scope(path: str) -> ObjectAcl:
    # create project: droit: project_creator
    return ObjectAcl("create", path)

"""
This function create the ObjectAcl with the path of the endpoint for the get request
"""
def get_put_permission_scope(path: str) -> ObjectAcl:
    if 'links' in path:
        return ObjectAcl("link_filter", path)
    return ObjectAcl('update', path)


"""
This function return the good object for the endpoint
"""
def get_required_scopes_from_endpoint(request: Request) -> ObjectAcl:
    if request.method == "POST":
        return get_post_permission_scope(request.url.path)
    elif request.method == "PUT":
        return get_put_permission_scope(request.url.path)
    elif request.method == "GET":
        return get_get_permission_scope(request.url.path)
    else:
        return get_delete_permission_scope(request.url.path)
#changement : ne recupere plus les acl en fonction des ressources


"""
This function is the one that verify everything
"""
#TODO doit-on verifier si le user est bien authenticated sur une api ?
def verify_permission(endpoint_object: ObjectAcl, user_data, authenticate_value: str):
    #todo this case must not be use => we cant give base rights to object, only user have permission
    """ #check for role
    for endpoint_role in endpoint_object.roles:
        for user_role in user_data.token_role:
            if user_role == endpoint_role[0]: #on recuperer seulement le role du user
                if endpoint_role[1] == endpoint_object.action:
                    return True"""

    #before
    """has_role = False
    #check allowed scope
    for elt in user_data.scopes:
        if elt[1] == endpoint_object.action or elt[1] == "all":
            if scope_matching(endpoint_object.scopes, elt[0]):
                has_role = True
                break
    #check denied scope
    for elt in user_data.deny_uri:
        if elt[1] == endpoint_object.action or elt[1] == "all":
            if scope_matching(endpoint_object.scopes, elt[0]):
                has_role = False"""


    #after

    #meme concept que le pare-feu, je check les acl les une à la suite des autres et je return false/true au premier match
    for elt in user_data.scopes:
        if elt[1] == endpoint_object.action or elt[1] == "all":
            res = scope_matching(endpoint_object.scopes, elt[0])
            if res and elt[2] == "Allow":#todo elt[2] a rajouter avec le allow, deny aux scopes
                return True
            elif res and elt[2] == "Deny":
                return False
    # base case
    return False


"""
This function will get the token and decode it.
Then it verifies that the user has the right to call this endpoint.
"""
#Todo Besoin de laisser autant d'information dans le token ou il suffit de récupérer ça de la base de donnée ?
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    #if security_scopes.scopes:
    #    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    #else:
    #    authenticate_value = f"Bearer"
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
        tmp_token_scopes = payload.get("scopes", [])# get scope, username, deny_scope, role from user's token
        #for some reason when you encode a list a tuple if become a list of list with 2 elt
        token_scopes = []
        for elt in tmp_token_scopes:
            token_scopes.append((elt[0], elt[1], elt[2])) #todo add index check
        token_role = payload.get("role", [])
        token_data = TokenData(scopes=token_scopes, username=username, token_role=token_role)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_user_db, username=token_data.username)
    if user is None:
        raise credentials_exception

    if not verify_permission(get_required_scopes_from_endpoint(request), token_data, authenticate_value):
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user

"""
This function is the one to depends with.
It will manage automatically the permission of the user
"""
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

