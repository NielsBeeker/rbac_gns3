from datetime import datetime, timedelta
from typing import List

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi_permissions import (
    Allow,
    Authenticated,
    Deny,
    Everyone,
    configure_permissions,
    list_permissions,
    has_permission,
    All
)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


##DB de la table USER
fake_users_db = {
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


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    principals: List[str] = []


class UserInDB(User):
    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)




def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

#TODO
"""
classe permettant de gérer les acl:
    - besoin de def __acl__ ou bien d'un attribut __acl__
    - def __acl__ pour les class héritant de BaseModel

-owner: permet de gérer les droits sur les projets/noeuds/liens créer par le user

question: est ce que on peut facilement intégrer cette liste aux object de la class sur gns3 ainsi que la modifier facilement si on veut changer la base acl de l'object ?

"""

"""
classe permettant de passer d'un objet dans la base de donnée à un objet d'une classe existante
"""

test = [("Allow", "Authenticated","all")]

class Item(BaseModel):
    name: str
    owner: str
    acll: type(test)
    def __acl__(self):
        res = []
        for elt in self.acll:
            if elt[0] == "Allow":
                transform = Allow
            else:
                transform = Deny
            if elt[1] == "Authenticated":
                tmp = Authenticated
            elif elt[1] == "Everyone":
                tmp = Everyone
            else:
                tmp = elt[1]
            if elt[2] == "all":
                tmp2 = All
            else:
                tmp2 = elt[2]
            res.append((transform, tmp, tmp2))

        return res

        """"
        return acll
        """
"""
def __acl__(self):
    fonction qui passe [(str,str,str), ...] a quelque chose d'interprétable par Permission
    ps: inutile transformer 'Authenticated' par Authenticated, ce sont des maccro de string ("system:authenticated" = Authenticated)
"""


#TODO
"""
exemple d'une situation ou la base de donnée contient les instances avec le owner ainsi que les acl

"""
fake_items_db = {
    1: {"name": "project_166661", "owner": "bob", "acll":[("Allow", "role:user","use")]},
    2: {"name": "project_177733", "owner": "alice", "acll":[("Deny", "user:bob","use"), ("Allow", "Authenticated","all")]},
}

def get_project(project: int):
    if project in fake_items_db:
        item_dict = fake_items_db[project]
        res = Item(**item_dict)
        return res


#TODO
"""
Une manière de récupérer les principals d'un user sous la forme d'une liste de tuples

pour les groupes, faire une fonction intermediaire qui permettrait de transformer un group -> list: role

le user est récupéré de la base de donnée ou bien il obtient les droits "d'invité" si nécessaire
"""

def get_active_principals(user: User = Depends(get_current_user)):
    if user:
        # user is logged in
        principals = [Everyone, Authenticated] #base role for a user
        principals.extend(getattr(user, "principals", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals


#TODO
"""
fonction mère de l'authentification qui permet de load les acl du current user pour ensuite le passer en paramètre de la fonction callable
"""

Permission = configure_permissions(get_active_principals)

#TODO class permettant l'envoie du curl --data{"username":"blabla", "password": "blabla"} au lieu du xxx-formurl pour la fonction login access
class Auth(BaseModel):
    username: str
    password: str


#TODO
"""
creation classique d'un jwt avec un temps d'expiration
"""
@app.post("/token", response_model=Token)
async def login_for_access_token(
    auth : Auth
):
    user = authenticate_user(
        fake_users_db,auth.username, auth.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}

#TODO exemple très simple d'une autorisation
"""
project_id = 2 : dans ce cas tout le monde peut acceder au projet de alice sauf bob
project_id = 1 : tout le monde a acces a la ressource
"""
@app.get("/project/{project}/use")
async def test_use_project(project: Item = Permission("use",get_project)):
    return {"test": project}

"""
IMPORTANT:
Pour une requete create, on ne peut pas recuperer les droits de l'objet car il n'existe pas
Du coup à partir de quelle acl doit on se référer ?
Comment vois tu la choses ?
Je n'ai remarqué ce comportement que sur les create pour le moment

"""


"""
external add
"""

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



#union csur les paramatres
@app.post("/authenticate", response_model=Token)
async def authenticate(credentials: HTTPBasicCredentials):

    user = authenticate_user(fake_users_db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/project", status_code=status.HTTP_201_CREATED)
async def test_use_project(user: User = Depends(get_current_user)):

    if "role:admin" not in user.principals:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden to create a new project")
    print("Project created!")

import uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port='8080')