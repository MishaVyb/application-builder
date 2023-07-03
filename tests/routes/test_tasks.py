import json

import pytest
from httpx import AsyncClient
from starlette import status

from app.main import app
from app.schemas.tasks import TaskSchema

pytestmark = pytest.mark.anyio


async def test_get_tasks_200(client: AsyncClient, build_name: str):
    response = await client.post('/api/v1/get_tasks', content=json.dumps({'build': build_name}))

    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == expected # TODO


async def test_get_tasks_404_build(client: AsyncClient):
    response = await client.post('/api/v1/get_tasks', content=json.dumps({'build': 'invalid name'}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_tasks_404_task(client: AsyncClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delitem(app.extra['tasks_store'], 'build_teal_leprechauns')

    response = await client.post('/api/v1/get_tasks', content=json.dumps({'build': 'forward_interest'}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_tasks_409_recursion(client: AsyncClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setitem(
        app.extra['tasks_store'],
        'build_teal_leprechauns',
        TaskSchema(name='build_teal_leprechauns', dependencies=['build_teal_leprechauns']),  # Task depends on itself
    )

    response = await client.post('/api/v1/get_tasks', content=json.dumps({'build': 'forward_interest'}))
    assert response.status_code == status.HTTP_409_CONFLICT
