from fastapi import APIRouter

from app.schemas.api import GetTasksSchemaIn


router = APIRouter()


@router.post('/get_tasks', response_model=list[str])
async def get_tasks(schema: GetTasksSchemaIn):
    """Get tasks in order to setup for provided build."""
    return
