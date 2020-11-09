"""
This file contains middleware for security
"""

from fastapi import Depends, FastAPI, HTTPException, Security, status, APIRouter
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from starlette.requests import Request
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from src.models.Token import Token, TokenData
from src.models.User import UserInDB, User
from src.models.ObjectAcl import ObjectAcl
from src.dependencies.authentication import oauth2_scheme, SECRET_KEY, ALGORITHM
from src.dependencies.database import get_user
from src.db.db_ressource import fake_user_db
import re


"""
return [] remplacé par get base acl
#TODO dossier database
"""

async def scope_matching(matching_scope: str, scope: str) -> bool:
    sub_match = matching_scope.split("/")
    sub_scope = scope.split("/")

    for i in range(1, len(sub_match) - 1):
        if sub_match[i] != sub_scope[i]:
            if sub_scope[i] == "*":
                return True
            return False
        if i == len(sub_match):
            return False
    return True

async def get_base_acl_from_ressource(path: str):
    if "computes" in path:
        return []
    if "appliances" in path:
        return []
    if "drawings" in path:
        return []
    if "links" in path:
        return []
    if "nodes" in path:
        return []
    if "users" in path: # pour futur endpoint api ,pas encore mis en place
        return []
    if "groups" in path:#
        return []
    if "snapshot" in path:
        return []
    if "templates" in path:
        return []
    if "images" in path:
        return []
    if "symbols" in path:
        return []
    if "projects" in path:
        return []
    return [] # controler

    #return: [("role:amdin", "all"), ("user:authenticated, "use")]
    #voir le format de retour du tuple pour les droits
 # google doc : ressource with acls, ces ressources doivent etre recuperer dans une db ou bien un fichier flat, variable ...



async def get_delete_permission_scope(path: str) -> ObjectAcl:
    if "snapshot" in path:
        return ObjectAcl("NODE_SNAPSHOT", path, get_base_acl_from_ressource(path))
    return ObjectAcl("DELETE", path, get_base_acl_from_ressource(path))
#je traite les cas precis et ensuite je renvoie le triplet


"la logique est la meme pour celle d'en dessous"
async def get_get_permission_scope(path: str):
    pass

async def get_post_permission_scope(path: str):
    pass
    # create project: droit: project_creator

async def get_put_permission_scope(path: str):
    pass

#todo rajouter patch ?
#todo rajouter au parametre de security() dans le endpoint
async def get_required_scopes_from_endpoint(request: Request) -> ObjectAcl:
    if request.method == "POST":
        return get_post_permission_scope(request.url.path)
    elif request.method == "PUT":
        return get_put_permission_scope(request.url.path)
    elif request.method == "GET":
        return get_get_permission_scope(request.url.path)
    else:
        return get_delete_permission_scope(request.url.path)


#TODO doit-on verifier si le user est bien authenticated sur une api
def verify_permission(endpoint_object: ObjectAcl, user_data, authenticate_value: str):
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    #try to match user role and role requiered for the endpoint
    has_role = False
    for endpoint_role in endpoint_object.roles:
        for user_role in user_data.role:
            if endpoint_role == user_role:
                has_role = True
                break

    if not has_role:
        raise exception
    has_role = False
    for elt in user_data.scopes:
        if elt[0] == endpoint_object.action or elt[0] == "ALL": #todo mettre la verification dans quel ordre ?
            if scope_matching(endpoint_object.scopes, elt):#check if the user has scope
                if not scope_matching(endpoint_object.scopes, elt):#check if the user don't access a denied scope
                    has_role = True
                    break
    if not has_role:
        raise exception


#add endpoint parameter
async def get_current_user(endpoint_object: ObjectAcl,
    token: str = Depends(oauth2_scheme)
):
    #if security_scopes.scopes:
    #    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' #a voir pour la modif
    #else:
    #    authenticate_value = f"Bearer"
    authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", []) # TODO permet de récuprer les scopes du current user ces |||||||| ces informations soit dans le token, soit dans le bdd
        token_role = payload.get("role", []) #TODO permet de recuperer les roles du current user
        deny_user_scope = payload.get("deny_user_scope")#TODO recup les deny scope du user
        token_data = TokenData(scopes=token_scopes, username=username, token_role=token_role, deny_user_scope=deny_user_scope)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_user_db, username=token_data.username)
    if user is None:
        raise credentials_exception

    verify_permission(endpoint_object, token_data, authenticate_value)

    """for scope in security_scopes.scopes:
        if scope not in token_data.scopes: ## TODO ici on peut comparé les scopes du token avec les scopes requis
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )"""
    return user


#a la place de scope=["me"] mettre une fonction qui deduis les scopes required pour endpoint (scope=get_endpoint_scope)
async def get_current_active_user(
    endpoint_object: ObjectAcl
):
    current_user: User = Depends(get_current_user(endpoint_object=endpoint_object))
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



scope_requiered = ("update", "projects/{}/links/{}")


user_scope_in_db = ("update", "project/{}/*")
deny_user_scope = ("update", "project/{}/links/{}")
