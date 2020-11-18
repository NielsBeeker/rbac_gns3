"""
This file contains unit test
"""

import pytest
import json
import requests
from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from src.endpoint.authentication import login_for_access_token1
from src.models.User import Auth

pytestmark = pytest.mark.asyncio

def memoize(function):
    memo = {}
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper

tested_user = {
    'alice' : 'secret',
    'bob': 'secret'
}

def getUserToken(username):
    url = "http://127.0.0.1:8000/v3/token2"
    headers = {'content-type': 'application/json'}
    res_dict = json.load(requests.post(url, headers=headers).text)
    return res_dict['access_token']


#todo strange function
@pytest.fixture
@memoize
def get_token(username="alice"):
    return getUserToken(username)


class Testendpoint:
    @pytest.mark.asyncio
    async def test_endpoint_exist(self, app: FastAPI, client: AsyncClient, token: get_token) -> None:

        res = await client.post(app.url_path_for("api:read-me"), headers={'Accept': 'application/json', 'Authorization': token})#todo rajout token
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_invalid_input_raise_error(self, app: FastAPI, client: AsyncClient, token: get_token) -> None:
        res = await client.post(app.url_path_for("api:read-me"), headers={'Accept': 'application/json', 'Authorization': token})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

