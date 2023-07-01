from __future__ import annotations

from pprint import pprint
from typing import TypeAlias

from app.schemas.builds import BuildSchema, BuildsSchema
from app.schemas.tasks import TaskSchema, TasksSchema

TasksStore: TypeAlias = dict[str, TaskSchema]
BuildsStore: TypeAlias = dict[str, BuildSchema]

# TODO
# - try speed without pydantic
# - try private field in pydantic
# - requirements update

if __name__ == '__main__':
    # builds_schema = BuildsSchema.parse_yaml(settings.BUILDS_FILE_PATH)
    # tasks_schema = TasksSchema.parse_yaml(settings.TASKS_FILE_PATH)
    # builds_mapping = builds_schema.as_mapping()
    # tasks_mapping = tasks_schema.as_mapping()
    ...
    ...

    build_mapping = BuildsSchema(builds=[]).as_mapping()
    tasks_mapping = TasksSchema(
        tasks=[
            TaskSchema(name='task A', dependencies=['task C', 'task B']),
            TaskSchema(name='task B', dependencies=['task C']),
            TaskSchema(name='task C', dependencies=[]),
        ]
    ).as_mapping()

    # Example
    build = BuildSchema(name='build A', tasks=['task A', 'task B'])

    result = set()
    for task_name in build.tasks:
        task = tasks_mapping[task_name]
        task.resolve_dependence(tasks_mapping)
        result.add(task)

    sorted_result = sorted(result)

    print()
    pprint(sorted_result)
    ...
