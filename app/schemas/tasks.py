from __future__ import annotations

from typing import TYPE_CHECKING

from app.core import logger

from app.schemas.base import BaseSchema

if TYPE_CHECKING:
    from app.main import TasksStore
    from app.main import TaskName


class TaskSchema(BaseSchema):
    name: str
    """Unique task name. """
    dependencies: list[str] = []
    """List of dependent task names. """


class TaskEntity:
    """
    As `TaskSchema`, but it's not Pydantic shemas.
    So there are no any cheking on attribute assignment which improves ordering speed in 2-3 times.
    """

    def __init__(self, name: str, dependencies: list[str]) -> None:
        self.name = name
        self.dependencies = dependencies

    def resolve_dependence(self, store: TasksStore, resolved_tasks: set[TaskName]):
        # Handle task deps
        for task_name in self.dependencies:
            if task_name in resolved_tasks:
                continue  # task was taken before already - skip

            # retrun all deps
            yield from store[task_name].resolve_dependence(store, resolved_tasks)

        # Handle task itself
        if self.name in resolved_tasks:
            return  # task was taken before already - skip

        resolved_tasks.add(self.name)
        yield self.name


class TasksSchema(BaseSchema):
    tasks: list[TaskSchema]

    def as_store(self):
        """As strore."""
        return {task.name: TaskEntity(task.name, task.dependencies) for task in self.tasks}
