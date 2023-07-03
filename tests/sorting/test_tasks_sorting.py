import logging
from timeit import timeit

import pytest

from app.core import logger, settings
from app.main import TasksStore
from app.schemas.builds import BuildSchema, BuildsSchema
from app.schemas.tasks import TaskSchema, TasksSchema


@pytest.mark.parametrize(
    ['build', 'tasks', 'expected'],
    argvalues=[
        # [001] simple test
        pytest.param(
            BuildSchema(name='test build', tasks=['task A', 'task B']),
            TasksSchema(
                tasks=[
                    TaskSchema(name='task A', dependencies=['task C', 'task B']),
                    TaskSchema(name='task B', dependencies=['task C']),
                    TaskSchema(name='task C', dependencies=[]),
                ]
            ),
            # expected order
            ['task C', 'task B', 'task A'],
            id='[001] simple test',
        ),
        # [002] hard test
        pytest.param(
            BuildSchema(name='test build', tasks=['task I', 'task A', 'task B', 'task F']),
            TasksSchema(
                tasks=[
                    # build tasks:
                    TaskSchema(name='task I', dependencies=[]),
                    TaskSchema(name='task A', dependencies=['task Q', 'task Y']),
                    TaskSchema(name='task B', dependencies=['task C', 'task D', 'task E']),
                    TaskSchema(name='task F', dependencies=['task B']),
                    # sub-tasks:
                    TaskSchema(name='task Q', dependencies=[]),
                    TaskSchema(name='task Y', dependencies=['task C']),
                    TaskSchema(name='task C', dependencies=[]),
                    TaskSchema(name='task D', dependencies=[]),
                    TaskSchema(name='task E', dependencies=['task Q']),
                ]
            ),
            # expected order:
            ['task I', 'task Q', 'task C', 'task Y', 'task A', 'task D', 'task E', 'task B', 'task F'],
            id='[002] hard test',
        ),
    ],
)
def test_tasks_sorting_common(build: BuildSchema, tasks: TasksSchema, expected: list[str]):
    store = tasks.as_store()
    assert expected == list(build.resolve_tasks(store))


def test_tasks_sorting_from_yaml_speed(build: BuildSchema, store: TasksStore):
    def run():
        list(build.resolve_tasks(store))

    logger.setLevel(logging.WARNING)
    taken_seconds = timeit('run()', globals=locals(), number=20000)

    logger.setLevel(settings.LOG_LEVEL)
    logger.info(f'Speed test: {taken_seconds}. ')


def test_tasks_sorting_from_yaml_logic(build: BuildSchema, store: TasksStore):
    result = list(build.resolve_tasks(store))

    # Check no duplicates
    assert len(result) == len(set(result))

    # Check that every build's task appears at result
    assert set(result).issuperset(build.tasks)

    # Check that for every task all its dependencies appear before task itself
    for idx, task_name in enumerate(result):
        task_dependencies = set(store[task_name].get_all_dependencies(store))
        assert set(result[0:idx]).issuperset(task_dependencies)
