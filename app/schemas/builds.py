from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Iterator

from app.core.settings import logger
from app.core.utils import timer
from app.schemas.base import BaseSchema, TaskName

if TYPE_CHECKING:
    from app.store import TasksStore


class BuildSchema(BaseSchema):
    name: str
    """Unique build name. """
    tasks: list[TaskName] = []
    """List of dependent task names. """

    @timer('Build: resolve')
    def resolve_tasks(self, store: TasksStore) -> Generator[TaskName, None, None]:
        """
        Build`s tasks and their dependenices traversal.

        Generator factory function to iterate through task names in order to setup depending on each task dependencies.
        If task is not sub-dependence of any other task, it leaves in order of appereance.
        """
        logger.info(f'Resolve: {self}')

        resolved_tasks: set[TaskName] = set()
        for task_name in self.tasks:
            if task_name in resolved_tasks:
                continue  # task was taken before already - skip

            yield from store[task_name].resolve_dependence(store, resolved_tasks)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.name


class BuildsSchema(BaseSchema):
    builds: list[BuildSchema]

    def __iter__(self) -> Iterator[BuildSchema]:  # type: ignore
        return iter(self.builds)
