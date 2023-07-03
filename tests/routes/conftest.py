import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def client():
    # NOTE
    # Invokes app lifespan: https://github.com/encode/httpx/issues/350
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            yield client
