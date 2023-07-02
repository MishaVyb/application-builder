from __future__ import annotations

from typing import TYPE_CHECKING, Generator
from app.core.utils import timer

from app.schemas.base import BaseSchema
from app.schemas.tasks import TaskEntity, TaskSchema

if TYPE_CHECKING:
    from app.main import TasksStore
    from app.main import TaskName


class BuildSchema(BaseSchema):
    name: str
    """Unique build name. """
    tasks: list[str] = []
    """List of dependent task names. """

    # UNUSED
    def tasks_generator(self, store: TasksStore) -> Generator[TaskEntity, None, None]:
        """Tasks as `TaskEntity` instances generator factory."""
        return (store[task_name] for task_name in self.tasks)

    @timer(name='Build - resolve')
    def resolve_tasks(self, store: TasksStore):
        """Generator factory...TODO tasks in order to setup depending on each task dependencies."""
        resolved_tasks = set()

        for task in self.tasks_generator(store):
            yield from task.resolve_dependence(store, resolved_tasks)


class BuildsSchema(BaseSchema):
    builds: list[BuildSchema]

    def as_store(self):
        return {build.name: build for build in self.builds}
