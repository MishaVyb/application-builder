from __future__ import annotations

from typing import TypeAlias

import uvicorn
from fastapi import FastAPI

from app.api.v1.router import router
from app.core import settings
from app.schemas.builds import BuildSchema
from app.schemas.tasks import TaskEntity

TasksStore: TypeAlias = dict[str, TaskEntity]
BuildsStore: TypeAlias = dict[str, BuildSchema]

# TODO
# - try speed without pydantic
# - try private field in pydantic
# - requirements update
# - cspell!!
# - remove expensive logs
# - typeing on return
# - CI / CD

app = FastAPI(
    title='Build system',
    description='Service to handle builds, tasks and their dependencies',
    version='1',
    debug=settings.DEBUG,
)

app.include_router(router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8080)
