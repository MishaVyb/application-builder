from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from app.core.utils import timer

from app.schemas.base import BaseSchema
from app.schemas.tasks import TaskEntity, TaskSchema

if TYPE_CHECKING:
    from app.main import TasksStore


class BuildSchema(BaseSchema):
    name: str
    """Unique build name. """
    tasks: list[str] = []
    """List of dependent task names. """

    def tasks_generator(self, store: TasksStore) -> Generator[TaskEntity, None, None]:
        """Tasks as `TaskEntity` instances generator factory."""
        return (store[task_name] for task_name in self.tasks)

    @timer(name='Resolve build')
    def resolve(self, store: TasksStore):
        """Resolve tasks dependencies. Return sorted list."""
        for task in self.tasks_generator(store):
            task.resolve_dependence(store)

        return sorted(self.tasks_generator(store))


class BuildsSchema(BaseSchema):
    builds: list[BuildSchema]

    def as_store(self):
        return {build.name: build for build in self.builds}
