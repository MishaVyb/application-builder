from __future__ import annotations

from functools import total_ordering
from typing import TYPE_CHECKING

from app.core import logger
from app.schemas.base import BaseSchema

if TYPE_CHECKING:
    from app.main import TasksStore


@total_ordering
class TaskSchema(BaseSchema):
    name: str
    """Unique task name. """
    dependencies: list[str] = []
    """List of dependent task names. """

    resolved_dependencies: set[str] | None = None
    """Internal cash field. Includes depended task names and all sub-depended task names. Calculated once. """

    # def __hash__(self) -> int:
    #     # NOTE: All tasks has unique names, so we may use `name` as hash value
    #     return hash(self.name)

    def resolve_dependence(self, tasks: TasksStore):
        if self.resolved_dependencies is not None:
            logger.debug(f'Already resolved  : {self}')
            return

        self.resolved_dependencies = set()
        if not self.dependencies:
            logger.debug(f'Nothing to resolve: {self}')
            return

        logger.debug(f'Start resolving: {self}. Deps: {self.dependencies}. ')
        for task_name in self.dependencies:
            # set dependence name
            self.resolved_dependencies.add(task_name)

            # set all sub-dependencies task names
            task = tasks[task_name]
            task.resolve_dependence(tasks)
            self.resolved_dependencies.update(task.resolved_dependencies)

        logger.debug(
            f'End resolving: {self}. Deps: {self.dependencies}. '
            f'All: {self.resolved_dependencies} ({len(self.resolved_dependencies)}) '
        )

    def release_cash(self):
        self.resolved_dependencies = None

    def __lt__(self, other: object):
        if isinstance(other, TaskSchema):
            if self.resolved_dependencies is None or other.resolved_dependencies is None:
                raise ValueError('Unresolved dependencies. ')

            return (len(self.resolved_dependencies), self.name) < (len(other.resolved_dependencies), other.name)

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, TaskSchema):
            return self.name == other.name
        return NotImplemented

    def __str__(self):
        return self.name


class TasksSchema(BaseSchema):
    tasks: list[TaskSchema]

    def as_mapping(self):
        return {task.name: task for task in self.tasks}

    # __iter__
    # __get__
    # __bool__
