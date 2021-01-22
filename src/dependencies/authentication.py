"""
File that contains middleware for the api
"""

from fastapi import APIRouter
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from db import fastapi_db

#some global var to make it work
router = APIRouter()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v3/token") #if v4 is realease, this has to be change
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""
This function check if the 2 encrypted passwords match.
"""
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

"""
This function return True if the user exists in the database.
"""
async def authenticate_user(username: str, password: str) -> bool:
    query = f"""SELECT PASSWORD FROM USERS WHERE NAME='{username}';"""
    if not fastapi_db.database.is_connected:
        await fastapi_db.database.connect()
    res = await fastapi_db.database.fetch_one(query=query)
    if not res[0]:
        return False
    user_password = res[0] #res = (elt,)
    #if not verify_password(password, user_password): password is actually not hash in the database
    if password != user_password:
        return False
    return True


"""
This function create an access_token to reach endpoint with.
"""
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta #time after the user need to login again
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

