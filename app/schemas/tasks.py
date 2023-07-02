from __future__ import annotations

from functools import total_ordering
from typing import TYPE_CHECKING

from app.core import logger
from app.schemas.base import BaseSchema

if TYPE_CHECKING:
    from app.main import TasksStore


class TaskSchema(BaseSchema):
    name: str
    """Unique task name. """
    dependencies: list[str] = []
    """List of dependent task names. """


@total_ordering
class TaskEntity:
    """
    As `TaskSchema`, but it's not Pydantic shemas.
    So there are no any cheking on attribute assignment which improves ordering speed in 2-3 times.
    """

    def __init__(self, name: str, dependencies: list[str]) -> None:
        self.name = name
        self.dependencies = dependencies
        self._resolved_dependencies: set[str] | None = None
        """Internal cash field. Includes depended task names and all sub-depended task names. Calculated once. """

    def resolve_dependence(self, store: TasksStore):
        if self._resolved_dependencies is not None:
            logger.debug(f'Already resolved  : {self}')
            return

        self._resolved_dependencies = set()
        if not self.dependencies:
            logger.debug(f'Nothing to resolve: {self}')
            return

        logger.debug(f'Start resolving: {self}. Deps: {self.dependencies}. ')
        for task_name in self.dependencies:
            # set dependence name
            self._resolved_dependencies.add(task_name)

            # set all sub-dependencies task names
            task = store[task_name]
            task.resolve_dependence(store)
            self._resolved_dependencies.update(task._resolved_dependencies)

        logger.debug(
            f'End resolving: {self}. Deps: {self.dependencies}. '
            f'All: {self._resolved_dependencies} ({len(self._resolved_dependencies)}) '
        )

    def release_cash(self):
        self._resolved_dependencies = None

    def __lt__(self, other: object):
        if not isinstance(other, TaskEntity):
            return NotImplemented

        if self._resolved_dependencies is None or other._resolved_dependencies is None:
            raise NotImplemented  # Unresolved dependencies.

        # TODO why name?
        return (len(self._resolved_dependencies), self.name) < (len(other._resolved_dependencies), other.name)

    def __eq__(self, other):
        if not isinstance(other, TaskEntity):
            return NotImplemented
        return self.name == other.name

    def __str__(self):
        return self.name

    # def __hash__(self) -> int:
    #     # NOTE: All tasks has unique names, so we may use `name` as hash value
    #     return hash(self.name)


class TasksSchema(BaseSchema):
    tasks: list[TaskSchema]

    def as_store(self):
        """As strore."""
        return {task.name: TaskEntity(task.name, task.dependencies) for task in self.tasks}
