from typing import TYPE_CHECKING

from fastapi import APIRouter, FastAPI, HTTPException, Request
from starlette import status

from app.core.settings import logger
from app.schemas.api import GetTasksSchemaIn

if TYPE_CHECKING:
    from app.main import BuildsStore, TasksStore

router = APIRouter()


@router.post('/get_tasks', response_model=list[str])
async def get_tasks(request: Request, schema: GetTasksSchemaIn):
    """Get tasks in order to setup for provided build."""
    builds_store: BuildsStore = request.app.extra['builds_store']
    tasks_store: TasksStore = request.app.extra['tasks_store']

    if not (build := builds_store.get(schema.build)):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f'Build not found. Available builds: {list(builds_store.values())}'
        )

    return list(build.resolve_tasks(tasks_store))
