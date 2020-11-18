"""
This file contains unit test with easy use
"""
import pytest
from httpx import AsyncClient
from main import app
import json
import os

data_base_user = {
    "alice" : "secret",
    "bob": "secret"
}

auth_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}


@pytest.mark.asyncio
async def test_get_project():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        token = await ac.post("v3/token2", headers=auth_header, json={"username":"alice", "password": "secret"})#TODO a gerer selon le endpoint
        res = token.json()
        header = {'Accept': 'application/json', 'Authorization': f"Bearer {res['access_token']}"}
        response = await ac.post("/v3/templates", headers=header)
    assert response.status_code == 200
    assert response.json() == ["ok"]

if __name__ == '__main__':
    pytest.main(['-x', 'test.py'])