from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from starlette import status

from app.schemas.api import GetTasksSchemaIn

if TYPE_CHECKING:
    from app.store import BuildsStore, TasksStore

router = APIRouter()


@router.post('/get_tasks', response_model=list[str])
async def get_tasks(request: Request, schema: GetTasksSchemaIn):
    """Get tasks in order to setup for provided build."""

    builds_store: BuildsStore = request.app.extra['builds_store']
    tasks_store: TasksStore = request.app.extra['tasks_store']

    try:
        return list(builds_store[schema.build].resolve_tasks(tasks_store))
    except RecursionError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Invalid tasks dependencies. Recursion found: {e}. ',
        )
