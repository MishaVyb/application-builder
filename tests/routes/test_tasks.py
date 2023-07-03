import json

import pytest
from httpx import AsyncClient
from starlette import status

from app.api.v1.endpoints.tasks import get_tasks
from app.main import app

pytestmark = pytest.mark.anyio


async def test_get_tasks_200(client: AsyncClient, build_name: str):
    response = await client.post('/api/v1/get_tasks', content=json.dumps({'build': build_name}))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected


async def test_get_tasks_404(client: AsyncClient):
    response = await client.post('/api/v1/get_tasks', content=json.dumps({'build': 'invalid name'}))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    print(response.json())
