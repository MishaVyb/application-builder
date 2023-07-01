from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from app.core import settings

from app.schemas.base import BaseSchema
from app.schemas.tasks import TaskSchema


if settings.DEBUG:
    import line_profiler

    profile = line_profiler.LineProfiler()
else:
    profile = lambda x: x

if TYPE_CHECKING:
    from app.main import TasksStore


class BuildSchema(BaseSchema):
    name: str
    """Unique build name. """
    tasks: list[str] = []
    """List of dependent task names. """

    def tasks_generator(self, store: TasksStore) -> Generator[TaskSchema, None, None]:
        """Tasks as `TaskSchema` instances generator factory."""
        return (store[task_name] for task_name in self.tasks)

    @profile
    def resolve(self, store: TasksStore):
        """Resolve tasks dependencies. Return sorted list."""
        for task in self.tasks_generator(store):
            task.resolve_dependence(store)

        return sorted(self.tasks_generator(store))


class BuildsSchema(BaseSchema):
    builds: list[BuildSchema]

    def as_mapping(self):
        return {build.name: build for build in self.builds}
