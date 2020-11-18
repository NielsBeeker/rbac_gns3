"""
This file contains unit test
"""

import pytest

from httpx import AsyncClient
from fastapi import FastAPI

from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from src.endpoint.authentication import login_for_access_token1
from src.models.User import Auth

#manière barbare de récupérer le token du user
token = login_for_access_token1(Auth({"username": "alice", "password": "secret"}))

pytestmark = pytest.mark.asyncio

class Testendpoint:
    @pytest.mark.asyncio
    async def test_endpoint_exist(self, app: FastAPI, client: AsyncClient) -> None:

        res = await client.post(app.url_path_for("api:read-me"), headers={'Accept': 'application/json', 'Authorization': token})#todo rajout token
        assert res.status_code != HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_invalid_input_raise_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("api:read-me"), headers={'Accept': 'application/json', 'Authorization': token})  # todo rajout token
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

