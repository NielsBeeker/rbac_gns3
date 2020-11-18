"""
This file contains config for unit test
"""
from asgi_lifespan import LifespanManager
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import app

@pytest.fixture
def app() -> FastAPI:
    return app

#todo rajouter le token d'authentification
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://127.0.0.1:8000",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client