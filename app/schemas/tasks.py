from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Iterator

from app.schemas.base import BaseSchema, TaskName

if TYPE_CHECKING:
    from app.store import TasksStore


class TaskSchema(BaseSchema):
    name: TaskName
    """Unique task name. """
    dependencies: list[TaskName] = []
    """List of dependent task names. """

    def resolve_dependence(self, store: TasksStore, resolved_tasks: set[TaskName]) -> Generator[TaskName, None, None]:
        """
        Task dependencies traversal.

        Generator factory to iterate on task names. Implementation similar as for `Post Order Dearth First Traversal`.
        - Iterate through task dependencies, then yield task itself.
        - Exclude duplicates by shared `resolved_tasks` among all build`s tasks.
        """
        # Handle task dependencies
        for task_name in self.dependencies:
            if task_name in resolved_tasks:
                continue  # task was taken before already - skip

            yield from store[task_name].resolve_dependence(store, resolved_tasks)

        # Handle task itself
        resolved_tasks.add(self.name)
        yield self.name

    def get_all_dependencies(self, store: TasksStore) -> Generator[TaskName, None, None]:
        """Helper tool for test assertion."""
        for task_name in self.dependencies:
            yield task_name
            yield from store[task_name].get_all_dependencies(store)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.name


class TasksSchema(BaseSchema):
    tasks: list[TaskSchema]

    def __iter__(self) -> Iterator[TaskSchema]:  # type: ignore
        return iter(self.tasks)
