from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TypeAlias

import uvicorn
from fastapi import FastAPI

from app.api.v1.router import router
from app.core import logger, settings
from app.core.utils import timer
from app.schemas.builds import BuildSchema, BuildsSchema
from app.schemas.tasks import TaskSchema, TasksSchema

# from app.schemas.tasks import TaskEntity

TasksStore: TypeAlias = dict[str, TaskSchema]
BuildsStore: TypeAlias = dict[str, BuildSchema]

# TODO
# - try speed without pydantic
# - try private field in pydantic
# - requirements update
# - cspell!!
# - remove expensive logs
# - typeing on return
# - CI / CD


@asynccontextmanager
async def initialize_store(app: FastAPI):
    """Load builds/tasks from yaml file. Arrange list of builds/tasks as dict to perfrom easy access."""

    logger.info(f'Initialize: {app.title}. Settings: {settings}. ')

    with timer('App: init', logger.info):
        builds_schema = BuildsSchema.parse_yaml(settings.BUILDS_FILE_PATH)
        tasks_schema = TasksSchema.parse_yaml(settings.TASKS_FILE_PATH)
        app.extra['builds_store'] = builds_schema.as_store()
        app.extra['tasks_store'] = tasks_schema.as_store()

    yield

    del app.extra['builds_store']
    del app.extra['tasks_store']


app = FastAPI(
    title='Application build system',
    description='Service to handle builds, tasks and their dependencies',
    version='1',
    debug=settings.DEBUG,
    lifespan=initialize_store,
)

app.include_router(router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080)
