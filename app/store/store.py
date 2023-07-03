from typing import Generic, TypeVar

from fastapi import HTTPException
from starlette import status

from app.schemas.builds import BuildSchema, BuildsSchema
from app.schemas.tasks import TaskSchema, TasksSchema

_T = TypeVar('_T')


class StoreBase(dict[str, _T], Generic[_T]):
    message: str = 'Not found: {key}. '

    @classmethod
    def from_schema(cls, schema: BuildsSchema | TasksSchema):
        return cls({entity.name: entity for entity in schema})

    def __getitem__(self, key: str) -> _T:
        try:
            return super().__getitem__(key)
        except KeyError:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail=self.message.format(key=key, available=list(self.values())),
            )


class BuildsStore(StoreBase[BuildSchema]):
    """Represents builds as mapping for easy access by build name."""

    message: str = 'Build "{key}" not found. Available builds: {available}. '


class TasksStore(StoreBase[TaskSchema]):
    """Represents tasks as mapping for easy access by task name."""

    message: str = 'Task "{key}" not found. Check initial yaml file. '
